import yaml
import os
import json
import subprocess
import urllib.request

DEBUG_LIMIT = 4000


def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def overwrite_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError:
        return False


def split_header_42(content):
    lines = content.splitlines()
    if len(lines) < 11:
        return None, None
    return "\n".join(lines[:11]), "\n".join(lines[11:])


def run_norminette(path, cmd):
    try:
        result = subprocess.run(
            [cmd, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return result.stdout.strip()
    except OSError:
        return "norminette failed"


def extract_result_strict(text):
    start = text.find("<RESULT>")
    end = text.find("</RESULT>")

    if start == -1 or end == -1 or start >= end:
        return None

    content = text[start + 8:end].strip()

    if not content:
        return None
    if "```" in content:
        return None

    return content


def call_ollama(prompt, model, url):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }


    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
        return data.get("response", "")


def norm_ai_fixer(file_path, config):
    original = load_file(file_path)
    if original is None:
        print("❌ lecture fichier impossible")
        return

    header, code = split_header_42(original)
    if header is None:
        print("❌ header 42 invalide")
        return

    norm_errors = ""
    if config["norminette"]["use_norminette"]:
        norm_errors = run_norminette(
            file_path,
            config["norminette"]["norminette_cmd"]
        )

    prompt_template = load_file(config["ollama"]["prompt_file"])
    if prompt_template is None:
        print("❌ prompt introuvable")
        return

    prompt = (
        prompt_template
        .replace("{{HEADER}}", header)
        .replace("{{CODE}}", code)
        .replace("{{NORM_ERRORS}}", norm_errors)
    )

    print("\n[DEBUG] prompt envoyé:")
    print(prompt[:DEBUG_LIMIT])

    response = call_ollama(
        prompt,
        config["ollama"]["model"],
        config["ollama"]["url"]
    )

    print("\n[DEBUG] réponse brute IA:")
    print(response[:DEBUG_LIMIT])

    new_code = extract_result_strict(response)
import yaml
import os
import json
import subprocess
import urllib.request
import sys

DEBUG_LIMIT = 4000


def load_file(path):
	try:
		with open(path, "r", encoding="utf-8") as file:
			return file.read()
	except OSError:
		return None


def overwrite_file(path, content):
	try:
		with open(path, "w", encoding="utf-8") as file:
			file.write(content)
		return True
	except OSError:
		return False


def split_header_42(content):
	lines = content.splitlines()
	if len(lines) < 11:
		return None, None
	return "\n".join(lines[:11]), "\n".join(lines[11:])


def run_norminette(path, command):
	try:
		result = subprocess.run(
			[command, path],
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			text=True
		)
		return result.stdout.strip()
	except OSError:
		return "norminette failed"


def extract_result_strict(text):
	start = text.find("<RESULT>")
	end = text.find("</RESULT>")

	if start == -1 or end == -1 or start >= end:
		return None

	content = text[start + 8:end].strip()

	if not content:
		return None
	if "```" in content:
		return None

	return content


def call_ollama(prompt, model, url):
	payload = {
		"model": model,
		"prompt": prompt,
		"stream": False
	}

	request = urllib.request.Request(
		url,
		data=json.dumps(payload).encode("utf-8"),
		headers={"Content-Type": "application/json"}
	)

	with urllib.request.urlopen(request) as response:
		data = json.loads(response.read().decode("utf-8"))
		return data.get("response", "")


def norm_ai_fixer(file_path, config, debug_enabled):
	original = load_file(file_path)
	if original is None:
		print("Error: unable to read file")
		return

	header, code = split_header_42(original)
	if header is None:
		print("Error: invalid 42 header")
		return

	norm_errors = ""
	if config["norminette"]["use_norminette"]:
		norm_errors = run_norminette(
			file_path,
			config["norminette"]["norminette_cmd"]
		)

	prompt_template = load_file(config["ollama"]["prompt_file"])
	if prompt_template is None:
		print("Error: prompt file not found")
		return

	prompt = (
		prompt_template
		.replace("{{HEADER}}", header)
		.replace("{{CODE}}", code)
		.replace("{{NORM_ERRORS}}", norm_errors)
	)

	if debug_enabled:
		print("\n[DEBUG] Prompt sent to AI:")
		print(prompt[:DEBUG_LIMIT])

	response = call_ollama(
		prompt,
		config["ollama"]["model"],
		config["ollama"]["url"]
	)

	if debug_enabled:
		print("\n[DEBUG] Raw AI response:")
		print(response[:DEBUG_LIMIT])

	new_code = extract_result_strict(response)
	if new_code is None:
		print("Error: invalid AI output format")
		return

	overwrite_file(file_path, header + "\n" + new_code + "\n")

	if debug_enabled:
		print("File successfully modified")
	else:
		print("Code modified successfully")


def main():
	debug_enabled = "--debug" in sys.argv

	config = yaml.safe_load(load_file("config.yaml"))
	if config is None:
		print("Error: invalid config.yaml")
		return

	file_path = input("Choose file: ").strip()
	if not os.path.isfile(file_path):
		print("Error: file not found")
		return

	norm_ai_fixer(file_path, config, debug_enabled)


if __name__ == "__main__":
	main()

