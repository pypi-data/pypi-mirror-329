use anyhow::{anyhow, Result};
use jsonwebtoken::{decode, Algorithm, DecodingKey, TokenData, Validation};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub iss: String,
    pub sub: String,
    #[serde(default)]
    pub aud: Vec<String>,
    pub iat: i64,
    pub exp: i64,
    pub scope: String,
    pub azp: String,
    #[serde(default)]
    pub permissions: Vec<String>,
}

pub struct JwtVerifier {
    decoding_key: DecodingKey,
}

impl JwtVerifier {
    pub fn new(public_key_pem: &str) -> Result<Self> {
        let decoding_key = DecodingKey::from_rsa_pem(public_key_pem.as_bytes())
            .map_err(|e| anyhow!("Failed to create decoding key: {}", e))?;

        Ok(Self { decoding_key })
    }

    pub fn new_unchecked() -> Self {
        Self {
            decoding_key: DecodingKey::from_secret(&[]), // Dummy key for unchecked decoding
        }
    }

    pub fn verify_token(&self, token: &str) -> Result<Claims> {
        let mut validation = Validation::new(Algorithm::RS256);
        validation.validate_exp = true;
        validation.leeway = 0;

        let token_data: TokenData<Claims> =
            decode::<Claims>(token, &self.decoding_key, &validation)
                .map_err(|e| anyhow!("Invalid token: {}", e))?;

        Ok(token_data.claims)
    }

    pub fn decode_token_unchecked(&self, token: &str) -> Result<Claims> {
        let mut validation = Validation::new(Algorithm::RS256);
        validation.validate_exp = false;
        validation.validate_nbf = false;
        validation.validate_aud = false;
        validation.required_spec_claims.clear();
        validation.insecure_disable_signature_validation();

        let token_data = decode::<Claims>(token, &self.decoding_key, &validation)
            .map_err(|e| anyhow!("Failed to decode token: {}", e))?;

        Ok(token_data.claims)
    }
}
