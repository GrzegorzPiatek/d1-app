import json
import os

import streamlit as st

PASSWORD = "x7A9kLmP2qW8rT5vBnC3"  # 20 znaków
DATA_FILE = "sales_tracker.json"


def load_data():
    default_data = {
        "goal_name": "Awans",
        "target_amount": 50000.0,
        "current_amount": 0.0
    }

    if not os.path.exists(DATA_FILE):
        return default_data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "goal_name": data.get("goal_name", "Awans"),
            "target_amount": float(data.get("target_amount", 50000.0)),
            "current_amount": float(data.get("current_amount", 0.0)),
        }
    except Exception:
        return default_data


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if "authorized" not in st.session_state:
    st.session_state.authorized = False

data = load_data()

goal_name = data["goal_name"]
target_amount = data["target_amount"]
current_amount = data["current_amount"]

remaining_amount = max(target_amount - current_amount, 0.0)
progress = 0.0 if target_amount <= 0 else min(current_amount / target_amount, 1.0)
progress_percent = progress * 100

st.set_page_config(page_title="Tracker wyniku sprzedażowego", layout="centered")

st.title("📈 Tracker wyniku sprzedażowego")
st.subheader(f"Cel: {goal_name}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Cel", f"{target_amount:,.2f} JB".replace(",", " "))

with col2:
    st.metric("Aktualny wynik", f"{current_amount:,.2f} JB".replace(",", " "))

with col3:
    st.metric("Brakuje", f"{remaining_amount:,.2f} JB".replace(",", " "))

st.progress(progress)

st.markdown(f"### Realizacja celu: {progress_percent:.2f}%")

if current_amount >= target_amount:
    st.success(f"🎉 Cel osiągnięty — awans {goal_name} zrobiony!")
else:
    st.warning(
        f"Do osiągnięcia celu **{goal_name}** brakuje jeszcze "
        f"**{remaining_amount:,.2f} JB**.".replace(",", " ")
    )

st.divider()

st.subheader("🔐 Panel edycji")

password_input = st.text_input("Podaj hasło", type="password")

if st.button("Zaloguj"):
    if password_input == PASSWORD:
        st.session_state.authorized = True
        st.success("Zalogowano.")
    else:
        st.error("Nieprawidłowe hasło.")

if st.session_state.authorized:
    st.subheader("Edytuj dane")

    new_goal_name = st.text_input("Nazwa celu / awansu", value=goal_name)
    new_target_amount = st.number_input(
        "Kwota celu (JB)",
        min_value=0.0,
        value=float(target_amount),
        step=1000.0
    )
    new_current_amount = st.number_input(
        "Aktualny wynik sprzedaży (JB)",
        min_value=0.0,
        value=float(current_amount),
        step=100.0
    )

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Zapisz dane"):
            updated_data = {
                "goal_name": new_goal_name,
                "target_amount": new_target_amount,
                "current_amount": new_current_amount,
            }
            save_data(updated_data)
            st.success("Dane zapisane.")
            st.rerun()

    with col_b:
        if st.button("Wyzeruj wynik"):
            updated_data = {
                "goal_name": new_goal_name,
                "target_amount": new_target_amount,
                "current_amount": 0.0,
            }
            save_data(updated_data)
            st.success("Wynik wyzerowany.")
            st.rerun()