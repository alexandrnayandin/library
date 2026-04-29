from dal.db import init_db
from ui.console_ui import ConsoleUI


def main():
    init_db()
    app = ConsoleUI()
    app.run()


if __name__ == "__main__":
    main()
