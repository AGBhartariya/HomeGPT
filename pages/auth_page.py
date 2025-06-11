import streamlit as st
import time
def authentication_page():
    """Custom login page for HomeGPT - Family AI Companion"""
    st.markdown('<h1 class="main-header">🏡 Welcome to HomeGPT</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <h3>🤗 Your Personal Family AI Companion</h3>
        <p>Interact naturally, store memories, play games, and access everything with a smile or a click!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("🔐 How would you like to login today?")

        login_method = st.radio("Select login method:",
                                ["😃 Face Unlock", "🔑 Enter Password", "🎉 Casual Guest Access"])

        if login_method == "😃 Face Unlock":
            st.info("📷 Smile to login securely and quickly!")
            if st.button("Start Face Scan"):
                with st.spinner("Scanning your face..."):
                    time.sleep(2)  # Simulated delay
                    success = face_recognition.authenticate()
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_name = "Mom/Dad"
                        st.success("✅ Welcome back! ❤️")
                        st.rerun()
                    else:
                        st.error("Face not recognized. Try another method!")

        elif login_method == "🔑 Enter Password":
            password = st.text_input("Enter your HomeGPT secret password:", type="password")
            if st.button("Login"):
                if password_vault.verify_master_password(password):
                    st.session_state.authenticated = True
                    st.session_state.user_name = "Trusted User"
                    st.success("🎉 Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please try again.")

        else:  # 🎉 Casual Guest Access
            name = st.text_input("Who's visiting today?")
            if st.button("Let Me In!"):
                if name:
                    st.session_state.authenticated = True
                    st.session_state.user_name = name
                    st.success(f"✨ Welcome, {name}! Enjoy exploring HomeGPT.")
                    st.rerun()
 
