# norm-ai-fixer

`norm-ai-fixer` is a **Python-based CLI tool** that automatically analyzes and rewrites C code to comply with **strict and customizable coding standards**, including the **42 school norm**, using **local AI models only**.

The project is built to be **deterministic, offline, and machine-safe**, making it suitable for automation, CI-like workflows, and environments where reliability matters more than creativity.

---

## ✨ Key Features

- Automatic fixing of **42 norminette errors**
- Uses **local LLMs via Ollama** (no internet required)
- Deterministic, strictly parsed AI output
- Logic-preserving code transformations
- Fully customizable rules via prompt files
- Optional `--debug` mode to inspect AI I/O
- Safe-by-design: invalid AI output is rejected

---

## 🧩 Why This Project Exists

Most AI coding tools are:
- Online only
- Non-deterministic
- Unsafe for strict coding standards

`norm-ai-fixer` proves that **local AI models** can be integrated into **highly constrained engineering pipelines** while remaining reliable, auditable, and predictable.

---

## 📦 Requirements

- Python **3.8+**
- `norminette` (optional but recommended)
- **Ollama** (local LLM runtime)
- A local model (e.g. `mistral`, `codellama`, `qwen`)
- **codellama:34b** (highly recommended for best results)
---

## 📁 Project Structure

```
norm-ai-fixer/
├── norm_ai_fixer.py
├── config.yaml
├── prompts/
│   └── norm42.txt
└── test/
    └── test.c
```

---

## ⚙️ Configuration

Edit `config.yaml` to select the model, prompt, and norminette usage:

```yaml
ollama:
  model: codellama:34b
  url: http://localhost:11434/api/generate
  prompt_file: prompts/norm42.txt

norminette:
  use_norminette: true
  norminette_cmd: norminette
```

---

## ▶️ Usage

### Basic Usage

```bash
python3 norm_ai_fixer.py
```

You will be prompted to select a file. If the AI output is valid, the file is **rewritten in place**.

Output (non-debug mode):
```
Code successfully modified
```

---

### Debug Mode

```bash
python3 norm_ai_fixer.py --debug
```

Debug mode prints:
- Prompt sent to the AI
- Raw AI response
- Parsing and validation details

---

## 🧠 How It Works (Pipeline)

1. Load the C source file
2. Split the 42 header from the code
3. Run `norminette` (optional)
4. Inject data into a strict AI prompt
5. Call a **local AI model**
6. Extract `<RESULT>` content only
7. Validate syntax and formatting
8. Overwrite the file only if valid

Any malformed AI output is **automatically rejected**.

---

## 🛡️ Determinism & Safety Guarantees

- Exact `<RESULT>...</RESULT>` parsing
- No markdown, comments, or explanations allowed
- No extra characters permitted
- No header modification
- No internet dependency

This makes the tool safe for automation and CI pipelines.

---

## 📏 Enforced 42 Norm Rules (Default Prompt)

- C language only
- Max **25 lines per function**
- Tabs only (ASCII 0x09)
- Braces on their own lines
- `(void)` for empty argument lists
- One instruction per line
- No `for`, `switch`, `goto`, or ternary
- No global variables
- Max line length: **80 characters**

Rules are **fully customizable** via prompt files.

---

## 🎯 Custom Rules & Experiments

The project is not limited to the 42 norm.

You can:
- Invent your own coding standard
- Enforce absurd or experimental rules
- Rename variables (e.g. kawaii mode)
- Use emojis or unconventional constraints

All behavior is controlled **only by the prompt**.

---

## 💼 Skills Demonstrated (For Recruiters)

- CLI tool development
- Prompt engineering
- Offline AI integration
- Deterministic systems design
- Static code analysis automation
- Defensive programming
- Strict C coding standards

---

## 🧪 Example Use Cases

- Auto-fix norm errors before submission
- CI pipeline enforcing coding standards
- Teaching strict formatting rules
- AI experimentation under constraints
- Local AI tooling without cloud dependency

---

## 📌 Philosophy

> AI should adapt to engineering constraints — not the other way around.

`norm-ai-fixer` is about **control, predictability, and robustness**, not creativity.

---

## 📄 License

MIT

---

## 👤 Author

Zibgame
