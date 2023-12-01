from pydantic import BaseModel


class Template(BaseModel):
    name: str
    fields: dict[str, str]
