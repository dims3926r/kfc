import json
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "meters_data.json"
HISTORY_FILE = "history.json"

TARIFFS = {"day": 5.2, "night": 3.4}
ADJUSTMENT = {"day": 100, "night": 80}

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_history(entry):
    history = load_history()
    meter_id = entry["meter_id"]
    
    if meter_id not in history:
        history[meter_id] = []
    
    history[meter_id].append({"day": entry["day"], "night": entry["night"], "bill": entry["bill"]})
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def calculate_bill(meter_id, new_day, new_night):
    data = load_data()
    
    if meter_id not in data:
        data[meter_id] = {"prev_day": new_day, "prev_night": new_night}
        save_data(data)
        return 0.0, "Це новий лічильник. Рахунок = 0 грн"
    
    prev_day, prev_night = data[meter_id]["prev_day"], data[meter_id]["prev_night"]
    
    if new_day < prev_day:
        new_day += ADJUSTMENT["day"]
    if new_night < prev_night:
        new_night += ADJUSTMENT["night"]
    
    usage_day = new_day - prev_day
    usage_night = new_night - prev_night
    
    if usage_day == 0 and usage_night == 0:
        return 0.0, "Показники не змінилися, рахунок = 0 грн"
    
    bill = usage_day * TARIFFS["day"] + usage_night * TARIFFS["night"]
    
    data[meter_id] = {"prev_day": new_day, "prev_night": new_night}
    save_data(data)
    
    save_history({"meter_id": meter_id, "day": new_day, "night": new_night, "bill": bill})
    
    return bill, f"Споживання: день={usage_day} кВт, ніч={usage_night} кВт. Рахунок = {bill:.2f} грн"
    
def show_meters():
    data = load_history()
    result = []
    
    for k, v in data.items():
        result.append(f"{k}:")
        for entry in v:
            result.append(f"день={entry['day']}, ніч={entry['night']}, рахунок={entry['bill']} грн")
    
    result_text.set("\n".join(result) or "Немає даних")


def submit():
    meter_id = meter_id_entry.get().strip()
    
    try:
        new_day = int(day_entry.get())
        new_night = int(night_entry.get())
        
        bill, message = calculate_bill(meter_id, new_day, new_night)
        
        messagebox.showinfo("Результат", f"Рахунок за електроенергію: {bill:.2f} грн\n{message}")
        
        meter_id_entry.delete(0, tk.END)
        day_entry.delete(0, tk.END)
        night_entry.delete(0, tk.END)
    
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть числові значення!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Електролічильник")

    tk.Label(root, text="ID лічильника:").pack()
    meter_id_entry = tk.Entry(root)
    meter_id_entry.pack()

    tk.Label(root, text="Денні показники:").pack()
    day_entry = tk.Entry(root)
    day_entry.pack()

    tk.Label(root, text="Нічні показники:").pack()
    night_entry = tk.Entry(root)
    night_entry.pack()

    tk.Button(root, text="Відправити", command=submit).pack()
    tk.Button(root, text="Показати всі лічильники", command=show_meters).pack()

    result_text = tk.StringVar()
    tk.Label(root, textvariable=result_text, justify=tk.LEFT).pack()

    root.mainloop()
