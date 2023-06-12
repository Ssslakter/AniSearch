import os
from dataclasses import dataclass, fields
import dotenv
from dataclass_wizard import YAMLWizard

ENV = "PROJECT_ENV"


@dataclass
class QdrantConfig:
    """Config for qdrant storage client"""

    collection_name: str
    url: str | None
    api_key: str | None
    distance_func: str = "Cosine"


@dataclass
class Secrets:
    """All app secrets. Get transfered into configs at runtime after calling `load_configs`"""

    qdrant_key: str


@dataclass
class Config(YAMLWizard):
    """Main config"""

    qdrant: QdrantConfig
    models_dir: str

    def transfer_secrets(self, secrets: Secrets):
        """Takes secrets and puts them into configs"""
        self.qdrant.api_key = secrets.qdrant_key
        return self


def _load_secrets(dotenvs: dict[str, str | None]) -> Secrets:
    secrets_fields = fields(Secrets)
    secrets = Secrets(
        **{  # type: ignore
            field.name: value
            if (value := os.getenv(field.name)) is not None
            else dotenvs.get(field.name)
            for field in secrets_fields
        }
    )
    return secrets


def load_configs(dotenv_path: str | None = None) -> Config:
    """Loads config from .yml and .env files and environment variables"""
    dotenvs = dotenv.dotenv_values(dotenv_path)

    current_env = value if (value := os.getenv(ENV)) is not None else dotenvs.get(ENV)

    secrets = _load_secrets(dotenvs)
    config_file = f"settings.{current_env}.yaml"

    yaml_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), config_file
    )
    config: Config = Config.from_yaml_file(yaml_file_path)  # type: ignore

    return config.transfer_secrets(secrets)
