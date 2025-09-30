"""
Vue principale pour la gestion des clients
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QLabel, QHeaderView, QMessageBox,
    QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from controllers.client_controller import ClientController
from views.client_form_dialog import ClientFormDialog
from utils.validators import format_telephone


class ClientsView(QWidget):
    """Vue principale de gestion des clients"""

    def __init__(self):
        super().__init__()
        self.controller = ClientController()
        self.init_ui()
        self.load_clients()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === Barre supérieure ===
        header_layout = QHBoxLayout()

        # Titre
        title = QLabel("Gestion des Clients")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Bouton Nouveau Client avec animations
        self.new_client_btn = QPushButton("+ Nouveau Client")
        self.new_client_btn.setFixedHeight(38)
        self.new_client_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_client_btn.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border: none;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 13px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
            QPushButton:pressed {
                background-color: #138d75;
            }
        """)
        self.new_client_btn.clicked.connect(self.on_new_client)
        header_layout.addWidget(self.new_client_btn)

        layout.addLayout(header_layout)

        # === Barre de recherche et filtres ===
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(15)

        # Recherche avec icône
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Rechercher par nom, email, SIRET...")
        self.search_input.setFixedHeight(36)
        self.search_input.textChanged.connect(self.on_search_changed)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #1abc9c;
                padding: 7px 11px;
            }
            QLineEdit::placeholder {
                color: #7f8c8d;
            }
        """)
        filters_layout.addWidget(self.search_input, stretch=3)

        # Filtre Type
        type_label = QLabel("Type:")
        type_label.setStyleSheet("font-weight: 600; color: #2c3e50; font-size: 13px;")
        filters_layout.addWidget(type_label)

        self.type_filter = QComboBox()
        self.type_filter.addItems(["Tous", "Particuliers", "Entreprises"])
        self.type_filter.setFixedHeight(36)
        self.type_filter.setMinimumWidth(150)
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        self.type_filter.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid #1abc9c;
            }
            QComboBox:focus {
                border: 2px solid #1abc9c;
            }
        """)
        filters_layout.addWidget(self.type_filter, stretch=1)

        # Filtre Statut
        status_label = QLabel("Statut:")
        status_label.setStyleSheet("font-weight: 600; color: #2c3e50; font-size: 13px;")
        filters_layout.addWidget(status_label)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Tous", "Actifs", "Inactifs"])
        self.status_filter.setFixedHeight(36)
        self.status_filter.setMinimumWidth(150)
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid #1abc9c;
            }
            QComboBox:focus {
                border: 2px solid #1abc9c;
            }
        """)
        filters_layout.addWidget(self.status_filter, stretch=1)

        layout.addLayout(filters_layout)

        # === Compteur avec icône ===
        self.counter_label = QLabel()
        self.counter_label.setStyleSheet("""
            color: #2c3e50;
            font-size: 13px;
            padding: 10px 0px;
            font-weight: 600;
        """)
        layout.addWidget(self.counter_label)

        # === Tableau des clients ===
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Nom / Raison sociale", "Type", "Email", "Téléphone",
            "Nb factures", "Statut", "Actions"
        ])

        # Configuration du tableau
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setMouseTracking(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        # Style premium avec alternance, hover fluide et bordures subtiles
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                gridline-color: #e8ecef;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                font-size: 12px;
                selection-background-color: transparent;
            }
            QTableWidget::item {
                padding: 10px 12px;
                border-right: none;
                border-bottom: 1px solid #e8ecef;
            }
            QTableWidget::item:hover {
                background-color: #e3f2fd;
            }
            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 14px 12px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)

        # Activer le curseur pointer sur les lignes
        self.table.viewport().setCursor(Qt.CursorShape.PointingHandCursor)

        # Définir la hauteur des lignes à 48px
        self.table.verticalHeader().setDefaultSectionSize(48)
        self.table.verticalHeader().setMinimumSectionSize(48)

        # Ajuster les colonnes avec largeurs optimisées
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        for column in (1, 4, 5, 6):
            header_item = self.table.horizontalHeaderItem(column)
            if header_item is not None:
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

        # Définir les largeurs optimales finales
        self.table.setColumnWidth(0, 220)  # Nom/Raison sociale
        self.table.setColumnWidth(1, 110)  # Type
        # Colonne 2 (Email) en Stretch avec min 250px
        self.table.setColumnWidth(3, 120)  # Téléphone
        self.table.setColumnWidth(4, 90)   # Nb factures
        self.table.setColumnWidth(5, 85)   # Statut (réduit)
        self.table.setColumnWidth(6, 70)   # Actions (2 boutons 26px)

        # Double-clic pour modifier
        self.table.doubleClicked.connect(self.on_row_double_clicked)

        layout.addWidget(self.table)

    def load_clients(self):
        """Charge tous les clients dans le tableau"""
        clients = self.controller.get_all_clients(actif_only=False)
        self.populate_table(clients)

    def populate_table(self, clients):
        """Remplit le tableau avec la liste des clients"""
        self.table.setRowCount(0)

        for client in clients:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Colonne 0: Nom / Raison sociale
            nom_item = QTableWidgetItem(client.nom_complet)
            nom_item.setData(Qt.ItemDataRole.UserRole, client.id)
            self.table.setItem(row, 0, nom_item)

            # Colonne 1: Type (badge coloré)
            type_widget = self.create_type_badge(client.type)
            self.table.setCellWidget(row, 1, type_widget)

            # Colonne 2: Email
            self.table.setItem(row, 2, QTableWidgetItem(client.email or ""))

            # Colonne 3: Téléphone
            tel = format_telephone(client.telephone) if client.telephone else ""
            tel_item = QTableWidgetItem(tel)
            tel_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, tel_item)

            # Colonne 4: Nb factures (badge)
            stats = self.controller.get_client_statistics(client.id)
            factures_widget = self.create_factures_badge(stats['nb_factures'])
            self.table.setCellWidget(row, 4, factures_widget)

            # Colonne 5: Statut (badge coloré)
            status_widget = self.create_status_badge(client.actif)
            self.table.setCellWidget(row, 5, status_widget)

            # Colonne 6: Actions
            actions_widget = self.create_actions_widget(client.id)
            self.table.setCellWidget(row, 6, actions_widget)

        # Mettre à jour le compteur
        self.update_counter(clients)

    def create_type_badge(self, type_client):
        """Crée un badge coloré uniforme pour le type de client"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-bottom: 1px solid #e8ecef;
            }
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Particulier" if type_client == "particulier" else "Entreprise")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if type_client == "particulier":
            color = "#3498db"  # Bleu
        else:
            color = "#e67e22"  # Orange

        label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 6px 14px;
                border-radius: 15px;
                font-size: 11px;
                font-weight: bold;
                min-width: 90px;
                max-width: 90px;
            }}
        """)
        label.setFixedHeight(26)

        layout.addWidget(label)
        return widget

    def create_status_badge(self, actif):
        """Crée un badge coloré compact pour le statut"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-bottom: 1px solid #e8ecef;
            }
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Actif" if actif else "Inactif")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setCursor(Qt.CursorShape.PointingHandCursor)

        color = "#27ae60" if actif else "#95a5a6"  # Vert ou Gris

        label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 5px 10px;
                border-radius: 13px;
                font-size: 10px;
                font-weight: bold;
                min-width: 60px;
                max-width: 60px;
            }}
        """)
        label.setFixedHeight(24)

        layout.addWidget(label)
        return widget

    def create_factures_badge(self, nb_factures):
        """Crée un badge élégant pour le nombre de factures"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-bottom: 1px solid #e8ecef;
            }
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel(str(nb_factures))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Badge gris pour 0, bleu pour >0
        if nb_factures == 0:
            color = "#95a5a6"  # Gris
            text_color = "white"
        else:
            color = "#3498db"  # Bleu
            text_color = "white"

        label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: {text_color};
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
                min-width: 28px;
            }}
        """)
        label.setFixedHeight(24)

        layout.addWidget(label)
        return widget

    def create_actions_widget(self, client_id):
        """Crée les boutons d'action compacts pour une ligne"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-bottom: 1px solid #e8ecef;
            }
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)  # Espacement ultra-serré
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Bouton Modifier (26x26px ultra-compact)
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(26, 26)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setToolTip("Modifier ce client")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
            QPushButton:pressed {
                background-color: #138d75;
            }
        """)
        edit_btn.clicked.connect(lambda: self.on_edit_client(client_id))
        layout.addWidget(edit_btn)

        # Bouton Supprimer (26x26px ultra-compact)
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(26, 26)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setToolTip("Supprimer ce client")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        delete_btn.clicked.connect(lambda: self.on_delete_client(client_id))
        layout.addWidget(delete_btn)

        return widget

    def update_counter(self, clients):
        """Met à jour le compteur de clients avec icône"""
        total = len(clients)
        actifs = sum(1 for c in clients if c.actif)
        self.counter_label.setText(f"👥  {total} client(s)  •  {actifs} actif(s)")

    def on_new_client(self):
        """Ouvre le formulaire de création de client"""
        dialog = ClientFormDialog(self)
        dialog.client_saved.connect(self.load_clients)
        dialog.exec()

    def on_edit_client(self, client_id):
        """Ouvre le formulaire de modification de client"""
        dialog = ClientFormDialog(self, client_id=client_id)
        dialog.client_saved.connect(self.load_clients)
        dialog.exec()

    def on_delete_client(self, client_id):
        """Supprime un client après confirmation"""
        client = self.controller.get_client_by_id(client_id)
        if not client:
            return

        # Confirmation
        reply = QMessageBox.question(
            self,
            "Confirmer la suppression",
            f"Voulez-vous vraiment supprimer le client '{client.nom_complet}' ?\n\n"
            f"Cette action est irréversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.delete_client(client_id)

            if success:
                QMessageBox.information(self, "Succès", message)
                self.load_clients()
            else:
                QMessageBox.warning(self, "Erreur", message)

    def on_row_double_clicked(self, index):
        """Gère le double-clic sur une ligne"""
        row = index.row()
        client_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.on_edit_client(client_id)

    def on_search_changed(self):
        """Applique la recherche en temps réel"""
        self.apply_filters()

    def apply_filters(self):
        """Applique les filtres de recherche et de type/statut"""
        search_query = self.search_input.text().strip()

        # Type
        type_text = self.type_filter.currentText()
        type_filter = None
        if type_text == "Particuliers":
            type_filter = "particulier"
        elif type_text == "Entreprises":
            type_filter = "entreprise"

        # Statut
        status_text = self.status_filter.currentText()
        actif_filter = None
        if status_text == "Actifs":
            actif_filter = True
        elif status_text == "Inactifs":
            actif_filter = False

        # Rechercher
        clients = self.controller.search_clients(search_query, type_filter, actif_filter)
        self.populate_table(clients)