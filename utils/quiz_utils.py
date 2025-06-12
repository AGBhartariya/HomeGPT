import streamlit as st
import pandas as pd
import time
import random







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

    # Pick a new word if starting or after "Play Again"
    if "scramble_word" not in st.session_state or st.session_state.get("scramble_new", False):
        word = random.choice(word_list)
        scrambled = "".join(random.sample(word, len(word)))
        st.session_state.scramble_word = word
        st.session_state.scrambled = scrambled
        st.session_state.scramble_attempts = 0
        st.session_state.scramble_new = False  # Reset flag

    st.write(f"Scrambled word: **{st.session_state.scrambled}**")
    guess = st.text_input("Your guess:", key="scramble_guess")
    if st.button("Submit Guess", key="scramble_submit"):
        st.session_state.scramble_attempts += 1
        if guess.lower() == st.session_state.scramble_word:
            st.success(f"🎉 Correct! The word was '{st.session_state.scramble_word}'. Attempts: {st.session_state.scramble_attempts}")
            if st.button("Play Again", key="scramble_restart"):
                st.session_state.scramble_new = True
                st.session_state["scramble_guess"] = ""  # Reset input
                st.experimental_rerun()
        else:
            st.error("❌ Incorrect. Try again!")


def math_challenge_game():
    st.subheader("➕ Math Challenge")
    st.write("Try these trickier math questions!")

    operators = ["+", "-", "*", "/", "**"]
    # Generate a new question if needed
    if "math_question" not in st.session_state or st.session_state.get("math_new", False):
        op = random.choice(operators)
        if op == "+":
            num1, num2 = random.randint(10, 99), random.randint(10, 99)
            answer = num1 + num2
            q = f"{num1} + {num2}"
        elif op == "-":
            num1, num2 = random.randint(50, 150), random.randint(10, 49)
            answer = num1 - num2
            q = f"{num1} - {num2}"
        elif op == "*":
            num1, num2 = random.randint(5, 20), random.randint(5, 20)
            answer = num1 * num2
            q = f"{num1} × {num2}"
        elif op == "/":
            num2 = random.randint(2, 12)
            answer = random.randint(2, 12)
            num1 = num2 * answer
            q = f"{num1} ÷ {num2}"
        else:  # Exponent
            num1 = random.randint(2, 5)
            num2 = random.randint(2, 3)
            answer = num1 ** num2
            q = f"{num1}^{num2}"
        st.session_state.math_question = q
        st.session_state.math_answer = answer
        st.session_state.math_new = False
        st.session_state.math_score = st.session_state.get("math_score", 0)
        st.session_state.math_attempts = st.session_state.get("math_attempts", 0)

    st.write(f"Solve: **{st.session_state.math_question} = ?**")
    user_ans = st.text_input("Your answer:", key="math_answer_input")
    if st.button("Submit Answer", key="math_submit"):
        st.session_state.math_attempts += 1
        try:
            if float(user_ans) == float(st.session_state.math_answer):
                st.success("✅ Correct!")
                st.session_state.math_score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer was {st.session_state.math_answer}.")
            st.session_state.math_new = True
            st.experimental_rerun()  # Immediately show a new question
        except:
            st.warning("Please enter a valid number.")

    st.info(f"Score: {st.session_state.math_score} / {st.session_state.math_attempts}")
