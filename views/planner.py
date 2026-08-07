import streamlit as st
from database.planner import (
    create_task,
    get_tasks
)

USER_ID = 1

st.title("🚀 AI Planner")

goal = st.text_input(
    "What do you want to achieve?"
)

if st.button("Create Mission"):

    missions = [

        "Brand Name",

        "Logo",

        "Moodboard",

        "Fashion Collection",

        "Fabric Selection",

        "Cost Estimation",

        "Tech Pack",

        "Marketing",

        "Website",

        "Launch"

    ]

    for task in missions:

        create_task(USER_ID, task)

    st.success("Mission Created!")

tasks = get_tasks(USER_ID)

st.divider()

for task in tasks:

    st.checkbox(
        task[2],
        value=(task[3] == "Completed")
    )