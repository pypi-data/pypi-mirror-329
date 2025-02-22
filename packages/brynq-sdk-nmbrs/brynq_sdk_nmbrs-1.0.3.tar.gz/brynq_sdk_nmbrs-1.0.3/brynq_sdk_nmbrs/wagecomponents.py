import math
import pandas as pd
import requests


class EmployeeFixedWageComponents:
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
        if employee_id:
            params['year'] = year
        if employee_id:
            params['period'] = period
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/fixedwagecomponents",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='fixedWageComponents',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def create(self,
               employee_id: str,
               data: dict):
        allowed_fields = {
            'end_year': "endYear",
            'end_period': "endPeriod",
            "comment": "comment",
            "costcenter": "costCenterId",
            "costunit": "costUnitId"
        }
        required_fields = ['code', "year", "period", "value"]
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "code": data["code"],
            "value": data["value"],
            "periodDetails": {
                "year": int(data["year"]),
                "period": int(data["period"])
            },
            "unprotectedMode": True
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedwagecomponent",
                                       json=payload)
        return resp

    def update(self,
               employee_id: str,
               data: dict):

        allowed_fields = {
            'end_year': "endYear",
            'end_period': "endPeriod",
            "comment": "comment",
            "costcenter": "costCenterId",
            "costunit": "costUnitId",
            "code": "code",
            "value": "value"
        }
        required_fields = ["fixed_wage_component_id", "period", "year"]
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "fixedWageComponentId": data["fixed_wage_component_id"],
            "periodDetails": {
                "year": int(data["year"]),
                "period": int(data["period"])
            },
            "unprotectedMode": True
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedwagecomponent",
                                      json=payload)
        return resp

    def delete(self,
               employee_id: str,
               wagecomponent_id: str):
        resp = self.nmbrs.session.delete(url=f"{self.nmbrs.base_url}employees/{employee_id}/wagecomponents/{wagecomponent_id}")
        return resp


class EmployeeVariableWageComponents:
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
        if employee_id:
            params['year'] = year
        if employee_id:
            params['period'] = period
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/variablewagecomponents",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='variablewagecomponents',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def create(self,
               employee_id: str,
               data: dict):
        allowed_fields = {
            'end_year': "endYear",
            'end_period': "endPeriod",
            "comment": "comment",
            "costcenter": "costCenterId",
            "costunit": "costUnitId"
        }
        required_fields = ['code', "year", "period", "value"]
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "code": data["code"],
            "value": data["value"],
            "periodDetails": {
                "year": data["year"],
                "period": data["period"]
            },
            "unprotectedMode": True
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/variablewagecomponent",
                                       json=payload)
        return resp

    def update(self,
               employee_id: str,
               params: dict):
        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/variablewagecomponent",
                                      params=params)
        return resp

    def delete(self,
               employee_id: str,
               wagecomponent_id: str):
        resp = self.nmbrs.session.delete(url=f"{self.nmbrs.base_url}employees/{employee_id}/wagecomponents/{wagecomponent_id}")

        return resp
