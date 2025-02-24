from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.polygonio.polygon_options import PolygonOptions
from fudstop.apis.ultimate.ultimate_sdk import UltimateSDK
from fudstop.apis.webull.webull_trading import WebullTrading
from fudstop.apis.webull.webull_ta import WebullTA
from fudstop.apis.webull.webull_options.webull_options import WebullOptions
from fudstop.apis.webull.webull_markets import WebullMarkets
from fudstop.apis.occ.occ_sdk import occSDK
from fudstop.apis.y_finance.yf_sdk import YfSDK
from fudstop.apis.nasdaq.nasdaq_sdk import Nasdaq
from fudstop.apis.newyork_fed.newyork_fed_sdk import FedNewyork
from fudstop.apis.ofr.ofr_sdk import OFR,MMF_OFR,FNYR_OFR,TYLD_OFR,NYPD_OFR,REPO_OFR




###HELPERS#####
from fudstop.apis.helpers import format_large_numbers_in_dataframe2, get_human_readable_string, get_next_trading_day, flatten_list_of_dicts, format_large_number, convert_to_eastern_time, is_etf
from fudstop.all_helpers import chunk_string

###POLYGON MAPS AND MODELS######
from fudstop.apis.polygonio.mapping import stock_condition_desc_dict, stock_condition_dict,STOCK_EXCHANGES, option_condition_desc_dict, option_condition_dict, OPTIONS_EXCHANGES, TAPES
from fudstop.apis.polygonio.models.aggregates import Aggregates
from fudstop.apis.polygonio.models.company_info import CompanyResults
from fudstop.apis.polygonio.models.daily_open_close import DailyOpenClose
from fudstop.apis.polygonio.models.gainers_losers import GainersLosers
from fudstop.apis.polygonio.models.option_models.universal_snapshot import UniversalOptionSnapshot
from fudstop.apis.polygonio.models.option_models.option_snapshot import OptionSnapshotData, WorkingUniversal
from fudstop.apis.polygonio.models.option_models.universal_option import OptionsSnapshotResult
from fudstop.apis.polygonio.models.quotes import LastStockQuote, StockQuotes
from fudstop.apis.polygonio.models.technicals import RSI, EMA, MACD, SMA
from fudstop.apis.polygonio.models.ticker_news import TickerNews
from fudstop.apis.polygonio.models.trades import TradeData,LastTradeData
from fudstop.apis.polygonio.models.ticker_snapshot import StockSnapshot, SingleStockSnapshot


###OCC MAPS AND MODELS######
from fudstop.apis.occ.occ_models import OCCMostActive,OICOptionsMonitor,StockLoans,AllCompBoundVola,CalculateGreeks,CalculatorMetrics,DailyMarketShare,ExpiryDates,HistoricIVX,StockInfo,OptionsMonitor,ProbabilityMetrics,NEWOIC,VolaSnapshot,VolatilityScale,VolumeTotals

###WEBULL MAPS AND MODELS######
from fudstop.apis.webull.toprank_models import EarningSurprise,Dividend,MicroFutures
from fudstop.apis.webull.trade_models.analyst_ratings import Analysis
from fudstop.apis.webull.trade_models.financials import BalanceSheet,CashFlow,FinancialStatement,Forecast
from fudstop.apis.webull.trade_models.company_brief import CompanyBrief
from fudstop.apis.webull.trade_models.capital_flow import CapitalFlow,CapitalFlowHistory
from fudstop.apis.webull.trade_models.cost_distribution import NewCostDist
from fudstop.apis.webull.trade_models.deals import Deals
from fudstop.apis.webull.trade_models.econ_data import EconEvents,EconomicData
from fudstop.apis.webull.trade_models.etf_holdings import ETFHoldings
from fudstop.apis.webull.trade_models.events import Event
from fudstop.apis.webull.trade_models.forecast_evaluator import ForecastEvaluator
from fudstop.apis.webull.trade_models.institutional_holdings import InstitutionHolding,InstitutionStat,Stat
from fudstop.apis.webull.trade_models.news import NewsItem
from fudstop.apis.webull.trade_models.order_flow import OrderFlow
from fudstop.apis.webull.trade_models.short_interest import ShortInterest
from fudstop.apis.webull.trade_models.volume_analysis import WebullVolAnalysis
from fudstop.apis.webull.trade_models.us_treasuries import US_TREASURIES
from fudstop.apis.webull.trade_models.treasury_models import TreasuryData
from fudstop.apis.webull.trade_models.ticker_query import WebullStockData,MultiQuote

##WEBULL OPTIONS###
from fudstop.apis.webull.webull_options.models.options_data import From_, GroupData, OptionData, BaseData


##FED NEWYORK##
from fudstop.apis.newyork_fed.models import AsOfDates,AuctionResult,TimeSeriesData,FXSwaps,SecuritiesLending,RepoOperations,SecuredReferenceRates,TimeSeries

###OFR###
from fudstop.apis.ofr.ofr_stuff import OFR, fetch_all_data,fetch_data,mnemonics,urls_with_names





from fudstop.discord_.bot_menus.pagination import AlertMenus
from fudstop._markets.list_sets.ticker_lists import most_active_nonetf,most_active_tickers
from fudstop._markets.list_sets.dicts import hex_color_dict
from tabulate import tabulate
import asyncio
import pandas as pd
import numpy as np
import datetime
import time
import os
import json
import requests
import math
import re
import sys
import logging
import random
import disnake
from disnake.ext import commands
import asyncpg
import aiohttp
from discord_webhook import AsyncDiscordWebhook,DiscordEmbed
from datetime import timezone, timedelta
from fudstop_middleware.fudstop_channels import ticker_channels,ticker_webhooks



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the bot
intents = disnake.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

wbt = WebullTrading()
wbm = WebullMarkets()
wb_opts = WebullOptions()
ta = WebullTA()
poly = Polygon()
poly_opts = PolygonOptions()
ultim = UltimateSDK()
yf = YfSDK()
nas = Nasdaq()
occ = occSDK()