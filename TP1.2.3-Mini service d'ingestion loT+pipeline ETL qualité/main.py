from src.server import start_server
from src.client import run_client
from src.etl_pipeline import run_etl


def menu():
    print("1. Start TCP Server")
    print("2. Run Client Simulation")
    print("3. Run ETL Pipeline")
    choice = input("Choose an option: ")

    if choice == "1":
        start_server()
    elif choice == "2":
        run_client()
    elif choice == "3":
        run_etl()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    menu()