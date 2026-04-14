import streamlit as st
import random
import wikipedia
import string
import re
from gtts import gTTS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="CI Buddy 🤖", layout="centered")

# -----------------------------
# CSS (FULL UI FIX)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #020617 !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.main > div {
    max-width: 750px;
    margin: auto;
}

p, label, span, div {
    color: white !important;
}

input {
    color: white !important;
    background-color: #1e293b !important;
}

::placeholder {
    color: #94a3b8 !important;
}

.stButton>button {
    background-color: #22c55e;
    color: black;
    border-radius: 12px;
    padding: 8px 16px;
    font-weight: bold;
}

h1, h2, h3 {
    color: #22c55e;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGO
# -----------------------------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(r"C:\Users\SHREE\Downloads\logo.png", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------
# CLEAN TEXT (REMOVE EMOJIS + ADD PAUSES)
# -----------------------------
def clean_text_for_voice(text):
    # Remove emojis
    text = re.sub(r'[^\w\s.,!?]', '', text)

    # Add pauses
    text = text.replace("—", ". ")
    text = text.replace("-", ". ")

    # Ensure spacing after punctuation
    text = re.sub(r'([.,!?])', r'\1 ', text)

    return text

# -----------------------------
# TEXT TO SPEECH
# -----------------------------
def speak(text):
    clean_text = clean_text_for_voice(text)
    tts = gTTS(clean_text, lang='en', slow=False)
    tts.save("output.mp3")
    st.audio("output.mp3")

# -----------------------------
# PREPROCESS
# -----------------------------
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# -----------------------------
# SHORT FORMS
# -----------------------------
short_forms = {
    "ci": "computational intelligence",
    "ga": "genetic algorithm",
    "rl": "reinforcement learning",
    "nn": "neural network"
}

# -----------------------------
# ML MODEL
# -----------------------------
training_sentences = [
    "what is genetic algorithm",
    "explain reinforcement learning",
    "start quiz",
    "quiz please"
]

training_labels = ["definition","explanation","quiz","quiz"]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(training_sentences)

model = MultinomialNB()
model.fit(X, training_labels)

# -----------------------------
# RESPONSES (VOICE OPTIMIZED)
# -----------------------------
responses = {
    "genetic algorithm": "Great question. Genetic Algorithm works like evolution. Solutions improve over time.",
    
    "reinforcement learning": "Reinforcement Learning works like training a pet. Good actions are rewarded. Bad actions are penalized.",
    
    "neural network": "Neural Networks are inspired by the human brain. They learn patterns from data.",
    
    "fuzzy logic": "Fuzzy Logic deals with uncertainty. It allows partial truth instead of only true or false.",
    
    "computational intelligence": "Computational Intelligence includes neural networks, fuzzy logic, and evolutionary algorithms.",
    
    "ant colony optimization": "Ant Colony Optimization is inspired by how ants find shortest paths using pheromones.",
    
    "bee colony optimization": "Bee Colony Optimization is inspired by how honey bees search for food efficiently."
}

# -----------------------------
# WIKIPEDIA
# -----------------------------
def get_wiki_answer(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return None
        page = wikipedia.page(results[0])
        summary = wikipedia.summary(page.title, sentences=2)
        return f"{summary}"
    except:
        return None

# -----------------------------
# QUIZ QUESTIONS
# -----------------------------
quiz_questions = [
    {"question": "Which algorithm is based on natural selection?",
     "options": ["A. Genetic Algorithm", "B. KNN", "C. SVM"],
     "answer": "A"},

    {"question": "RL stands for?",
     "options": ["A. Random Learning", "B. Reinforcement Learning", "C. Regression Learning"],
     "answer": "B"},

    {"question": "Which technique handles uncertainty?",
     "options": ["A. Neural Network", "B. Fuzzy Logic", "C. GA"],
     "answer": "B"},

    {"question": "Which is inspired by the human brain?",
     "options": ["A. Neural Network", "B. GA", "C. Fuzzy Logic"],
     "answer": "A"},

    {"question": "Which uses rewards and penalties?",
     "options": ["A. RL", "B. GA", "C. KNN"],
     "answer": "A"}
]

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "history" not in st.session_state:
    st.session_state.history = []

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("📜 Chat History")
    for role, msg in st.session_state.history:
        if role == "You":
            st.write(f"🧑 {msg}")

# -----------------------------
# HOME
# -----------------------------
if st.session_state.page == "home":
    st.title("🤖 Welcome to CI Buddy")
    st.success("✨ Your Smart Learning Assistant")

    if st.button("🚀 Start Chat"):
        st.session_state.page = "chat"
        st.rerun()

    if st.button("🧠 Go to Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

# -----------------------------
# CHAT
# -----------------------------
elif st.session_state.page == "chat":
    st.title("💬 Chat with CI Buddy")

    st.info("💡 Try: GA, RL, Neural Network, Bee Colony Optimization")

    user_input = st.text_input("Ask your question...")

    if st.button("Send") and user_input:
        user_input = preprocess(user_input)

        if user_input in short_forms:
            user_input = short_forms[user_input]

        response = None

        for key in responses:
            words = key.split()
            if all(word in user_input for word in words):
                response = responses[key]
                break

        if not response:
            response = get_wiki_answer(user_input)

        if not response:
            response = "Hmm. Try asking about computational intelligence topics."

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("CI Buddy", response))

    # Latest first
    for i, (role, msg) in enumerate(reversed(st.session_state.history)):
        st.write(f"**{role}:** {msg}")

        if role == "CI Buddy":
            if st.button(f"🔊 Speak {i}"):
                speak(msg)

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

# -----------------------------
# QUIZ
# -----------------------------
elif st.session_state.page == "quiz":
    st.title("🧠 Quiz Time!")

    if st.session_state.q_index < len(quiz_questions):
        q = quiz_questions[st.session_state.q_index]

        st.subheader(q["question"])
        option = st.radio("Choose:", q["options"], index=None)

        if st.button("Submit"):
            if option is None:
                st.warning("Select an option!")
            elif option[0] == q["answer"]:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct: {q['answer']}")

            st.session_state.q_index += 1
            st.rerun()

    else:
        st.success(f"Final Score: {st.session_state.score}/{len(quiz_questions)}")

        if st.button("Restart"):
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

# -----------------------------
# EXIT
# -----------------------------
if st.button("❌ Exit"):
    st.session_state.page = "exit"
    st.rerun()

if st.session_state.page == "exit":
    st.title("Thank You!")
    st.success("Thanks for using CI Buddy.")