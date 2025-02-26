from typing import Any, Dict
from uuid import UUID

from ul_api_utils.internal_api.internal_api import InternalApi

from notification_sdk.notification_sdk_config import NotificationSdkConfig


class NotificationSdk:
    def __init__(self, config: NotificationSdkConfig) -> None:
        self._config = config

        self._api_notification = InternalApi(
            entry_point=self._config.api_url, default_auth_token=self._config.api_token,
        )

    def send_email_message(
        self,
        template_id: UUID,
        template_data: Dict[str, Any],
        email_to: str,
    ) -> None:
        self._api_notification.request_post(
            f"templates/{template_id}/emails",
            json={
                "template_data": template_data,
                "email_to": email_to,
            },
        ).check()
