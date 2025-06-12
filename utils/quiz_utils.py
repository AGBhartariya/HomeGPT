import streamlit as st
import pandas as pd
import time
import random


def simon_says_game():
    st.subheader("🎨 Simon Says (Color Sequence Game)")
    st.write("Repeat the color sequence. Each round, a new color is added. How long can you go?")

    colors = ["🟥 Red", "🟦 Blue", "🟩 Green", "🟨 Yellow"]
    if "simon_sequence" not in st.session_state:
        st.session_state.simon_sequence = [random.choice(colors) for _ in range(2)]
        st.session_state.simon_user_input = []
        st.session_state.simon_round = 1
        st.session_state.simon_game_over = False

    if not st.session_state.simon_game_over:
        st.markdown(f"**Round {st.session_state.simon_round}**")
        st.write("Simon says:")
        st.write(" ➡️ " + " ".join(st.session_state.simon_sequence))
        st.info("Memorize the sequence, then repeat it below.")
        user_input = st.multiselect(
            "Repeat the color sequence in order:",
            options=colors,
            default=[],
            key=f"simon_input_{st.session_state.simon_round}"
        )
        if st.button("Submit Sequence", key=f"simon_submit_{st.session_state.simon_round}"):
            if user_input == st.session_state.simon_sequence:
                st.success("✅ Correct! Next round...")
                st.session_state.simon_sequence.append(random.choice(colors))
                st.session_state.simon_round += 1
                st.rerun()
            else:
                st.error("❌ Wrong sequence! Game Over.")
                st.session_state.simon_game_over = True
    else:
        st.warning(f"Game Over! You reached round {st.session_state.simon_round}.")
        if st.button("Play Again", key="simon_restart"):
            for k in ["simon_sequence", "simon_user_input", "simon_round", "simon_game_over"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

def word_scramble_game():
    st.subheader("🔤 Word Scramble")
    st.write("Unscramble the word! Can you guess it?")

    word_list = [
    # Family & Relationships
    "mother", "father", "sister", "brother", "grandmother", "grandfather", "aunt", "uncle", "cousin", "niece", "nephew",
    "son", "daughter", "wife", "husband", "parent", "child", "baby", "family", "relative",
    # Home & Rooms
    "house", "home", "room", "kitchen", "bedroom", "bathroom", "garden", "balcony", "window", "door", "roof", "floor", "wall", "ceiling", "stairs",
    # Furniture & Objects
    "table", "chair", "sofa", "bed", "pillow", "blanket", "sheet", "lamp", "clock", "mirror", "cupboard", "drawer", "shelf", "desk", "carpet",
    # Food & Meals
    "breakfast", "lunch", "dinner", "snack", "fruit", "vegetable", "rice", "bread", "milk", "water", "juice", "tea", "coffee", "sugar", "salt",
    "spoon", "fork", "knife", "plate", "bowl", "glass", "bottle", "pan", "pot", "stove", "oven",
    # Clothes
    "shirt", "pants", "dress", "skirt", "socks", "shoes", "slippers", "jacket", "coat", "sweater", "scarf", "gloves", "hat", "cap", "belt",
    # Daily Activities
    "sleep", "wake", "eat", "drink", "cook", "clean", "wash", "iron", "read", "write", "draw", "paint", "sing", "dance", "play", "study", "work",
    # School & Learning
    "school", "teacher", "student", "class", "lesson", "book", "pencil", "pen", "eraser", "bag", "notebook", "paper", "board", "chalk", "exam",
    # Feelings & Emotions
    "happy", "sad", "angry", "excited", "bored", "tired", "scared", "brave", "proud", "kind", "funny", "friendly", "quiet", "loud", "calm",
    # Nature & Outdoors
    "tree", "flower", "grass", "river", "mountain", "hill", "beach", "lake", "park", "cloud", "rain", "sun", "moon", "star", "wind",
    # Animals & Pets
    "dog", "cat", "bird", "fish", "rabbit", "cow", "goat", "sheep", "horse", "duck", "hen", "chicken", "frog", "lion", "tiger",
    # Colors
    "red", "blue", "green", "yellow", "orange", "pink", "purple", "brown", "black", "white", "grey", "gold", "silver", "violet", "indigo",
    # Body & Health
    "head", "face", "eye", "ear", "nose", "mouth", "teeth", "tongue", "hand", "leg", "foot", "arm", "hair", "skin", "heart",
    # Transportation
    "car", "bus", "train", "plane", "boat", "bicycle", "motorcycle", "truck", "auto", "rickshaw", "taxi", "scooter", "ship", "van", "ambulance",
    # Festivals & Celebrations
    "birthday", "party", "cake", "gift", "balloon", "festival", "holiday", "wedding", "anniversary", "fireworks", "music", "dance", "song", "game", "prize"
]

    if "scramble_word" not in st.session_state or st.session_state.get("scramble_new", False):
        word = random.choice(word_list)
        scrambled = "".join(random.sample(word, len(word)))
        st.session_state.scramble_word = word
        st.session_state.scrambled = scrambled
        st.session_state.scramble_attempts = 0
        st.session_state.scramble_new = False

    st.write(f"Scrambled word: **{st.session_state.scrambled}**")
    guess = st.text_input("Your guess:", key="scramble_guess")
    if st.button("Submit Guess", key="scramble_submit"):
        st.session_state.scramble_attempts += 1
        if guess.lower() == st.session_state.scramble_word:
            st.success(f"🎉 Correct! The word was '{st.session_state.scramble_word}'. Attempts: {st.session_state.scramble_attempts}")
            if st.button("Play Again", key="scramble_restart"):
                st.session_state.scramble_new = True
                st.rerun()
        else:
            st.error("❌ Incorrect. Try again!")


def math_challenge_game():
    st.subheader("➕ Simple Math Challenge")
    st.write("Solve as many math questions as you can!")

    if "math_num1" not in st.session_state or st.session_state.get("math_new", False):
        st.session_state.math_num1 = random.randint(1, 20)
        st.session_state.math_num2 = random.randint(1, 20)
        st.session_state.math_op = random.choice(["+", "-", "*"])
        st.session_state.math_score = st.session_state.get("math_score", 0)
        st.session_state.math_attempts = st.session_state.get("math_attempts", 0)
        st.session_state.math_new = False

    num1 = st.session_state.math_num1
    num2 = st.session_state.math_num2
    op = st.session_state.math_op
    if op == "+":
        answer = num1 + num2
    elif op == "-":
        answer = num1 - num2
    else:
        answer = num1 * num2

    st.write(f"Solve: **{num1} {op} {num2} = ?**")
    user_ans = st.text_input("Your answer:", key="math_answer")
    if st.button("Submit Answer", key="math_submit"):
        st.session_state.math_attempts += 1
        try:
            if int(user_ans) == answer:
                st.success("✅ Correct!")
                st.session_state.math_score += 1
                st.session_state.math_new = True
                st.rerun()
            else:
                st.error(f"❌ Incorrect. The correct answer was {answer}.")
                st.session_state.math_new = True
                st.rerun()
        except:
            st.warning("Please enter a valid number.")

    st.info(f"Score: {st.session_state.math_score} / {st.session_state.math_attempts}")

