# 🐾 VetBrief

**Better information before the veterinary appointment.**

VetBrief is a lightweight tool designed to help pet owners organise relevant information before contacting a veterinary clinic.

It turns a pre-visit questionnaire into a structured veterinary brief and combines it with an appointment request.

---

## Why VetBrief?

Pet owners often describe concerns in an unstructured way:

- “He seems strange.”
- “She is eating less.”
- “He vomited yesterday.”
- “I think she is drinking more.”

All of this may be useful, but veterinary staff often need to quickly identify the most relevant facts.

VetBrief helps organise that information before the appointment.

---

## What it does

VetBrief guides the pet owner through a short intake form covering:

- basic patient information
- main reason for contacting the clinic
- onset and progression
- appetite
- water intake
- vomiting
- stool
- urination
- respiratory signs
- activity and movement
- additional observations
- known medical conditions
- medication and supplements

It then generates a structured veterinary brief for review by clinic staff.

The user can also prepare an appointment request with:

- owner contact information
- preferred date
- preferred time
- an attached veterinary brief

---

## Important

VetBrief does **not**:

- diagnose
- assess urgency
- recommend treatment
- replace professional veterinary evaluation

It only structures owner-reported information.

All information should be reviewed by veterinary staff.

---

## How the flow works

1. The pet owner completes a short pre-visit questionnaire.
2. VetBrief structures the information into a veterinary intake brief.
3. The owner selects a preferred appointment date and time.
4. The veterinary clinic can review the request and contact the owner to confirm the appointment.

---

## Technologies

- Python
- Streamlit

---

## Run locally

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run VetBrief:

```bash
python3 -m streamlit run app.py
```

---

## Future development

Possible next steps include:

- clinic-side appointment management
- secure data storage
- multilingual support
- exportable veterinary briefs
- integration with veterinary practice software
- optional local open-weight AI for structuring free-text owner reports
- veterinarian-designed intake templates
- user testing with veterinary professionals

---

## Project goal

VetBrief explores how simple digital tools can improve communication between humans caring for animals and veterinary professionals.

The long-term goal is to support clearer, more structured and more useful communication around animal health and welfare.