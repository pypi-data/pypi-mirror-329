import pandas as pd
import requests
from .costcenter import Costcenter, Costunit
from .hours import Hours
from .bank import Bank


class Companies:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs
        self.costcenters = Costcenter(nmbrs)
        self.costunits = Costunit(nmbrs)
        self.hours = Hours(nmbrs)
        self.banks = Bank(nmbrs)

    def get(self) -> pd.DataFrame:
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies")
        data = self.nmbrs.get_paginated_result(request)
        df = self.nmbrs._rename_camel_columns_to_snake_case(pd.DataFrame(data))

        return df
