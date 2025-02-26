use jsonwebtoken::{
    decode, decode_header,
    jwk::{AlgorithmParameters, JwkSet},
    Algorithm, DecodingKey, Validation,
};
use log::info;
use moka::future::Cache;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use std::time::Duration;
use std::{fs, path::PathBuf};
use thiserror::Error;
use tokio::sync::RwLock;
#[derive(Clone, Deserialize, Serialize)]
pub struct Auth0Config {
    pub audience: String,
    pub domain: String,
    pub client_id: String,
    pub scope: String,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct Auth0PrivilegedConfig {
    pub audience: String,
    pub domain: String,
    pub client_id: String,
    pub scope: String,
    pub client_secret: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Claims {
    pub sub: String,
    pub iss: String,
    pub aud: AudClaim, // Using an enum to handle both cases
    pub iat: i64,
    pub exp: i64,
    pub azp: String,
    pub scope: String,
    pub permissions: Option<std::collections::HashSet<String>>,
}

#[derive(Debug, Deserialize, Serialize)]
#[serde(untagged)]
pub enum AudClaim {
    Single(String),
    Multiple(Vec<String>),
}

impl Claims {
    pub fn get_audiences(&self) -> Vec<String> {
        match &self.aud {
            AudClaim::Single(s) => vec![s.clone()],
            AudClaim::Multiple(v) => v.clone(),
        }
    }
}

#[derive(Error, Debug)]
pub enum Auth0Error {
    #[error("JWT decode error: {0}")]
    JwtDecode(#[from] jsonwebtoken::errors::Error),

    #[error("HTTP request error: {0}")]
    Request(#[from] reqwest::Error),

    #[error("Token not found: {0}")]
    NotFound(String),

    #[error("Unsupported algorithm: {0:?}")]
    UnsupportedAlgorithm(AlgorithmParameters),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),

    #[error("Operation not supported: {0}")]
    Unsupported(String),
}

impl Claims {
    pub fn validate_permissions(
        &self,
        required_permissions: &std::collections::HashSet<String>,
    ) -> bool {
        self.permissions
            .as_ref()
            .map(|permissions| permissions.is_superset(required_permissions))
            .unwrap_or(false)
    }
}

pub trait Auth0ClientTrait {
    fn get_config(&self) -> &Auth0Config;
    fn get_jwks_cache(&self) -> &Cache<String, JwkSet>;
}

pub struct Auth0Client {
    config: Auth0Config,
    jwks_cache: Cache<String, JwkSet>,
}

pub struct Auth0PrivilegedClient {
    config: Auth0PrivilegedConfig,
    unprivileged_config: Auth0Config,
    jwks_cache: Cache<String, JwkSet>,
    access_token_cache: Arc<RwLock<Option<AccessTokenCache>>>,
    token_file_path: PathBuf,
}

impl Auth0ClientTrait for Auth0Client {
    fn get_config(&self) -> &Auth0Config {
        &self.config
    }

    fn get_jwks_cache(&self) -> &Cache<String, JwkSet> {
        &self.jwks_cache
    }
}

impl Auth0ClientTrait for Auth0PrivilegedClient {
    fn get_config(&self) -> &Auth0Config {
        &self.unprivileged_config
    }

    fn get_jwks_cache(&self) -> &Cache<String, JwkSet> {
        &self.jwks_cache
    }
}

impl Auth0Client {
    pub fn new(domain: String, client_id: String, audience: String, scope: String) -> Self {
        let jwks_cache = Cache::builder()
            .time_to_live(Duration::from_secs(3600))
            .build();

        let config = Auth0Config {
            domain,
            client_id,
            audience,
            scope,
        };

        Self { config, jwks_cache }
    }

    pub async fn validate_token(&self, token: &str) -> Result<Claims, Auth0Error> {
        validate_token_internal(self, token).await
    }
}

impl Auth0PrivilegedClient {
    pub fn new(
        domain: String,
        client_id: String,
        audience: String,
        scope: String,
        client_secret: String,
        token_file_name: String,
    ) -> Self {
        let config = Auth0PrivilegedConfig {
            domain: domain.clone(),
            client_id: client_id.clone(),
            client_secret,
            audience,
            scope,
        };

        let unprivileged_config = Auth0Config {
            domain,
            client_id,
            audience: String::new(),
            scope: String::new(),
        };

        // Create token file path in the newbringer config directory
        let token_file_path = crate::config_path::get_newbringer_config_dir()
            .join(format!("{}.json", token_file_name));

        // Ensure the auth directory exists
        if let Some(auth_dir) = token_file_path.parent() {
            std::fs::create_dir_all(auth_dir).unwrap_or_default();
        }

        let client = Self {
            config,
            unprivileged_config,
            jwks_cache: Cache::builder()
                .max_capacity(100)
                .time_to_live(Duration::from_secs(3600))
                .build(),
            access_token_cache: Arc::new(RwLock::new(None)),
            token_file_path,
        };

        // Initialize token cache without blocking
        if let Ok(token_data) = fs::read_to_string(&client.token_file_path) {
            if let Ok(cached_token) = serde_json::from_str::<AccessTokenCache>(&token_data) {
                let now = chrono::Utc::now().timestamp();
                if cached_token.expires_at > now {
                    if let Ok(mut token_cache) = client.access_token_cache.try_write() {
                        *token_cache = Some(cached_token);
                    }
                }
            }
        }

        client
    }

    pub async fn validate_token(&self, token: &str) -> Result<Claims, Auth0Error> {
        validate_token_internal(self, token).await
    }

    pub async fn get_access_token(&self) -> Result<String, Auth0Error> {
        if let Some(cached_token) = self.access_token_cache.read().await.as_ref() {
            if !cached_token.is_expired() && !cached_token.needs_refresh() {
                return Ok(cached_token.token.clone());
            }
        }

        let token_url = format!("https://{}/oauth/token", self.config.domain);
        let client = reqwest::Client::new();

        let response = client
            .post(&token_url)
            .json(&serde_json::json!({
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "audience": self.config.audience,
                "grant_type": "client_credentials",
                "scope": self.config.scope,
            }))
            .send()
            .await?;

        let token_response: serde_json::Value = response.json().await?;

        info!("Token response: {}", token_response);

        let access_token = token_response["access_token"]
            .as_str()
            .ok_or_else(|| Auth0Error::NotFound("Access token not found in response".to_string()))?
            .to_string();

        let expires_in = token_response["expires_in"].as_i64().unwrap_or(3600);

        let scope = token_response["scope"]
            .as_str()
            .ok_or_else(|| Auth0Error::NotFound("Scope not found in response".to_string()))?
            .to_string();

        let token_type = token_response["token_type"]
            .as_str()
            .ok_or_else(|| Auth0Error::NotFound("Token type not found in response".to_string()))?
            .to_string();

        let now = chrono::Utc::now().timestamp();
        let expires_at = now + expires_in;

        let token_cache = AccessTokenCache {
            token: access_token.clone(),
            expires_at,
            scope,
            token_type,
            raw_response: token_response,
            issued_at: now,
        };

        *self.access_token_cache.write().await = Some(token_cache.clone());

        if let Ok(token_json) = serde_json::to_string(&token_cache) {
            let _ = fs::write(&self.token_file_path, token_json);
        }

        Ok(access_token)
    }

    pub async fn token_status(&self) -> Result<TokenStatus, Auth0Error> {
        if let Some(token) = self.access_token_cache.read().await.as_ref() {
            if token.is_expired() {
                Ok(TokenStatus::Expired {
                    expired_for: -token.expires_in(),
                })
            } else if token.needs_refresh() {
                Ok(TokenStatus::NeedsRefresh {
                    expires_in: token.expires_in(),
                    time_until_refresh: token.time_until_refresh(),
                })
            } else {
                Ok(TokenStatus::Valid {
                    expires_in: token.expires_in(),
                    time_until_refresh: token.time_until_refresh(),
                })
            }
        } else {
            Ok(TokenStatus::NotPresent)
        }
    }
}

#[derive(Debug, Deserialize, Serialize, Clone)]
struct AccessTokenCache {
    token: String,
    expires_at: i64,
    scope: String,
    token_type: String,
    raw_response: serde_json::Value,
    issued_at: i64,
}

impl AccessTokenCache {
    fn is_expired(&self) -> bool {
        let now = chrono::Utc::now().timestamp();
        now >= self.expires_at
    }

    fn expires_in(&self) -> i64 {
        let now = chrono::Utc::now().timestamp();
        self.expires_at - now
    }

    fn time_until_refresh(&self) -> i64 {
        let expires_in = self.expires_in();
        // Refresh when less than 10% of lifetime remains
        let refresh_threshold = (self.expires_at - self.issued_at) / 10;
        expires_in - refresh_threshold
    }

    fn needs_refresh(&self) -> bool {
        self.time_until_refresh() <= 0
    }
}

#[derive(Debug, Clone)]
pub enum TokenStatus {
    Valid {
        expires_in: i64,
        time_until_refresh: i64,
    },
    NeedsRefresh {
        expires_in: i64,
        time_until_refresh: i64,
    },
    Expired {
        expired_for: i64,
    },
    NotPresent,
}

// Internal helper functions to avoid code duplication
async fn validate_token_internal<T: Auth0ClientTrait>(
    client: &T,
    token: &str,
) -> Result<Claims, Auth0Error> {
    let header = decode_header(token)?;
    let jwks = get_jwks_internal(client).await?;

    let kid = header
        .kid
        .ok_or_else(|| Auth0Error::NotFound("Token kid not found".to_string()))?;

    let jwk = jwks
        .find(&kid)
        .ok_or_else(|| Auth0Error::NotFound("JWK not found".to_string()))?;

    match &jwk.algorithm {
        AlgorithmParameters::RSA(ref rsa) => {
            let decoding_key = DecodingKey::from_rsa_components(&rsa.n, &rsa.e)?;
            let mut validation = Validation::new(Algorithm::RS256);
            let config = client.get_config();
            validation.set_audience(&[config.audience.clone()]);
            validation.set_issuer(&[format!("https://{}/", config.domain)]);

            let token_result = decode::<Claims>(token, &decoding_key, &validation);

            match token_result {
                Ok(token_data) => Ok(token_data.claims),
                Err(err) => {
                    info!("Error validating token: {}", err);
                    if err.to_string().contains("InvalidAudience") {
                        let mut validation = Validation::new(Algorithm::RS256);
                        validation.set_audience(&[config.audience.clone()]);
                        validation.set_issuer(&[format!("https://{}/", config.domain)]);

                        let token_data = decode::<Claims>(token, &decoding_key, &validation)?;
                        Ok(token_data.claims)
                    } else {
                        Err(err.into())
                    }
                }
            }
        }
        alg => Err(Auth0Error::UnsupportedAlgorithm(alg.clone())),
    }
}

async fn get_jwks_internal<T: Auth0ClientTrait>(client: &T) -> Result<JwkSet, Auth0Error> {
    let cache = client.get_jwks_cache();
    let config = client.get_config();

    if let Some(jwks) = cache.get("jwks").await {
        return Ok(jwks);
    }

    let jwks_url = format!("https://{}/.well-known/jwks.json", config.domain);
    let reqwest_client = reqwest::Client::new();
    let jwks: JwkSet = reqwest_client.get(&jwks_url).send().await?.json().await?;

    cache.insert("jwks".to_string(), jwks.clone()).await;
    Ok(jwks)
}
