import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "campusbot.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def fetch_all(query, params=()):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def fetch_one(query, params=()):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None


def init_database(reset=False):
    connection = get_connection()
    cursor = connection.cursor()

    if reset:
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("DROP TABLE IF EXISTS professors")
        cursor.execute("DROP TABLE IF EXISTS modules")
        cursor.execute("DROP TABLE IF EXISTS planning")
        cursor.execute("DROP TABLE IF EXISTS exams")
        cursor.execute("DROP TABLE IF EXISTS announcements")
        cursor.execute("DROP TABLE IF EXISTS general_info")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professors (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            office TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            aliases TEXT,
            professor_id TEXT NOT NULL,
            room TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (professor_id) REFERENCES professors(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            time TEXT NOT NULL,
            module_id TEXT NOT NULL,
            professor_id TEXT NOT NULL,
            room TEXT NOT NULL,
            group_name TEXT,
            session_type TEXT NOT NULL,
            FOREIGN KEY (module_id) REFERENCES modules(id),
            FOREIGN KEY (professor_id) REFERENCES professors(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            module_id TEXT NOT NULL,
            professor_id TEXT NOT NULL,
            room TEXT NOT NULL,
            group_name TEXT,
            exam_type TEXT NOT NULL,
            FOREIGN KEY (module_id) REFERENCES modules(id),
            FOREIGN KEY (professor_id) REFERENCES professors(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS general_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        students = [
            ("Mouad Fassi Fihri", "mouad@ueuromed.org", "1234"),
            ("Benlhabib Mohamed El Ghali", "ghali@ueuromed.org", "1234"),
            ("Étudiant Test", "student@ueuromed.org", "1234")
        ]
        cursor.executemany("""
            INSERT INTO students (full_name, email, password)
            VALUES (?, ?, ?)
        """, students)

    cursor.execute("SELECT COUNT(*) FROM professors")
    if cursor.fetchone()[0] == 0:
        professors = [
            ("elhili", "EL HILALI ALAOUI Ahmed", "elhili@ueuromed.org", "Bureau pédagogique"),
            ("moutik", "MOUTIK Oumaima", "moutik@ueuromed.org", "Bureau pédagogique"),
            ("elalami", "ELALAMI Abdelmajid", "elalami@ueuromed.org", "Bureau pédagogique"),
            ("amamou", "AMAMOU Ahmed", "amamou@ueuromed.org", "Bureau pédagogique"),
            ("majikumna", "MAJIKUMNA Kaloma Usman", "majikumna@ueuromed.org", "Bureau pédagogique"),
            ("workneh", "WORKNEH Abebaw Degu", "workneh@ueuromed.org", "Bureau pédagogique"),
            ("bouleft", "BOULEFT Yousra", "bouleft@ueuromed.org", "Bureau pédagogique"),
            ("bella", "BELLA Oussama", "bella@ueuromed.org", "Bureau pédagogique")
        ]
        cursor.executemany("""
            INSERT INTO professors (id, name, email, office)
            VALUES (?, ?, ?, ?)
        """, professors)

    cursor.execute("SELECT COUNT(*) FROM modules")
    if cursor.fetchone()[0] == 0:
        modules = [
            (
                "applications_reparties",
                "Calcul parallèle et applications réparties",
                "applications reparties,application repartie,calcul parallele,calcul parallèle",
                "amamou",
                "B4.1.65",
                "Module consacré aux applications réparties, au calcul parallèle, aux architectures distribuées et à la communication entre services."
            ),
            (
                "infographies",
                "Infographies",
                "infographie,infographies",
                "elalami",
                "B4.1.65",
                "Module consacré aux bases de l'infographie, aux images numériques, aux couleurs et aux représentations visuelles."
            ),
            (
                "traitement_image",
                "Traitement d'image",
                "traitement dimage,traitement image,traitement d'image",
                "moutik",
                "B4.1.65",
                "Module consacré au filtrage, seuillage, détection de contours, morphologie mathématique et analyse d'images."
            ),
            (
                "advanced_algorithmics",
                "Advanced Algorithmics / Algorithmique avancé",
                "advanced algorithmics,algorithmique avance,algorithmique avancé",
                "workneh",
                "B4.1.65",
                "Module consacré aux algorithmes avancés, à la complexité, aux graphes et à la programmation dynamique."
            ),
            (
                "recherche_operationnelle",
                "Recherche Opérationnelle",
                "recherche operationnelle,recherche opérationnelle,recherche operationnel,ro",
                "elhili",
                "B4.1.65",
                "Module consacré à l'optimisation, la programmation linéaire, le simplexe et les problèmes de décision."
            ),
            (
                "ihm",
                "Interfaces hommes machines",
                "interface homme machine,interfaces hommes machines,ihm",
                "majikumna",
                "B4.1.65",
                "Module consacré à l'interaction homme-machine, l'ergonomie, les interfaces et l'expérience utilisateur."
            ),
            (
                "francais",
                "Français",
                "francais,français",
                "bella",
                "B2.1.41",
                "Module de communication en langue française."
            )
        ]
        cursor.executemany("""
            INSERT INTO modules (id, name, aliases, professor_id, room, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, modules)

    cursor.execute("SELECT COUNT(*) FROM planning")
    if cursor.fetchone()[0] == 0:
        planning = [
            ("Lundi", "08:30 - 10:30", "recherche_operationnelle", "elhili", "B101", "EIDIA_CI_1A_BDA1", "Cours"),
            ("Lundi", "14:00 - 16:00", "infographies", "elalami", "B102", "EIDIA_CI_1A_BDA1", "Cours"),

            ("Mardi", "08:30 - 10:30", "traitement_image", "moutik", "B103", "EIDIA_CI_1A_BDA1", "Cours"),
            ("Mardi", "10:31 - 12:31", "traitement_image", "moutik", "B103", "EIDIA_CI_1A_BDA1", "TP/TD"),
            ("Mardi", "14:00 - 16:00", "applications_reparties", "amamou", "B104", "EIDIA_CI_1A_BDA1", "Cours"),
            ("Mardi", "16:01 - 18:01", "applications_reparties", "amamou", "B104", "EIDIA_CI_1A_BDA1", "TP/TD"),

            ("Mercredi", "08:30 - 10:30", "ihm", "majikumna", "B105", "EIDIA_CI_1A_BDA1", "Cours"),
            ("Mercredi", "10:31 - 12:31", "ihm", "majikumna", "B105", "EIDIA_CI_1A_BDA1", "TP/TD"),

            ("Jeudi", "08:30 - 10:30", "advanced_algorithmics", "workneh", "B106", "EIDIA_CI_1A_BDA1", "Cours"),
            ("Jeudi", "10:31 - 12:31", "advanced_algorithmics", "workneh", "B106", "EIDIA_CI_1A_BDA1", "TP/TD"),
            ("Jeudi", "14:00 - 16:00", "recherche_operationnelle", "bouleft", "B107", "EIDIA_CI_1A_BDA1", "TP/TD"),
            ("Jeudi", "16:01 - 18:01", "francais", "bella", "B108", "EIDIA_CI_1A_BDA1", "Cours"),

            ("Vendredi", "14:30 - 16:00", "recherche_operationnelle", "bouleft", "B109", "EIDIA_CI_1A_BDA1", "TP/TD"),

            ("Samedi", "08:30 - 10:30", "infographies", "elalami", "B110", "EIDIA_CI_1A_BDA1", "Cours")
        ]
        cursor.executemany("""
            INSERT INTO planning (day, time, module_id, professor_id, room, group_name, session_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, planning)

    cursor.execute("SELECT COUNT(*) FROM exams")
    if cursor.fetchone()[0] == 0:
        exams = [
            ("Lundi", "08 Juin 2026", "08:30 - 10:30", "recherche_operationnelle", "elhili", "B101", "EIDIA_CI_1A_BDA1", "Examen final"),
            ("Lundi", "08 Juin 2026", "14:00 - 15:00", "infographies", "elalami", "B102", "EIDIA_CI_1A_BDA1", "Examen final"),
            ("Lundi", "08 Juin 2026", "15:01 - 18:01", "infographies", "elalami", "B102", "EIDIA_CI_1A_BDA1", "Examen final"),

            ("Mardi", "09 Juin 2026", "08:30 - 10:30", "traitement_image", "moutik", "B103", "EIDIA_CI_1A_BDA1", "Examen final"),
            ("Mardi", "09 Juin 2026", "14:00 - 16:00", "applications_reparties", "amamou", "B104", "EIDIA_CI_1A_BDA1", "Examen final"),

            ("Mercredi", "10 Juin 2026", "08:30 - 10:30", "advanced_algorithmics", "workneh", "B106", "EIDIA_CI_1A_BDA1", "Examen final"),
            ("Mercredi", "10 Juin 2026", "10:31 - 12:31", "ihm", "majikumna", "B105", "EIDIA_CI_1A_BDA1", "Examen final"),

            ("Jeudi", "11 Juin 2026", "16:01 - 18:01", "francais", "bella", "B108", "EIDIA_CI_1A_BDA1", "Examen final")
        ]
        cursor.executemany("""
            INSERT INTO exams (day, date, time, module_id, professor_id, room, group_name, exam_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, exams)

    cursor.execute("SELECT COUNT(*) FROM announcements")
    if cursor.fetchone()[0] == 0:
        announcements = [
            (
                "Période des examens",
                "La période des examens aura lieu pendant la semaine du 8 au 14 Juin 2026. Les étudiants doivent vérifier les salles et les horaires.",
                "01 Juin 2026",
                "Examens"
            ),
            (
                "Jour férié",
                "L'université informe les étudiants qu'un jour férié peut entraîner un changement dans le planning des cours.",
                "À confirmer",
                "Jour férié"
            ),
            (
                "Annulation de cours",
                "En cas d'absence d'un professeur ou de contrainte administrative, une annonce d'annulation sera publiée sur CampusBot.",
                "À confirmer",
                "Annulation"
            ),
            (
                "Révision avant examens",
                "Les étudiants sont encouragés à réviser les modules principaux : Recherche Opérationnelle, Traitement d'image, Algorithmique avancé et Applications réparties.",
                "05 Juin 2026",
                "Révision"
            )
        ]
        cursor.executemany("""
            INSERT INTO announcements (title, content, date, type)
            VALUES (?, ?, ?, ?)
        """, announcements)

    cursor.execute("SELECT COUNT(*) FROM general_info")
    if cursor.fetchone()[0] == 0:
        general_info = [
            (
                "Université",
                "CampusBot est destiné aux étudiants de l'Université Euromed de Fès."
            ),
            (
                "Objectif",
                "Le projet aide les étudiants à accéder rapidement aux modules, professeurs, planning, examens, salles et annonces."
            ),
            (
                "Encadrant",
                "Le projet CampusBot est encadré par AMAMOU Ahmed."
            ),
            (
                "Réalisé par",
                "Le projet est réalisé par Mouad Fassi Fihri et Benlhabib Mohamed El Ghali."
            )
        ]
        cursor.executemany("""
            INSERT INTO general_info (title, content)
            VALUES (?, ?)
        """, general_info)

    connection.commit()
    connection.close()


def get_student_by_credentials(email, password):
    return fetch_one("""
        SELECT id, full_name, email
        FROM students
        WHERE LOWER(email) = LOWER(?) AND password = ?
    """, (email, password))


def get_students():
    return fetch_all("SELECT id, full_name, email FROM students ORDER BY full_name")


def get_professors():
    return fetch_all("SELECT id, name, email, office FROM professors ORDER BY name")


def get_modules():
    return fetch_all("""
        SELECT 
            m.id,
            m.name,
            m.aliases,
            m.room,
            m.description,
            p.id AS professor_id,
            p.name AS professor_name,
            p.email AS professor_email
        FROM modules m
        JOIN professors p ON m.professor_id = p.id
        ORDER BY m.name
    """)


def get_planning():
    return fetch_all("""
        SELECT 
            pl.id,
            pl.day,
            pl.time,
            m.id AS module_id,
            m.name AS module,
            p.name AS professor,
            pl.room,
            pl.group_name,
            pl.session_type
        FROM planning pl
        JOIN modules m ON pl.module_id = m.id
        JOIN professors p ON pl.professor_id = p.id
        ORDER BY
            CASE pl.day
                WHEN 'Lundi' THEN 1
                WHEN 'Mardi' THEN 2
                WHEN 'Mercredi' THEN 3
                WHEN 'Jeudi' THEN 4
                WHEN 'Vendredi' THEN 5
                WHEN 'Samedi' THEN 6
                WHEN 'Dimanche' THEN 7
                ELSE 8
            END,
            pl.time
    """)


def get_exams():
    return fetch_all("""
        SELECT 
            e.id,
            e.day,
            e.date,
            e.time,
            m.id AS module_id,
            m.name AS module,
            p.name AS professor,
            e.room,
            e.group_name,
            e.exam_type
        FROM exams e
        JOIN modules m ON e.module_id = m.id
        JOIN professors p ON e.professor_id = p.id
        ORDER BY e.id
    """)


def get_announcements():
    return fetch_all("""
        SELECT id, title, content, date, type
        FROM announcements
        ORDER BY id DESC
    """)


def get_general_info():
    return fetch_all("""
        SELECT id, title, content
        FROM general_info
        ORDER BY id
    """)