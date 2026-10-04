import streamlit as st
import requests
from datetime import date


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="VetBrief",
    page_icon="🐾",
    layout="centered"
)


# --------------------------------------------------
# AI CONFIGURATION
# --------------------------------------------------

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

HF_MODEL = "openai/gpt-oss-120b:fastest"


def ai_structure_notes(text):

    if not text.strip():
        return ""

    try:
        token = st.secrets["HF_TOKEN"]

    except Exception:
        st.error(
            "Hugging Face token not found. "
            "Check .streamlit/secrets.toml"
        )
        return ""

    messages = [
        {
            "role": "system",
            "content": (
                "You assist veterinary clinic staff by transforming "
                "pet-owner observations into concise factual intake notes. "
                "Do NOT diagnose. "
                "Do NOT assess urgency. "
                "Do NOT recommend treatment. "
                "Do NOT infer diseases, emotions, pain, or causes. "
                "Do NOT invent information. "
                "Only use facts explicitly provided by the owner. "
                "Rewrite the information as a concise professional "
                "veterinary intake note using short bullet points."
            ),
        },
        {
            "role": "user",
            "content": (
                "Transform this owner report into a concise factual "
                "veterinary intake note:\n\n"
                + text
            ),
        },
    ]

    try:

        response = requests.post(
            HF_API_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "model": HF_MODEL,
                "messages": messages,
                "max_tokens": 180,
                "temperature": 0.1,
            },
            timeout=60,
        )

        if response.status_code != 200:

            st.error(
                f"AI request failed "
                f"({response.status_code}): "
                f"{response.text[:400]}"
            )

            return ""

        data = response.json()

        ai_text = (
            data["choices"][0]["message"]["content"]
            .strip()
        )

        return ai_text

    except requests.exceptions.Timeout:

        st.error(
            "The AI request timed out."
        )

        return ""

    except Exception as error:

        st.error(
            f"AI request failed: {error}"
        )

        return ""


# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 2rem;
        border-radius: 22px;

        background: linear-gradient(
            135deg,
            rgba(255, 240, 245, 0.95),
            rgba(240, 247, 255, 0.95)
        );

        margin-bottom: 1.5rem;

        border:
            1px solid
            rgba(120, 120, 120, 0.15);
    }

    .hero-title {
        font-size: 2.7rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        opacity: 0.85;
    }

    .small-label {
        font-size: 0.85rem;
        opacity: 0.65;
        margin-top: 0.6rem;
    }

    .footer {
        text-align: center;
        opacity: 0.65;
        font-size: 0.85rem;
        margin-top: 2.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """<div class="hero">
<div class="hero-title">🐾 VetBrief</div>
<div class="hero-subtitle">Better information before the veterinary appointment.</div>
<div class="small-label">Structured veterinary intake and appointment request.</div>
</div>""",
    unsafe_allow_html=True
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "brief" not in st.session_state:
    st.session_state.brief = None

if "appointment_ready" not in st.session_state:
    st.session_state.appointment_ready = False

if "appointment_data" not in st.session_state:
    st.session_state.appointment_data = None


# --------------------------------------------------
# INTAKE FORM
# --------------------------------------------------

with st.form(
    "veterinary_intake_form",
    enter_to_submit=False
):

    # --------------------------------------------------
    # STEP 1
    # --------------------------------------------------

    st.header(
        "1 · Pet information"
    )

    st.caption(
        "Tell us a little about the animal "
        "before describing the current concern."
    )


    col1, col2 = st.columns(2)


    with col1:

        pet_name = st.text_input(
            "Pet name"
        )

        species = st.selectbox(
            "Species",
            [
                "Cat",
                "Dog",
                "Rabbit",
                "Bird",
                "Other"
            ]
        )

        age = st.text_input(
            "Age",
            placeholder="Example: 8 years"
        )


    with col2:

        sex = st.selectbox(
            "Sex",
            [
                "Female",
                "Male",
                "Unknown"
            ]
        )

        neutered = st.selectbox(
            "Neutered / spayed",
            [
                "Yes",
                "No",
                "Unknown"
            ]
        )

        weight = st.text_input(
            "Weight",
            placeholder="Optional"
        )


    existing_conditions = st.text_area(
        "Known medical conditions",
        placeholder=(
            "Example: chronic kidney disease, allergies. "
            "Leave blank if none are known."
        )
    )


    medication = st.text_area(
        "Current medication or supplements",
        placeholder="Leave blank if none."
    )


    st.divider()


    # --------------------------------------------------
    # STEP 2
    # --------------------------------------------------

    st.header(
        "2 · What has changed?"
    )

    st.caption(
        "Use the fields below to describe "
        "what you have directly noticed."
    )


    main_concern = st.text_input(
        "Main reason for contacting the clinic",
        placeholder=(
            "Example: vomiting, itching, "
            "reduced appetite..."
        )
    )


    duration = st.text_input(
        "When did you first notice the problem?",
        placeholder=(
            "Example: yesterday, "
            "3 days ago, about 2 weeks ago"
        )
    )


    progression = st.selectbox(
        "Since it started, the problem seems to be",
        [
            "Not sure",
            "About the same",
            "Improving",
            "Getting worse",
            "Coming and going"
        ]
    )


    st.subheader(
        "Eating and drinking"
    )


    col3, col4 = st.columns(2)


    with col3:

        appetite = st.selectbox(
            "Appetite",
            [
                "Not sure",
                "Normal",
                "Eating less",
                "Not eating",
                "Eating more"
            ]
        )


    with col4:

        water_intake = st.selectbox(
            "Water intake",
            [
                "Not sure",
                "Normal",
                "Drinking less",
                "Drinking more",
                "Not drinking"
            ]
        )


    st.subheader(
        "Digestive and elimination"
    )


    col5, col6 = st.columns(2)


    with col5:

        vomiting = st.selectbox(
            "Vomiting",
            [
                "Not observed",
                "Once",
                "More than once",
                "Not sure"
            ]
        )


        stool = st.selectbox(
            "Stool",
            [
                "Not sure",
                "Normal",
                "Diarrhoea",
                "Constipation",
                "No stool observed",
                "Other change"
            ]
        )


    with col6:

        urination = st.selectbox(
            "Urination",
            [
                "Not sure",
                "Normal",
                "More frequent",
                "Less frequent",
                "Straining",
                "No urine observed",
                "Other change"
            ]
        )


        respiratory = st.selectbox(
            "Breathing / respiratory signs",
            [
                "None observed",
                "Coughing",
                "Sneezing",
                "Breathing differently",
                "Not sure"
            ]
        )


    st.subheader(
        "Behaviour and movement"
    )


    col7, col8 = st.columns(2)


    with col7:

        activity = st.selectbox(
            "Activity level",
            [
                "Not sure",
                "Normal",
                "Less active",
                "More active",
                "Hiding more than usual"
            ]
        )


    with col8:

        movement = st.selectbox(
            "Movement",
            [
                "Not sure",
                "Normal",
                "Limping",
                "Moving less",
                "Difficulty jumping",
                "Other change"
            ]
        )


    st.subheader(
        "Other observations"
    )


    selected_observations = st.multiselect(
        "Have you noticed any of these?",
        [
            "Scratching",
            "Repeated licking",
            "Hair loss",
            "Skin redness",
            "Swelling",
            "Discharge from eyes",
            "Discharge from nose",
            "Change in vocalisation",
            "Change in sleep",
            "Change in social behaviour",
            "Possible injury",
            "Possible toxin exposure",
            "Possible foreign-body ingestion"
        ]
    )


    owner_description = st.text_area(
        "Anything else you have noticed",
        height=150,
        placeholder=(
            "Example: She started hiding under "
            "the bed yesterday and does not "
            "want to be touched."
        )
    )


    st.caption(
        "Free-text observations can be structured "
        "with an open-weight AI model."
    )


    create_brief_button = (
        st.form_submit_button(
            "Create veterinary brief",
            type="primary",
            use_container_width=True
        )
    )


# --------------------------------------------------
# CREATE BRIEF
# --------------------------------------------------

def create_brief():

    observations = []


    if appetite != "Not sure":

        observations.append(
            f"Appetite: {appetite}"
        )


    if water_intake != "Not sure":

        observations.append(
            f"Water intake: {water_intake}"
        )


    if vomiting not in [
        "Not observed",
        "Not sure"
    ]:

        observations.append(
            f"Vomiting: {vomiting}"
        )


    if stool != "Not sure":

        observations.append(
            f"Stool: {stool}"
        )


    if urination != "Not sure":

        observations.append(
            f"Urination: {urination}"
        )


    if respiratory not in [
        "None observed",
        "Not sure"
    ]:

        observations.append(
            f"Respiratory signs: {respiratory}"
        )


    if activity != "Not sure":

        observations.append(
            f"Activity: {activity}"
        )


    if movement != "Not sure":

        observations.append(
            f"Movement: {movement}"
        )


    for item in selected_observations:

        observations.append(
            item
        )


    missing_information = []


    if appetite == "Not sure":

        missing_information.append(
            "Appetite"
        )


    if water_intake == "Not sure":

        missing_information.append(
            "Water intake"
        )


    if stool == "Not sure":

        missing_information.append(
            "Stool"
        )


    if urination == "Not sure":

        missing_information.append(
            "Urination"
        )


    if not age.strip():

        missing_information.append(
            "Age"
        )


    if not weight.strip():

        missing_information.append(
            "Weight"
        )


    ai_summary = ""

    if owner_description.strip():

        ai_summary = ai_structure_notes(
            owner_description
        )


    return {

        "pet_name":
            pet_name.strip()
            or "Not provided",

        "species":
            species,

        "age":
            age.strip()
            or "Not provided",

        "sex":
            sex,

        "neutered":
            neutered,

        "weight":
            weight.strip()
            or "Not provided",

        "conditions":
            existing_conditions.strip()
            or "None reported",

        "medication":
            medication.strip()
            or "None reported",

        "main_concern":
            main_concern.strip()
            or "Not provided",

        "duration":
            duration.strip()
            or "Not provided",

        "progression":
            progression,

        "observations":
            observations,

        "owner_description":
            owner_description.strip(),

        "ai_summary":
            ai_summary,

        "missing_information":
            missing_information
    }


# --------------------------------------------------
# CREATE BRIEF BUTTON
# --------------------------------------------------

if create_brief_button:

    if not pet_name.strip():

        st.warning(
            "Please enter the pet's name."
        )


    elif not main_concern.strip():

        st.warning(
            "Please enter the main reason "
            "for contacting the clinic."
        )


    else:

        with st.spinner(
            "Creating veterinary brief..."
        ):

            st.session_state.brief = (
                create_brief()
            )

        st.session_state.appointment_ready = False

        st.session_state.appointment_data = None


brief = st.session_state.brief


# --------------------------------------------------
# STEP 3 — VETERINARY BRIEF
# --------------------------------------------------

if brief:

    st.divider()

    st.header(
        "3 · Veterinary brief"
    )

    st.caption(
        "Structured information "
        "for veterinary staff review."
    )


    with st.container(
        border=True
    ):

        st.markdown(
            "### 🐾 Patient"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                f"**Name:** "
                f"{brief['pet_name']}"
            )

            st.write(
                f"**Species:** "
                f"{brief['species']}"
            )

            st.write(
                f"**Age:** "
                f"{brief['age']}"
            )


        with col2:

            st.write(
                f"**Sex:** "
                f"{brief['sex']}"
            )

            st.write(
                f"**Neutered / spayed:** "
                f"{brief['neutered']}"
            )

            st.write(
                f"**Weight:** "
                f"{brief['weight']}"
            )


        st.divider()


        st.markdown(
            "### 🩺 Current concern"
        )


        st.write(
            f"**Main concern:** "
            f"{brief['main_concern']}"
        )

        st.write(
            f"**Onset / duration:** "
            f"{brief['duration']}"
        )

        st.write(
            f"**Progression:** "
            f"{brief['progression']}"
        )


        st.divider()


        st.markdown(
            "### 👀 Reported observations"
        )


        if brief["observations"]:

            for item in brief[
                "observations"
            ]:

                st.write(
                    f"• {item}"
                )

        else:

            st.write(
                "No additional structured "
                "observations reported."
            )


        if brief["owner_description"]:

            st.markdown(
                "### 📝 Owner description"
            )

            st.write(
                brief[
                    "owner_description"
                ]
            )


        if brief["ai_summary"]:

            st.markdown(
                "### 🤖 AI-structured note"
            )

            st.write(
                brief[
                    "ai_summary"
                ]
            )

            st.caption(
                "Generated using an open-weight "
                "language model. Veterinary staff "
                "should review the result."
            )


        st.divider()


        st.markdown(
            "### 📋 Relevant background"
        )


        st.write(
            f"**Known medical conditions:** "
            f"{brief['conditions']}"
        )

        st.write(
            f"**Medication / supplements:** "
            f"{brief['medication']}"
        )


        if brief[
            "missing_information"
        ]:

            st.divider()

            st.markdown(
                "### ❓ Information still missing"
            )

            for item in brief[
                "missing_information"
            ]:

                st.write(
                    f"• {item}"
                )


    st.caption(
        "VetBrief structures owner-reported "
        "information only. All information "
        "should be reviewed by veterinary staff."
    )


    # --------------------------------------------------
    # STEP 4 — APPOINTMENT
    # --------------------------------------------------

    st.divider()

    st.header(
        "4 · Request an appointment"
    )

    st.caption(
        "Choose a preferred appointment "
        "time and attach the brief."
    )


    with st.form(
        "appointment_form",
        enter_to_submit=False
    ):

        owner_name = st.text_input(
            "Owner name"
        )


        phone = st.text_input(
            "Phone number"
        )


        email = st.text_input(
            "Email",
            placeholder="Optional"
        )


        col9, col10 = st.columns(2)


        with col9:

            preferred_date = st.date_input(
                "Preferred date",
                min_value=date.today()
            )


        with col10:

            preferred_time = st.selectbox(
                "Preferred time",
                [
                    "Morning",
                    "Afternoon",
                    "No preference"
                ]
            )


        additional_notes = st.text_area(
            "Message for the clinic",
            placeholder="Optional"
        )


        submit_request = (
            st.form_submit_button(
                "Send appointment request",
                type="primary",
                use_container_width=True
            )
        )


    if submit_request:

        if not owner_name.strip():

            st.warning(
                "Please enter the owner's name."
            )


        elif not phone.strip():

            st.warning(
                "Please enter a phone number."
            )


        else:

            st.session_state.appointment_ready = True

            st.session_state.appointment_data = {

                "owner_name":
                    owner_name.strip(),

                "phone":
                    phone.strip(),

                "email":
                    email.strip(),

                "preferred_date":
                    preferred_date,

                "preferred_time":
                    preferred_time,

                "additional_notes":
                    additional_notes.strip()
            }


# --------------------------------------------------
# FINAL APPOINTMENT REQUEST
# --------------------------------------------------

if (
    st.session_state.appointment_ready
    and brief
    and st.session_state.appointment_data
):

    appointment = (
        st.session_state.appointment_data
    )


    st.divider()


    st.success(
        "Your appointment request has been sent."
    )


    st.header(
        "Appointment request"
    )


    with st.container(
        border=True
    ):

        st.markdown(
            "### Appointment preferences"
        )


        st.write(
            f"**Owner:** "
            f"{appointment['owner_name']}"
        )


        st.write(
            f"**Phone:** "
            f"{appointment['phone']}"
        )


        if appointment[
            "email"
        ]:

            st.write(
                f"**Email:** "
                f"{appointment['email']}"
            )


        st.write(
            f"**Preferred date:** "
            f"{appointment['preferred_date']}"
        )


        st.write(
            f"**Preferred time:** "
            f"{appointment['preferred_time']}"
        )


        if appointment[
            "additional_notes"
        ]:

            st.write(
                f"**Message:** "
                f"{appointment['additional_notes']}"
            )


        st.divider()


        st.markdown(
            "### Attached veterinary brief"
        )


        st.write(
            f"**Patient:** "
            f"{brief['pet_name']} "
            f"({brief['species']})"
        )


        st.write(
            f"**Age:** "
            f"{brief['age']}"
        )


        st.write(
            f"**Sex:** "
            f"{brief['sex']}"
        )


        st.write(
            f"**Main concern:** "
            f"{brief['main_concern']}"
        )


        st.write(
            f"**Duration:** "
            f"{brief['duration']}"
        )


        st.write(
            f"**Progression:** "
            f"{brief['progression']}"
        )


        st.markdown(
            "**Reported observations:**"
        )


        if brief[
            "observations"
        ]:

            for item in brief[
                "observations"
            ]:

                st.write(
                    f"• {item}"
                )


        if brief[
            "ai_summary"
        ]:

            st.markdown(
                "**AI-structured note:**"
            )

            st.write(
                brief[
                    "ai_summary"
                ]
            )


        st.markdown(
            "**Medical background:**"
        )


        st.write(
            f"Known conditions: "
            f"{brief['conditions']}"
        )


        st.write(
            f"Medication / supplements: "
            f"{brief['medication']}"
        )


    st.info(
        "The veterinary clinic will review "
        "your request and send a message "
        "to your phone to confirm the appointment."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">

        🐾 VetBrief<br>

        Better information.
        Better conversations.

    </div>
    """,
    unsafe_allow_html=True
)