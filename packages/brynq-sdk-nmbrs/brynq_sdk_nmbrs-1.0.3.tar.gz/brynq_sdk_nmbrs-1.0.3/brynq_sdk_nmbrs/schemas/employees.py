import pandas as pd
import pandera as pa
from pandera.typing import Series, String, DateTime


class EmployeeSchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    personal_info_id: Series[String] = pa.Field(coerce=True)
    created_at: Series[DateTime] = pa.Field(coerce=True)
    basic_info_employee_number: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    basic_info_first_name: Series[String] = pa.Field(coerce=True, nullable=True)
    basic_info_first_name_in_full: Series[String] = pa.Field(coerce=True, nullable=True)
    basic_info_prefix: Series[String] = pa.Field(coerce=True, nullable=True)
    basic_info_initials: Series[String] = pa.Field(coerce=True, nullable=True)
    basic_info_last_name: Series[String] = pa.Field(coerce=True)
    basic_info_employee_type: Series[String] = pa.Field(coerce=True)
    birth_info_birth_date: Series[DateTime] = pa.Field(coerce=True)
    birth_info_birth_country_code_i_s_o: Series[String] = pa.Field(coerce=True, nullable=True)
    birth_info_nationality_code_i_s_o: Series[String] = pa.Field(coerce=True, nullable=True)
    birth_info_gender: Series[String] = pa.Field(coerce=True)
    contact_info_private_email: Series[String] = pa.Field(coerce=True, nullable=True)
    contact_info_business_email: Series[String] = pa.Field(coerce=True, nullable=True)
    contact_info_business_phone: Series[String] = pa.Field(coerce=True, nullable=True)
    contact_info_business_mobile_phone: Series[String] = pa.Field(coerce=True, nullable=True)
    contact_info_private_phone: Series[String] = pa.Field(coerce=True, nullable=True)
    contact_info_private_mobile_phone: Series[String] = pa.Field(coerce=True, nullable=True)
    contact_info_other_phone: Series[String] = pa.Field(coerce=True, nullable=True)
    partner_info_partner_prefix: Series[String] = pa.Field(coerce=True, nullable=True)
    partner_info_partner_name: Series[String] = pa.Field(coerce=True, nullable=True)
    period_year: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    period_period: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    birth_info_birth_country: Series[String] = pa.Field(coerce=True, nullable=True)
    company_id: Series[String] = pa.Field(coerce=True)