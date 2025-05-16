import unittest
from predictor import df_day, predict_for_date

class TestPredictor(unittest.TestCase):

    def test_predict_valid_dates(self):
        sample_dates = df_day["date"].sample(10).sort_values()
        max_day_num = df_day["day_num"].max()
        start_date = df_day["date"].min()

        for date_val in sample_dates:
            with self.subTest(date=date_val):
                day_num = (date_val - start_date).days
                pred, err = predict_for_date(str(date_val.date()))

                actual_temp_row = df_day[df_day["date"] == date_val]
                actual_temp = actual_temp_row["temp"].values[0] if not actual_temp_row.empty else None

                print(f"Date: {date_val.date()}, Actual: {actual_temp}, Predicted: {pred}, Error: {err}")

                if day_num == max_day_num:
                    self.assertIsNone(pred)
                    self.assertIsNotNone(err)
                else:
                    self.assertIsNone(err)
                    self.assertIsInstance(pred, float)

if __name__ == "__main__":
    unittest.main()
