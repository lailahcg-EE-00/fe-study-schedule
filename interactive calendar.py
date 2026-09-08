import streamlit as st
import datetime
import calendar
st.write("APP IS RUNNING")

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FE Electrical Study Calendar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# APPEARANCE
# ============================================================

st.markdown(
    """
    <style>
        /* Use more of the available screen width */
        .block-container {
            max-width: 100%;
            padding-top: 1.4rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            padding-bottom: 3rem;
        }

        /* Main title */
        .tracker-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: #17233c;
            margin-bottom: 0.15rem;
        }

        .tracker-subtitle {
            color: #5d6676;
            font-size: 1.02rem;
            margin-bottom: 1.2rem;
        }

        /* Calendar weekday headers */
        .weekday-header {
            background-color: #17233c;
            color: white;
            text-align: center;
            font-weight: 700;
            border-radius: 7px;
            padding: 0.55rem 0.15rem;
            margin-bottom: 0.25rem;
        }

        /* Styling for Streamlit column containers */
        div[data-testid="stHorizontalBlock"] {
            align-items: stretch;
        }

        /* Calendar day label */
        .calendar-date {
            font-size: 1.05rem;
            font-weight: 800;
            color: #17233c;
            margin-bottom: 0.3rem;
        }

        /* Today's date label */
        .today-date {
            display: inline-block;
            background-color: #17233c;
            color: white;
            border-radius: 999px;
            padding: 0.2rem 0.62rem;
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        /* Topic heading displayed inside a day */
        .topic-title {
            font-size: 0.88rem;
            font-weight: 750;
            line-height: 1.2;
            color: #243657;
            margin-top: 0.15rem;
            margin-bottom: 0.35rem;
        }

        /* Topic label for rolled tasks */
        .rolled-topic {
            font-size: 0.78rem;
            font-weight: 750;
            color: #9a5215;
            margin-top: 0.3rem;
            margin-bottom: 0.05rem;
        }

        /* Small scheduled-date text */
        .original-date {
            color: #8b5d32;
            font-size: 0.69rem;
            margin-bottom: 0.1rem;
        }

        /* Empty calendar day */
        .empty-day {
            min-height: 155px;
        }

        /* Make checkbox labels smaller inside calendar cells */
        div[data-testid="stCheckbox"] label p {
            font-size: 0.78rem;
            line-height: 1.15rem;
        }

        /* Reduce whitespace around checkboxes */
        div[data-testid="stCheckbox"] {
            margin-top: -0.18rem;
            margin-bottom: -0.25rem;
        }

        /* Metric card appearance */
        div[data-testid="stMetric"] {
            background: #f7f8fa;
            border: 1px solid #d9dde5;
            border-radius: 10px;
            padding: 0.8rem;
        }

        /* Responsive adjustments for smaller screens */
        @media (max-width: 900px) {
            .tracker-title {
                font-size: 1.8rem;
            }

            .block-container {
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }

            div[data-testid="stCheckbox"] label p {
                font-size: 0.72rem;
                line-height: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FE ELECTRICAL STUDY SCHEDULE
# ============================================================

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
            "Solve Time Value of Money problems"
        ]
    },

    datetime.date(2026, 9, 10): {
        "topic": "Properties of Electrical Materials",
        "tasks": [
            "Review XLPE & Thermoset wire insulation specs",
            "Practice Semiconductor physics",
            "Review chemical material properties"
        ]
    },

    datetime.date(2026, 9, 11): {
        "topic": "Circuit Analysis: DC & AC Steady State",
        "tasks": [
            "Solve KCL/KVL Node & Mesh equations",
            "Practice Thevenin/Norton Equivalent circuits",
            "Calculate AC Impedance & Phasors"
        ]
    },

    datetime.date(2026, 9, 12): {
        "topic": "Circuit Analysis: Transient & Three-Phase",
        "tasks": [
            "Review First-Order RL/RC Transient responses",
            "Calculate Balanced Three-Phase Power",
            "Review Delta/Wye junctions"
        ]
    },

    datetime.date(2026, 9, 14): {
        "topic": "Linear Systems & Signal Processing",
        "tasks": [
            "Practice Continuous-time Convolution",
            "Review Laplace & Fourier Transform mappings",
            "Review Nyquist sampling criteria"
        ]
    },

    datetime.date(2026, 9, 15): {
        "topic": "Electronics",
        "tasks": [
            "Analyze Ideal & Non-Ideal Op-Amp configurations",
            "Solve Diode circuits",
            "Study BJT/FET bias states and switching thresholds"
        ]
    },

    datetime.date(2026, 9, 16): {
        "topic": "Power Systems",
        "tasks": [
            "Practice Power Factor correction calculations",
            "Review Transformer equivalent circuits",
            "Solve Transmission line model equations"
        ]
    }
}


# ============================================================
# DATE SETTINGS
# ============================================================

# Uses the actual date reported by the Streamlit server.
TODAY = datetime.date.today()

# This lets you test rollover without waiting until tomorrow.
# Set USE_TEST_DATE to True, then change TEST_DATE.
USE_TEST_DATE = False
TEST_DATE = datetime.date(2026, 9, 9)

if USE_TEST_DATE:
    TODAY = TEST_DATE


# Determine which month should be shown.
# During the schedule, show the current month.
# Before the schedule starts, show the first schedule month.
# After the schedule ends, show the last schedule month.

schedule_dates = sorted(STUDY_SCHEDULE.keys())
first_schedule_date = schedule_dates[0]
last_schedule_date = schedule_dates[-1]

if TODAY < first_schedule_date:
    DISPLAY_YEAR = first_schedule_date.year
    DISPLAY_MONTH = first_schedule_date.month

elif TODAY > last_schedule_date:
    DISPLAY_YEAR = last_schedule_date.year
    DISPLAY_MONTH = last_schedule_date.month

else:
    DISPLAY_YEAR = TODAY.year
    DISPLAY_MONTH = TODAY.month


# ============================================================
# CHECKBOX AND TASK FUNCTIONS
# ============================================================

def task_key(original_date, task_number):
    """
    Produces one permanent identity for each action item.

    The identity uses the task's originally scheduled date rather
    than the date on which the task is currently displayed.

    This is important because a task may roll forward to today,
    but it must retain the same checkbox value.
    """
    return (
        f"task_"
        f"{original_date.strftime('%Y_%m_%d')}_"
        f"{task_number}"
    )


def initialize_task_states():
    """
    Creates an unchecked state for each action item the first time
    the item is encountered during the current Streamlit session.
    """
    for original_date, day_data in STUDY_SCHEDULE.items():
        for task_number in range(len(day_data["tasks"])):
            key = task_key(original_date, task_number)

            if key not in st.session_state:
                st.session_state[key] = False


def is_task_complete(original_date, task_number):
    """
    Returns whether one specific action item is complete.
    """
    key = task_key(original_date, task_number)
    return st.session_state.get(key, False)


def is_topic_complete(original_date):
    """
    A topic is complete only when all its action items are checked.
    """
    day_data = STUDY_SCHEDULE[original_date]

    return all(
        is_task_complete(original_date, task_number)
        for task_number in range(len(day_data["tasks"]))
    )


def get_total_task_count():
    """
    Returns the total number of configured study action items.
    """
    return sum(
        len(day_data["tasks"])
        for day_data in STUDY_SCHEDULE.values()
    )


def get_completed_task_count():
    """
    Counts all checked action items.
    """
    completed = 0

    for original_date, day_data in STUDY_SCHEDULE.items():
        for task_number in range(len(day_data["tasks"])):
            if is_task_complete(original_date, task_number):
                completed += 1

    return completed


def get_incomplete_overdue_tasks():
    """
    Returns incomplete action items originally scheduled before today.

    Each returned dictionary retains:
    - The original scheduled date
    - The original topic
    - The task's index
    - The task description

    These items will be displayed inside today's calendar cell.
    """
    overdue_tasks = []

    for original_date in schedule_dates:
        if original_date >= TODAY:
            continue

        day_data = STUDY_SCHEDULE[original_date]

        for task_number, task_text in enumerate(day_data["tasks"]):
            if not is_task_complete(original_date, task_number):
                overdue_tasks.append(
                    {
                        "original_date": original_date,
                        "topic": day_data["topic"],
                        "task_number": task_number,
                        "task": task_text
                    }
                )

    return overdue_tasks


def reset_progress():
    """
    Sets every task checkbox back to unchecked.
    """
    for original_date, day_data in STUDY_SCHEDULE.items():
        for task_number in range(len(day_data["tasks"])):
            key = task_key(original_date, task_number)
            st.session_state[key] = False


initialize_task_states()


# ============================================================
# CALENDAR DISPLAY FUNCTIONS
# ============================================================

def display_regular_scheduled_tasks(
    cell,
    display_date,
    disable_tasks=False
):
    """
    Displays tasks originally scheduled for the supplied date.

    Future action items are shown for preview but disabled.
    Today's and past tasks are interactive.
    """
    if display_date not in STUDY_SCHEDULE:
        return

    day_data = STUDY_SCHEDULE[display_date]

    cell.markdown(
        f"""
        <div class="topic-title">
            {day_data["topic"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    for task_number, task_text in enumerate(day_data["tasks"]):
        key = task_key(display_date, task_number)

        cell.checkbox(
            task_text,
            key=key,
            disabled=disable_tasks
        )

    if is_topic_complete(display_date):
        cell.success("Topic complete")


def display_rolled_tasks(cell):
    """
    Displays every overdue incomplete item inside today's cell.

    Rolled items use their original checkbox key, so the same item
    does not get duplicated or lose its completion state.
    """
    overdue_tasks = get_incomplete_overdue_tasks()

    if not overdue_tasks:
        return

    cell.warning(
        f"{len(overdue_tasks)} unfinished "
        f"{'item has' if len(overdue_tasks) == 1 else 'items have'} "
        f"rolled into today."
    )

    last_topic_and_date = None

    for overdue_item in overdue_tasks:
        topic_and_date = (
            overdue_item["topic"],
            overdue_item["original_date"]
        )

        if topic_and_date != last_topic_and_date:
            cell.markdown(
                f"""
                <div class="rolled-topic">
                    ↪ {overdue_item["topic"]}
                </div>
                <div class="original-date">
                    Originally scheduled:
                    {overdue_item["original_date"].strftime("%b %d")}
                </div>
                """,
                unsafe_allow_html=True
            )

            last_topic_and_date = topic_and_date

        key = task_key(
            overdue_item["original_date"],
            overdue_item["task_number"]
        )

        cell.checkbox(
            overdue_item["task"],
            key=key
        )


def display_calendar_day(cell, display_date):
    """
    Renders one calendar date and determines which action items
    belong in the date's cell.
    """

    if display_date == TODAY:
        cell.markdown(
            f"""
            <div class="today-date">
                {display_date.day} · TODAY
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        cell.markdown(
            f"""
            <div class="calendar-date">
                {display_date.day}
            </div>
            """,
            unsafe_allow_html=True
        )
