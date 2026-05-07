import streamlit as st
import pandas as pd

STATE_MAP = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
    "Colorado":"CO","Connecticut":"CT","Delaware":"DE","Florida":"FL","Georgia":"GA",
    "Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS",
    "Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA",
    "Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT",
    "Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM",
    "New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK",
    "Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC",
    "South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT",
    "Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
}

st.title("Farmers Markets Data Finder")
st.write("In this page, you are provided with 2 interactive tables that:"
             "\n 1. Can be filtered by state, city, and accepted payment options"
             "\n 2. Shows a table with the specific metrics of markets based on filters"
             "\n 3. Shows a table with the top cities based off of number of markets according to the filters")

try:
    df = pd.read_csv("farmersmarket_2026.csv", encoding="UTF-8")
except FileNotFoundError:
    st.error("Dataset file not found.")
    st.stop()

df.columns = df.columns.str.strip()
df = df[df["Parsed_State"].isin(STATE_MAP.keys())]

pay_cols = ["acceptedpayment_6", "acceptedpayment_3", "FNAP_1", "FNAP_2", "FNAP_5"]
for col in pay_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

df["State_Abbrev"] = df["Parsed_State"].map(STATE_MAP)

# Sidebar
st.sidebar.header("Filters")
selected_abbrev = st.sidebar.selectbox("Select State", sorted(df["State_Abbrev"].unique()))
selected_state = [k for k, v in STATE_MAP.items() if v == selected_abbrev][0]
city_search = st.sidebar.text_input("Search City")

st.sidebar.subheader("Accepted Payments")
filter_credit = st.sidebar.checkbox("Credit/Debit")
filter_cash   = st.sidebar.checkbox("Cash")
filter_snap   = st.sidebar.checkbox("SNAP/EBT")
filter_wic    = st.sidebar.checkbox("WIC")
filter_senior = st.sidebar.checkbox("Senior FMNP")

# Filter
df_filtered = df[df["Parsed_State"] == selected_state]

if city_search != "":
    df_filtered = df_filtered[
        df_filtered["Parsed_City"].str.contains(city_search, case=False, na=False)
    ]

payment_filter = []
if filter_credit: payment_filter.append("acceptedpayment_6")
if filter_cash:   payment_filter.append("acceptedpayment_3")
if filter_snap:   payment_filter.append("FNAP_2")
if filter_wic:    payment_filter.append("FNAP_1")
if filter_senior: payment_filter.append("FNAP_5")

if len(payment_filter) > 0:
    mask = df_filtered[payment_filter[0]] == 1
    for col in payment_filter[1:]:
        mask = mask | (df_filtered[col] == 1)
    df_filtered = df_filtered[mask]

# Results
st.header(f"Markets in {selected_abbrev}")
st.write(f"**{len(df_filtered)} markets found**")

if len(df_filtered) == 0:
    st.warning("No markets found. Try adjusting your filters.")
else:
    sorted_df = df_filtered.sort_values(by="listing_name")
    st.dataframe(
        sorted_df[["listing_name", "Parsed_City", "Parsed_State", "Parsed_Zip"]]
        .rename(columns={
            "listing_name": "Market Name",
            "Parsed_City": "City",
            "Parsed_State": "State",
            "Parsed_Zip": "Zip Code"
        })
    )

    st.divider()
    st.header(f"Top Cities in {selected_abbrev}")
    top_cities = (
        df_filtered.groupby("Parsed_City")
        .size()
        .reset_index(name="Markets")
        .sort_values("Markets", ascending=False)
    )
    st.write(top_cities.head(10))