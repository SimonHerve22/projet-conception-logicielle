from utils.log_init import initialiser_logs
from utils.reset_database import ResetDatabase


if __name__ == "__main__":
    initialiser_logs("Application")
    ResetDatabase().lancer()
