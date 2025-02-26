from typing import Optional, List, Tuple

from thestage.services.clients.thestage_api.core.api_client_abstract import TheStageApiClientAbstract
from thestage.services.clients.thestage_api.dtos.base_response import TheStageBaseResponse
from thestage import __version__


class TheStageApiClientCore(TheStageApiClientAbstract):

    def __init__(self, timeout: int = 90, url: Optional[str] = None):
        super(TheStageApiClientCore, self).__init__(timeout=timeout, url=url)

    def validate_token(self, token: str) -> bool:
        data = {
            "userApiToken": token,
            "cliVersion": __version__,
        }

        response = self._request(
            method='POST',
            url='/user-api/v1/validate-token',
            data=data,
        )
        result = TheStageBaseResponse.model_validate(response) if response else None
        return result.is_success if result else False
