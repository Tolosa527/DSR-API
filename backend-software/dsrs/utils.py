import requests
from digital.settings import EXCHANGE_API_KEY, EXCHANGE_URL
import pandas as pd
import numpy as npzz


class Utils:

    """
    This class provides you some methods to work with DSRS in a more abstract
    and maintainable way
    """

    def __init__(self):
        pass

    def AnyCurrencyToEUR(self, CurrencyFrom: list, currencyTo="EUR") -> dict:
        """
        This method allows you to convert any currency amount to
        Euros.

        Example:
            euros = AnyCunrrencyToEUR(CurrenctFrom)

        """
        currencies = ",".join(CurrencyFrom)
        request = f"{EXCHANGE_URL}?access_key={EXCHANGE_API_KEY}&base={currencyTo}&symbols={currencies}"
        print(f"REQUESTING: {request}")
        try:
            response = requests.get(request)
            return self.__rates_calc(response.json().get("rates"))
        except Exception as e:
            print(f"IT WAS AN EXCEPTION: {e}")

    def from_tsv_to_list(self, path) -> list:

        import gzip

        """
            This function takes a path where the file is stored
            and returns a list of dsrs

            Examaple:

                list_of_dsr = from_tsv_to_list(path)
        """

        with gzip.open(path) as file:
            return [
                line.decode("utf-8").split("\t") for line in file.read().splitlines()
            ]

    def get_dict_from_model(self, model) -> dict:

        """
        Return a dictionary from a Data Model
        """

        dict = {
            "dsp_id": [],
            "title": [],
            "artists": [],
            "isrc": [],
            "usages": [],
            "revenue": [],
            "dsr": [],
        }
        for item in model:
            dict["dsp_id"].append(item.dsp_id)
            dict["title"].append(item.title)
            dict["artists"].append(item.artists)
            dict["isrc"].append(item.isrc)
            dict["usages"].append(item.usages)
            dict["revenue"].append(item.revenue)
            dict["dsr"].append(item.dsrs)

        return dict

    def make_resource_payload(self, resources: list) -> dict:

        """
        Returns a dict from a list of resources
        """

        result = []

        for index in range(len(resources)):
            resource_dict = {}

            dsr_dict = {
                "path": resources[index].get("dsr").path,
                "period_start": resources[index].get("dsr").period_start,
                "period_end": resources[index].get("dsr").period_end,
                "status": resources[index].get("dsr").status,
                "territory": resources[index].get("dsr").territory.code_2,
                "currency": resources[index].get("dsr").currency.code,
            }

            resource_dict["dsp_id"] = resources[index].get("dsp_id")
            resource_dict["title"] = resources[index].get("title")
            resource_dict["artists"] = resources[index].get("artists")
            resource_dict["isrc"] = resources[index].get("isrc")
            resource_dict["usages"] = resources[index].get("usages")
            resource_dict["revenue"] = resources[index].get("revenue")
            resource_dict["dsr"] = dsr_dict

            result.append(resource_dict)

        return result

    def dataFrame_resource_process(
        self, resources: dict, rates: dict, percentile: float
    ) -> list:

        """
        It takes tow dicts and creates a dataFrame to make the modifications and cals.
        It returns a list with the resources ordered and filtered by the percentile
        specified as a parameter.
        """

        result = []
        revenue_EUR_list = []
        revenue_sum = 0

        df = pd.DataFrame(resources)
        df["revenue"] = df["revenue"].replace("", 0)
        for index in range(len(df)):
            revenue_EUR_list.append(
                rates.get(df["dsr"][index].currency.code) * df["revenue"][index]
            )
        df["revenue_EUR"] = np.array(revenue_EUR_list)
        sorted_df = df.sort_values(by="revenue_EUR", ascending=False)
        percentile_condition = sum(sorted_df["revenue_EUR"]) * percentile

        for index, row in sorted_df.iterrows():
            revenue_sum += row["revenue_EUR"]
            if revenue_sum <= percentile_condition:
                result.append(row.to_dict())

        return result

    def __rates_calc(self, rates: dict) -> dict:

        result_dict = {}

        for key, value in rates.items():
            result_dict[key] = 1 / value

        return result_dict
