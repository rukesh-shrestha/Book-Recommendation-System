import os

ROOT = os.path.dirname(os.path.abspath(__file__))
print(ROOT)
# /home/rukesh/Documents/djangobegineers/Recomendation-System/myrecommendationsystem
DATABASE_PATH = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/myrecommendationsystem/db.sqlite3'

