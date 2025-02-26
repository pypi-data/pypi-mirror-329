from AnyQt.QtWidgets import QApplication, QVBoxLayout, QLabel, QSpinBox, QPushButton, QTextEdit, QMessageBox
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
import Orange.data
import numpy as np

class OWExtraChunks(widget.OWWidget):
    name = "Extra Chunks"
    description = "Extract surrounding chunks from a dataset"
    icon = "icons/extra_chunks.png"
    priority = 1001

    class Inputs:
        complete_data = Input("Complete Dataset", Orange.data.Table)
        selected_data = Input("Chunks", Orange.data.Table)

    class Outputs:
        data = Output("Data", Orange.data.Table)

    def __init__(self):
        super().__init__()
        self.complete_data = None  # Stocke le dataset complet
        self.selected_data = None  # Stocke les chunks sélectionnés
        self.num_surrounding = 2  # Nombre d'éléments avant et après
        self.ready_to_propagate = False  # Contrôle la propagation des résultats

        # Interface utilisateur
        self.mainArea.layout().setSpacing(10)

        # Label pour indiquer la sélection du nombre d'éléments
        self.label = QLabel("Nombre d'éléments à couvrir avant et après :")
        self.mainArea.layout().addWidget(self.label)

        # Sélecteur de nombre d'éléments avant/après
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(10)
        self.spin_box.setValue(self.num_surrounding)
        self.spin_box.valueChanged.connect(self.update_num_surrounding)
        self.mainArea.layout().addWidget(self.spin_box)

        # Zone de texte pour afficher les indices couverts
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Affichage des indices couverts...")
        self.text_area.setReadOnly(True)
        self.mainArea.layout().addWidget(self.text_area)

        # Bouton pour exécuter le traitement
        self.button_process = QPushButton("📝 Mettre à jour")
        self.button_process.clicked.connect(self.enable_propagation)
        self.mainArea.layout().addWidget(self.button_process)

    def update_num_surrounding(self):
        """Met à jour le nombre d'éléments à extraire avant/après."""
        self.num_surrounding = self.spin_box.value()

    def enable_propagation(self):
        """Active la propagation des données et lance le traitement."""
        self.ready_to_propagate = True
        self.process()

    @Inputs.complete_data
    def set_complete_data(self, data):
        """Réceptionne et stocke le dataset complet."""
        self.complete_data = data

    @Inputs.selected_data
    def set_selected_data(self, data):
        """Réceptionne et stocke les chunks sélectionnés."""
        self.selected_data = data

    def process(self):
        """Traite les données et extrait les indices sélectionnés avec leur voisinage."""
        if not self.ready_to_propagate:
            print("Propagation en attente, appuyez sur 'Mettre à jour'.")
            return

        if self.complete_data is None or self.selected_data is None:
            self.text_area.setText("Données manquantes : pas de traitement")
            print("Aucune donnée complète ou sélectionnée reçue.")
            return
        domain = self.complete_data.domain
        if "Chunks index" not in domain:
            QMessageBox.critical(self, "Erreur", "La colonne 'index' est introuvable dans le dataset complet.")
            print("Erreur : La colonne 'index' est introuvable dans le dataset complet.")
            return

        index_var = domain["Chunks index"]

        # Extraction des indices des chunks sélectionnés
        selected_indices = [int(row[index_var]) for row in self.selected_data]

        # Génération des indices étendus (n avant et n après)
        full_indices = set()
        for idx in selected_indices:
            extracted_range = range(idx - self.num_surrounding, idx + self.num_surrounding + 1)
            full_indices.update(extracted_range)

        # Vérification des index négatifs
        if any(i < 0 for i in full_indices):
            QMessageBox.warning(self, "Avertissement", "Certains indices générés sont négatifs et seront ignorés.")
            print("Avertissement : Certains indices générés sont négatifs et seront ignorés.")

        # Extraction des indices valides dans le dataset complet
        complete_indices = [int(row[index_var]) for row in self.complete_data]

        covered_indices = sorted(full_indices.intersection(set(complete_indices)))

        # Sélection des lignes correspondantes dans le dataset complet
        selected_rows = [row for row in self.complete_data if int(row[index_var]) in covered_indices]
        self.text_area.setText("Indices couverts: " + str(covered_indices))

        # Construire la sortie
        output_data = Orange.data.Table(self.complete_data.domain, selected_rows)
        self.Outputs.data.send(output_data)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = OWExtraChunks()
    window.show()
    sys.exit(app.exec_())
