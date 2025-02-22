import pandas as pd
import requests
import math


class Bank:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            company_id: str,
            created_from: str = None) -> pd.DataFrame:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        try:
            request = requests.Request(method='GET',
                                       url=f"{self.nmbrs.base_url}companies/{company_id}/employees/bankaccounts",
                                       params=params)

            data = self.nmbrs.get_paginated_result(request)
            df = pd.json_normalize(
                data,
                record_path='bankAccounts',
                meta=['employeeId']
            )
            df = self.nmbrs._rename_camel_columns_to_snake_case(df)
        except requests.HTTPError as e:
            df = pd.DataFrame()

        return df

    def create(self,
               employee_id: str,
               data: dict):

        required_fields = ["iban"]
        allowed_fields = {
            "account_number": "number",
            "description": "description",
            "city_of_bank": "city",
            "name_of_bank": "name",
            "bank_account_type": "bankAccountType"
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "IBAN": data["iban"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/bankaccount",
                                       json=payload)
        return resp

    def update(self,
               employee_id: str,
               data: dict):

        required_fields = ["bank_account_id"]
        allowed_fields = {
            "account_number": "number",
            "description": "description",
            "city_of_bank": "city",
            "name_of_bank": "name",
            "bank_country_code": "countryCode"
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "bankAccountId": data["bank_account_id"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/bankaccount",
                                      json=payload)
        return resp
