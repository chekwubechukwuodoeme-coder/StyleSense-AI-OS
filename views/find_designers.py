import streamlit as st

from services.designer_data import designers


def render_find_designers():

    st.header("👗 Find Fashion Designers")

    city = st.text_input(
        "Search by city",
        placeholder="Owerri, Lagos..."
    )

    speciality = st.selectbox(
        "Specialization",
        [
            "All",
            "Luxury Native Wear",
            "Wedding Fashion",
            "Corporate Fashion"
        ]
    )

    filtered_designers = []

    for designer in designers:

        if city and city.lower() not in designer["location"].lower():
            continue

        if (
            speciality != "All"
            and speciality != designer["specialty"]
        ):
            continue

        filtered_designers.append(designer)

    if not filtered_designers:
        st.warning("No designers found.")
        return

    for designer in filtered_designers:

        with st.container(border=True):

            col1, col2 = st.columns([1, 3])

            with col1:

                st.image(
                    designer["image"],
                    use_container_width=True
                )

            with col2:

                st.subheader(designer["name"])

                st.write(f"⭐ Rating: {designer['rating']}")

                st.write(f"📍 Location: {designer['location']}")

                st.write(f"✂ Specialty: {designer['specialty']}")

                st.write(f"💼 Experience: {designer['experience']}")

                st.write(f"💰 Price: {designer['price']}")

                st.code(designer["phone"])

            st.divider()