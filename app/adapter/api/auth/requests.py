from pydantic import BaseModel


class LoginInfo(BaseModel):
    user_id: str
    password: str

    def to_dict(self):
        return {"user_id": self.user_id, "password": self.password}