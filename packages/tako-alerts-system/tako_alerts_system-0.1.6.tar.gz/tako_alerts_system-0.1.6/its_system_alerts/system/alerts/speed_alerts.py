"""
Class to handle alerts related to speed
sleep are going to be reading from the P60 and P20 tram
This is detected by Tako

Note: This is a punctual speed
"""

import datetime
import os
import time

import pytz
import redis
from loguru import logger

from its_system_alerts.system.alerts.alert_tracker import AlertTracker

ALERT_NAME_CODE = "speeding"
ALERT_TAKO_TYPE_CODE = "6"
COOLDOWN_SECONDS = 180  # 3 minutos
SPEED_OVERRIDE_THRESHOLD = 65  # km/h
TEMPLATE_MESSAGE = """
🚨 *Alerta de velocidad*
⏰ {fechaHoraLecturaDato}
🚍 Vehículo: {numero_carro}
🚏 Ruta: {idRuta}
🚫 Velocidad: {velocidad} km/h
📍 {direccion}
"""


class SpeedAlerts(AlertTracker):
    """
    Class to handle alerts related to speed
    """

    def __init__(
        self,
        redis_client: redis.Redis,
        whatsapp_config: dict,
        time_window: int = 300,
        alert_threshold: int = 2,
    ):
        """
        Initialize the SpeedAlerts class.

        Args:
            redis_client (redis.Redis): Redis client instance.
            whatsapp_config (dict): Configuration for WhatsApp.
            time_window (int, optional): Time window for alert tracking. Defaults to 300 seconds.
            alert_threshold (int, optional): Alert threshold. Defaults to 2.
        """
        super().__init__(
            redis_client=redis_client,
            whatsapp_config=whatsapp_config,
            time_window=time_window,
            alert_threshold=alert_threshold,
        )

    def _check_cooldown(self, company_id: str, vehicle_id: str) -> bool:
        """
        Verifica si el vehículo está en período de cooldown.

        Returns:
            bool: True si está en cooldown, False si no
        """
        cooldown_key = f"{ALERT_NAME_CODE}:cooldown:{company_id}:{vehicle_id}"
        return bool(self.redis_client.exists(cooldown_key))

    def _set_cooldown(self, company_id: str, vehicle_id: str):
        """
        Establece el período de cooldown para un vehículo
        """
        cooldown_key = f"{ALERT_NAME_CODE}:cooldown:{company_id}:{vehicle_id}"
        self.redis_client.setex(cooldown_key, COOLDOWN_SECONDS, "1")

    def send_email_notification(self, message: str):
        raise NotImplementedError

    def save_alert(self, data, alert_count, alert_type_code, whatsapp_send):
        """
        Save alert into the system
        """
        company_id = data.get("company_id")
        vehicle_id = data.get("idVehiculo")
        timestamp = data.get("fechaHoraLecturaDato")

        latitud = data.get("localizacionVehiculo", {}).get("latitud")
        longitud = data.get("localizacionVehiculo", {}).get("longitud")

        dt = datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S.%f")
        formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")

        alert = {
            "vehicle": vehicle_id,
            "longitud": str(longitud),
            "latitud": str(latitud),
            "last_reported_time": formatted_timestamp,
            "total_events": alert_count,
            "id_alert_type": alert_type_code,
            "send_whatsapp": whatsapp_send,
            "send_email": False,
            "company_id": company_id,
            "reported_its_route": data["idRuta"],
        }

        url_post = os.getenv("URL_POST_ALERT", "")
        url_login = os.getenv("URL_LOGIN_TAKO", "")

        self.save_to_postgres(url=url_post, login_url=url_login, data=alert)

    def _rule_activation(self, speed: float):
        return float(speed) >= 52

    def process_alert(self, data: dict):
        """
        Process the alert
        """
        company_id = data.get("company_id")
        vehicle_id = data.get("idVehiculo")
        route = data.get("idRuta")
        latitud = data.get("localizacionVehiculo", {}).get("latitud")
        longitud = data.get("localizacionVehiculo", {}).get("longitud")
        speed: float = data.get("velocidadVehiculo", 0.0)
        timestamp = data.get("fechaHoraLecturaDato")

        if not all([company_id, vehicle_id, speed, timestamp]):
            return

        if not self._rule_activation(speed):
            return

        # Verificar cooldown, a menos que la velocidad sea mayor al umbral de override
        if speed < SPEED_OVERRIDE_THRESHOLD and self._check_cooldown(str(company_id), str(vehicle_id)):
            logger.info(f"Cooldown detected for company {company_id} and vehicle {vehicle_id}")
            return

        redis_key = f"{ALERT_NAME_CODE}:{company_id}:{vehicle_id}:vel"
        current_time = time.time()

        if not timestamp:
            return

        local_tz = pytz.timezone("America/Bogota")
        dt = datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S.%f")
        dt_local = local_tz.localize(dt)
        dt_utc = dt_local.astimezone(pytz.utc)
        timestamp = dt_utc.timestamp()

        self.redis_client.zadd(redis_key, {timestamp: timestamp})
        self.redis_client.expire(redis_key, self.time_window * 5)
        self.redis_client.zremrangebyscore(redis_key, 0, current_time - self.time_window)
        alert_count = self.redis_client.zcard(redis_key)

        if alert_count >= self.alert_threshold or speed >= 60:
            logger.info(f"Speed alert triggered for company {company_id}, vehicle {vehicle_id}, speed {speed}")
            self.redis_client.delete(redis_key)
            address = self.get_address_from_coordinates(latitude=latitud, longitude=longitud)
            whatsapp_send = self.send_whatsapp_notification(
                message=TEMPLATE_MESSAGE.format(
                    fechaHoraLecturaDato=dt.strftime("%d/%m/%Y %H:%M:%S"),
                    numero_carro=vehicle_id,
                    velocidad=round(speed, 2),
                    idRuta=route,
                    direccion=address,
                ),
                recipients=self.whatsapp_config["recipients"],
            )

            # Establecer el cooldown después de enviar la alerta
            self._set_cooldown(str(company_id), str(vehicle_id))

            self.save_alert(
                data=data, alert_count=alert_count, alert_type_code=ALERT_TAKO_TYPE_CODE, whatsapp_send=whatsapp_send
            )
