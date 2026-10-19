import sys
from PyQt6.QtWidgets import QApplication
from gestion_zoo import GestionZoo
from interface.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    gestion = GestionZoo("animaux.csv")
    fenetre = MainWindow(gestion)
    fenetre.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()