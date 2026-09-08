import streamlit as st
import datetime
import calendar

from subjects import SUBJECTS

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

def generate_schedule():

    start_date = datetime.date(2026, 9, 8)

    schedule = {}

    current_date = start_date

    for subject in SUBJECTS:

        schedule[current_date] = {
            "topic": subject["topic"],
            "tasks": subject["tasks"],
            "days": subject["days"]
        }

        current_date += datetime.timedelta(
            days=subject["days"]
        )

    return schedule
STUDY_SCHEDULE = generate_schedule()    

# ============================================================
# CHECKBOX AND TASK FUNCTIONS
# ============================================================

def task_key(original_date, task_number):

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

    if original_date not in STUDY_SCHEDULE:
        return False

    key = task_key(original_date, task_number)

    return st.session_state.get(
        key,
        False
    )

def is_topic_complete(original_date):

    if original_date not in STUDY_SCHEDULE:
        return False

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
# HEADER
# ============================================================

st.markdown(
    """
    <div class="tracker-title">
        ⚡ FE Electrical Exam Study Calendar
    </div>
    <div class="tracker-subtitle">
        Check off each action item as it is completed.
        Unfinished past-due items automatically roll into today.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PROGRESS SUMMARY
# ============================================================

total_tasks = get_total_task_count()
completed_tasks = get_completed_task_count()

remaining_tasks = total_tasks - completed_tasks

if total_tasks > 0:
    completion_percentage = completed_tasks / total_tasks
else:
    completion_percentage = 0

remaining_tasks = total_tasks - completed_tasks

completion_percentage = (
    completed_tasks / total_tasks
    if total_tasks > 0
    else 0
)

metric_columns = st.columns(3)

metric_columns[0].metric(
    "Completed",
    completed_tasks
)

metric_columns[1].metric(
    "Remaining",
    remaining_tasks
)

metric_columns[2].metric(
    "Progress",
    f"{completion_percentage:.0%}"
)

st.progress(completion_percentage)

st.markdown("---")

# ============================================================
# STUDY PLAN
# ============================================================

st.markdown("## FE Study Plan")

for study_date in sorted(STUDY_SCHEDULE.keys()):

    day_data = STUDY_SCHEDULE[study_date]

    st.markdown("---")

    st.subheader(
        f"{study_date.strftime('%B %d, %Y')}"
    )

    st.write(
        f"**{day_data['topic']}**"
    )

    for task_number, task_text in enumerate(
        day_data["tasks"]
    ):

        checkbox_key = task_key(
            study_date,
            task_number
        )

        st.checkbox(
            task_text,
            key=checkbox_key
        )

    if is_topic_complete(study_date):
        st.success("✅ Topic Complete")

