import streamlit as st
import datetime

# --- SET UP WEB PAGE LAYOUT ---
st.set_page_config(page_title="FE Electrical Schedule", page_icon="⚡", layout="centered")

st.title("⚡ FE Electrical Exam Study Tracker")
st.write("Select a date from the calendar below to check your exam preparation agenda.")

# --- FE ELECTRICAL STUDY SCHEDULE DATABASE ---
# Keys are actual datetime.date objects for seamless calendar interaction
STUDY_SCHEDULE = {
    datetime.date(2026, 9, 8): {
        "topic": "Mathematics & Professional Practice",
        "tasks": [
            "Review Analytic Geometry & Calculus formulas",
            "Practice Vector Analysis problems",
            "Study NCEES Ethics, Liability, and contract rules"
        ]
    },
    datetime.date(2026, 9, 9): {
        "topic": "Probability, Statistics & Engineering Economics",
        "tasks": [
            "Practice Mean, Variance, and Normal Distributions",
            "Solve Time Value of Money problems (Present/Future Worth)"
        ]
    },
    datetime.date(2026, 9, 10): {
        "topic": "Properties of Electrical Materials",
        "tasks": [
            "Review XLPE & Thermoset wire insulation specs",
            "Practice Semiconductor physics & Chemical material properties"
        ]
    },
    datetime.date(2026, 9, 11): {
        "topic": "Circuit Analysis (DC & AC Steady State)",
        "tasks": [
            "Solve KCL/KVL Node & Mesh equations",
            "Practice Thevenin/Norton Equivalent circuits",
            "Calculate AC Impedance & Phasors"
        ]
    },
    datetime.date(2026, 9, 12): {
        "topic": "Circuit Analysis (Transient & Three-Phase)",
        "tasks": [
            "Review First-Order RL/RC Transient responses",
            "Calculate Balanced Three-Phase Power and Delta/Wye junctions"
        ]
    },
    datetime.date(2026, 9, 14): {
        "topic": "Linear Systems & Signal Processing",
        "tasks": [
            "Practice Continuous-time Convolution",
            "Review Laplace & Fourier Transform mappings",
            "Review Nyquist sampling criteria parameters"
        ]
    },
    datetime.date(2026, 9, 15): {
        "topic": "Electronics",
        "tasks": [
            "Analyze Ideal & Non-Ideal Op-Amp configurations",
            "Solve Diode circuits (clippers, clampers, rectifiers)",
            "Study BJT/FET bias states and switching thresholds"
        ]
    },
    datetime.date(2026, 9, 16): {
        "topic": "Power Systems",
        "tasks": [
            "Practice Power Factor correction calculations",
            "Review Transformer equivalent circuits & voltage regulation",
            "Solve Transmission line model equations"
        ]
    }
}

# --- MOBILE FRIENDLY CALENDAR PICKER WIDGET ---
# Default starting date set to today (September 8, 2026)
selected_date = st.date_input("📅 Choose a Study Date:", datetime.date(2026, 9, 8))

st.markdown("---")

# --- DAILY STUDY AGENDA DISPLAY ---
if selected_date in STUDY_SCHEDULE:
    day_data = STUDY_SCHEDULE[selected_date]
    
    # Highlight the main topic area
    st.subheader(f"📚 {day_data['topic']}")
    
    # Display each sub-task nicely with a mobile checklist layout
    st.write("**Your Action Items for Today:**")
    for task in day_data['tasks']:
        st.write(f"⬜ {task}")
else:
    # Fallback option for unscheduled tracking days
    st.subheader("🗓️ Free Study / Catch-up Day")
    st.write("⬜ Review weak topics from previous sections")
    st.write("⬜ Open the NCEES Reference Handbook to browse formulas")
    st.write("⬜ Take a quick 15-minute diagnostic practice quiz")
