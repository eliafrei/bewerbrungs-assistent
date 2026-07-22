import anthropic
from dotenv import load_dotenv
from profile import MEIN_PROFIL

load_dotenv()

client = anthropic.Anthropic()

verlauf = []

print("Bewerbungsassistent für Elia Frei – stell deine Fragen! ('exit' zum Beenden)")

while True:
    frage = input("\nDeine Frage: ")

    if frage.lower() == "exit":
        print("Auf Wiedersehen!")
        break

    verlauf.append({"role": "user", "content": frage})

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        system=MEIN_PROFIL,
        messages=verlauf,
        thinking={"type": "disabled"}
    )

    antwort = None
    for block in response.content:
        if block.type == "text":
            antwort = block.text
            break
    print("\nAntwort:", antwort)

    verlauf.append({"role": "assistant", "content": antwort})