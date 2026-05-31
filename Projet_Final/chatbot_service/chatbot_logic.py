import unicodedata


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    return text


def get_professor_by_id(data, professor_id):
    for professor in data["professors"]:
        if professor["id"] == professor_id:
            return professor
    return None


def find_module(data, user_message):
    message = normalize_text(user_message)

    for module in data["modules"]:
        module_name = normalize_text(module["name"])
        module_id = normalize_text(module["id"])
        aliases = normalize_text(module.get("aliases") or "")

        if module_name in message or module_id in message:
            return module

        for alias in aliases.split(","):
            alias = alias.strip()
            if alias and alias in message:
                return module

        words = [word for word in module_name.split() if len(word) > 2]
        score = 0

        for word in words:
            if word in message:
                score += 1

        if score >= 2:
            return module

    return None


def find_professor(data, user_message):
    message = normalize_text(user_message)

    for professor in data["professors"]:
        professor_name = normalize_text(professor["name"])
        professor_id = normalize_text(professor["id"])

        if professor_name in message or professor_id in message:
            return professor

        for part in professor_name.split():
            if len(part) > 3 and part in message:
                return professor

    return None


def format_modules(data):
    response = "Voici les modules enregistrés dans CampusBot :\n\n"

    for module in data["modules"]:
        response += (
            f"- {module['name']} | Professeur : {module['professor_name']} "
            f"| Salle principale : {module['room']}\n"
        )

    return response


def format_professors(data):
    response = "Voici la liste des professeurs :\n\n"

    for professor in data["professors"]:
        response += f"- {professor['name']} | Email : {professor['email']} | Bureau : {professor['office']}\n"

    return response


def format_full_planning(data):
    response = "Voici le planning hebdomadaire de la filière Big Data :\n\n"

    for item in data["schedule"]:
        response += (
            f"- {item['day']} | {item['time']} | {item['module_id']} "
            f"| Professeur : {item['professor']} | Salle : {item['room']} "
            f"| {item['session_type']}\n"
        )

    return response


def format_planning_by_day(data, day):
    response = f"Voici le planning du {day} :\n\n"
    found = False

    for item in data["schedule"]:
        if normalize_text(item["day"]) == normalize_text(day):
            response += (
                f"- {item['time']} : {item['module_id']} "
                f"avec {item['professor']} en salle {item['room']} "
                f"({item['session_type']})\n"
            )
            found = True

    if not found:
        return f"Aucune séance trouvée pour le {day}."

    return response


def format_planning_by_module(data, module_name):
    response = f"Voici le planning du module {module_name} :\n\n"
    found = False

    for item in data["schedule"]:
        if normalize_text(item["module_id"]) == normalize_text(module_name):
            response += (
                f"- {item['day']} de {item['time']} avec {item['professor']} "
                f"en salle {item['room']} ({item['session_type']})\n"
            )
            found = True

    if not found:
        return f"Aucun planning trouvé pour le module {module_name}."

    return response


def format_exams(data):
    response = "Voici les examens programmés :\n\n"

    for exam in data["exams"]:
        response += (
            f"- {exam['day']} {exam['date']} | {exam['time']} | {exam['module']} "
            f"| Professeur : {exam['professor']} | Salle : {exam['room']} "
            f"| {exam['exam_type']}\n"
        )

    return response


def format_exam_by_module(data, module_name):
    response = f"Voici les examens du module {module_name} :\n\n"
    found = False

    for exam in data["exams"]:
        if normalize_text(exam["module"]) == normalize_text(module_name):
            response += (
                f"- {exam['day']} {exam['date']} de {exam['time']} "
                f"en salle {exam['room']} ({exam['exam_type']})\n"
            )
            found = True

    if not found:
        return f"Aucun examen trouvé pour le module {module_name}."

    return response


def format_announcements(data):
    response = "Voici les annonces importantes :\n\n"

    for announcement in data["announcements"]:
        response += (
            f"- {announcement['date']} | {announcement['title']} "
            f"({announcement['type']}) : {announcement['content']}\n"
        )

    return response


def format_general_info(data):
    response = "Voici les informations générales :\n\n"

    for info in data["general_info"]:
        response += f"- {info['title']} : {info['content']}\n"

    return response


def generate_response(user_message, data):
    message = normalize_text(user_message)

    if message.strip() == "":
        return "Veuillez écrire une question."

    if any(word in message for word in ["bonjour", "salut", "hello", "salam"]):
        return (
            "Bonjour, je suis CampusBot. "
            "Je peux vous aider à trouver les modules, professeurs, planning, salles, examens et annonces."
        )

    if any(word in message for word in ["merci", "thanks"]):
        return "Avec plaisir. Posez-moi une autre question quand vous voulez."

    if any(word in message for word in ["realise par", "realisee par", "réalisé par", "auteur", "auteurs", "cree par", "créé par"]):
        return (
            "Le projet CampusBot est réalisé par Mouad Fassi Fihri "
            "et Benlhabib Mohamed El Ghali."
        )

    if any(word in message for word in ["encadrant", "encadre", "superviseur", "prof encadrant"]):
        return "Le projet CampusBot est encadré par AMAMOU Ahmed."

    if any(word in message for word in ["objectif du projet", "but du projet", "campusbot sert a quoi", "campusbot sert à quoi"]):
        return (
            "CampusBot est un chatbot universitaire destiné aux étudiants de l'Université Euromed de Fès. "
            "Il facilite l'accès aux informations importantes comme les modules, professeurs, planning, salles, examens et annonces, "
            "surtout pendant la période des examens."
        )

    module = find_module(data, user_message)
    professor = find_professor(data, user_message)

    if any(word in message for word in ["annonce", "annonces", "jour ferie", "jours feries", "férié", "ferie", "annulation", "cours annule"]):
        return format_announcements(data)

    if any(word in message for word in ["information generale", "infos generales", "universite", "ueuromed", "euromed", "scolarite", "administration"]):
        return format_general_info(data)

    if any(word in message for word in ["modules", "liste des modules", "quels sont les modules"]):
        return format_modules(data)

    if any(word in message for word in ["professeurs", "enseignants", "liste des professeurs"]):
        return format_professors(data)

    if any(word in message for word in ["planning", "emploi du temps", "horaire", "horaires", "seance", "séance"]):
        days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

        for day in days:
            if day in message:
                return format_planning_by_day(data, day.capitalize())

        if module:
            return format_planning_by_module(data, module["name"])

        return format_full_planning(data)

    if any(word in message for word in ["examen", "examens", "exam", "exams", "controle", "contrôle", "test"]):
        if module:
            return format_exam_by_module(data, module["name"])

        return format_exams(data)

    if module:
        if any(word in message for word in ["prof", "professeur", "enseignant", "enseigne", "qui"]):
            return (
                f"Le module {module['name']} est enseigné par {module['professor_name']}. "
                f"Email : {module['professor_email']}."
            )

        if any(word in message for word in ["salle", "classe", "ou", "où"]):
            return f"Le module {module['name']} se déroule principalement en salle {module['room']}."

        if any(word in message for word in ["description", "contenu", "programme", "objectif"]):
            return f"Description du module {module['name']} : {module['description']}"

        return (
            f"Module : {module['name']}\n"
            f"Professeur : {module['professor_name']}\n"
            f"Salle principale : {module['room']}\n"
            f"Description : {module['description']}"
        )

    if professor:
        taught_modules = []

        for module_item in data["modules"]:
            if normalize_text(module_item["professor_name"]) == normalize_text(professor["name"]):
                taught_modules.append(module_item["name"])

        if any(word in message for word in ["email", "mail", "contact"]):
            return f"L'email de {professor['name']} est : {professor['email']}."

        if taught_modules:
            return (
                f"{professor['name']} enseigne : {', '.join(taught_modules)}. "
                f"Bureau : {professor['office']}."
            )

        return f"Aucun module trouvé pour {professor['name']}."

    if any(word in message for word in ["salle", "salles"]):
        rooms = sorted(set(item["room"] for item in data["schedule"]))
        response = "Voici les salles utilisées dans le planning :\n\n"
        for room in rooms:
            response += f"- {room}\n"
        return response

    return (
        "Désolé, je n'ai pas trouvé cette information dans la base officielle. "
        "Je vais utiliser OpenClaw IA pour répondre à votre question."
    )