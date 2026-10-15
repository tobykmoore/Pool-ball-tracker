import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Pool Ball Tracker")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("Pool Ball Tracker")
st.subheader("Player Login")

email = st.text_input("Email address")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if email and password:
        try:
            supabase.auth.sign_up({
                "email": email.strip(),
                "password": password
            })
            st.success("Check your email to confirm your account!")
        except Exception as e:
            st.error(f"sign up failed: {e}")
    else:
        st.warning ("Enter your email and password.")
if st.button("Log In"):
    if email and password:
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.user and response.session:
                st.session_state["user_id"] = response.user.id
                st.success("Login succseeful!")
            else:
                st.error("Login Failed.")
        except Exception:
            st.error("Check your email and password.")
