import streamlit as st
import pandas as pd
import time
import random

# Load your CSV of 1000+ questions (cleaned and deduplicated)
@st.cache_data
def load_questions():
    df = pd.read_csv("quiz_questions_unique.csv")
    return df.sample(frac=1, random_state=42).reset_index(drop=True)

# App state initialization
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False

questions = load_questions()
total_questions = len(questions)
question = questions.iloc[st.session_state.question_index]

st.header("🎯 Bollywood & Cricket Quiz")
st.markdown(f"**Q{st.session_state.question_index + 1}:** {question['question']}")

options = [question[f"option{i}"] for i in range(1, 5)]
random.shuffle(options)
selected = st.radio("Choose an answer:", options, key=f"q{st.session_state.question_index}")

if st.button("Submit"):
    st.session_state.show_feedback = True
    if selected == question['answer']:
        st.success("✅ Correct Answer!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Wrong! The correct answer is: **{question['answer']}**")

    # Automatically go to next question after delay
    time.sleep(5)
    st.session_state.question_index += 1
    if st.session_state.question_index >= total_questions:
        st.balloons()
        st.write(f"🏁 Quiz Completed! Your final score is **{st.session_state.score} / {total_questions}**")
        st.stop()
    else:
        st.rerun()


def emoji_memory_game():
    st.subheader("🧠 Emoji Memory Game")
    st.write("Find all the matching pairs! Click two cards to flip them. Try to win in as few moves as possible.")

    # List of emoji pairs
    emojis = ["🐶", "🐱", "🦁", "🐼", "🐸", "🐵", "🐰", "🦊"]
    cards = emojis * 2  # 8 pairs = 16 cards
    random.seed(42)  # For consistent shuffling per session
    if "memory_cards" not in st.session_state:
        random.shuffle(cards)
        st.session_state.memory_cards = cards
        st.session_state.flipped = [False] * 16
        st.session_state.matched = [False] * 16
        st.session_state.moves = 0
        st.session_state.last_pick = None
        st.session_state.game_over = False

    cols = st.columns(4)
    for i in range(16):
        with cols[i % 4]:
            if st.session_state.flipped[i] or st.session_state.matched[i]:
                st.button(st.session_state.memory_cards[i], key=f"card_{i}", disabled=True)
            else:
                if st.button("❓", key=f"card_{i}"):
                    st.session_state.flipped[i] = True
                    if st.session_state.last_pick is None:
                        st.session_state.last_pick = i
                    else:
                        st.session_state.moves += 1
                        j = st.session_state.last_pick
                        if st.session_state.memory_cards[i] == st.session_state.memory_cards[j]:
                            st.session_state.matched[i] = True
                            st.session_state.matched[j] = True
                        else:
                            # Briefly show both, then flip back
                            st.experimental_rerun()
                            time.sleep(0.7)
                            st.session_state.flipped[i] = False
                            st.session_state.flipped[j] = False
                        st.session_state.last_pick = None
                    st.experimental_rerun()

    if all(st.session_state.matched):
        st.success(f"🎉 You won in {st.session_state.moves} moves!")
        st.balloons()
        if st.button("Play Again"):
            for key in ["memory_cards", "flipped", "matched", "moves", "last_pick", "game_over"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()