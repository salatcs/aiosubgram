from pydantic import BaseModel, ConfigDict

class SubgramObject(BaseModel):
    """Base class for all types"""
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        extra='ignore'
    )