import mplfinance as mpf
from pandas_datareader import data
df = data.DataReader("TSLA", 'yahoo', start='01-01-2021')
mpf.plot(df, type='candle', ylabel='Price US$', title="TESLA", volume=True, mav=(20,50), style='yahoo')