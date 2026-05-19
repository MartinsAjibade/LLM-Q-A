# Phase 1 Mini Project: LLM Q&A CLI

A simple command-line question-and-answer app powered by OpenAI.

Created by **Martins Ajibade**, this project was built as a Phase 1 Python mini project to practice core programming skills while creating a useful terminal app. The app lets users ask Python-related questions, view their question history, save history to a JSON file, and exit cleanly.

---
## Features

- Ask Python-related questions from the terminal
- Get AI-generated answers using OpenAI
- Store Q&A history during the session
- Save history to a local JSON file
- Load previous history when the app starts
- Clear in-memory history
- Exit cleanly while saving progress
- Handle errors using `try/except`

---

## Skills Practiced

This project intentionally uses beginner-friendly Python concepts, including:

- Variables and data types
- Conditional logic with `if`, `elif`, and `else`
- Loops for continuous user input
- Functions for modular code
- Lists and dictionaries for storing history
- JSON file handling
- Error handling with `try/except`
- Environment variables for API key security
- Basic command-line interface design

---

## Commands

/help - Show commands
/history - View saved Q&A
/save - Save history
/clear - Clear history
/exit or /quit - Exit

---

## Project Structure

```text
Phase 1 LLM QA/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── qa_history.json