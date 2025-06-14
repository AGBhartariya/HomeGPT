




import streamlit as st
import sqlite3
import hashlib
import time
import requests
from streamlit_lottie import st_lottie
import json
import os
from datetime import datetime
import pandas as pd
import random
import base64

# Import your existing modules
from utils.gpt_chat import *
from utils.games import *
from utils.quiz_utils import *
from utils.send_love import *
from utils.surprise import *
from utils.face_recog_temp import save_password, retrieve_password, capture_live_image


# Ensure required folders exist
os.makedirs("sync_folder", exist_ok=True)
os.makedirs("assets/photos", exist_ok=True)
os.makedirs("faces", exist_ok=True)

st.set_page_config(
        page_title="HomeGPT - Welcome Home!",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed"  # Hide sidebar initially
    )



def search_youtube(query, api_key):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query + " song",
        "key": api_key,
        "type": "video",
        "maxResults": 1,
        "videoCategoryId": "10"  # Music
    }
    response = requests.get(search_url, params=params)
    results = response.json()
    if results.get("items"):
        video_id = results["items"][0]["id"]["videoId"]
        title = results["items"][0]["snippet"]["title"]
        return video_id, title
    return None, None


def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)




def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottie_file(filepath: str):
    """Load Lottie animation from local file"""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

# def play_sound(sound_file):
#     """Play sound file"""
#     try:
#         if os.path.exists(f"assets/{sound_file}"):
#             pygame.mixer.music.load(f"assets/{sound_file}")
#             pygame.mixer.music.play()
#     except:
#         pass

def play_sound(sound_file):
    if os.path.exists(f"assets/{sound_file}"):
        with open(f"assets/{sound_file}", "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/wav")


def play_sound_base64(sound_file):
    """Play sound using base64 encoding for Streamlit"""
    try:
        with open(sound_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
            <audio autoplay>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)
    except:
        pass



import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

lottie_balloons = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_3zr20t7m.json")


import sqlite3
import pytz

def show_welcome_animation():
    st.markdown("""
        <style>
            .main-header {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                color: #4CAF50;
                margin-bottom: 0.5em;
            }
            .time-greeting {
                font-size: 28px;
                text-align: center;
                color: #FF9800;
                margin-top: 0.3em;
            }
            .welcome-message {
                font-size: 20px;
                text-align: center;
                color: #2196F3;
                margin-top: 0.5em;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Get current IST time
        ist = pytz.timezone('Asia/Kolkata')
        ist_now = datetime.now(pytz.utc).astimezone(ist)
        current_hour_ist = ist_now.hour

        # Lottie animation
        lottie_home = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_puciaact.json")
        if lottie_home:
            st_lottie(lottie_home, height=200, key="home_animation")

        # Header and time-based greeting
        st.markdown('<h1 class="main-header">🏠 Welcome to HomeGPT! 🏠</h1>', unsafe_allow_html=True)
        if 5 <= current_hour_ist < 12:
            greeting = "Good Morning! ☀️"
        elif 12 <= current_hour_ist < 17:
            greeting = "Good Afternoon! 🌤️"
        elif 17 <= current_hour_ist < 21:
            greeting = "Good Evening! 🌅"
        else:
            greeting = "Good Night! 🌙"
        st.markdown(f'<div class="time-greeting">{greeting}</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-message">Your personal AI assistant is ready to help! 💖</div>', unsafe_allow_html=True)


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user


from datetime import datetime

def update_login_details(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        UPDATE users
        SET login_count = login_count + 1,
            last_login = ?
        WHERE username = ?
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
    conn.commit()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    updated_user = c.fetchone()
    conn.close()
    return updated_user

def init_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            login_count INTEGER DEFAULT 0,
            last_login TEXT
        )
    """)
    try:
        c.execute("ALTER TABLE users ADD COLUMN login_count INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (username, password, login_count, last_login)
            VALUES (?, ?, 0, NULL)
        """, (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()



def create_login_page():

    show_welcome_animation()
    username = st.session_state.get("login_username", username)


    tab1, tab2 = st.tabs(["🔓 Login", "🆕 Register"])

    with tab1:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # if st.button("🚀 Login"):
        #     user = login_user(username, password)
        #     if user:
        #         updated_user = update_login_details(username)
        #         st.session_state.authenticated = True
        #         st.session_state.user_info = updated_user
        #         st.success(f"Welcome back, {username}!")
        #         st.markdown(
        #             """<audio autoplay><source src="https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg" type="audio/ogg"></audio>""",
        #             unsafe_allow_html=True,
        #         )
        #         # autoplay_audio("assets/Welcome.wav")
        #         if lottie_balloons:
        #             st_lottie(lottie_balloons, height=250, loop=False)
        #         st.balloons()
        #         st.rerun()
        if st.button("🚀 Login"):
            username = st.session_state.get("login_username", username)
            password = st.session_state.get("login_password", password)
            user = login_user(username, password)
            if user:
                updated_user = update_login_details(username)
                st.session_state.authenticated = True
                st.session_state.user_info = updated_user

                # Show welcome message and animations **before** rerun
                st.success(f"Welcome back, {username}!")

                # 🎵 Play welcome sound using HTML5 <audio>
                st.markdown(
                    """<audio autoplay>
                        <source src="https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg" type="audio/ogg">
                    </audio>""",
                    unsafe_allow_html=True,
                )

                # 🎈 Play balloon animation
                if lottie_balloons:
                    st_lottie(lottie_balloons, height=250, loop=False)

                # 🎉 Show confetti balloons
                st.balloons()

                # Give animations time to finish before rerunning
                time.sleep(2.5)

                # Rerun after delay
                st.rerun()
            else:
                st.error("Invalid username or password")
                st.markdown(
                    """<audio autoplay>
                        <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
                    </audio>""",
                    unsafe_allow_html=True,
                )
        # autoplay_audio("assets/Forget.wav")

            # else:
            #     st.error("Invalid username or password")
            #     st.markdown(
            #         """<audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>""",
            #         unsafe_allow_html=True,
            #     )
            #     autoplay_audio("assets/Forget.wav")

    with tab2:
        st.subheader("🆕 Register")
        username = st.text_input("Choose a Username", key="register_username")
        password = st.text_input("Choose a Password", type="password", key="register_password")
        if st.button("🎉 Register"):
            if username and password:
                success = register_user(username, password)
                if success:
                    st.success("Registration successful! You can now login.")
                    st.balloons()
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Please fill out all required fields.")


if "memories" not in st.session_state:
    st.session_state["memories"] = {}


def create_main_app():
    """Create the main application after login"""
    
    user_info = st.session_state.user_info

    if not user_info:
        st.warning("⚠️ You are not logged in. Please log in to continue.")
        st.session_state['authenticated'] = False
        st.rerun()
        return  # Exit the function early

    username = user_info[0]
    login_count = user_info[2]
    last_login = user_info[3]
    # Page config for main app
    # st.set_page_config(
    #     page_title="HomeGPT: AI Companion for Family",
    #     layout="wide",
    #     page_icon="🏠"
    # )
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.markdown(f"Welcome, {username}!")
        st.markdown(f"**Login Count:** {login_count}")
        if last_login:
            st.markdown(f"**Last Visit:** {last_login}")
        
        st.markdown("---")
        
        # if st.button("🚪 Logout", use_container_width=True):
        #     st.session_state.authenticated = False
        #     st.session_state.user_info = None
        #     st.session_state.user_name = None
        #     st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    
    # Main app content
    st.title(f"🏠 HomeGPT: AI Family Companion")
    st.caption(f"Welcome {username}! 💖")
    
    # Initialize quiz session state variables
    if "quiz_mode" not in st.session_state:
        st.session_state.quiz_mode = "Mixed"
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = []
    if "questions_pool" not in st.session_state:
        st.session_state.questions_pool = []
    if "current_options" not in st.session_state:
        st.session_state.current_options = []
    if "correct_answer" not in st.session_state:
        st.session_state.correct_answer = ""
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    
    # Navigation tabs - All tabs from second code integrated
    memory_tab, password_tab, chat_tab, music_tab, games_tab, love_tab = st.tabs([
        "📝 Memory Vault", 
        "🔐 Password Vault",
        "🧠 ChatGPT",
        "🎵 Music",
        "🎮 Games & Quiz",
        "💌 Message"
    ])
    
    def load_memories():
        username = st.session_state.get("username")
        if not username:
            return []
        return st.session_state.get("memories", {}).get(username, [])

    def save_memory(title, content):
        username = st.session_state.get("username")
        if not username:
            return  # Don't save if username is missing

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "title": title,
            "content": content,
            "timestamp": timestamp
        }

        if "memories" not in st.session_state:
            st.session_state["memories"] = {}

        if username not in st.session_state["memories"]:
            st.session_state["memories"][username] = []

        st.session_state["memories"][username].append(new_entry)




    with memory_tab:
        st.header("📝 Record or View Memories")
        title = st.text_input("Memory Title")
        content = st.text_area("Your memory or story")
        if st.button("Save Memory"):
            if title and content:
                save_memory(title, content)
                st.success("Memory saved!")
            else:
                st.warning("Please fill in both title and content.")

        st.markdown("---")
        st.subheader("📚 Your Saved Memories")
        memories = load_memories()
        if memories:
            for mem in reversed(memories):
                st.markdown(f"**{mem['timestamp']}**  \n*{mem['title']}*  \n{mem['content']}")
                st.markdown("---")
        else:
            st.info("No memories saved yet.")

    
    with password_tab:
        st.header("🔐 Encrypted Password Manager")
        st.info("AES protected password access")
        
        # Password management functionality
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💾 Save Password")
            site_name = st.text_input("Website/App Name")
            password_to_save = st.text_input("Password", type="password")
            if st.button("Save Password"):
                if site_name and password_to_save:
                    success = save_password(site_name, password_to_save, username)
                    if success:
                        st.success("Password saved securely!")
                    else:
                        st.error("Failed to save password")
        
        with col2:
            st.subheader("🔓 Retrieve Password")
            site_to_retrieve = st.text_input("Website/App to retrieve")
            if st.button("Retrieve Password"):
                if site_to_retrieve:
                    password = retrieve_password(site_to_retrieve, username)
                    if password:
                        st.success(f"Password: {password}")
                    else:
                        st.error("Password not found or face verification failed")
    

    
    with chat_tab:
        st.header("🧠 Ask Anything")
        user_query = st.text_input("Talk to HomeGPT:")
        if st.button("Ask"):
            response = ask_homegpt(user_query)
            st.success(response)
    
    with music_tab:
        st.header("🎵 YouTube Music Player")
        song_query = st.text_input("Enter song name or artist:", key="music_search")
        api_key = st.secrets["YOUTUBE_API_KEY"]

        if st.button("Search & Play", key="music_play_btn") and song_query:
            video_id, title = search_youtube(song_query, api_key)
            if video_id:
                st.success(f"Playing: {title}")
                st.video(f"https://www.youtube.com/watch?v={video_id}")
            else:
                st.error("No results found.")

    

    import random
    import time
    import base64
    import pandas as pd
    with games_tab:
        def play_sound(sound_file):
            with open(sound_file, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                <audio autoplay>
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                </audio>
                """
                st.markdown(md, unsafe_allow_html=True)


        st.header("🎮 Bollywood & Cricket Quiz Game")

        @st.cache_data
        def load_questions():
            df = pd.read_csv("real_bollywood_cricket_quiz_1.csv")
            return df

        df = load_questions()

        if "quiz_mode" not in st.session_state:
            st.session_state.quiz_mode = "Mixed"
        if "question_index" not in st.session_state:
            st.session_state.question_index = 0
        if "score" not in st.session_state:
            st.session_state.score = 0
        if "player_name" not in st.session_state:
            st.session_state.player_name = ""
        if "leaderboard" not in st.session_state:
            st.session_state.leaderboard = []
        if "questions_pool" not in st.session_state:
            st.session_state.questions_pool = []
        if "current_options" not in st.session_state:
            st.session_state.current_options = []
        if "correct_answer" not in st.session_state:
            st.session_state.correct_answer = ""
        if "selected_option" not in st.session_state:
            st.session_state.selected_option = None
        if "show_result" not in st.session_state:
            st.session_state.show_result = False

        def reset_quiz(mode):
            st.session_state.quiz_mode = mode
            if mode == "Bollywood":
                filtered = df[df["category"] == "Bollywood"]
            elif mode == "Cricket":
                filtered = df[df["category"] == "Cricket"]
            else:
                filtered = df

            st.session_state.questions_pool = filtered.sample(frac=1).to_dict("records")
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.current_options = []
            st.session_state.correct_answer = ""
            st.session_state.selected_option = None
            st.session_state.show_result = False

        if not st.session_state.player_name:
            st.session_state.player_name = st.text_input("👤 Enter your name to begin:")

        st.subheader("🎲 Select Quiz Mode:")
        col1, col2, col3 = st.columns(3)
        if col1.button("🎬 Bollywood"):
            reset_quiz("Bollywood")
            st.rerun()
        if col2.button("🏏 Cricket"):
            reset_quiz("Cricket")
            st.rerun()
        if col3.button("🔀 Mixed"):
            reset_quiz("Mixed")
            st.rerun()

        if st.session_state.questions_pool:
            qlist = st.session_state.questions_pool
            qidx = st.session_state.question_index

            if qidx < min(5,len(qlist)):
                q = qlist[qidx]

                # Shuffle options once
                if not st.session_state.current_options:
                    options = [q["option1"], q["option2"], q["option3"], q["option4"]]
                    random.shuffle(options)
                    st.session_state.current_options = options
                    st.session_state.correct_answer = q["answer"]
                    st.session_state.selected_option = None
                    st.session_state.show_result = False

                options = st.session_state.current_options
                correct = st.session_state.correct_answer

                st.write(f"**Q{qidx+1}:** {q['question']}")
                st.session_state.selected_option = st.radio(
                    "Choose your answer:",
                    options,
                    index=None,
                    key=f"radio_{qidx}"
                )

                if st.button("✅ Submit Answer") and st.session_state.selected_option:
                    if st.session_state.selected_option == correct:
                        st.success("🎉 Correct!")
                        st.session_state.score += 1
                        autoplay_audio("assets/correct.wav")

                    else:
                        st.error(f"❌ Wrong! Correct answer: **{correct}**")
                        autoplay_audio("assets/wrong.wav")

                    st.session_state.show_result = True
                    time.sleep(3)

                    # Move to next question
                    st.session_state.question_index += 1
                    st.session_state.current_options = []
                    st.session_state.selected_option = None
                    st.session_state.correct_answer = ""
                    st.session_state.show_result = False
                    st.rerun()
                # elif st.button("✅ Submit Answer", key=f"submit_{st.session_state.question_index}"):
                #     st.warning("Please select an option before submitting.")

            else:
                st.balloons()
                st.success(f"🏁 Quiz finished, {st.session_state.player_name}!")
                st.success(f"Your Score: {st.session_state.score} / {5}")
                st.session_state.leaderboard.append((st.session_state.player_name, st.session_state.score))
                st.session_state.questions_pool = []

        if st.session_state.leaderboard:
            st.markdown("### 🏆 Leaderboard")
            leaderboard_df = pd.DataFrame(
                st.session_state.leaderboard, columns=["Name", "Score"]
            )
            st.table(leaderboard_df.sort_values("Score", ascending=False).reset_index(drop=True))

        word_scramble_game()
        math_challenge_game()




    with love_tab:
        st.header("💌 Send a Message to Abhigyan via Telegram")

        # Get sender's name from session state or fallback
        sender_name = st.text_input("Your Name", placeholder="Enter your name")

        # Display previous messages in session (optional)
        if "love_messages" not in st.session_state:
            st.session_state.love_messages = []

        for msg in st.session_state.love_messages:
            with st.chat_message("user"):
                st.markdown(msg["content"])

        # Chat input for new message
        user_message = st.chat_input("Type your message here and press Enter to send to Abhigyan")

        if user_message:
            if not sender_name.strip():
                st.warning("Please enter your name before sending a message.")
            else:
                sent = send_telegram_message(user_message, sender_name)
            if sent:
                st.success("✅ Your message was sent to Abhigyan on Telegram!")
                st.session_state.love_messages.append({"role": "user", "content": user_message})
            else:
                st.error("❌ Failed to send message. Please try again later.")


    




def main():
    """Main application function"""
    
    
    # Initialize session state variables FIRST
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = None
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = None
    if 'loading_complete' not in st.session_state:
        st.session_state['loading_complete'] = False
    
    # Initialize database
    init_database()
    
    # ===== AUTHENTICATION GATE - STOPS EVERYTHING UNTIL LOGIN =====
    if not st.session_state.get('authenticated', False):
        
        # Optional: Show catchy loader on first visit
        if not st.session_state['loading_complete']:
            with st.spinner('✨ Setting up your HomeGPT experience...'):
                time.sleep(2)  # Simulate loading time
            st.session_state['loading_complete'] = True
            st.rerun()
        
        # Show only the authentication page
        create_login_page()
        st.stop()  # ⭐ THIS PREVENTS ANYTHING ELSE FROM LOADING
    
    # ===== ONLY RUNS AFTER SUCCESSFUL AUTHENTICATION =====
    create_main_app()

if __name__ == "__main__":
    main()



