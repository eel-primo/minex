from pydantic import BaseModel

class ServersBase(BaseModel):
    ip: str
    title: str | None = None
    note: str | None = None
    last_online: int


class ServerCreate(ServersBase):
    ip: str
    title: str | None = "My server"
    note: str | None = None
    last_online: int


class Server(ServersBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    uuid: str


class UserCreate(UserBase):
    uuid: str


class User(UserBase):
    id: int
    is_banned: bool
    servers: list[Server] = []

    class Config:
        orm_mode = True