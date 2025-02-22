import math
import pandas as pd
import requests


class Address:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            company_id: str,
            created_from: str = None) -> pd.DataFrame:
        params = {} if created_from is None else {'createdFrom': created_from}
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/addresses",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='addresses',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def create(self,
               employee_id: str,
               data: dict):
        required_fields = ["street", "city", "country_code", "period", "year"]
        allowed_fields = {
            "house_number": "houseNumber",
            "house_number_addition": "houseNumberAddition",
            "postal_code": "postalCode",
            "province": "stateProvince",
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "isDefault": True,
            "type": "homeAddress",
            "street": data["street"],
            "city": data["city"],
            "countryISOCode": data["country_code"],
            "period": {
                "period": data["period"],
                "year": data["year"]
            }
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/address",
                                       json=payload)
        return resp
