# src/stratio/api/session/sessions.py
from abc import abstractmethod


class ApiSession:
    @abstractmethod
    def get_session_info(self):
        pass


class ProfileApiSession(ApiSession):
    def __init__(self, profile_name: str):
        self.profile_name = profile_name

    def get_profile_name(self):
        return self.profile_name

    def get_session_info(self):
        return {"profile": self.profile_name}


class CredentialsApiSession(ApiSession):
    def __init__(self, key_id: str, secret_key: str, account_id: str, region_name: str = None):
        self.key_id = key_id
        self.secret_key = secret_key
        self.account_id = account_id
        self.region_name = region_name

    def get_session_info(self):
        return {
            "key_id": self.key_id,
            "secret_key": self.secret_key,
            "account_id": self.account_id,
            "region_name": self.region_name,
        }
