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

# 과거 및 예측 데이터를 분석하여 간단한 코멘트를 생성: 추세 분석, 수치 요약, 코멘트.
def generate_analysis_comment(df_history, df_pred, value_name, unit):
    if df_pred is None or df_pred.empty:
        return "예측 결과가 없습니다."

    pred_values = df_pred.iloc[0].tolist()

    trend = ""
    if pred_values[-1] > pred_values[0]:
        trend = "증가 추세"
        trend_icon = "📈"
    elif pred_values[-1] < pred_values[0]:
        trend = "감소 추세"
        trend_icon = "📉"
    else:
        trend = "보합세 유지"
        trend_icon = "➡️"

    avg_pred = int(sum(pred_values) / len(pred_values))
    max_pred = int(max(pred_values))

    comment = f"""
    - **{trend_icon} 향후 전망:** {trend}가 예상됩니다.
    - **평균 예측:** 약 **{avg_pred:,} {unit}**
    - **최대 예상:** 약 **{max_pred:,} {unit}**
    """
    return comment