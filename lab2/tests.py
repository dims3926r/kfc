import unittest
from main import calculate_bill, DATA_FILE

def clear_data():
    with open(DATA_FILE, "w") as f:
        f.write("{}") 

class TestSimple(unittest.TestCase):
    def setUp(self):
        clear_data() 

    def test_first_time(self):
        bill, message = calculate_bill("101", 150, 90)
        self.assertEqual(bill, 0.0)
        self.assertIn("Це новий лічильник. Рахунок = 0 грн", message)

    def test_second_time(self):
        calculate_bill("102", 200, 100)
        bill, message = calculate_bill("102", 300, 200)
        expected_bill = (100 * 5.2) + (100 * 3.4)
        self.assertAlmostEqual(bill, expected_bill)
        self.assertIn("Споживання: день=100 кВт, ніч=100 кВт", message)

    def test_night_less(self):
        calculate_bill("103", 500, 300)
        bill, message = calculate_bill("103", 600, 250)
        expected_bill = (100 * 5.2) + (30 * 3.4)
        self.assertAlmostEqual(bill, expected_bill) 
        self.assertIn("Споживання: день=100 кВт, ніч=30 кВт", message)

    def test_day_less(self):
        calculate_bill("104", 500, 300) 
        bill, message = calculate_bill("104", 450, 350) 
        expected_bill = (50 * 5.2) + (50 * 3.4)
        self.assertAlmostEqual(bill, expected_bill)
        self.assertIn("Споживання: день=50 кВт, ніч=50 кВт", message)

    def test_both_less(self):
        calculate_bill("105", 500, 300) 
        bill, message = calculate_bill("105", 400, 250)  
        expected_bill =  (30 * 3.4)  
        self.assertAlmostEqual(bill, expected_bill, places=2)  
        self.assertIn("Споживання: день=0 кВт, ніч=30 кВт", message)


if __name__ == "__main__":
    unittest.main()
