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
        key = task_key(
    STUDY_SCHEDULE[display_date]["topic"],
    task_num
)

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
    # Past date:
    if display_date < TODAY:

        display_regular_scheduled_tasks(
            cell=cell,
            display_date=display_date,
            disable_tasks=False
        )

    # Today:
    elif display_date == TODAY:

        display_regular_scheduled_tasks(
            cell=cell,
            display_date=display_date,
            disable_tasks=False
        )

        display_rolled_tasks(cell)

        if (
            display_date not in STUDY_SCHEDULE
            and not get_incomplete_overdue_tasks()
        ):
            cell.caption("No scheduled or overdue study items.")

    # Future date:
    else:

        display_regular_scheduled_tasks(
            cell=cell,
            display_date=display_date,
            disable_tasks=True
        )

        if display_date in STUDY_SCHEDULE:
            cell.caption("Preview")

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
# MONTH NAVIGATION
# ============================================================

if "month_offset" not in st.session_state:
    st.session_state.month_offset = 0

nav1, nav2, nav3 = st.columns([1, 3, 1])

with nav1:
    if st.button("◀ Previous"):
        st.session_state.month_offset -= 1

with nav3:
    if st.button("Next ▶"):
        st.session_state.month_offset += 1

base_date = datetime.date(
    DISPLAY_YEAR,
    DISPLAY_MONTH,
    1
)

month_number = (
    base_date.month
    + st.session_state.month_offset
)

display_year = base_date.year + (
    (month_number - 1) // 12
)

display_month = (
    ((month_number - 1) % 12)
    + 1
)

month_name = calendar.month_name[display_month]

st.markdown(
    f"## {month_name} {display_year}"
)

weekday_names = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]

weekday_columns = st.columns(7)

for i, day_name in enumerate(weekday_names):

    weekday_columns[i].markdown(
        f"""
        <div class="weekday-header">
            {day_name}
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# CALENDAR GRID
# ============================================================

month_calendar = calendar.Calendar(
    firstweekday=calendar.MONDAY
).monthdatescalendar(
    display_year,
    display_month
)

for week in month_calendar:

    cols = st.columns(7)

    for day_index, display_date in enumerate(week):

        with cols[day_index]:
            if display_date.month != display_month:
                st.empty()
                continue

            st.markdown(
                f"### {display_date.day}"
            )

            if display_date in STUDY_SCHEDULE:
                st.write(
                    STUDY_SCHEDULE[display_date]["topic"]
                )                
                for task_num, task in enumerate(
                    STUDY_SCHEDULE[display_date]["tasks"]
                ):

                    checkbox_key = task_key(
                        display_date,
                        task_num
                    )

                    st.checkbox(
                        task,
                        key=checkbox_key
                    )

                if is_topic_complete(display_date):
                    st.success("✅ Topic Complete")

st.markdown("---")
