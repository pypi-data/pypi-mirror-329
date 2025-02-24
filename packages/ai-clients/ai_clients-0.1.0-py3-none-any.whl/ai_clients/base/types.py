from pydantic import BaseModel, ConfigDict


class ExtendBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')
