import pandas as pd
import requests


class Hours:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get_types(self,
                  company_id: str) -> pd.DataFrame:
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/hourcodes")

        df = self.nmbrs.get_paginated_result(request)

        return df


class VariableHours:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            employee_id: str,
            created_from: str = None,
            period: int = None,
            year: int = None) -> pd.DataFrame:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        if period:
            params['period'] = period
        if year:
            params['year'] = year
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}employees/{employee_id}/variablehours",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = self.nmbrs._rename_camel_columns_to_snake_case(pd.DataFrame(data))

        return df

    def create(self,
               employee_id: str,
               params: dict):
        # TODO: implement required and optional fields
        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/variablehours",
                                       params=params)
        return resp

    def update(self,
               employee_id: str,
               params: dict):
        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/variablehours",
                                      params=params)
        return resp

    def delete(self,
               employee_id: str,
               hourcomponent_id: str):
        resp = self.nmbrs.session.delete(url=f"{self.nmbrs.base_url}employees/{employee_id}/hours/{hourcomponent_id}")
        return resp


class FixedHours:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            company_id: str,
            created_from: str = None,
            employee_id: str = None,
            period: int = None,
            year: int = None) -> pd.DataFrame:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        if employee_id:
            params['employeeId'] = employee_id
        if period:
            params['period'] = period
        if year:
            params['year'] = year
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedhours",
                                   params=params)

        df = self.nmbrs.get_paginated_result(request)

        return df

    def create(self,
               employee_id: str,
               params: dict):
        # TODO: implement required and optional fields
        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedhours",
                                       params=params)
        return resp

    def update(self,
               employee_id: str,
               params: dict):
        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedhours",
                                      params=params)
        return resp

    def delete(self,
               employee_id: str,
               hourcomponent_id: str):
        resp = self.nmbrs.session.delete(url=f"{self.nmbrs.base_url}employees/{employee_id}/hours/{hourcomponent_id}")
        return resp