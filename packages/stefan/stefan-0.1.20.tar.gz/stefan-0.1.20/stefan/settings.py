import json
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    stefan_openai_api_key: str
    stefan_anthropic_api_key: str
    stefan_deepseek_api_key: str
    stefan_google_service_account_json_string: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def google_service_account_json_dict(self) -> dict:
        return json.loads(self.stefan_google_service_account_json_string)

    @property
    def openai_api_key(self) -> str:
        return self.stefan_openai_api_key

    @property
    def anthropic_api_key(self) -> str:
        return self.stefan_anthropic_api_key

    @property
    def deepseek_api_key(self) -> str:
        return self.stefan_deepseek_api_key
