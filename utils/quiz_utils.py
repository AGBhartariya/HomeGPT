import streamlit as st
import pandas as pd
import time
import random


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
                            st.rerun()
                            time.sleep(0.7)
                            st.session_state.flipped[i] = False
                            st.session_state.flipped[j] = False
                        st.session_state.last_pick = None
                    st.rerun()

    if all(st.session_state.matched):
        st.success(f"🎉 You won in {st.session_state.moves} moves!")
        st.balloons()
        if st.button("Play Again"):
            for key in ["memory_cards", "flipped", "matched", "moves", "last_pick", "game_over"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()