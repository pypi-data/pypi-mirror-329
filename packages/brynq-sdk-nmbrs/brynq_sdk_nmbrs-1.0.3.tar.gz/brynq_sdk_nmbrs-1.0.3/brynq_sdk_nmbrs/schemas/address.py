import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions


class AddressSchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    address_id: Series[String] = pa.Field(coerce=True)
    is_default: Series[Bool] = pa.Field(coerce=True)
    type: Series[String] = pa.Field(coerce=True, isin=["homeAddress", "postAddress", "absenceAddress", "holidaysAddress", "weekendAddress", "workAddress"])
    street: Series[String] = pa.Field(coerce=True)
    house_number: Series[String] = pa.Field(coerce=True, nullable=True)
    house_number_addition: Series[String] = pa.Field(coerce=True, nullable=True)
    postal_code: Series[String] = pa.Field(coerce=True)
    city: Series[String] = pa.Field(coerce=True)
    state_province: Series[String] = pa.Field(coerce=True, nullable=True)
    country_i_s_o_code: Series[String] = pa.Field(coerce=True, nullable=True)
    period_year: Series[pd.Int64Dtype] = pa.Field(coerce=True, nullable=True)
    period_period: Series[pd.Int64Dtype] = pa.Field(coerce=True, nullable=True)
    # created_at: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    # company_id: Series[String] = pa.Field(coerce=True)
