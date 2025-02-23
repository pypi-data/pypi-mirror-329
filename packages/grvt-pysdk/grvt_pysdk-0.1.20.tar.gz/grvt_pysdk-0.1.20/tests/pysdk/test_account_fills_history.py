import os
import time
import traceback
from datetime import datetime, timezone

import pandas as pd

from pysdk.grvt_ccxt import GrvtCcxt
from pysdk.grvt_ccxt_env import GrvtEnv
from pysdk.grvt_ccxt_logging_selector import logger


def fetch_my_trades(api: GrvtCcxt, env: GrvtEnv, api_params: dict, start_time: float):
    FN = "fetch_my_trades"
    logger.info(f"{FN}: START")
    for symbol in ["BTC_USDT_Perp", "ETH_USDT_Perp"]:
        done: bool = False
        cursor: str = ""
        trades: list = []
        attempts: int = 0
        while not done and attempts < 10:
            try:
                params = {"cursor": cursor} if cursor else {}
                attempts += 1
                next_trades = api.fetch_my_trades(
                    symbol=symbol,
                    limit=1_000,
                    params=params,
                )
                logger.info(
                    f"my_trades: next_trades:{len(next_trades.get('result', []))}"
                )
                if next_trades.get("result"):
                    trades.extend(next_trades["result"])
                cursor = next_trades.get("cursor", "")
                if not cursor:
                    done = True
                    logger.info(f"{FN} {symbol}")
                done = True
            except Exception as e:
                logger.error(f"Error in {FN}: {e} {traceback.format_exc()}")
                time.sleep(1)
        logger.info(f"{FN} {symbol} {done=} {attempts=} num trades:{len(trades)}")
        df = pd.DataFrame.from_records(trades)
        df["event_time"] = df["event_time"].astype(int) / 1_000_000_000
        df = df.loc[df["event_time"] > start_time]
        df["size"] = df["size"].astype(float)
        df["price"] = df["price"].astype(float)
        df["side"] = "BUY"
        df.loc[~df["is_buyer"], "side"] = "SELL"
        df.loc[~df["is_buyer"], "size"] *= -1  # df.loc[~df["is_buyer"], "size"] * -1
        df["notional"] = df["size"] * df["price"]
        df["abs_notional"] = df["notional"].abs()
        df["datetime"] = pd.to_datetime(df["event_time"], unit="s")
        df.drop(
            columns=[
                "signer",
                "interest_rate",
                "forward_price",
                "realized_pnl",
                "venue",
                "index_price",
                "fee",
                "fee_rate",
                "trade_id",
                "client_order_id",
            ],
            inplace=True,
        )
        trading_account_id = api_params.get("trading_account_id", "")
        FILLS_CSV_FN: str = f"fills_{env.value.upper()}_{trading_account_id}_{symbol}.csv"
        df.to_csv(FILLS_CSV_FN, index=False)
        liq_df = df.loc[df["order_id"] == "0x00"].copy()
        liq_df.sort_values(by="abs_notional", inplace=True)
        liq_df.reset_index(drop=True, inplace=True)
        liq_df["cum_abs_notional"] = liq_df["abs_notional"].cumsum()
        total_abs_notional = liq_df["abs_notional"].sum()
        liq_df["cum_abs_notional_pct"] = liq_df["cum_abs_notional"] / total_abs_notional
        liq_df["row_num"] = liq_df.index + 1
        liq_df["perc_of_occurrences"] = liq_df["row_num"] / liq_df.shape[0]
        LIQ_CSV_FN: str = f"liqs_{env.value.upper()}_{trading_account_id}_{symbol}.csv"
        liq_df.to_csv(LIQ_CSV_FN, index=False)
        logger.info(f"{FN} {symbol} {FILLS_CSV_FN=} {LIQ_CSV_FN=}")


def test_grvt_ccxt():
    params = {
        "api_key": os.getenv("GRVT_API_KEY"),
        "trading_account_id": os.getenv("GRVT_TRADING_ACCOUNT_ID"),
    }
    env = GrvtEnv(os.getenv("GRVT_ENV", "testnet"))
    test_api = GrvtCcxt(env, logger, parameters=params)
    range_start = datetime.strptime("2024-12-22", "%Y-%m-%d")
    range_start = range_start.replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    )
    start_time: float = range_start.timestamp()
    logger.info(f"{range_start=} {start_time=}")
    function_list = [fetch_my_trades]
    for f in function_list:
        try:
            f(test_api, env, params, start_time)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {e} {traceback.format_exc()}")


if __name__ == "__main__":
    test_grvt_ccxt()
