import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from openai import OpenAI

ASSISTANT_NAME = "Sanny"
HISTORY_FILE = Path(__file__).resolve().parent / "qa_history.json"


def validate_api_key(api_key: str) -> None:
    """Raise an error if the OpenAI API key is missing."""
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Export it first, e.g.:\n"
            'export OPENAI_API_KEY="your_key_here"'
        )


def ensure_history_file() -> None:
    """Create the history file if it does not already exist."""
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_history() -> List[Dict[str, str]]:
    """Load Q&A history from the JSON file."""
    ensure_history_file()

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print("Warning: qa_history.json was not a list. Resetting history.")
        save_history([])
        return []

    except json.JSONDecodeError:
        print("Warning: qa_history.json was corrupted. Resetting history.")
        save_history([])
        return []


def save_history(history: List[Dict[str, str]]) -> None:
    """Save current Q&A history to the JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def is_name_question(question: str) -> bool:
    """Check whether the user is asking for the assistant's name."""
    triggers = [
        "your name",
        "who are you",
        "what are you called",
        "what's your name",
        "whats your name",
    ]

    q = question.lower()
    return any(trigger in q for trigger in triggers)


def is_code(question: str) -> bool:
    """Check whether the input looks like code."""
    keywords = ["def ", "print(", "=", "for ", "while ", "{", "}", "import "]
    return any(keyword in question for keyword in keywords)


def show_history(history: List[Dict[str, str]]) -> None:
    """Display the saved Q&A history."""
    if not history:
        print("No history yet.")
        return

    for index, item in enumerate(history, start=1):
        print(f"\n{index}. [{item.get('timestamp', 'No timestamp')}]")
        print(f"Q: {item.get('question', '')}")
        print(f"A: {item.get('answer', '')}")


def ask_openai_question(client: OpenAI, model: str, question: str) -> str:
    """Send the user's question to OpenAI and return the answer."""
    if is_name_question(question):
        return f"My name is {ASSISTANT_NAME}! 👋"

    system_prompt = (
        f"You are {ASSISTANT_NAME}, a Python coding assistant. "
        "Answer only Python coding questions. Politely decline anything else. "
        "For greetings and small talk, reply briefly and ask what the user needs help with. "
        "Do not include code examples for greetings or small talk. "
        "Only provide code if the user explicitly asks a coding question."
    )

    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=question,
    )

    return response.output_text.strip()


def run_app(client: OpenAI, model: str) -> None:
    """Run the interactive CLI loop for asking and storing questions."""
    history = load_history()

    print("=== Phase 1 LLM Q&A ===")
    print("Type a Python question, or /history, /save, /clear, /exit, /quit.")

    while True:
        user_input = input("\nYou> ").strip()
        command = user_input.lower()

        if not user_input:
            print("Please enter a Python-related question.")
            continue

        if command in ["/exit", "/quit"]:
            save_history(history)
            print(f"Saved history to {HISTORY_FILE}. Bye.")
            break

        if command == "/history":
            show_history(history)
            continue

        if command == "/save":
            save_history(history)
            print(f"Saved to {HISTORY_FILE}.")
            continue

        if command == "/clear":
            history = []
            save_history(history)
            print("History cleared.")
            continue

        try:
            answer = ask_openai_question(client, model, user_input)

            history.append(
                {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "question": user_input,
                    "answer": answer,
                }
            )

            print(f"LLM> {answer}")

        except Exception as exc:
            print(f"Error while calling OpenAI: {exc}")
            print("Tip: check API key, network, and model name.")


def main() -> None:
    """Configure dependencies and start the Q&A terminal app."""
    try:
        model = "gpt-4o-mini"
        api_key = os.getenv("OPENAI_API_KEY", "").strip()

        validate_api_key(api_key)

        client = OpenAI(api_key=api_key)
        run_app(client, model)

    except Exception as exc:
        print(f"Startup error: {exc}")


if __name__ == "__main__":
    main()