# 🐾 VetBrief

**Better information before the veterinary appointment.**

VetBrief is a lightweight veterinary intake and appointment request tool designed to help pet owners organise relevant information before contacting a veterinary clinic.

It combines a structured pre-visit questionnaire with open-weight AI assistance for free-text owner observations.

The goal is simple: help veterinary staff receive clearer, more structured information before reviewing an appointment request.

---

## Why VetBrief?

Pet owners often describe concerns in an unstructured way:

- “He seems strange.”
- “She is eating less.”
- “He vomited yesterday.”
- “I think she is drinking more.”
- “She has been hiding and does not want to be touched.”

All of this information may matter, but veterinary staff often need to quickly identify the most relevant facts.

VetBrief helps organise that information before the appointment.

---

## What VetBrief does

VetBrief guides the pet owner through a short intake form covering:

- basic patient information
- main reason for contacting the clinic
- onset and duration
- progression
- appetite
- water intake
- vomiting
- stool
- urination
- respiratory signs
- activity level
- movement
- additional observations
- known medical conditions
- medication and supplements

The application then generates a structured veterinary brief for review by clinic staff.

---

## Open-weight AI assistance

VetBrief also allows pet owners to describe additional observations in their own words.

An open-weight language model is used to transform this free-text description into a concise, factual veterinary intake note.

For example:

**Owner description**

> She has been hiding under the bed since yesterday. She normally sleeps on the sofa. She did not eat breakfast this morning and walked away when I tried to touch her.

**AI-structured note**

- Hiding under the bed since yesterday (normally sleeps on the sofa)
- Did not eat breakfast this morning
- Walked away when approached for touch

The AI is intentionally limited.

It does **not**:

- diagnose diseases
- assess urgency
- recommend treatment
- infer medical conditions
- infer emotions or causes
- replace veterinary judgement

Its role is only to improve the structure and clarity of owner-reported information.

Veterinary staff should always review the generated note.

---

## Why open-weight AI?

VetBrief explores a narrow and responsible use of generative AI in animal health communication.

Instead of asking an AI system to make clinical decisions, the model is used for a much more limited task:

**turning unstructured owner observations into clearer factual notes.**

This keeps the human veterinarian at the centre of clinical decision-making.

The current version uses an open-weight language model through Hugging Face Inference Providers.

Using an open-weight model also makes it possible to explore future versions that could run locally, giving veterinary clinics greater control over privacy, deployment and model choice.

---

## Appointment request

After creating the veterinary brief, the owner can prepare an appointment request including:

- owner name
- phone number
- optional email
- preferred appointment date
- preferred time
- optional message for the clinic
- attached veterinary brief

The veterinary clinic can then review the information and contact the owner by phone to confirm the appointment.

---

## How the flow works

1. The pet owner completes a short pre-visit questionnaire.
2. Structured information is collected about the animal and current concern.
3. Free-text observations can be processed by an open-weight language model.
4. VetBrief creates a concise veterinary intake brief.
5. The owner selects a preferred appointment date and time.
6. The veterinary brief is attached to the appointment request.
7. The clinic can review the request and contact the owner to confirm the appointment.

---

## Responsible AI design

VetBrief follows a deliberately conservative approach to AI.

The model is not used to provide veterinary advice.

AI output is restricted to the organisation and rewriting of information already provided by the owner.

The application explicitly avoids:

- diagnosis
- treatment recommendations
- urgency classification
- clinical decision-making
- unsupported assumptions

This separation is intentional:

**AI structures the information. Veterinary professionals interpret it.**

---

## Technologies

- Python
- Streamlit
- Requests
- Hugging Face Inference Providers
- Open-weight language model

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

Create:

```text
.streamlit/secrets.toml
```

and add your Hugging Face token:

```toml
HF_TOKEN = "your_hugging_face_token"
```

Run VetBrief:

```bash
python3 -m streamlit run app.py
```

---

## Privacy

The Hugging Face token is stored locally in:

```text
.streamlit/secrets.toml
```

This file is excluded from Git through `.gitignore` and should never be committed to a public repository.

---

## Current limitations

VetBrief is an early-stage application.

The current version does not:

- send appointments to a real veterinary clinic
- connect to veterinary practice management software
- store medical records
- provide emergency triage
- make clinical recommendations

The appointment workflow demonstrates how structured intake information could be attached to a future clinic booking system.

---

## Future development

Possible next steps include:

- veterinarian-designed intake templates
- user testing with veterinary professionals
- clinic-side appointment management
- secure data storage
- multilingual support
- downloadable veterinary briefs
- integration with veterinary practice software
- local AI inference for greater privacy
- model comparison and evaluation
- improved extraction of relevant observations
- species-specific intake forms
- validation of the AI-generated summaries with veterinary professionals

---

## Project goal

VetBrief explores how simple digital tools and carefully scoped AI can improve communication between humans caring for animals and veterinary professionals.

The long-term goal is to support clearer, more structured and more useful communication around animal health and welfare while keeping clinical judgement in the hands of veterinary professionals.

---

## Repository

GitHub:

https://github.com/Maribele/vetbrief