# src/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # AI Config
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # Epic FHIR Config
    epic_client_id: str = Field(default="pending_client_id", env="EPIC_CLIENT_ID")
    epic_private_key_path: str = Field(default="", env="EPIC_PRIVATE_KEY_PATH")
    epic_fhir_base_url: str = Field(
        default="https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/", 
        env="EPIC_FHIR_BASE_URL"
    )

    # Automatically load the .env file at the root of the project
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Create a global instance of the settings to be imported across the app
config = Settings()