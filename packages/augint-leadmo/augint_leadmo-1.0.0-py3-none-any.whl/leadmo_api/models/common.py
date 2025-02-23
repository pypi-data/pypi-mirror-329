from pydantic import BaseModel, field_validator


def snake_to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string.")
    words = value.split("_")
    value = "".join(word.title() for word in words if word)
    return f"{value[0].lower()}{value[1:]}"


class BaseLeadmoApiCallModel(BaseModel):
    """Base class for all serializable objects. Provides a stable interface and convenient serialization methods."""

    class Config:
        """Pydantic configuration for the Serializable class"""

        alias_generator = snake_to_camel_case
        extra = "ignore"
        populate_by_name = True
        validate_assignment = True
        populate_by_alias = True

    def model_dump(self, exclude_none=True, **kwargs):
        return super().model_dump(exclude_none=exclude_none, **kwargs)

    @field_validator("*", mode="before")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v
