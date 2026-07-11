import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ========= PAGE SETUP =========
st.set_page_config(page_title="Punjab Bus Booking", layout="centered", page_icon="🚌")

# ========= LOGO + HEADER =========
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=70) # Bus Logo
with col2:
    st.title("Punjab Bus Booking")
    st.caption("Fast • Reliable • Affordable")
   
    

st.markdown("---")

# ========= 1. MODEL LOAD =========
try:
    model = joblib.load('punjab_40_model.pkl')
    df = pd.read_csv('punjab.csv')
    punjab_cities = sorted(df['From'].unique().tolist())
    city_index = {city: i for i, city in enumerate(punjab_cities)}
except Exception as e:
    st.error(f"System Error: {e}")
    st.stop()

# ========= 2. BOOKING FORM =========
with st.form("booking_form"):
    st.subheader("Route Details")
    col1, col2 = st.columns(2)
    with col1:
        from_city = st.selectbox("📍 From", punjab_cities)
    with col2:
        to_city = st.selectbox("📍 To", punjab_cities)

    col3, col4 = st.columns(2)
    with col3:
        distance_km = st.number_input("🛣️ Distance in KM", min_value=1, max_value=1000, value=100, step=5)
    with col4:
        fuel_price = st.number_input("⛽ Fuel Price PKR/L", value=295.0, step=1.0)

    submit = st.form_submit_button("🔍 Get Booking Price", type="primary", use_container_width=True)

# ========= 3. CALCULATION =========
if submit:
    if from_city == to_city:
        st.warning("⚠️ From and To city cannot be same")
    else:
        # 1. TRIP COST CALCULATION
        fuel_cost = (distance_km / 5.0) * fuel_price
        maintenance = distance_km * 4.0
        toll_driver = 1200
        total_trip_cost = fuel_cost + maintenance + toll_driver # YEH COST HAI

        # 2. MODEL BASE PRICE
        from_enc = city_index[from_city]
        to_enc = city_index[to_city]
        input_data = [[from_enc, to_enc, 0, distance_km, fuel_price, fuel_cost]]
        base_price = model.predict(input_data)[0]

        # 3. 40% PROFIT ADD - HIDDEN
        profit_margin = 0.40
        final_price = base_price * (1 + profit_margin)

        # ========= 4. RESULT DISPLAY =========
        st.markdown("---")
        st.subheader("💰 Booking Summary")

        colA, colB, colC = st.columns(3)
        colA.metric("Total Distance", f"{distance_km} KM")
        colB.metric("Trip Cost", f"PKR {round(total_trip_cost,2)}")
        colC.metric("Final Price", f"PKR {round(final_price,2)}")

        st.info(f"Route: {from_city} → {to_city}")
        st.success("Price includes all taxes and charges")