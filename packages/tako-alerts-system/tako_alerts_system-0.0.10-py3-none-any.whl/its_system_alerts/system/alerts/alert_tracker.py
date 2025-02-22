"""
Abstract class to handle alert tracker
"""

import json
import os
from abc import ABC, abstractmethod
from typing import TypeVar, Union

import requests as rq
from loguru import logger
from twilio.rest import Client

T = TypeVar("T", bound=Union[list, dict])


class AlertTracker(ABC):
    """
    Abstract class to handle alert tracker
    """

    def __init__(self, redis_client, whatsapp_config: dict, time_window: int = 300, alert_threshold: int = 5):
        """
        Constructor for the class

        :param redis_client: Redis client
        :param whatsapp_config: Whatsapp configuration
        :param time_window: Time window in seconds
        :param alert_threshold: Alert threshold
        """
        self.redis_client = redis_client
        self.whatsapp_config = whatsapp_config
        self.time_window = time_window
        self.alert_threshold = alert_threshold

    @abstractmethod
    def process_alert(self, data: T):  # type: ignore
        """
        Process the alert
        """

    def send_whatsapp_notification(self, message: str, recipients: list):
        """
        Send a whatsapp notification
        """
        if not recipients:
            logger.warning("No recipients provided for WhatsApp notification")
            return False

        twilio_client = Client(self.whatsapp_config["twilio_account_sid"], self.whatsapp_config["twilio_auth_token"])
        for recipient in recipients:
            message_sent = twilio_client.messages.create(
                body=message, from_=self.whatsapp_config["twilio_phone_number"], to=recipient
            )
            logger.info(f"WhatsApp notification sent to {recipient} message: {message_sent.body}")  # type: ignore
        return True

    @abstractmethod
    def send_email_notification(self, message: str):
        """
        Send an email notification
        """

    def login_tako(self, url_login: str) -> str:
        """
        Login in the platform
        """
        payload_for_login = {"username": os.getenv("USERNAME_CCZ_LOGIN"), "password": os.getenv("PASSWORD_CCZ_LOGIN")}
        headers_for_login = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = rq.request("POST", url_login, headers=headers_for_login, data=payload_for_login, timeout=20)
            return response.json()["access_token"]
        except KeyError:
            return ""

    def save_to_postgres(self, url: str, login_url, data: dict, token: str = ""):
        """
        Save the alert to postgres
        """
        try:
            if token == "":
                token = self.login_tako(url_login=login_url)

            response = rq.post(
                url,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=10,
            )
            response.raise_for_status()
        except rq.exceptions.Timeout:
            logger.error("Timeout error")
            return
        except rq.exceptions.ConnectionError:
            logger.error("Connection error")
            return
        except rq.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return
        except rq.exceptions.RequestException as e:
            logger.error(f"Request exception occurred: {e}")
            return
