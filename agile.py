
import streamlit as st
import json

# Load questions from JSON
@st.cache_data
def load_questions():
    with open("agile.json", "r") as f:
        return json.load(f)

questions = load_questions()

# Initialize session state
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False

q = questions[st.session_state.q_index]
st.title(f"Question {st.session_state.q_index + 1} / {len(questions)}")
st.write(q["question"])

user_answer = None
if q["type"] == "single":
    user_answer = st.radio("Choose one:", q["options"], key=f"q{st.session_state.q_index}")
elif q["type"] == "multi":
    user_answer = []
    for option in q["options"]:
        if st.checkbox(option, key=f"{st.session_state.q_index}_{option}"):
            user_answer.append(option)
elif q["type"] == "blank":
    user_answer = st.text_input("Enter your answer:", key=f"q{st.session_state.q_index}")

def is_correct(user, correct, qtype):
    if qtype == "single":
        return user == correct
    elif qtype == "multi":
        return set(user) == set(correct)
    elif qtype == "blank":
        return user.strip().lower() == correct.strip().lower()
    return False

if st.button("Submit Answer", disabled=st.session_state.submitted):
    st.session_state.submitted = True
    correct = q["correct"] if q["type"] != "blank" else q["answer"]
    if is_correct(user_answer, correct, q["type"]):
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error("❌ Incorrect.")
        st.info(f"Correct Answer: {correct}")

if st.session_state.submitted:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("Next Question"):
            st.session_state.q_index += 1
            st.session_state.submitted = False
    else:
        st.success("🎉 Quiz Completed!")
        st.write(f"Your Score: **{st.session_state.score} / {len(questions)}**")
        if st.button("Restart"):
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.submitted = False
