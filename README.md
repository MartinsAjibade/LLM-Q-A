# Phase 1 Mini Project: LLM Q&A CLI

A simple terminal question-and-answer app powered by OpenAI.

This project intentionally uses Phase 1 skills:
- variables and data types
- control flow (`if`, loops)
- functions and modular design
- lists/dictionaries for history
- file handling (JSON save/load)
- error handling with `try/except`

## 1) Setup

```bash
cd Phase 1 LLM QA
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Add your API key

```bash
export OPENAI_API_KEY="your_key_here"
```

## 3) Run

```bash
python main.py
```

## 4) Commands inside the app

- Ask any python related question directly.
- `/history` prints your Q&A history.
- `/save` saves history to `qa_history.json`.
- `/clear` clears in-memory history.
- `/exit` and `/quit` saves and quits.
