import subprocess
import json
import shutil


def find_openclaw_command():
    return shutil.which("openclaw.cmd") or shutil.which("openclaw")


def extract_openclaw_text(output):
    try:
        start_index = output.find("{")
        end_index = output.rfind("}")

        if start_index != -1 and end_index != -1:
            json_text = output[start_index:end_index + 1]
            data = json.loads(json_text)

            outputs = data.get("outputs", [])
            if outputs and "text" in outputs[0]:
                return outputs[0]["text"]

        return output

    except Exception:
        return output


def ask_openclaw(user_message):
    openclaw_command = find_openclaw_command()

    if openclaw_command is None:
        return (
            "OpenClaw n'est pas reconnu sur ce PC. "
            "Vérifiez avec : openclaw.cmd --version"
        )

    if not user_message or user_message.strip() == "":
        return "Veuillez écrire une question."

    prompt = f"""
Tu es CampusBot, un assistant universitaire intelligent destiné aux étudiants de l'Université Euromed de Fès.

Tu réponds aux questions générales ou complexes concernant :
les études, les révisions, les examens, la programmation, les projets informatiques,
les applications réparties, les API REST, FastAPI, les microservices, le cloud,
l'algorithmique, le traitement d'image, l'infographie, les modèles de couleur,
l'IHM et les méthodes de travail.

Règles :
- Réponds toujours en français.
- Réponds de façon claire, simple et pédagogique.
- Ne donne pas une réponse trop longue.
- Ne dis jamais que tu es ChatGPT.
- Tu es CampusBot.
- Si la question demande une information officielle précise comme planning, professeurs, modules, examens ou salles, explique que ces informations sont gérées par la base de données CampusBot.

Question de l'étudiant : {user_message}
"""

    prompt = " ".join(prompt.split())

    command = [
        openclaw_command,
        "infer",
        "model",
        "run",
        f"--prompt={prompt}",
        "--json"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120
        )

        if result.returncode != 0:
            error_message = result.stderr.strip() or result.stdout.strip()
            return f"OpenClaw a rencontré une erreur.\n\nDétail : {error_message}"

        return extract_openclaw_text(result.stdout.strip())

    except subprocess.TimeoutExpired:
        return (
            "OpenClaw a pris trop de temps pour répondre. "
            "Réessayez avec une question plus courte."
        )

    except Exception as error:
        return f"Erreur lors de l'appel à OpenClaw : {str(error)}"