import hmac
import hashlib
import urllib.parse


class InvalidInitDataError(Exception):
    pass

class InitData:
    def __init__(self, data: str, bot_token: str):
        if not data or not bot_token:
            missing = [param for param in ("data", "bot_token") if not eval(param)]
            raise InvalidInitDataError(f"Missing {" and ".join(missing)}")
        self.data_raw = data
        self.bot_token = bot_token

    def _decode_data(self, times_to_decode: int) -> None:
        for _ in range(times_to_decode):
            self.data_raw = urllib.parse.unquote(self.data_raw)

    def _pop_hash(self, data_entries: list[str]) -> str:
        for i, entry in enumerate(data_entries):
            if entry.startswith("hash="):
                hash_ = data_entries.pop(i)[5:]
                return hash_
        raise InvalidInitDataError("Hash is missing")
    
    def _generate_bot_signature(self) -> bytes:
        bot_signature = hmac.new(
            b"WebAppData",
            self.bot_token.encode(),
            hashlib.sha256
        ).digest()
        return bot_signature
    
    def _generate_init_data_signature(self) -> str:
        init_data_signature = hmac.new(
            self._generate_bot_signature(),
            self.data_raw.encode(),
            hashlib.sha256
        ).hexdigest()
        return init_data_signature
    
    def _prepare_hash_and_data(self) -> None:
        data_entries = self.data_raw.split("&")
        self.hash = self._pop_hash(data_entries)
        data_entries.sort()
        self.data_raw = "\n".join(data_entries)

    def validate(self, *, times_to_decode: int = 1) -> bool:
        self._decode_data(times_to_decode)
        self._prepare_hash_and_data()
        self.signature = self._generate_init_data_signature()
        return self.signature == self.hash