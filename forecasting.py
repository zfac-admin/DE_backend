import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

def calculate_forecast(history_dict: dict, method: str, forecast_months: int):
    if not history_dict:
        return {}

    dates = list(history_dict.keys())
    values = list(history_dict.values())
    series = pd.Series(values, index=pd.to_datetime(dates))

    if len(series) < 3:
        avg_val = int(series.mean())
        future_dates = pd.date_range(start=series.index[-1], periods=forecast_months + 1, freq='MS')[1:]
        return {d.strftime("%Y-%m"): avg_val for d in future_dates}

    predictions = []

    try:
        if method == "ARIMA":
            model = ARIMA(series, order=(1, 1, 0))
            model_fit = model.fit()
            predictions = model_fit.forecast(steps=forecast_months)

        elif method == "지수평활법":
            model = SimpleExpSmoothing(series)
            model_fit = model.fit(smoothing_level=0.2, optimized=False)
            predictions = model_fit.forecast(forecast_months)

        elif method == "이동평균법":
            temp_list = values.copy()
            for _ in range(forecast_months):
                next_val = sum(temp_list[-3:]) / 3
                temp_list.append(next_val)
            predictions = temp_list[-forecast_months:]
            
        else:
            predictions = [series.iloc[-1]] * forecast_months

    except Exception as e:
        print(f"예측 모델 에러 발생: {e}")
        predictions = [series.mean()] * forecast_months

    future_dates = pd.date_range(start=series.index[-1], periods=forecast_months + 1, freq='MS')[1:]
    
    result_dict = {
        date.strftime("%Y-%m"): int(round(pred)) if not pd.isna(pred) else 0 
        for date, pred in zip(future_dates, predictions)
    }
    
    return result_dict