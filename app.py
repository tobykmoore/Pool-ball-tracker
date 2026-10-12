import csv
from pathlib import Path
import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
file_path=Path(__file__).with_name("pool_games.csv")
st.title("pool ball tracker")

st.subheader("Player login")
email=st.text_input("Email address")
passward = st.text_input("passward",type="passward")
if st.button("sign up"):
    if email and passward:
        supabase.auth.sign_up({
            "email": email,
            "passward": passward
        })
        st.success("Check your email to confirm your account!")
    else:
        st.warning("Enter your email and password.")
if st.button("log in"):
    if email and passward:
    try:
       supabase.auth.sign_in_with_passward({
        "email": email,
        "passward": passward
       })
       st.success("login successful!")
    except Execption:
         st.error("login failed. check your email and passward.")
    else:
    st.warning("Enter your email and passward.")

player = st.text_input("Player name")
game = st.selectbox("game type",["8 ball","9 ball"])
number_of_games = st.number_input("how many games in the match",min_value=1, step=1)
ball_counts=[]

for game_number in range(1,number_of_games+1):
    balls= st.number_input(f"Balls made in game{game_number}",min_value=0,step=1)
    ball_counts.append(balls)
average=sum(ball_counts)/number_of_games
st.write("average balls per game:",round(average,2))
save_match= st.button("save match")
if save_match:
    if not player.strip():
        st.error("enter a player name first.")
    else:
        new_file = not file_path.exists() or file_path.stat().st_size ==0
        with file_path.open("a",newline="")as file:
            writer = csv.writer(file)
            if new_file:
                writer.writerow(["player","game_type","game_number","balls_made"])
            for game_number, balls in enumerate(ball_counts,start=1):
                writer.writerow([player.strip(),game, game_number,balls])
        st.success("match saved!")
if player.strip()and file_path.exists():
    eight_ball=[]
    nine_ball=[]

    with file_path.open("r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["player"].strip().lower()==player.strip().lower():
                if row["game_type"]== "8 ball":
                    eight_ball.append(int(row["balls_made"]))
                elif row["game_type"]=="9 ball":
                    nine_ball.append(int(row["balls_made"]))

    if eight_ball:
        st.write("saved 8-ball average:", round(sum(eight_ball)/len(eight_ball),2))
        st.write("8-ball scores:", eight_ball)
    if nine_ball:
        st.write("saved 9-ball average:", round(sum(nine_ball)/len(nine_ball),2))
        st.write("9-ball scores:", nine_ball)
