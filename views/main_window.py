"""
Fenêtre principale de l'application
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QStackedWidget, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from config import APP_NAME, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application avec navigation latérale"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        # Configuration de la fenêtre
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal (horizontal : menu + contenu)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Créer le menu latéral
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Créer la zone de contenu avec QStackedWidget
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #f5f5f5;")
        main_layout.addWidget(self.content_stack)

        # Créer les vues placeholder
        self.create_views()

        # Afficher le tableau de bord par défaut
        self.content_stack.setCurrentIndex(0)

    def create_sidebar(self):
        """Crée le menu latéral de navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 2px solid #34495e;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 15px 20px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
            QPushButton[active="true"] {
                background-color: #1abc9c;
                border-left: 4px solid #16a085;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # En-tête
        header = QLabel("Facturation Coach Pro")
        header.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 20px;
            background-color: #1abc9c;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Boutons de navigation
        self.nav_buttons = []

        menu_items = [
            ("🏠  Tableau de bord", 0),
            ("👥  Clients", 1),
            ("📋  Prestations", 2),
            ("📄  Devis", 3),
            ("🧾  Factures", 4),
            ("💰  Avoirs", 5),
            ("⚙️  Paramètres", 6),
        ]

        for text, index in menu_items:
            btn = QPushButton(text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self.change_view(idx))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        # Espaceur pour pousser les boutons vers le haut
        layout.addStretch()

        # Bouton version en bas
        version_label = QLabel("Version 1.0.0")
        version_label.setStyleSheet("""
            color: #95a5a6;
            font-size: 11px;
            padding: 10px;
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Marquer le premier bouton comme actif
        self.nav_buttons[0].setProperty("active", "true")

        return sidebar

    def create_views(self):
        """Crée les vues pour chaque section"""
        # Import des vues
        from views.clients_view import ClientsView

        # Tableau de bord (placeholder)
        self.content_stack.addWidget(self.create_placeholder_view("Tableau de bord"))

        # Clients (vue complète)
        self.clients_view = ClientsView()
        self.content_stack.addWidget(self.clients_view)

        # Autres sections (placeholders)
        for view_name in ["Prestations", "Devis", "Factures", "Avoirs", "Paramètres"]:
            placeholder = self.create_placeholder_view(view_name)
            self.content_stack.addWidget(placeholder)

    def create_placeholder_view(self, title):
        """Crée une vue placeholder avec un titre"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titre
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Sous-titre
        subtitle = QLabel("Cette section sera implémentée prochainement")
        subtitle.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(subtitle)

        return widget

    def change_view(self, index):
        """Change la vue affichée et met à jour le bouton actif"""
        # Retirer l'état actif de tous les boutons
        for btn in self.nav_buttons:
            btn.setProperty("active", "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Marquer le bouton cliqué comme actif
        self.nav_buttons[index].setProperty("active", "true")
        self.nav_buttons[index].style().unpolish(self.nav_buttons[index])
        self.nav_buttons[index].style().polish(self.nav_buttons[index])

        # Changer la vue
        self.content_stack.setCurrentIndex(index)