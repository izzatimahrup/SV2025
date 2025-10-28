import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Student Survey",
    page_icon="🎓",
    layout="wide"
)

# --- Sidebar Navigation (acts as your Menu) ---
pg = st.sidebar.radio(
    "Menu",
    ["Homepage", "Pencapaian Akademik"]
)

# --- Homepage ---
if pg == "Homepage":
    st.title("🏠 Homepage")
    st.write("Welcome to the Student Survey application.")
    st.write("Use the menu on the left to navigate between pages.")

# --- Pencapaian Akademik ---
elif pg == "Pencapaian Akademik":
    st.title("🎓 Pencapaian Akademik")
    st.write("This page shows academic achievement visualization.")
    st.write("You can add graphs, data, or analysis here later.")
