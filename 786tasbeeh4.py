import streamlit as st
import json
from datetime import datetime, timedelta

# Title and Instructions
st.title("📿 Online Zikr Count Tracker")
st.write("Track your daily Zikr effortlessly. Minimal design, mobile-friendly!")

# Predefined Zikr List
zikr_list = [
    "سُبْحَانَ اللهِ (SubhanAllah)",
    "الْحَمْدُ لِلَّهِ (Alhamdulillah)",
    "اللَّهُ أَكْبَرُ (Allahu Akbar)",
    "لَا إِلٰهَ إِلَّا اللَّهُ (La ilaha illallah)",
    "أَسْتَغْفِرُ اللَّهَ (Astaghfirullah)",
    "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ (Allahumma salli 'ala Muhammad)",
]

# User selects a Zikr
selected_zikr = st.selectbox("Choose a Zikr for today's Tasbeeh", zikr_list)

# Initialize Session State for Counter
if "count" not in st.session_state:
    st.session_state.count = 0

# Increment Counter Function
def increment():
    st.session_state.count += 1

# Reset Counter Function
def reset_counter():
    st.session_state.count = 0

# Load and Save Progress Functions
def load_progress():
    """Load progress data from JSON file."""
    try:
        with open("progress.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_progress(data):
    """Save progress data to JSON file."""
    with open("progress.json", "w") as f:
        json.dump(data, f)

# Filter Last Week's Data
def filter_last_week(data):
    """Filter progress data to keep only the last 7 days."""
    last_week = datetime.now() - timedelta(days=7)
    return [entry for entry in data if datetime.fromisoformat(entry['date']) > last_week]

# Load Existing Progress
progress = load_progress()

# Display Current Count
st.markdown(f"### Today's Count for **{selected_zikr}**: {st.session_state.count}")

# Buttons for Count and Reset
st.button("Count", on_click=increment, key="count_button")
st.button("Reset", on_click=reset_counter, key="reset_button")

# Save Daily Progress
if st.button("Save Progress", key="save_button"):
    today = datetime.now().strftime("%Y-%m-%d")
    # Append new progress data
    progress.append({"date": today, "zikr": selected_zikr, "count": st.session_state.count})
    # Filter only the last 7 days
    progress = filter_last_week(progress)
    # Save updated progress to JSON
    save_progress(progress)
    st.success("Progress Saved!")

# Show Last Week's Progress
st.markdown("### Progress (Last 7 Days)")
if progress:
    filtered_progress = filter_last_week(progress)
    for entry in filtered_progress:
        zikr_display = entry.get("zikr", "N/A")  # Handle missing zikr key
        st.write(f"**{entry['date']}** - {zikr_display}: {entry['count']} counts")
else:
    st.write("No progress recorded yet.")

# Style for Mobile-Friendliness
st.markdown(
    """
    <style>
    .main {
        max-width: 500px;
        margin: auto;
    }
    button {
        font-size: 18px;
        margin: 5px 0;
    }
    h1, h3, p {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
