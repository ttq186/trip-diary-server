from pydantic import BaseModel

from utils import to_camel


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
