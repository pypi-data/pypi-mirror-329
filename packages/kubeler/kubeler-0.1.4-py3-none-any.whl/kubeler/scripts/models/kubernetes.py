from pydantic import BaseModel
from pydantic.fields import Field

class Resource(BaseModel):
    type: str = Field(title="Type of the resource", min_length=3)
    name: str | bool | int = Field(title="Name of the resource", min_length=3)
    namespace: str | bool | int = Field(title="Namespace of the resource", min_length=3)
