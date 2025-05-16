import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/dataexport_20250515T133555.csv", header=None)
df.columns = ["datetime", "temp"]

dates = df["datetime"].str[:8]

df["date"] = pd.to_datetime(dates, format="%Y%m%d", errors='coerce')

grouped = df.groupby("date")
temp_mean = grouped["temp"].mean()

df_day = temp_mean.reset_index()

min_date = df_day["date"].min()
df_day["day_num"] = (df_day["date"] - min_date).dt.days

df_day["day_of_year"] = df_day["date"].dt.dayofyear

X = df_day[["day_num", "day_of_year"]]
y = df_day["temp"].values

degree = 3
poly = PolynomialFeatures(degree)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)

def predict_for_date(input_date_str):
    input_date = pd.to_datetime(input_date_str)
    min_date = df_day["date"].min()
    max_date = df_day["date"].max()

    if input_date < min_date or input_date > max_date:
        return None, f"Дата поза межами: {min_date.date()} - {max_date.date()}"

    day_num = (input_date - min_date).days
    next_day_num = day_num + 1
    next_date = min_date + pd.Timedelta(days=next_day_num)
    day_of_year = next_date.dayofyear

    if next_day_num > df_day["day_num"].max():
        return None, "Немає даних для наступного дня, прогноз недоступний"

    df_pred = pd.DataFrame({"day_num": [next_day_num], "day_of_year": [day_of_year]})
    X_pred = poly.transform(df_pred)
    pred = model.predict(X_pred)[0]
    return round(pred, 2), None


