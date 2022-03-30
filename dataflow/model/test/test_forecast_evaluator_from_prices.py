import logging
from typing import List

import numpy as np
import pandas as pd

import core.finance_data_example as cfidaexa
import dataflow.model.forecast_evaluator_from_prices as dtfmfefrpr
import helpers.hpandas as hpandas
import helpers.hunit_test as hunitest

_LOG = logging.getLogger(__name__)


class TestForecastEvaluatorFromPrices1(hunitest.TestCase):
    def test_to_str_intraday_1_asset_targeted_gmv(self) -> None:
        data = self.get_data(
            pd.Timestamp("2022-01-03 09:30:00", tz="America/New_York"),
            pd.Timestamp("2022-01-03 10:00:00", tz="America/New_York"),
            asset_ids=[101],
        )
        forecast_evaluator = dtfmfefrpr.ForecastEvaluatorFromPrices(
            price_col="price",
            volatility_col="volatility",
            prediction_col="prediction",
        )
        actual = forecast_evaluator.to_str(
            data,
            target_gmv=1e4,
            quantization="nearest_share",
        )
        expected = r"""
# holdings=
                            101
2022-01-03 09:35:00-05:00   NaN
2022-01-03 09:40:00-05:00   NaN
2022-01-03 09:45:00-05:00   NaN
2022-01-03 09:50:00-05:00  10.0
2022-01-03 09:55:00-05:00 -10.0
2022-01-03 10:00:00-05:00 -10.0
# holdings marked to market=
                               101
2022-01-03 09:35:00-05:00      NaN
2022-01-03 09:40:00-05:00      NaN
2022-01-03 09:45:00-05:00      NaN
2022-01-03 09:50:00-05:00  9976.60
2022-01-03 09:55:00-05:00 -9974.12
2022-01-03 10:00:00-05:00 -9975.38
# flows=
                                101
2022-01-03 09:35:00-05:00       NaN
2022-01-03 09:40:00-05:00       NaN
2022-01-03 09:45:00-05:00       NaN
2022-01-03 09:50:00-05:00  -9976.60
2022-01-03 09:55:00-05:00  19948.23
2022-01-03 10:00:00-05:00     -0.00
# pnl=
                               101
2022-01-03 09:35:00-05:00      NaN
2022-01-03 09:40:00-05:00      NaN
2022-01-03 09:45:00-05:00      NaN
2022-01-03 09:50:00-05:00 -9976.60
2022-01-03 09:55:00-05:00    -2.48
2022-01-03 10:00:00-05:00    -1.26
# statistics=
                               pnl  gross_volume  net_volume      gmv      nmv
2022-01-03 09:35:00-05:00      NaN           NaN         NaN      NaN      NaN
2022-01-03 09:40:00-05:00      NaN           NaN         NaN      NaN      NaN
2022-01-03 09:45:00-05:00      NaN           NaN         NaN      NaN      NaN
2022-01-03 09:50:00-05:00 -9976.60       9976.60     9976.60  9976.60  9976.60
2022-01-03 09:55:00-05:00    -2.48      19948.23   -19948.23  9974.12 -9974.12
2022-01-03 10:00:00-05:00    -1.26          0.00        0.00  9975.38 -9975.38"""
        self.assert_equal(actual, expected, fuzzy_match=True)

    def test_to_str_intraday_3_assets_targeted_gmv(self) -> None:
        data = self.get_data(
            pd.Timestamp("2022-01-03 09:30:00", tz="America/New_York"),
            pd.Timestamp("2022-01-03 10:00:00", tz="America/New_York"),
            asset_ids=[101, 201, 301],
        )
        forecast_evaluator = dtfmfefrpr.ForecastEvaluatorFromPrices(
            price_col="price",
            volatility_col="volatility",
            prediction_col="prediction",
        )
        actual = forecast_evaluator.to_str(
            data, target_gmv=1e5, quantization="nearest_share"
        )
        expected = r"""
# holdings=
                            101   201  301
2022-01-03 09:35:00-05:00   NaN   NaN  NaN
2022-01-03 09:40:00-05:00   NaN   NaN  NaN
2022-01-03 09:45:00-05:00   NaN   NaN  NaN
2022-01-03 09:50:00-05:00  30.0 -64.0  6.0
2022-01-03 09:55:00-05:00 -36.0 -57.0 -7.0
2022-01-03 10:00:00-05:00 -58.0 -39.0  3.0
# holdings marked to market=
                                101       201      301
2022-01-03 09:35:00-05:00       NaN       NaN      NaN
2022-01-03 09:40:00-05:00       NaN       NaN      NaN
2022-01-03 09:45:00-05:00       NaN       NaN      NaN
2022-01-03 09:50:00-05:00  29929.79 -63840.07  5991.55
2022-01-03 09:55:00-05:00 -35906.82 -56874.95 -6997.02
2022-01-03 10:00:00-05:00 -57857.19 -38842.45  3000.61
# flows=
                                101       201       301
2022-01-03 09:35:00-05:00       NaN       NaN       NaN
2022-01-03 09:40:00-05:00       NaN       NaN       NaN
2022-01-03 09:45:00-05:00       NaN       NaN       NaN
2022-01-03 09:50:00-05:00 -29929.79  63840.07  -5991.55
2022-01-03 09:55:00-05:00  65829.16  -6984.64  12994.47
2022-01-03 10:00:00-05:00  21945.83 -17927.28 -10002.05
# pnl=
                                101       201      301
2022-01-03 09:35:00-05:00       NaN       NaN      NaN
2022-01-03 09:40:00-05:00       NaN       NaN      NaN
2022-01-03 09:45:00-05:00       NaN       NaN      NaN
2022-01-03 09:50:00-05:00 -29929.79  63840.07 -5991.55
2022-01-03 09:55:00-05:00     -7.44    -19.52     5.90
2022-01-03 10:00:00-05:00     -4.54    105.22    -4.41
# statistics=
                                pnl  gross_volume  net_volume       gmv       nmv
2022-01-03 09:35:00-05:00       NaN           NaN         NaN       NaN       NaN
2022-01-03 09:40:00-05:00       NaN           NaN         NaN       NaN       NaN
2022-01-03 09:45:00-05:00       NaN           NaN         NaN       NaN       NaN
2022-01-03 09:50:00-05:00  27918.73      99761.41   -27918.73  99761.41 -27918.73
2022-01-03 09:55:00-05:00    -21.06      85808.28   -71839.00  99778.79 -99778.79
2022-01-03 10:00:00-05:00     96.27      49875.16     5983.50  99700.25 -93699.02"""
        self.assert_equal(actual, expected, fuzzy_match=True)

    def test_log_portfolio_read_portfolio(self) -> None:
        data = self.get_data(
            pd.Timestamp("2022-01-03 09:30:00", tz="America/New_York"),
            pd.Timestamp("2022-01-03 10:00:00", tz="America/New_York"),
            asset_ids=[101, 201, 301],
        )
        forecast_evaluator = dtfmfefrpr.ForecastEvaluatorFromPrices(
            price_col="price",
            volatility_col="volatility",
            prediction_col="prediction",
        )
        #
        log_dir = self.get_scratch_space()
        _ = forecast_evaluator.log_portfolio(
            data, log_dir, target_gmv=1e6, quantization="nearest_share"
        )
        #
        portfolio_df, stats_df = forecast_evaluator.read_portfolio(log_dir)
        # Ensure that the `int` asset id type is recovered.
        asset_id_idx = portfolio_df.columns.levels[1]
        self.assertEqual(asset_id_idx.dtype.type, np.int64)
        #
        precision = 2
        portfolio_df_str = hpandas.df_to_str(
            portfolio_df, num_rows=None, precision=precision
        )
        expected_portfolio_df_str = r"""
                            price                  volatility                     prediction                     holdings                position                            flow                              pnl
                              101     201      301        101       201       301        101       201       301      101    201   301        101        201       301        101        201        301        101        201       301
2022-01-03 09:35:00-05:00  998.90  999.66   999.87        NaN       NaN       NaN   8.43e-04 -1.77e-04 -2.38e-04      NaN    NaN   NaN        NaN        NaN       NaN        NaN        NaN        NaN        NaN        NaN       NaN
2022-01-03 09:40:00-05:00  998.17  999.60   998.00   7.25e-04  5.14e-05  1.87e-03   8.58e-04  4.26e-04 -1.84e-03      NaN    NaN   NaN        NaN        NaN       NaN        NaN        NaN        NaN        NaN        NaN       NaN
2022-01-03 09:45:00-05:00  997.39  998.63   997.58   7.57e-04  7.29e-04  1.28e-03   4.75e-04 -9.85e-04  1.70e-04      NaN    NaN   NaN        NaN        NaN       NaN        NaN        NaN        NaN        NaN        NaN       NaN
2022-01-03 09:50:00-05:00  997.66  997.50   998.59   6.02e-04  9.21e-04  1.17e-03  -4.51e-04 -1.11e-03 -1.76e-04    298.0 -641.0  63.0  297302.55 -639398.23  62911.30 -297302.55  639398.23  -62911.30 -297302.55  639398.23 -62911.30
2022-01-03 09:55:00-05:00  997.41  997.81   999.57   5.07e-04  7.64e-04  1.11e-03  -7.55e-04 -7.61e-04  7.68e-05   -356.0 -575.0 -71.0 -355078.52 -573738.52 -70969.82  652307.17  -65855.20  133943.04     -73.89    -195.50     61.92
2022-01-03 10:00:00-05:00  997.54  995.96  1000.20   4.27e-04  1.21e-03  9.87e-04  -8.15e-04  6.48e-04  1.54e-03   -584.0 -392.0  27.0 -582562.04 -390416.40  27005.53  227438.61 -182260.72  -98020.08     -44.91    1061.40    -44.73"""
        self.assert_equal(
            portfolio_df_str, expected_portfolio_df_str, fuzzy_match=True
        )
        #
        stats_df_str = hpandas.df_to_str(
            stats_df, num_rows=None, precision=precision
        )
        expected_stats_df_str = r"""
                                 pnl  gross_volume  net_volume        gmv        nmv
2022-01-03 09:35:00-05:00        NaN           NaN         NaN        NaN        NaN
2022-01-03 09:40:00-05:00        NaN           NaN         NaN        NaN        NaN
2022-01-03 09:45:00-05:00        NaN           NaN         NaN        NaN        NaN
2022-01-03 09:50:00-05:00  279184.38     999612.07  -279184.38  999612.07 -279184.38
2022-01-03 09:55:00-05:00    -207.47     852105.42  -720395.01  999786.86 -999786.86
2022-01-03 10:00:00-05:00     971.76     507719.40    52842.19  999983.98 -945972.91"""
        self.assert_equal(stats_df_str, expected_stats_df_str, fuzzy_match=True)

    @staticmethod
    def get_data(
        start_datetime: pd.Timestamp,
        end_datetime: pd.Timestamp,
        asset_ids: List[int],
        *,
        bar_duration: str = "5T",
    ) -> pd.DataFrame:
        df = cfidaexa.get_forecast_price_based_dataframe(
            start_datetime,
            end_datetime,
            asset_ids,
            bar_duration=bar_duration,
        )
        return df