import streamlit as st
import pandas as pd
import pydeck as pdk

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

st.title("Farmers Markets Map")
st.write("In this page, you are provided with an interactive map that:"
         "\n 1. Allows you to filter a specific state and number of markets"
         "\n 2. Pinpoints the location of every market in the state"
         "\n 3. Provides the name, address, city, state, and zipcode of the market when hovering over the dot")

try:
    df = pd.read_csv("farmersmarket_2026.csv", encoding="UTF-8")
except FileNotFoundError:
    st.error("Dataset file not found.")
    st.stop()

df.columns = df.columns.str.strip()
df = df.rename(columns={"location_x": "lon", "location_y": "lat"})
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
df = df.dropna(subset=["lat", "lon"])
df = df[df["Parsed_State"].isin(STATE_MAP.keys())]
df["State_Abbrev"] = df["Parsed_State"].map(STATE_MAP)

# Sidebar
st.sidebar.header("Filters")
selected_abbrev = st.sidebar.selectbox("State", sorted(df["State_Abbrev"].unique()))
selected_state = [k for k, v in STATE_MAP.items() if v == selected_abbrev][0]
num_rows = st.sidebar.slider("Markets to display", 10, 300, 100)

# [PY1] Function with default parameter
def count_markets(dataframe, state="Massachusetts"):
    return len(dataframe[dataframe["Parsed_State"] == state])

# Filter
df_filtered = df[df["Parsed_State"] == selected_state].head(num_rows)
st.header(f"Farmers Markets in {selected_abbrev}")

# Map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    get_position="[lon, lat]",
    get_radius=5000,
    get_fill_color=[255, 0, 0, 160],
    pickable=True,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=pdk.ViewState(
        latitude=df_filtered["lat"].mean(),
        longitude=df_filtered["lon"].mean(),
        zoom=6,
    ),
    tooltip={
        "html": "<b>{listing_name}</b><br/>{location_address}",
        "style": {
            "backgroundColor": "rgba(20,20,20,0.85)",
            "color": "white",
            "borderRadius": "8px",
            "padding": "8px 12px",
            "fontSize": "13px",
        },
    },
)

st.pydeck_chart(deck)
st.caption(f"Showing {len(df_filtered)} of {count_markets(df, selected_state)} markets in {selected_abbrev}")