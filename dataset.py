import pandas as pd
import numpy as np
import random

# ========= 1. PUNJAB KI 40 CITIES =========
punjab_cities = [
    'Lahore', 'Faisalabad', 'Rawalpindi', 'Multan', 'Gujranwala', 'Bahawalpur', 'Sialkot',
    'Sargodha', 'Sheikhupura', 'Rahim Yar Khan', 'Jhang', 'Dera Ghazi Khan', 'Gujrat',
    'Sahiwal', 'Wah Cantt', 'Kasur', 'Okara', 'Chiniot', 'Khanewal', 'Hafizabad',
    'Mandi Bahauddin', 'Mianwali', 'Pakpattan', 'Bahawalnagar', 'Toba Tek Singh',
    'Vehari', 'Attock', 'Bhakkar', 'Chakwal', 'Jhelum', 'Khushab', 'Layyah', 'Lodhran',
    'Muzaffargarh', 'Nankana Sahib', 'Narowal', 'Rajanpur', 'Chowk Munda', 'Rangpur', 'Kot Addu'
]

# ========= 2. DISTANCE KM TABLE =========
distances = {
    'Lahore-Faisalabad': 140, 'Lahore-Rawalpindi': 275, 'Lahore-Multan': 340, 'Lahore-Gujranwala': 80,
    'Lahore-Bahawalpur': 420, 'Lahore-Sialkot': 125, 'Faisalabad-Multan': 240, 'Faisalabad-Rawalpindi': 320,
    'Rawalpindi-Multan': 480, 'Multan-Bahawalpur': 110, 'Sialkot-Gujranwala': 60, 'Sargodha-Faisalabad': 95,
    'Kot Addu-Multan': 85, 'Kot Addu-Muzaffargarh': 45, 'Kot Addu-Layyah': 70, 'Kot Addu-Dera Ghazi Khan': 95,
    'Chowk Munda-Multan': 110, 'Chowk Munda-Muzaffargarh': 35, 'Chowk Munda-Kot Addu': 40, 'Chowk Munda-Layyah': 60,
    'Rangpur-Multan': 65, 'Rangpur-Khanewal': 50, 'Rangpur-Lodhran': 80, 'Rangpur-Vehari': 90,
    'Kot Addu-Lahore': 420, 'Chowk Munda-Lahore': 380, 'Rangpur-Lahore': 350,
    'Kot Addu-Faisalabad': 280, 'Chowk Munda-Faisalabad': 250, 'Rangpur-Faisalabad': 300,
}

def get_distance(city1, city2):
    key1 = f"{city1}-{city2}"
    key2 = f"{city2}-{city1}"
    if key1 in distances:
        return distances[key1] # <-- YEH THEEK KIYA
    if key2 in distances:
        return distances[key2] # <-- YEH BHI
    return np.random.randint(80, 600) # agar na mile to estimate

# ========= 3. DATASET BANANA =========
print("Dataset ban raha hai... Thori dair lage gi")
np.random.seed(42)

data = []
for i in range(30000): # 30000 rows
    from_city = random.choice(punjab_cities)
    to_city = random.choice([c for c in punjab_cities if c!= from_city])
    distance_km = get_distance(from_city, to_city)

    fuel_price = round(np.random.uniform(260, 320), 2)
    fuel_avg = 4.0 # 25L = 100KM
    fuel_consumed = round(distance_km / fuel_avg, 2)
    fuel_cost = round(fuel_consumed * fuel_price, 2)

    toll = round(distance_km * 3.5, 2)
    maintenance = round(distance_km * 2.0, 2)
    other_expense = 1500
    base_cost = fuel_cost + toll + maintenance + other_expense

    booking_price = round((base_cost / 0.9) * 1.25, 2) # 10% driver + 25% profit
    driver_helper_fee = round(booking_price * 0.1, 2)

    data.append([
        f"TRP{i+1:05d}",
        from_city,
        to_city,
        distance_km,
        "Non-AC",
        72,
        fuel_price,
        fuel_avg,
        fuel_consumed,
        fuel_cost,
        toll,
        0,
        maintenance,
        other_expense,
        driver_helper_fee,
        round(base_cost,2),
        booking_price,
        round(booking_price - base_cost,2)
    ])

columns = [
    'Trip_ID', 'From', 'To', 'Distance_KM', 'Bus_Type', 'Seats',
    'Fuel_Price', 'Fuel_Average_KM_L', 'Fuel_Consumed_Liters', 'Fuel_Cost_Complete_Trip',
    'Toll_Plaza', 'Police_Challan', 'Maintenance', 'Other_Expense',
    'Driver_Helper_Fee', 'Total_Trip_Cost', 'Booking_Price', 'Profit'
]

df = pd.DataFrame(data, columns=columns)
df.to_csv('punjab_40cities_dataset.csv', index=False)
print(f"Ho gaya! File ban gayi: punjab_40cities_dataset.csv")
print(f"Total Rows: {len(df)}")
print(df.head())