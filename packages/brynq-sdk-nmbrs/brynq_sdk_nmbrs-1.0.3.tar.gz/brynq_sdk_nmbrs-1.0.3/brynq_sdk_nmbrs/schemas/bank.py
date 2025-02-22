from datetime import datetime

import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions


class BankSchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    bank_account_id: Series[String] = pa.Field(coerce=True, nullable=True)
    number: Series[String] = pa.Field(coerce=True, nullable=True)
    description: Series[String] = pa.Field(coerce=True, nullable=True)
    i_b_a_n: Series[String] = pa.Field(coerce=True, nullable=True)
    city: Series[String] = pa.Field(coerce=True, nullable=True)
    name: Series[String] = pa.Field(coerce=True, nullable=True)
    bank_account_type: Series[String] = pa.Field(
        coerce=True,
        isin=[
            "bankAccount1",
            "bankAccount2",
            "bankAccount3",
            "bankAccount4",
            "bankAccount5",
            "salarySavings",
            "lifecycleSavingSchemes",
            "standard",
        ]
    )
    created_at: Series[datetime] = pa.Field(coerce=True)