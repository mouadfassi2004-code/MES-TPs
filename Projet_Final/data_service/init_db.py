from database import init_database

init_database(reset=True)

print("Base de données campusbot.db recréée avec succès.")
print("Tables créées : students, professors, modules, planning, exams, announcements, general_info.")
print("Données initiales insérées avec succès.")