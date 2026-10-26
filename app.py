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
                st.session_state["access_token"] = response.session.access_token
                st.success("Login succseeful!")
            else:
                st.error("Login Failed.")
        except Exception as e:
            st.error(f"Login failed: {e}")

if "user_id" in st.session_state:
    st.divider()
    st.subheader("Player Management")
    
    player_name = st.text_input("Enter player name")

    if st.button("Add Player"):
        if player_name.strip():
            try:
                supabase.postgrest.auth(st.session_state["access_token"])
                supabase.table("players").insert({
                    "name": player_name.strip(),
                    "user_id": st.session_state["user_id"]
                }).execute()
                st.success("Player saved successfully!")
            except Exception as e:
                st.error(f"Could not save player: {e}")
        else:
            st.warning("Plase enter a player name.")
            
    st.subheader("Saved Players")
    try:
        players = supabase.table("players").select("name").eq(
            "user_id", st.session_state["user_id"]
        ).execute()
        if players.data:
            for player in players.data:
                st.write(player["name"])
        else:
            st.info("No player saved yet.")
    except Exception as e:
        st.error(f"Could not load players: {e}")

    st.divider()
    st.subheader("Pool Game Tracker")

    game_type = st.selectbox(
        "Choose game type",
        ["8-Ball", "9-Ball"]
    )

    if players.data:
        selected_player = st.selectbox(
            "Choose player",
            [player["name"]for player in players.data]
        )

        balls_made = st.number_input(
            "How many balls did the player make?",
            min_value=0,
            max_value=9,
            value=0,
            step=1
        )
        
        games_in_match = st.number-input(
            "How many games are in this match?",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )
        
