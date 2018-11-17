from jaqs_fxdayu.data.dataservice import LocalDataService
ds = LocalDataService()
from time import time
from jaqs_fxdayu.data.hf_dataview import HFDataView
import matplotlib.pyplot as plt
import mpl_finance as mpf
import seaborn


## 加freq参数

start = time()
path = r'./min_data/VnTrader_1Min_Db'
props = {'fields': 'open,high,low,close,volume','symbol': 'BTCUSDT:binance', 'freq': '4H',
         'start_date':20180601000000}

Time_dict = ds.bar_reader(path,props)

dv = HFDataView()
dv.create_init_dv(Time_dict.set_index(["trade_date","symbol"]))

def plot_chart(close,alpha,M):
    '''
    绘制图像
    '''
    fig,(ax,ax1) = plt.subplots(2,1,sharex=True, figsize=(15,8))
    ax.grid(axis='both')
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(500))
    ax1.grid()
    ax1.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax1.yaxis.set_major_locator(plt.MultipleLocator(M))
    ax.plot(close)
    ax1.plot(alpha)
    plt.show()

def RankPct(df):
    return df.rank(axis= 1, pct=True)

dv.add_formula("close_ret", "Return(close,1)", add_data=True)

# 夏普比率
SharpeRatio20 = dv.add_formula('SharpeRatio20_J', "(Ts_Mean(close_ret,20)*250-0.03)/StdDev(close_ret,20)/Sqrt(250)",add_data=True)
alpha2_plot = dv.get_ts('SharpeRatio20_J', date_type='datetime')
close = dv.get_ts('close', date_type='datetime')
print('此指标代表20日夏普比率，通过获得的超额收益除以策略波动率得出，主要衡量每单位风险承担的超额收益。\n'
      '现象：本指标往往处于-8到8之间，当指标在低点时超额收益低，可以作为买入信号，指标处于高点时，收益率较高，可以作为卖出信号')
plot_chart(close, alpha2_plot,1)

# 心理线
psy_j = dv.add_formula("psy_j", "Ts_Sum(close>Delay(close,1),12)/12*100", add_data=True)
alpha1_plot = dv.get_ts('psy_j', date_type='datetime')
open = dv.get_ts('open', date_type='datetime')
close = dv.get_ts('close', date_type='datetime')
print('PSY，俗称心理线指标，研究投资者的情绪波动指标，投资者的情绪往往会反应市场的情绪，可以看出市场对行情的反应，短期内可能会有一定的持续效应，但是长期可能存在反转效应。\n'
      '现象：通常指标在25到75之间波动，当价格下跌时，psy指标往往随之下跌，在25以下往往处于超卖阶段，市场情绪非理性波动，可以考虑买入；当标的价格下跌到一定程度时，psy随之上涨，75以上处于超买区，适合卖出')
plot_chart(open, alpha1_plot,5)

