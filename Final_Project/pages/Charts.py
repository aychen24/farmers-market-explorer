import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

st.title("Farmers Markets Charts")
st.write("In this page, you are provided with 3 charts: \n 1. Shows the top 10 States by the number of markets they have as a vertical bar chart"
         "\n 2. Shows the payment methods accepted in certain states depending on the state you have selected on the filter as a horizontal bar chart"
         "\n 3. Shows the top 5 cities by number of markets in the state you have selected on the filter as a pie chart")

try:
    pd.read_csv("Final_Project/farmersmarket_2026.csv", encoding="UTF-8")
except FileNotFoundError:
    st.error("Dataset file not found.")
    st.stop()

df.columns = df.columns.str.strip()
df = df[df["Parsed_State"].isin(STATE_MAP.keys())]
df["State_Abbrev"] = df["Parsed_State"].map(STATE_MAP)

pay_cols = ["acceptedpayment_6", "acceptedpayment_3", "FNAP_2", "FNAP_1", "FNAP_5"]
for col in pay_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# Sidebar
st.sidebar.header("Chart Filters")
selected_abbrev = st.sidebar.selectbox("Select State", sorted(df["State_Abbrev"].unique()))
selected_state = [k for k, v in STATE_MAP.items() if v == selected_abbrev][0]
df_state = df[df["Parsed_State"] == selected_state]

# Chart 1: Top 10 states
st.header("Top 10 States by Number of Markets")

state_counts = (
    df.groupby("State_Abbrev")
    .size()
    .reset_index(name="Markets")
    .sort_values("Markets", ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(state_counts["State_Abbrev"], state_counts["Markets"], color="steelblue")
ax1.set_xlabel("State")
ax1.set_ylabel("Number of Markets")
ax1.set_title("Top 10 States by Number of Markets")
st.pyplot(fig1)

# Chart 2: Payment methods
st.header(f"Payment Methods Accepted in {selected_abbrev}")

payment_labels = ["Credit/Debit", "Cash", "SNAP/EBT", "WIC", "Senior FMNP"]
payment_cols   = ["acceptedpayment_6", "acceptedpayment_3", "FNAP_2", "FNAP_1", "FNAP_5"]
payment_counts = [len(df_state[df_state[col] == 1]) for col in payment_cols]

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.barh(payment_labels, payment_counts, color="seagreen")
ax2.set_xlabel("Number of Markets")
ax2.set_title(f"Payment Methods in {selected_abbrev}")
st.pyplot(fig2)

# Chart 3: Top 5 cities pie
st.header(f"Top 5 Cities in {selected_abbrev}")

city_counts = (
    df_state.groupby("Parsed_City")
    .size()
    .reset_index(name="Markets")
    .sort_values("Markets", ascending=False)
    .head(5)
)

if len(city_counts) > 0:
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.pie(city_counts["Markets"], labels=city_counts["Parsed_City"], autopct="%1.1f%%")
    ax3.set_title(f"Top 5 Cities in {selected_abbrev}")
    st.pyplot(fig3)
else:
    st.write("Not enough city data for this state.")
