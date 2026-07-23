import streamlit as st
import anthropic
import time

st.title("Bewerbungsassistent Elia Frei")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
MEIN_PROFIL = st.secrets["MEIN_PROFIL"]


if "verlauf" not in st.session_state:
    st.session_state.verlauf = []

if "frage_anzahl" not in st.session_state:
    st.session_state.frage_anzahl = 0

if "letzte_frage_zeit" not in st.session_state:
    st.session_state.letzte_frage_zeit = 0

for nachricht in st.session_state.verlauf:
    with st.chat_message(nachricht["role"]):
        st.write(nachricht["content"])

frage = st.chat_input("Stell deine Frage...")

MAX_FRAGEN = 15
MIN_ABSTAND_SEKUNDEN = 3

if frage:
    jetzt = time.time()
    abstand = jetzt - st.session_state.letzte_frage_zeit

    if st.session_state.frage_anzahl >= MAX_FRAGEN:
        st.warning("Das Limit an Fragen für diese Sitzung ist erreicht. Lade die Seite neu, um von vorne zu beginnen.")
    elif abstand < MIN_ABSTAND_SEKUNDEN:
        st.warning("Bitte kurz warten, bevor du die nächste Frage stellst.")
    else:
        st.session_state.frage_anzahl += 1
        st.session_state.letzte_frage_zeit = jetzt

        st.session_state.verlauf.append({"role": "user", "content": frage})
        with st.chat_message("user"):
            st.write(frage)

        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2000,
            system=MEIN_PROFIL,
            messages=st.session_state.verlauf,
            thinking={"type": "disabled"}
        )

        antwort = None
        for block in response.content:
            if block.type == "text":
                antwort = block.text
                break
        if response.stop_reason == "max_tokens":
            antwort += "\n\n*(Antwort wurde aus Längengründen gekürzt.)*"

        with st.chat_message("assistant"):
            st.write(antwort)

        st.session_state.verlauf.append({"role": "assistant", "content": antwort})