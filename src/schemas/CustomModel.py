from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict

from src.utils.datetime_utils import convert_datetime_to_gmt


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: convert_datetime_to_gmt},
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)
