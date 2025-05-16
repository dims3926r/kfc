from predictor import df_day, predict_for_date
import matplotlib.pyplot as plt
import pandas as pd

def main():
    while True:
        date_input = input("Введіть дату (РРРР-ММ-ДД) для прогнозу, або 'exit' для виходу: ")
        if date_input.lower() == 'exit':
            break

        pred, err = predict_for_date(date_input)
        if err:
            print("Помилка:", err)
        else:
            print(f"Прогноз середньої температури на наступний день після {date_input}: {pred} °C")

            input_date = pd.to_datetime(date_input)
            min_date = df_day["date"].min()
            next_day_num = (input_date - min_date).days + 1
            forecast_date = min_date + pd.Timedelta(days=next_day_num)

            plt.figure(figsize=(10, 5))
            plt.plot(df_day["date"], df_day["temp"], label="Фактична середня")
            plt.plot(forecast_date, pred, "ro", label="Прогноз")
            plt.title(f"Прогноз середньодобової температури після {date_input}")
            plt.xlabel("Дата")
            plt.ylabel("Температура (°C)")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    main()
