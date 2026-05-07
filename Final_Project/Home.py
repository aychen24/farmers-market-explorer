"""
Adin Chen
CS230-8
URL:

This program is an interactive Streamlit application exploring USDA farmers market data across the United States. Users
can filter the markets by state, city, and accepted payment methods while viewing interactive maps, charts, and tables.
This dataset was processed and analyzed using Pandas to handle missing values and organizing the data for analysis.
"""


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

st.title("U.S. Farmers Markets Explorer")
st.write("In this interactive Streamlit application, you can use the side bar to: \n 1. View charts from market data"
         "\n 2. View information tables about markets \n 3. Use an interactive map to find the location of markets")

try:
    pd.read_csv("Final_Project/farmersmarket_2026.csv", encoding="UTF-8")
    df.columns = df.columns.str.strip()
    df = df[df["Parsed_State"].isin(STATE_MAP.keys())]
    df["State_Abbrev"] = df["Parsed_State"].map(STATE_MAP)

    pay_cols = ["acceptedpayment_6", "acceptedpayment_3", "FNAP_1", "FNAP_2", "FNAP_5"]
    for col in pay_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    st.divider()
    st.subheader("Quick Summary")
    st.write(f"**Total Markets:** {len(df)}")
    st.write(f"**States Covered:** {len(df['State_Abbrev'].unique())}")

    st.divider()
    st.subheader("Summary by State")

    abbrevs = df["State_Abbrev"].unique()
    abbrevs = pd.Series(abbrevs).sort_values().tolist()
    selected_abbrev = st.selectbox("Pick a state", abbrevs)
    selected_state = [k for k, v in STATE_MAP.items() if v == selected_abbrev][0]
    df_state = df[df["Parsed_State"] == selected_state]

    st.write(f"**Markets in {selected_abbrev}:** {len(df_state)}")
    st.write("**Accepted Payments:**")
    st.write(f"- Credit/Debit: {len(df_state[df_state['acceptedpayment_6'] == 1])} markets")
    st.write(f"- Cash: {len(df_state[df_state['acceptedpayment_3'] == 1])} markets")
    st.write(f"- SNAP/EBT: {len(df_state[df_state['FNAP_2'] == 1])} markets")
    st.write(f"- WIC: {len(df_state[df_state['FNAP_1'] == 1])} markets")
    st.write(f"- Senior FMNP: {len(df_state[df_state['FNAP_5'] == 1])} markets")

except FileNotFoundError:
    st.warning("Dataset file not found.")
