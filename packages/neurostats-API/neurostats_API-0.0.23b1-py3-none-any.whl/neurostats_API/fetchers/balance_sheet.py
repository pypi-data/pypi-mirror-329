from .base import StatsFetcher, StatsDateTime
import json
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import yaml


class BalanceSheetFetcher(StatsFetcher):
    """
    對應iFa.ai -> 財務分析 ->  資產負債表
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)
        self.table_settings = StatsProcessor.load_yaml("twse/balance_sheet.yaml")

        self.process_function_map = {
            "twse_stats": self.process_data_twse,
            "us_stats": self.process_data_us
        }

    def prepare_query(self):
        pipeline = super().prepare_query()

        pipeline = pipeline + [
            {
                "$unwind": "$seasonal_data"    # 展開 seasonal_data 陣列
            },
            {
                "$project": {
                    "_id": 0,
                    "ticker": 1,
                    "company_name": 1,
                    "year": "$seasonal_data.year",
                    "season": "$seasonal_data.season",
                    "balance_sheet": {
                        "$ifNull": ["$seasonal_data.balance_sheet", []]
                    }    # 避免 null
                }
            },
            {
                "$sort": {
                    "year": -1,
                    "season": -1
                }
            }
        ]

        return pipeline

    def collect_data(self):
        return super().collect_data()

    def query_data(self):
        fetched_data = self.collect_data()

        process_fn = self.process_function_map[self.collection_name]
        processed_data = process_fn(fetched_data)
        return processed_data

    def process_data_twse(self, fetched_data):
        latest_time = StatsDateTime.get_latest_time(
            self.ticker, self.collection
        ).get('last_update_time', {})
        # 取最新時間資料時間，沒取到就預設去年年底
        target_year = latest_time.get('seasonal_data', {}).get(
            'latest_target_year',
            StatsDateTime.get_today().year - 1
        )
        target_season = latest_time.get('seasonal_data',
                                        {}).get('latest_season', 4)

        return_dict = {
            "ticker": self.ticker,
            "company_name": fetched_data[-1]['company_name']
        }
        table_dict = {}

        # 將value與percentage跟著年分季度一筆筆取出
        for data in fetched_data:
            year, season, balance_sheet = data['year'], data['season'], data[
                'balance_sheet']
            time_index = f"{year}Q{season}"

            new_balance_sheet = dict()
            # 蒐集整體的keys
            index_names = list(balance_sheet.keys())

            table_dict[time_index] = balance_sheet
            # flatten dict:
            # {<key>: {"value": <value>, "percentage": <value>}}
            # -> {<key>_value: <value>, <key>_percentage:<value>}
        
        old_balance_sheet = pd.DataFrame(table_dict)
        target_season_col = old_balance_sheet.columns.str.endswith(f"Q{target_season}")
        old_balance_sheet = old_balance_sheet.loc[:, target_season_col]
        old_balance_sheet = StatsProcessor.expand_value_percentage(old_balance_sheet)

        for time_index, data_dict in table_dict.items():
            new_balance_sheet = self.flatten_dict(
                balance_sheet, 
                indexes = index_names,
                target_keys=["value", "percentage"]
            )

            table_dict[time_index] = new_balance_sheet

        total_table = pd.DataFrame.from_dict(table_dict)
        value_index = total_table.index.str.endswith("_value")
        total_table.loc[value_index, :] = (
            total_table.loc[value_index, :].apply(
                lambda x: StatsProcessor.cal_non_percentage(x, postfix="元"),
                axis=0
            )
        )

        percenrage_index = total_table.index.str.endswith(
            "_percentage"
        )
        total_table.loc[percenrage_index, :] = (
            total_table.loc[percenrage_index, :].apply(
                lambda x: StatsProcessor.
                cal_non_percentage(x, to_str=True, postfix="%"),
                axis=0
            )
        )

        target_season_columns = total_table.columns.str.endswith(
            f"Q{target_season}"
        )
        total_table_YoY = total_table.loc[:, target_season_columns]

        for name, setting in self.table_settings.items():
            target_indexes = setting.get('target_index', [None])
            for target_index in target_indexes:
                try:
                    return_dict[name] = StatsProcessor.slice_old_table(
                        total_table=old_balance_sheet,
                        target_index=target_index
                    )
                    break
                except Exception as e:
                    print(f"error : {str(e)}")
                    continue
        
        return_dict.update(
            {
                "balance_sheet": old_balance_sheet,
                "balance_sheet_all": total_table.copy(),
                "balance_sheet_YoY": total_table_YoY
            }
        )
        return return_dict

    def process_data_us(self, fetched_data):
        return_dict = {
            "ticker": self.ticker,
            "company_name": fetched_data[-1]['company_name']
        }

        table_dict = dict()

        for data in fetched_data:
            year, season, balance_sheet = data['year'], data['season'], data[
                'balance_sheet']
            table_dict[f"{year}Q{season}"] = balance_sheet

        table_dict = pd.DataFrame.from_dict(table_dict)

        return_dict["balance_sheet"] = table_dict

        latest_season = fetched_data[0]['season']
        target_season_columns = table_dict.columns.str.endswith(
            f"Q{latest_season}"
        )
        table_dict_YoY = table_dict.loc[:, target_season_columns]
        return_dict["balance_sheet_YoY"] = table_dict_YoY
        return return_dict
