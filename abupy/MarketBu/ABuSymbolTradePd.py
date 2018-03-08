# coding=utf-8
"""
    symbol模块
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from fnmatch import fnmatch

import numpy as np
import pandas as pd
import zipfile, os, logging, io



from .ABuSymbol import code_to_symbol
from ..CoreBu import ABuEnv
from ..CoreBu.ABuEnv import EMarketTargetType, EMarketSubType
from ..CoreBu.ABuFixes import six
from ..UtilBu.ABuStrUtil import to_unicode
from ..UtilBu.ABuLazyUtil import LazyFunc


class ABuSymbolTradePd(object):
    def __init__(self, symbol):
        self.target_symbol = code_to_symbol(symbol)
        self.target_trade_zipfile = None

    def load_trade_records(self):
        """
        加载股票的交易数据
        """
        #
        rttr_path = os.path.join(ABuEnv.g_project_data_dir,"detail/"+self.target_symbol.symbol_code+"/trade_list.zip")
        #logging.info("load_trade_records: %s (%s)" % (self.target_symbol.symbol_code, rttr_path))
        if os.path.exists(rttr_path):
            self.target_trade_zipfile = zipfile.ZipFile(rttr_path,"r")
            self.target_trade_filenames = self.target_trade_zipfile.namelist()

    def get_trade_pd(self, tradedate):
        """
        获取股票的某天的历史交易数据
        :param tradedate: 交易日期，例如：2015-01-01
        """
        df = None
        filename = ("%s.json")%(tradedate)
        if self.target_trade_zipfile is not None and filename in self.target_trade_filenames :
            try:
                buff = io.BytesIO(self.target_trade_zipfile.read(filename))
                df = pd.read_csv(filepath_or_buffer=buff,sep=",",index_col=0,header=0,encoding="utf8")
            except:
                raise RuntimeError("get_trade_pd error: %s %s" % (self.target_symbol.symbol_code, tradedate))
        return df

    def release_trade_records(self):
        """释放股票历史交易数据"""
        if self.target_trade_zipfile is not None:
            self.target_trade_filenames = []
            self.target_trade_zipfile.close()
        #    logging.info("release_trade_records: %s" % (self.target_symbol.symbol_code))
        