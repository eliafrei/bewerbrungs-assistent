import streamlit as st
import anthropic
from dotenv import load_dotenv
from profile import MEIN_PROFIL

load_dotenv()

client = anthropic.Anthropic()

st.title("Bewerbungsassistent Elia Frei")

if "verlauf" not in st.session_state:
    st.session_state.verlauf = []

for nachricht in st.session_state.verlauf:
    with st.chat_message(nachricht["role"]):
        st.write(nachricht["content"])

frage = st.chat_input("Stell deine Frage...")

if frage:
    st.session_state.verlauf.append({"role": "user", "content": frage})
    with st.chat_message("user"):
        st.write(frage)

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        system=MEIN_PROFIL,
        messages=st.session_state.verlauf,
        thinking={"type": "disabled"}
    )

    antwort = None
    for block in response.content:
        if block.type == "text":
            antwort = block.text
            break

    with st.chat_message("assistant"):
        st.write(antwort)

    st.session_state.verlauf.append({"role": "assistant", "content": antwort})