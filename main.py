import json
import os
import logging
from difflib import get_close_matches

STOPWORDS = {"the", "a", "of", "and", "to", "in", "for", "on", "is", "it", "this", "that", "with", "at", "by", "an"}

STEMMING_RULES = {
    "running": "run", "runner": "run", "runs": "run",
    "played": "play", "playing": "play", "plays": "play",
    "better": "good", "best": "good",
    "worse": "bad", "worst": "bad"
}

PROPER_NOUNS = {
    "python", "java", "javascript", "india", "google", "microsoft",
    "windows", "linux", "minecraft", "ultrakill",
    "guido", "rossum", "netherlands", "openai"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DEFAULT_KB = "knowledge_base.json"


def load_knowledge_base(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {"questions": []}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"questions": []}


def save_knowledge_base(file_path: str, data: dict):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def preprocess_question(text: str) -> str:
    tokens = text.lower().split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    tokens = [STEMMING_RULES.get(t, t) for t in tokens]
    return " ".join(tokens)


def find_best_match(query: str, questions: list):
    matches = get_close_matches(query, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer(question: str, kb: dict):
    for q in kb["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


def smart_capitalize(text: str) -> str:
    out = []
    for w in text.split():
        if w.lower() in PROPER_NOUNS:
            out.append(w.capitalize())
        else:
            out.append(w)
    return " ".join(out)


def export_kb(kb: dict, filename: str):
    save_knowledge_base(filename, kb)


def import_kb(filename: str):
    if not os.path.exists(filename):
        return None
    return load_knowledge_base(filename)


def show_help():
    print("Commands:")
    print("/help                 show commands")
    print("/exit or /quit        exit chatbot")
    print("/stats                show knowledge size")
    print("/list                 list all learned questions")
    print("/delete <index>       delete a question by index")
    print("/clear                clear knowledge base")
    print("/export <file>        export knowledge base")
    print("/import <file>        import knowledge base")
    print("/saveas <file>        save current KB as file")
    print("/load <file>          load KB from file")
    print("/backup               create automatic backup")
    print("/about                show bot info")
    print("/version              show version")
    print("/mode chat            chat + commands")
    print("/mode command         commands only")


def chat_bot():
    kb = load_knowledge_base(DEFAULT_KB)
    mode = "chat"

    print("Chatbot started. Type /help for commands. Version 1.1")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.startswith("/"):
            parts = user_input.split()
            cmd = parts[0].lower()

            if cmd in {"/exit", "/quit"}:
                print("Bot: Goodbye")
                break

            elif cmd == "/help":
                show_help()

            elif cmd == "/stats":
                print(f"Bot: Learned Q&A pairs: {len(kb['questions'])}")

            elif cmd == "/list":
                if not kb['questions']:
                    print("Bot: Knowledge base empty")
                else:
                    for i, q in enumerate(kb['questions']):
                        print(f"[{i}] {q['question']}")

            elif cmd == "/delete" and len(parts) == 2 and parts[1].isdigit():
                idx = int(parts[1])
                if 0 <= idx < len(kb['questions']):
                    removed = kb['questions'].pop(idx)
                    save_knowledge_base(DEFAULT_KB, kb)
                    print(f"Bot: Deleted '{removed['question']}'")
                else:
                    print("Bot: Invalid index")
                print(f"Bot: Learned Q&A pairs: {len(kb['questions'])}")

            elif cmd == "/clear":
                kb = {"questions": []}
                save_knowledge_base(DEFAULT_KB, kb)
                print("Bot: Knowledge base cleared")

            elif cmd == "/saveas" and len(parts) == 2:
                save_knowledge_base(parts[1], kb)
                print(f"Bot: Saved as {parts[1]}")

            elif cmd == "/load" and len(parts) == 2:
                loaded = import_kb(parts[1])
                if loaded:
                    kb = loaded
                    save_knowledge_base(DEFAULT_KB, kb)
                    print(f"Bot: Loaded {parts[1]}")
                else:
                    print("Bot: Load failed")

            elif cmd == "/backup":
                backup_name = "kb_backup.json"
                save_knowledge_base(backup_name, kb)
                print(f"Bot: Backup created ({backup_name})")

            elif cmd == "/about":
                print("Bot: Python Learning Chatbot | CLI AI | Created by Cadet")

            elif cmd == "/version":
                print("Bot: Version 1.1")
                kb = {"questions": []}
                save_knowledge_base(DEFAULT_KB, kb)
                print("Bot: Knowledge base cleared")

            elif cmd == "/export" and len(parts) == 2:
                export_kb(kb, parts[1])
                print(f"Bot: Exported to {parts[1]}")

            elif cmd == "/import" and len(parts) == 2:
                imported = import_kb(parts[1])
                if imported:
                    kb = imported
                    save_knowledge_base(DEFAULT_KB, kb)
                    print(f"Bot: Imported from {parts[1]}")
                else:
                    print("Bot: Import failed")

            elif cmd == "/mode" and len(parts) == 2:
                if parts[1] in {"chat", "command"}:
                    mode = parts[1]
                    print(f"Bot: Mode set to {mode}")
                else:
                    print("Bot: Invalid mode")

            else:
                print("Bot: Unknown command")

            continue

        if mode == "command":
            print("Bot: Command mode active. Use /help")
            continue

        processed = preprocess_question(user_input)
        questions = [q["question"] for q in kb["questions"]]
        match = find_best_match(processed, questions)

        if match:
            answer = get_answer(match, kb)
            print(f"Bot: {smart_capitalize(answer)}")
        else:
            print("Bot: I don't know that. Teach me?")
            ans = input("Type answer or 'skip': ").strip()
            if ans.lower() != "skip":
                kb["questions"].append({"question": user_input, "answer": ans})
                save_knowledge_base(DEFAULT_KB, kb)
                print("Bot: Learned")


if __name__ == "__main__":
    chat_bot()
