from .base import StatsFetcher, StatsDateTime
import importlib.resources as pkg_resources
import json
import numpy as np
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor, YoY_Calculator
import yaml


class ProfitLoseFetcher(StatsFetcher):
    """
    iFa.ai: 財務分析 -> 損益表
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)

        self.table_settings = StatsProcessor.load_yaml("twse/profit_lose.yaml")

        self.process_function_map = {
            "twse_stats": self.process_data_twse,
            "us_stats": self.process_data_us
        }

    def prepare_query(self):
        pipeline = super().prepare_query()

        name_map = {"twse_stats": "profit_lose", "us_stats": "income_statement"}

        chart_name = name_map.get(self.collection_name, "income_statement")

        append_pipeline = [
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
                    "profit_lose": {
                        "$ifNull": [f"$seasonal_data.{chart_name}", []]
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

        pipeline = pipeline + append_pipeline

        return pipeline

    def collect_data(self):
        return super().collect_data()

    def query_data(self):
        fetched_data = self.collect_data()

        process_fn = self.process_function_map.get(
            self.collection_name, self.process_data_us
        )
        return process_fn(fetched_data)

    def process_data_twse(self, fetched_data):

        latest_time = StatsDateTime.get_latest_time(
            self.ticker, self.collection
        ).get('last_update_time', {})

        # 取最新時間資料時間，沒取到就預設去年年底
        target_year = latest_time.get('seasonal_data', {}).get(
            'latest_target_year',
            StatsDateTime.get_today().year - 1
        )
        target_season = latest_time.get(
            'seasonal_data',{}
        ).get('latest_season', 4)

        return_dict = {
            "ticker": self.ticker,
            "company_name": fetched_data[-1]['company_name'],
        }

        profit_lose_dict = {
            f"{data['year']}Q{data['season']}": data['profit_lose'] 
            for data in fetched_data
        }

        profit_lose_df = pd.DataFrame.from_dict(profit_lose_dict)
        target_season_col = profit_lose_df.columns.str.endswith(
            f"Q{target_season}"
        )
        profit_lose_df = profit_lose_df.loc[:, target_season_col]
        profit_lose_df = StatsProcessor.expand_value_percentage(
            profit_lose_df
        )

        value_col = profit_lose_df.columns.str.endswith(f"_value")
        percentage_col = profit_lose_df.columns.str.endswith(f"_percentage")

        grand_total_value_col = profit_lose_df.columns.str.endswith(
            f"grand_total_value"
        )
        grand_total_percentage_col = profit_lose_df.columns.str.endswith(
            f"grand_total_percentage"
        )

        profit_lose_stats_df = profit_lose_df.loc[:, (
            (value_col & ~grand_total_value_col) |
            (percentage_col & ~grand_total_percentage_col)
        )]

        for time_index, profit_lose in profit_lose_dict.items():
            # 蒐集整體的keys
            index_names = list(profit_lose.keys())
            target_keys = [
                "value",
                "percentage",
                "grand_total",
                "grand_total_percentage",
                "YoY_1",
                "YoY_3",
                "YoY_5",
                "YoY_10",
                "grand_total_YoY_1",
                "grand_total_YoY_3",
                "grand_total_YoY_5",
                "grand_total_YoY_10",
            ]
            # flatten dict
            new_profit_lose = self.flatten_dict(
                profit_lose, index_names, target_keys
            )
            profit_lose_dict[time_index] = new_profit_lose

        profit_lose_df = pd.DataFrame.from_dict(profit_lose_dict)

        # EPS的value用元計算
        eps_index = profit_lose_df.index.str.endswith(
            "_value"
        ) & profit_lose_df.index.str.contains("每股盈餘")
        profit_lose_df.loc[eps_index] = profit_lose_df.loc[
            eps_index].apply(
                lambda x: StatsProcessor.cal_non_percentage(x, postfix="元")
            )

        # percentage處理
        percentage_index = profit_lose_df.index.str.endswith("percentage")
        profit_lose_df.loc[percentage_index] = profit_lose_df.loc[
            percentage_index].apply(
                lambda x: StatsProcessor.
                cal_non_percentage(x, to_str=True, postfix="%")
            )

        # YoY處理: 乘以100
        YoY_index = profit_lose_df.index.str.contains("YoY")
        profit_lose_df.loc[YoY_index] = profit_lose_df.loc[
            YoY_index].apply(lambda x: StatsProcessor.cal_percentage(x))

        # 剩下的處理: 乘以千元
        value_index = ~(
            percentage_index | YoY_index | profit_lose_df.index.isin(eps_index)
        )    # 除了上述以外的 index
        profit_lose_df.loc[value_index] = profit_lose_df.loc[
            value_index].apply(
                lambda x: StatsProcessor.cal_non_percentage(x, postfix="千元")
            )

        total_table = profit_lose_df.replace("N/A", None)

        # 取特定季度
        target_season_columns = total_table.columns.str.endswith(
            f"Q{target_season}"
        )
        total_table_YoY = total_table.loc[:, target_season_columns]

        for name, setting in self.table_settings.items():
            target_indexes = setting.get('target_index', [None])
            for target_index in target_indexes:
                try:
                    return_dict[name] = StatsProcessor.slice_table(
                        total_table=total_table_YoY,
                        mode=setting['mode'],
                        target_index=target_index
                    )
                    break
                except Exception as e:
                    print(str(e))
                    continue

        return_dict.update(
            {
                "profit_lose": profit_lose_stats_df,
                "profit_lose_all": total_table.copy(),
                "profit_lose_YoY": total_table_YoY
            }
        )
        return return_dict

    def process_data_us(self, fetched_data):

        table_dict = {
            f"{data['year']}Q{data['season']}": data['profit_lose']
            for data in fetched_data
        }

        table_dict = YoY_Calculator.cal_QoQ(table_dict)
        table_dict = YoY_Calculator.cal_YoY(table_dict)

        for time_index, data_dict in table_dict.items():
            table_dict[time_index] = self.flatten_dict(
                value_dict=data_dict,
                indexes=list(data_dict.keys()),
                target_keys=["value", "growth"] + 
                            [f"YoY_{i}" for i in [1, 3, 5, 10]]
            )

        # 計算QoQ

        return_dict = {
            "ticker": self.ticker,
            "company_name": fetched_data[-1]['company_name'],
            "profit_lose": pd.DataFrame.from_dict(table_dict)
        }

        return return_dict
