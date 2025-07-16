import datetime
import base64
import hmac
import hashlib


class LicenseGenerator:
    """
    Gera e valida códigos de licença.
    Cada código embute data de expiração + HMAC truncado.
    """

    def __init__(self, secret_key: bytes, mac_size: int=8):
        self.secret_key = secret_key
        self.mac_size = mac_size

    def generate_code(self, expiration_date: datetime.date) -> str:
        date_str = expiration_date.isoformat()
        digest = hmac.new(self.secret_key, date_str.encode(), hashlib.sha256).digest()
        mac = digest[:self.mac_size]
        payload = date_str.encode() + b'|' + mac
        return base64.urlsafe_b64encode(payload).decode()

    @staticmethod
    def _parse_payload(payload_b64: str) -> tuple[datetime.date, bytes]:
        raw = base64.urlsafe_b64decode(payload_b64.encode())
        date_part, mac_part = raw.split(b'|', 1)
        return datetime.date.fromisoformat(date_part.decode()), mac_part

    def validate_code(self, code: str) -> datetime.date:
        exp_date, mac_part = self._parse_payload(code)
        expected = hmac.new(self.secret_key, exp_date.isoformat().encode(), hashlib.sha256).digest()[:self.mac_size]
        if not hmac.compare_digest(mac_part, expected):
            raise ValueError("Código de licença inválido")
        return exp_date
