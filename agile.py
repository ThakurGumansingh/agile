
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
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "bookmarked" not in st.session_state:
    st.session_state.bookmarked = set()

q_index = st.session_state.q_index
q = questions[q_index]

st.title(f"Question {q_index + 1} / {len(questions)}")
st.write(q["question"])

# Bookmark / Attempt Later
if st.button("🔖 Bookmark / Attempt Later"):
    st.session_state.bookmarked.add(q_index)
    st.success("Question bookmarked for later.")

# Jump to question number
jump_to = st.number_input("Jump to question number:", min_value=1, max_value=len(questions), step=1)
if st.button("🚀 Jump"):
    st.session_state.q_index = int(jump_to) - 1
    st.session_state.submitted = False
    st.rerun()

# Show options based on question type
user_answer = None
if q["type"] == "single":
    user_answer = st.radio("Choose one:", q["options"], key=f"q{q_index}_single")
elif q["type"] == "multi":
    user_answer = []
    for option in q["options"]:
        if st.checkbox(option, key=f"{q_index}_{option}"):
            user_answer.append(option)
elif q["type"] == "blank":
    user_answer = st.text_input("Enter your answer:", key=f"q{q_index}_input")

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
    st.session_state.answers[q_index] = user_answer
    if is_correct(user_answer, correct, q["type"]):
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error("❌ Incorrect.")
        st.info(f"Correct Answer: {correct}")

# Navigation buttons
col1, col2 = st.columns([1, 1])

with col1:
    if q_index > 0:
        if st.button("⬅️ Go Back"):
            st.session_state.q_index -= 1
            st.session_state.submitted = False
            st.rerun()

with col2:
    if st.session_state.submitted:
        if q_index < len(questions) - 1:
            if st.button("➡️ Next Question"):
                st.session_state.q_index += 1
                st.session_state.submitted = False
                st.rerun()
        else:
            st.success("🎉 Quiz Completed!")
            st.write(f"Your Score: **{st.session_state.score} / {len(questions)}**")
            if st.session_state.bookmarked:
                st.subheader("📌 Review Bookmarked Questions")
                bookmarked_list = sorted(list(st.session_state.bookmarked))
                for i in bookmarked_list:
                    if st.button(f"Review Question {i + 1}", key=f"bmark_{i}"):
                        st.session_state.q_index = i
                        st.session_state.submitted = False
                        st.rerun()
            if st.button("🔁 Restart"):
                for key in list(st.session_state.keys()):
                    if key.startswith("q") or key in ["score", "submitted", "q_index", "answers", "bookmarked"]:
                        del st.session_state[key]
                st.rerun()
