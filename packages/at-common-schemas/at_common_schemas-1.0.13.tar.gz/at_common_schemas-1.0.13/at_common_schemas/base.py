from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class BaseSchema(BaseModel):
    """Base schema class with config for handling datetime and enum serialization"""
    model_config = ConfigDict(
        from_attributes=True
    )

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        # Convert datetime objects to ISO format strings and enum values to their values
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, Enum):
                data[key] = value.value
            elif isinstance(value, list):
                data[key] = [
                    item.isoformat() if isinstance(item, datetime)
                    else item.value if isinstance(item, Enum)
                    else item 
                    for item in value
                ]
        return data

    @classmethod
    def model_json_schema(cls, *args, **kwargs):
        schema = super().model_json_schema(*args, **kwargs)
        # Update schema to handle datetime serialization
        for prop in schema.get("properties", {}).values():
            if prop.get("type") == "string" and prop.get("format") == "date-time":
                prop["format"] = "date-time"
        return schema