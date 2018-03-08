# -*- encoding:utf-8 -*-
from __future__ import print_function

import sys
sys.path.append("/Users/chengshitao/workspace/backend/abu")

import pandas as pd

import logging
import warnings
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from collections import namedtuple
import itertools
# noinspection PyCompatibility
from concurrent.futures import ProcessPoolExecutor
# noinspection PyCompatibility
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# noinspection PyUnresolvedReferences
import abu_local_env
import abupy
from abupy import six, xrange, range, reduce, map, filter, partial
from abupy import ABuSymbolPd,AbuMetricsBase

from abupy.CoreBu.ABuEnv import EMarketSourceType, EMarketTargetType, EMarketSubType, \
    EMarketDataSplitMode, EMarketDataFetchMode, EDataCacheType


#abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_bd
#abupy.env.g_data_cache_type = EDataCacheType.E_DATA_CACHE_CSV
#abupy.abu.run_kl_update(start='2011-08-08', end='2017-08-08', market=EMarketTargetType.E_MARKET_TARGET_CN, n_jobs=10)

# buy_factors 60日向上突破，42日向上突破两个因子
buy_factors = []
#buy_factors.append({'xd': 60, 'class': abupy.AbuFactorBuyBreak})
#buy_factors.append({'xd': 42, 'class': abupy.AbuFactorBuyBreak})
buy_factors.append({'class': abupy.AbuDoubleMaBuy})


sell_factors = [
    {
        'xd': 120,
        'class': abupy.AbuFactorSellBreak
    },
    {
        'stop_loss_n': 0.5,
        'stop_win_n': 3.0,
        'class': abupy.AbuFactorAtrNStop
    },
    {
        'class': abupy.AbuFactorPreAtrNStop,
        'pre_atr_n': 1.0
    },
    {
        'class': abupy.AbuFactorCloseAtrNStop,
        'close_atr_n': 1.5
    }]


abupy.env.g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_FORCE_LOCAL
abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_CN

#abupy.ABuEnv.g_market_target = EMarketTargetType.E_MARKET_TARGET_CN

benchmark = abupy.AbuBenchmark(start="2015-01-01",end="2017-01-01")
capital = abupy.AbuCapital(1000000, benchmark)

choice_symbols = ['sh603600', 'sh603601', 'sh603602', 'sh603603', 'sh603605']

orders_pd, action_pd, all_fit_symbols_cnt = abupy.ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols,
                                                                                            benchmark,
                                                                                            buy_factors,
                                                                                            sell_factors,
                                                                                            capital,
                                                                                            show=False)

print(orders_pd)
print("##########")
print(action_pd)

metrics = AbuMetricsBase(orders_pd, action_pd, capital, benchmark)
metrics.fit_metrics()
metrics.plot_returns_cmp(only_info=True)

print(capital)
