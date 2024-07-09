from pandera.typing import Series
from pandera import Field
import numpy as np

from source.schema.base_schema import BaseSchema


class DummyData(BaseSchema):
    """Schema for dummy data."""

    _label = "dummy_data_schema"

    # x1_transaction_date: date of real estate sale
    x1_transaction_date: Series[np.datetime64] = Field()

    # x2_house_age: in years
    x2_house_age: Series[int] = Field()

    # x3_distance_to_nearest_mrt_station: in kms
    x3_distance_to_nearest_mrt_station: Series[int] = Field()

    # x4_number_of_convenience_stores: within 10 km radius
    x4_number_of_convenience_stores: Series[int] = Field()

    # x5_latitude: location measure
    x5_latitude: Series[float] = Field()

    # x6_longitude: location measure
    x6_longitude: Series[float] = Field()

    # y_house_price_of_unit_area: our target
    y_house_price_of_unit_area: Series[float] = Field()
