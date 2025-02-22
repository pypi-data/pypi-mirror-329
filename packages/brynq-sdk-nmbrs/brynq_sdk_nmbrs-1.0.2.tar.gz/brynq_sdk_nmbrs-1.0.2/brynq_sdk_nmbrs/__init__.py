import warnings
from typing import Union, List
import re
import pandas as pd
import requests
from brynq_sdk_brynq import BrynQ
from .children import Children
from .companies import Companies
from .employees import Employees


class Nmbrs(BrynQ):
    def __init__(self, label: Union[str, List], debug: bool = False):
        super().__init__()
        headers = self._get_request_headers(label=label)
        self.base_url = "https://api.nmbrsapp.com/api/"
        self.session = requests.Session()
        self.session.headers.update(headers)
        # self.session.headers.update({'Content-Type': 'application/json'})
        self.companies = Companies(self)
        self.employees = Employees(self)
        self.children = Children(self)
        self.debug = debug

    def _get_request_headers(self, label):
        initial_credentials = self.get_system_credential(system='nmbrs', label=label)
        credentials = self.refresh_system_credential(system='nmbrs', system_id=initial_credentials['id'])
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {credentials['access_token']}",
            # partner identifier
            "X-Subscription-Key": "39c45d5570ed4061a101ff2767106220"
        }

        return headers

    def get_paginated_result(self, request: requests.Request) -> List:
        has_next_page = True
        result_data = []
        while has_next_page:
            prepped = request.prepare()
            prepped.headers.update(self.session.headers)
            resp = self.session.send(prepped)
            resp.raise_for_status()
            response_data = resp.json()
            result_data += response_data['data']
            next_page_url = response_data.get('pagination').get('nextPage')
            has_next_page = next_page_url is not None
            request.url = next_page_url

        return result_data

    def check_fields(self, data: Union[dict, List], required_fields: List, allowed_fields: List):
        if isinstance(data, dict):
            data = data.keys()

        if self.debug:
            print(f"Required fields: {required_fields}")
            print(f"Allowed fields: {allowed_fields}")
            print(f"Data: {data}")

        for field in data:
            if field not in allowed_fields and field not in required_fields:
                warnings.warn('Field {field} is not implemented. Optional fields are: {allowed_fields}'.format(field=field, allowed_fields=tuple(allowed_fields)))

        for field in required_fields:
            if field not in data:
                raise ValueError('Field {field} is required. Required fields are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

    def _rename_camel_columns_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        def camel_to_snake_case(column):
            # Replace periods with underscores
            column = column.replace('.', '_')
            # Insert underscores before capital letters and convert to lowercase
            return re.sub(r'(?<!^)(?=[A-Z])', '_', column).lower()

        df.columns = map(camel_to_snake_case, df.columns)

        return df
