from .base import StatsFetcher
from datetime import datetime, timedelta, date
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor


class ValueFetcher(StatsFetcher):

    def __init__(self, ticker: str, db_client):
        super().__init__(ticker, db_client)

    def prepare_query(self, start_date, end_date):
        pipeline = super().prepare_query()

        pipeline.append(
            {
                "$project":
                    {
                        "_id": 0,
                        "ticker": 1,
                        "company_name": 1,
                        "daily_data":
                            {
                                "$map":
                                    {
                                        "input":
                                            {
                                                "$filter":
                                                    {
                                                        "input": "$daily_data",
                                                        "as": "daily",
                                                        "cond":
                                                            {
                                                                "$and":
                                                                    [
                                                                        {
                                                                            "$gte": ["$$daily.date", start_date]
                                                                        }, {
                                                                            "$lte": ["$$daily.date", end_date]
                                                                        }
                                                                    ]
                                                            }
                                                    }
                                            },
                                        "as": "daily_item",
                                        "in":
                                            {
                                                "date": "$$daily_item.date",
                                                "close": "$$daily_item.close",
                                                "P_B": "$$daily_item.P_B",
                                                "P_E": "$$daily_item.P_E",
                                                "P_FCF": "$$daily_item.P_FCF",
                                                "P_S": "$$daily_item.P_S",
                                                "EV_OPI": "$$daily_item.EV_OPI",
                                                "EV_EBIT": "$$daily_item.EV_EBIT",
                                                "EV_EBITDA": "$$daily_item.EV_EBITDA",
                                                "EV_S": "$$daily_item.EV_S"
                                            }
                                    }
                            },
                        "yearly_data": 1
                    }
            })

        return pipeline

    def collect_data(self, start_date, end_date):
        pipeline = self.prepare_query(start_date, end_date)

        fetched_data = list(self.collection.aggregate(pipeline))

        return fetched_data[0]

    def query_data(self):
        try:
            latest_time = StatsDateTime.get_latest_time(self.ticker, self.collection)['last_update_time']
            target_year = latest_time['daily_data']['last_update'].year
            start_date = latest_time['daily_data']['last_update'] - timedelta(days=31)
            end_date = latest_time['daily_data']['last_update']

        except Exception as e:
            today = StatsDateTime.get_today()
            target_year = today.year
            start_date = (today.date - timedelta(days=31))
            end_date = today.date

        this_year = target_year - 1911

        fetched_data = self.collect_data(start_date, end_date)

        fetched_data['daily_data'] = fetched_data['daily_data'][-1]

        fetched_data['yearly_data'] = ValueProcessor.transform_to_df(
            fetched_data['daily_data'],
            fetched_data['yearly_data'],
        )

        return fetched_data

    def query_value_serie(self):
        """
        回傳指定公司的歷來評價
        return : Dict[pd.DataFrame]
        Dict中包含以下八個key, 每個key對應DataFrame
            {
                P_E,
                P_FCF,
                P_S,
                P_B,
                EV_OPI,
                EV_EBIT,
                EV_EBITDA,
                EV_S
            }
        """

        pipeline = [
            {
                "$match": {
                    "ticker": self.ticker,
                }
            },
            {
                "$project":
                    {
                        "_id": 0,
                        "ticker": 1,
                        "company_name": 1,
                        "daily_data":
                            {
                                "$map":
                                    {
                                        "input": "$daily_data",    # 正確地指定要處理的陣列
                                        "as": "daily",    # 每個元素的名稱
                                        "in":
                                            {
                                                "date": "$$daily.date",
                                                "P_E": "$$daily.P_E",
                                                "P_FCF": "$$daily.P_FCF",
                                                "P_B": "$$daily.P_B",
                                                "P_S": "$$daily.P_S",
                                                "EV_OPI": "$$daily.EV_OPI",
                                                "EV_EBIT": "$$daily.EV_EBIT",
                                                "EV_EBITDA": "$$daily.EV_EBITDA",
                                                "EV_S": "$$daily.EV_S"
                                            }
                                    }
                            }
                    }
            }
        ]

        fetched_data = self.collection.aggregate(pipeline).to_list()
        fetched_data = fetched_data[0]

        value_keys = ["P_E", "P_FCF", "P_B", "P_S", "EV_OPI", "EV_EBIT", "EV_EVITDA", "EV_S"]
        return_dict = {value_key: dict() for value_key in value_keys}

        for value_key in value_keys:
            for data in fetched_data['daily_data']:
                if (value_key not in data.keys()):
                    continue
                else:
                    return_dict[value_key].update({data['date']: data[value_key]})

        return_dict = {
            value_key: pd.DataFrame.from_dict(value_dict, orient='index', columns=[value_key])
            for value_key, value_dict in return_dict.items()
        }
        return return_dict


class ValueProcessor(StatsProcessor):

    @staticmethod
    def transform_to_df(daily_dict, yearly_dict):
        latest_data = {"year": f"過去4季"}

        latest_data.update(daily_dict)
        latest_data.pop("date")
        latest_data.pop("close")

        yearly_dict.append(latest_data)

        yearly_dict = pd.DataFrame.from_dict(yearly_dict)

        return yearly_dict
