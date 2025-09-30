"""
Formulaire de création/modification de client (Dialog)
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLineEdit, QTextEdit, QRadioButton, QButtonGroup, QPushButton,
    QLabel, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from controllers.client_controller import ClientController
from models import Client
from utils.validators import (
    validate_email, validate_siret, validate_code_postal,
    validate_telephone, format_telephone, format_siret
)


class ClientFormDialog(QDialog):
    """Formulaire modal pour créer ou modifier un client"""

    # Signal émis quand le client est sauvegardé
    client_saved = pyqtSignal()

    def __init__(self, parent=None, client_id=None):
        """
        Initialise le formulaire.

        Args:
            parent: Widget parent
            client_id: ID du client à modifier (None pour création)
        """
        super().__init__(parent)
        self.controller = ClientController()
        self.client_id = client_id
        self.client = None

        # Charger le client si modification
        if client_id:
            self.client = self.controller.get_client_by_id(client_id)

        self.init_ui()

        # Pré-remplir le formulaire si modification
        if self.client:
            self.fill_form()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        # Configuration de la fenêtre
        title = "Modifier Client" if self.client_id else "Nouveau Client"
        self.setWindowTitle(title)
        self.setMinimumWidth(600)
        self.setModal(True)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Titre
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # === Section 1 : Type de client ===
        type_group = QGroupBox("Type de client")
        type_layout = QHBoxLayout()

        self.radio_particulier = QRadioButton("Particulier")
        self.radio_entreprise = QRadioButton("Entreprise")

        self.type_button_group = QButtonGroup()
        self.type_button_group.addButton(self.radio_particulier)
        self.type_button_group.addButton(self.radio_entreprise)

        self.radio_particulier.setChecked(True)
        self.radio_particulier.toggled.connect(self.on_type_changed)

        type_layout.addWidget(self.radio_particulier)
        type_layout.addWidget(self.radio_entreprise)
        type_layout.addStretch()
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # === Section 2 : Identité ===
        identity_group = QGroupBox("Identité")
        form_layout = QFormLayout()

        # Champs Particulier
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.nom_label = QLabel("Nom *")
        self.prenom_label = QLabel("Prénom")

        form_layout.addRow(self.nom_label, self.create_validated_field(self.nom_input))
        form_layout.addRow(self.prenom_label, self.prenom_input)

        # Champs Entreprise
        self.raison_sociale_input = QLineEdit()
        self.siret_input = QLineEdit()
        self.siret_input.setMaxLength(17)  # 14 chiffres + 3 espaces
        self.raison_sociale_label = QLabel("Raison sociale *")
        self.siret_label = QLabel("SIRET *")

        # Indicateurs de validation
        self.siret_indicator = QLabel()

        siret_container = QWidget()
        siret_layout = QHBoxLayout(siret_container)
        siret_layout.setContentsMargins(0, 0, 0, 0)
        siret_layout.addWidget(self.siret_input)
        siret_layout.addWidget(self.siret_indicator)

        self.raison_sociale_row = form_layout.rowCount()
        form_layout.addRow(self.raison_sociale_label, self.create_validated_field(self.raison_sociale_input))
        self.siret_row = form_layout.rowCount()
        form_layout.addRow(self.siret_label, siret_container)

        # Connecter les validations en temps réel
        self.siret_input.textChanged.connect(self.validate_siret_field)

        identity_group.setLayout(form_layout)
        layout.addWidget(identity_group)

        # === Section 3 : Coordonnées ===
        contact_group = QGroupBox("Coordonnées")
        contact_layout = QFormLayout()

        self.adresse_input = QTextEdit()
        self.adresse_input.setMaximumHeight(60)
        self.code_postal_input = QLineEdit()
        self.code_postal_input.setMaxLength(5)
        self.ville_input = QLineEdit()
        self.email_input = QLineEdit()
        self.telephone_input = QLineEdit()

        # Indicateurs de validation
        self.email_indicator = QLabel()
        self.cp_indicator = QLabel()
        self.tel_indicator = QLabel()

        # Conteneurs avec indicateurs
        email_container = self.create_field_with_indicator(self.email_input, self.email_indicator)
        cp_container = self.create_field_with_indicator(self.code_postal_input, self.cp_indicator)
        tel_container = self.create_field_with_indicator(self.telephone_input, self.tel_indicator)

        contact_layout.addRow("Adresse *", self.create_validated_field(self.adresse_input))
        contact_layout.addRow("Code postal *", cp_container)
        contact_layout.addRow("Ville *", self.create_validated_field(self.ville_input))
        contact_layout.addRow("Email *", email_container)
        contact_layout.addRow("Téléphone", tel_container)

        # Connecter les validations en temps réel
        self.email_input.textChanged.connect(self.validate_email_field)
        self.code_postal_input.textChanged.connect(self.validate_cp_field)
        self.telephone_input.textChanged.connect(self.validate_tel_field)

        contact_group.setLayout(contact_layout)
        layout.addWidget(contact_group)

        # === Section 4 : Notes ===
        notes_group = QGroupBox("Informations complémentaires")
        notes_layout = QFormLayout()

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Notes internes sur le client...")

        notes_layout.addRow("Notes", self.notes_input)
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)

        # === Boutons ===
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setFixedWidth(120)
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.setFixedWidth(120)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.save_button.clicked.connect(self.save_client)

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        layout.addLayout(buttons_layout)

        # Afficher les champs selon le type
        self.on_type_changed()

    def create_validated_field(self, widget):
        """Crée un conteneur pour un champ avec indicateur d'erreur"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(widget)
        return container

    def create_field_with_indicator(self, field, indicator):
        """Crée un conteneur avec champ et indicateur côte à côte"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(field)
        layout.addWidget(indicator)
        return container

    def on_type_changed(self):
        """Gère le changement de type de client"""
        is_particulier = self.radio_particulier.isChecked()

        # Afficher/masquer les champs selon le type
        self.nom_label.setVisible(is_particulier)
        self.nom_input.setVisible(is_particulier)
        self.prenom_label.setVisible(is_particulier)
        self.prenom_input.setVisible(is_particulier)

        self.raison_sociale_label.setVisible(not is_particulier)
        self.raison_sociale_input.setVisible(not is_particulier)
        self.siret_label.setVisible(not is_particulier)
        self.siret_input.setVisible(not is_particulier)
        self.siret_indicator.setVisible(not is_particulier)

    def validate_email_field(self):
        """Valide le champ email en temps réel"""
        email = self.email_input.text().strip()
        if not email:
            self.email_indicator.setText("")
            return

        if validate_email(email):
            self.email_indicator.setText("✓")
            self.email_indicator.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.email_indicator.setText("✗")
            self.email_indicator.setStyleSheet("color: red; font-weight: bold;")

    def validate_siret_field(self):
        """Valide le champ SIRET en temps réel"""
        siret = self.siret_input.text().strip()
        if not siret:
            self.siret_indicator.setText("")
            return

        valid, msg = validate_siret(siret)
        if valid:
            self.siret_indicator.setText("✓")
            self.siret_indicator.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.siret_indicator.setText("✗")
            self.siret_indicator.setStyleSheet("color: red; font-weight: bold;")
            self.siret_indicator.setToolTip(msg)

    def validate_cp_field(self):
        """Valide le code postal en temps réel"""
        cp = self.code_postal_input.text().strip()
        if not cp:
            self.cp_indicator.setText("")
            return

        if validate_code_postal(cp):
            self.cp_indicator.setText("✓")
            self.cp_indicator.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.cp_indicator.setText("✗")
            self.cp_indicator.setStyleSheet("color: red; font-weight: bold;")

    def validate_tel_field(self):
        """Valide le téléphone en temps réel"""
        tel = self.telephone_input.text().strip()
        if not tel:
            self.tel_indicator.setText("")
            return

        if validate_telephone(tel):
            self.tel_indicator.setText("✓")
            self.tel_indicator.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.tel_indicator.setText("✗")
            self.tel_indicator.setStyleSheet("color: red; font-weight: bold;")

    def fill_form(self):
        """Pré-remplit le formulaire avec les données du client"""
        if not self.client:
            return

        # Type
        if self.client.type == 'entreprise':
            self.radio_entreprise.setChecked(True)
        else:
            self.radio_particulier.setChecked(True)

        # Identité
        self.nom_input.setText(self.client.nom or "")
        self.prenom_input.setText(self.client.prenom or "")
        self.raison_sociale_input.setText(self.client.raison_sociale or "")
        self.siret_input.setText(format_siret(self.client.siret) if self.client.siret else "")

        # Coordonnées
        self.adresse_input.setPlainText(self.client.adresse or "")
        self.code_postal_input.setText(self.client.code_postal or "")
        self.ville_input.setText(self.client.ville or "")
        self.email_input.setText(self.client.email or "")
        self.telephone_input.setText(format_telephone(self.client.telephone) if self.client.telephone else "")

        # Notes
        self.notes_input.setPlainText(self.client.notes or "")

    def get_form_data(self) -> dict:
        """Récupère les données du formulaire"""
        is_particulier = self.radio_particulier.isChecked()

        return {
            'type': 'particulier' if is_particulier else 'entreprise',
            'nom': self.nom_input.text().strip() if is_particulier else "",
            'prenom': self.prenom_input.text().strip() if is_particulier else "",
            'raison_sociale': self.raison_sociale_input.text().strip() if not is_particulier else "",
            'siret': self.siret_input.text().strip() if not is_particulier else "",
            'adresse': self.adresse_input.toPlainText().strip(),
            'code_postal': self.code_postal_input.text().strip(),
            'ville': self.ville_input.text().strip(),
            'email': self.email_input.text().strip(),
            'telephone': self.telephone_input.text().strip(),
            'notes': self.notes_input.toPlainText().strip(),
            'actif': True  # Par défaut actif
        }

    def save_client(self):
        """Sauvegarde le client"""
        data = self.get_form_data()

        # Créer ou modifier
        if self.client_id:
            success, message, client = self.controller.update_client(self.client_id, data)
        else:
            success, message, client = self.controller.create_client(data)

        if success:
            QMessageBox.information(self, "Succès", message)
            self.client_saved.emit()
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", message)