import typer

from thestage.i18n.translation import __
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.core_files.config_entity import ConfigEntity


class ValidationService:
    _thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
    ):
        self._thestage_api_client = thestage_api_client
        self._config_provider = config_provider


    def check_token(
            self,
            config: ConfigEntity,
    ):
        token = config.main.thestage_auth_token
        if not token:
            token: str = typer.prompt(
                text=f'Authenticate using valid TheStage AI API token ({config.main.thestage_api_url})',
                show_choices=False,
                type=str,
                show_default=False,
            )

# TODO this fails with 503 error - AttributeError("'bytes' object has no attribute 'text'") from _parse_api_response method in core
        is_valid: bool = False
        if token:
            is_valid = self._thestage_api_client.validate_token(token=token)
        if not is_valid:
            typer.echo(__(
                'API token is invalid: generate API token using TheStage AI WebApp'
            ))
            raise typer.Exit(1)

        config.main.thestage_auth_token = token


    @staticmethod
    def is_present_token(config: ConfigEntity) -> bool:
        present_token = True
        if not config:
            present_token = False
        else:
            if not config.main.thestage_auth_token:
                present_token = False

            if config.start_on_daemon:
                if config.daemon and config.daemon.daemon_token:
                    present_token = True
                else:
                    present_token = False

        return present_token
