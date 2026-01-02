# 🧠 Python CLI Chatbot

A simple command-line chatbot that learns interactively from user input and stores Q&A pairs in a local JSON-based knowledge base. It supports basic natural language preprocessing and fuzzy matching to retrieve relevant answers.

---

## 🚀 Features

- Interactive Q&A learning
- Persistent knowledge base (`knowledge_base.json`)
- Fuzzy matching using `difflib`
- Basic NLP preprocessing (stopword removal, stemming)
- Proper noun capitalization
- Command-line interface with multiple modes
- Import/export/backup functionality

---

## 📦 Requirements

- Python 3.6+
- No external dependencies (uses built-in modules)

---

## 🛠️ How It Works

1. **Startup**: Loads the knowledge base from `knowledge_base.json`.
2. **Modes**:
   - `chat`: Responds to user input and learns new answers.
   - `command`: Only accepts commands (no chatting).
3. **Learning**: If the bot doesn't know an answer, it prompts the user to teach it.
4. **Matching**: Uses fuzzy matching to find the closest known question.
5. **Preprocessing**:
   - Removes stopwords
   - Applies basic stemming rules
   - Capitalizes known proper nouns in responses

---

## 💬 Commands

| Command              | Description                                  |
|----------------------|----------------------------------------------|
| `/help`              | Show available commands                      |
| `/exit` or `/quit`   | Exit the chatbot                             |
| `/stats`             | Show number of learned Q&A pairs             |
| `/list`              | List all learned questions                   |
| `/delete <index>`    | Delete a question by its index               |
| `/clear`             | Clear the entire knowledge base              |
| `/export <file>`     | Export knowledge base to a file              |
| `/import <file>`     | Import knowledge base from a file            |
| `/saveas <file>`     | Save current KB to a new file                |
| `/load <file>`       | Load KB from a specified file                |
| `/backup`            | Create a backup (`kb_backup.json`)           |
| `/about`             | Show bot info                                |
| `/version`           | Show version and clear KB                    |
| `/mode chat`         | Switch to chat + command mode                |
| `/mode command`      | Switch to command-only mode                  |

---

## 📁 File Structure

- `knowledge_base.json`: Default storage for Q&A pairs
- `kb_backup.json`: Backup file created via `/backup`

---

## ✍️ Example Interaction

```bash
You: What is Python?
Bot: I don't know that. Teach me?
Type answer or 'skip': A programming language created by Guido van Rossum.
Bot: Learned
