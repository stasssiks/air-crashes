import os
import joblib
from statsmodels.tsa.stattools import acf, pacf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


def load_data(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))
    file_path = os.path.join(grandparent_dir + "/app/data/", filename)
    return file_path


data = pd.read_csv(load_data('crashes-processed.csv'))
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

yearly_crashes = data.resample('YE').size()
differenced = yearly_crashes.diff().dropna()

plt.figure(figsize=(8, 4))
plt.plot(acf(differenced, nlags=20))
plt.title('ACF')
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(pacf(differenced, nlags=20))
plt.title('PACF')
plt.show()

model = ARIMA(yearly_crashes, order=(1, 1, 1))
model_fit = model.fit()

joblib.dump(model_fit, '../data/crashes_predictor_model.pkl')

forecast = model_fit.forecast(steps=10)

plt.figure(figsize=(12, 6))
plt.plot(yearly_crashes.index, yearly_crashes, label='Historical Crash Counts')
forecast_index = pd.date_range(start=yearly_crashes.index[-1], periods=11, freq='YE')[1:]
plt.plot(forecast_index, forecast, label='Forecasted Crash Counts', color='red')
plt.title('Forecast of Total Crashes Over the Next 10 Years')
plt.legend()
plt.grid(True)
plt.show()
