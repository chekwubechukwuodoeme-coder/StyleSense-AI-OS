import streamlit as st
import random

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="StyleSense AI",
    page_icon="👗",
    layout="wide"
)

# -----------------------------------
# SESSION STORAGE
# -----------------------------------

if "saved_designs" not in st.session_state:
    st.session_state.saved_designs = []

# -----------------------------------
# FUNCTIONS
# -----------------------------------

def generate_design(gender, category, fabric, occasion, complexity, theme):

    design_names = [
        "Royal Eclipse",
        "Urban Monarch",
        "Golden Heritage",
        "Midnight Prestige",
        "African Luxe",
        "Emerald Crown",
        "Elite Signature",
        "Modern Dynasty"
    ]

    colors = [
        "Black and Gold",
        "Royal Blue and Silver",
        "Wine and Black",
        "Emerald Green and White",
        "Cream and Brown",
        "Navy and Gold"
    ]

    sleeves = [
        "Long fitted sleeves",
        "Layered sleeves",
        "Luxury wide sleeves",
        "Modern tapered sleeves"
    ]

    collars = [
        "Mandarin collar",
        "Royal embroidered collar",
        "Classic collar",
        "Minimalist neckline"
    ]

    backs = [
        "Structured luxury back",
        "Layered back panel",
        "Embroidered rear section",
        "Clean modern finish"
    ]

    return {
        "Design Name": random.choice(design_names),
        "Theme": theme,
        "Description": f"A {complexity.lower()} {category.lower()} outfit designed for {occasion.lower()} occasions.",
        "Fabric": fabric,
        "Colors": random.choice(colors),
        "Front View": "Premium front structure with detailed finishing.",
        "Back View": random.choice(backs),
        "Sleeve Design": random.choice(sleeves),
        "Collar Design": random.choice(collars),
        "Tailor Notes": "Maintain premium stitching and neat finishing.",
        "Target Audience": gender
    }

# -----------------------------------
# HEADER
# -----------------------------------

st.title("👗 StyleSense AI")
st.caption("Fashion Design • Outfit Styling • Creative Inspiration")

# -----------------------------------
# TABS
# -----------------------------------

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "👔 Style My Outfit",
        "✨ Design Studio",
        "🎲 Idea Generator",
        "👗 Collection Builder",
        "📚 Design Library",
        "🎨 Sketch Studio",
        "🤖 Fashion Assistant"
    ]
)

# ===================================
# TAB 1
# ===================================

with tab1:

    st.header("Style My Outfit")

    photo = st.file_uploader(
        "Upload your outfit photo",
        type=["jpg", "jpeg", "png"]
    )

    occasion = st.selectbox(
        "Occasion",
        [
            "Wedding",
            "Office",
            "Church",
            "Party",
            "Date",
            "Casual"
        ]
    )

    if photo:
        st.image(photo, width=350)

        st.success("Photo uploaded successfully")

        st.subheader("Style Analysis")

        st.write("Style Score: 8.5/10")
        st.write("Recommended Shoes: White Sneakers")
        st.write("Recommended Accessories: Silver Watch")
        st.write("Best Occasion Match: " + occasion)

# ===================================
# TAB 2
# ===================================

with tab2:

    st.header("Generate Fashion Design")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Unisex"]
    )

    category = st.selectbox(
        "Category",
        [
            "Native Wear",
            "Wedding",
            "Corporate",
            "Luxury",
            "Streetwear",
            "Casual"
        ]
    )

    fabric = st.selectbox(
        "Fabric",
        [
            "Ankara",
            "Lace",
            "Silk",
            "Cashmere",
            "Cotton",
            "Denim"
        ]
    )

    occasion = st.selectbox(
        "Design Occasion",
        [
            "Wedding",
            "Graduation",
            "Church",
            "Party",
            "Office"
        ]
    )

    complexity = st.selectbox(
        "Complexity",
        [
            "Simple",
            "Moderate",
            "Luxury"
        ]
    )

    theme = st.selectbox(
        "Theme",
        [
            "African Royalty",
            "Modern Luxury",
            "Minimalist",
            "Futuristic",
            "Celebrity Fashion",
            "Traditional Heritage",
            "Red Carpet"
        ]
    )

    if st.button("🚀 Generate Design"):

        result = generate_design(
            gender,
            category,
            fabric,
            occasion,
            complexity,
            theme
        )

        st.session_state.saved_designs.append(result)

        st.success("Design Generated Successfully")

        st.subheader(result["Design Name"])

        st.write("### Theme")
        st.write(result["Theme"])

        st.write("### Description")
        st.write(result["Description"])

        st.write("### Fabric")
        st.write(result["Fabric"])

        st.write("### Colors")
        st.write(result["Colors"])

        st.write("### Front View")
        st.write(result["Front View"])

        st.write("### Back View")
        st.write(result["Back View"])

        st.write("### Sleeve Design")
        st.write(result["Sleeve Design"])

        st.write("### Collar Design")
        st.write(result["Collar Design"])

        st.write("### Tailor Notes")
        st.write(result["Tailor Notes"])

# ===================================
# TAB 3
# ===================================

with tab3:

    st.header("Creative Block Solver")

    if st.button("🎲 Generate Fresh Fashion Idea"):

        themes = [
            "African Futurism",
            "Royal Wedding",
            "Urban Luxury",
            "Minimalist Elegance",
            "Celebrity Red Carpet"
        ]

        fabrics = [
            "Ankara",
            "Silk",
            "Cashmere",
            "Lace"
        ]

        features = [
            "Gold embroidery",
            "Layered sleeves",
            "Luxury collar",
            "Asymmetrical cut"
        ]

        st.write("Theme:", random.choice(themes))
        st.write("Fabric:", random.choice(fabrics))
        st.write("Feature:", random.choice(features))

# ===================================
# TAB 4
# ===================================

with tab4:

    st.header("Collection Builder")

    collection_name = st.text_input("Collection Name")

    number = st.slider(
        "Number of Looks",
        1,
        10,
        5
    )

    if st.button("Generate Collection"):

        st.success(f"{collection_name} Collection")

        for i in range(number):
            st.write(f"Look {i+1}")

# ===================================
# TAB 5
# ===================================

with tab5:

    st.header("Design Library")

    if st.session_state.saved_designs:

        for design in st.session_state.saved_designs:

            st.write("###", design["Design Name"])
            st.write(design["Description"])
            st.divider()

    else:
        st.info("No saved designs yet")

# ===================================
# TAB 6
# ===================================

with tab6:

    st.header("Sketch Studio")

    design_type = st.selectbox(
        "Sketch Type",
        [
            "Luxury",
            "Wedding",
            "Native",
            "Streetwear",
            "Corporate"
        ]
    )

    if st.button("Generate Sketch Concept"):

        st.success("Sketch Concept Created")

        st.write("Front Sketch:")
        st.write("Structured premium front design.")

        st.write("Back Sketch:")
        st.write("Luxury embroidered rear panel.")

        st.write("Sleeve Sketch:")
        st.write("Layered sleeve concept.")

        st.write("Collar Sketch:")
        st.write("Modern royal collar.")

# ===================================
# TAB 7
# ===================================

with tab7:

    st.header("🤖 StyleSense Fashion Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    prompt = st.chat_input("Ask me anything about fashion...")

    if prompt:
        st.session_state.messages.append(("user", prompt))

        reply = (
            "Hello! I'm StyleSense AI. "
            "I'm still learning, but soon I'll give personalized fashion advice."
        )

        st.session_state.messages.append(("assistant", reply))

    for role, message in st.session_state.messages:
        with st.chat_message(role):
            st.write(message)