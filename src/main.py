from dotenv import load_dotenv
from utils.environment_printer import EnvironmentPrinter

if __name__ == "__main__":
    load_dotenv(dotenv_path='.env.local')
    EnvironmentPrinter.print_environment_variables()
