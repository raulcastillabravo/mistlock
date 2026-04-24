from dotenv import load_dotenv

from src.managers.user_status import Status, UserStatus

load_dotenv()


def main() -> None:
    username = "raulcastillabravo"
    user_status = UserStatus(username)

    print(f"--- Setting status for user: {username} ---")
    user_status.set_status(Status.AVAILABLE)

    current_status = user_status.get_status()

    print(f"\nUser: {username}")
    print(f"Current Status: {current_status.value if current_status else 'None'}")

    print("\n✓ Done! You can verify the data in Redis using the CLI.")


if __name__ == "__main__":
    main()