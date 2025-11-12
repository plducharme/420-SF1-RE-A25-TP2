from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton, QVBoxLayout, \
    QFrame, QGraphicsTextItem, QGraphicsEllipseItem, QGraphicsLineItem, QGridLayout, QMenu, QGraphicsPixmapItem
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtCore import QRect, QPoint, QSize, QLine
import random

################################################
# Auteurs
# nom prénom (no DA), <nom d'utilisateur github>
# nom prénom (no DA), <nom d'utilisateur github>
# nom prénom (no DA), <nom d'utilisateur github>
################################################


#### Fonctions à modifier ####
def choisir_mot(mots_dictionnaire: list[str]) -> str:
    pass

def tour_jeu(lettre: str, mot_a_deviner: str, lettres_utilisees: list, lettres_restantes: list, essais_restants: int):
    pass

def recommencer_partie():
    pass

### Fin des fonctions à modifier ###


####### NE PAS MODIFIER LE CODE CI-BAS ###########################################################

# Code pour l'interface graphique, ne pas modifier
# Le package PySide6 provient d'une bibliothèque C qui utilise le "camelCase".
class BonhommePendu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bonhomme Pendu")
        self.setWindowIcon(QIcon("./images/icone_bp.png"))

        # Ajout du menu fichier et de ses actions
        self.barre_menu = self.menuBar()
        self.menu_fichier = QMenu("Fichier")
        self.barre_menu.addMenu(self.menu_fichier)
        self.action_nouvelle_partie = QAction("Nouvelle partie", parent=self)
        self.action_nouvelle_partie.triggered.connect(self.action_recommencer_partie)
        self.action_nouvelle_partie.setShortcut("Ctrl+N")
        self.menu_fichier.addAction(self.action_nouvelle_partie)
        self.action_quitter = QAction("Quitter", parent=self)
        self.action_quitter.triggered.connect(self.close)
        self.action_quitter.setShortcut("Ctrl+Q")
        self.menu_fichier.addSeparator()
        self.menu_fichier.addAction(self.action_quitter)

        # Création de la disposition principale
        self.widget_central = QFrame()
        self.setCentralWidget(self.widget_central)
        self.disposition_principale = QVBoxLayout()
        self.widget_central.setLayout(self.disposition_principale)
        self.disposition_lettres = QGridLayout()


        # Ajoute la vue pour les Graphics
        self.vue_bonhomme = QGraphicsView()
        # Ajout de la scene qui contiendra les éléments graphiques
        self.scene = QGraphicsScene(QRect(0, 0, 400, 300))
        self.setMinimumSize(QSize(400, 300))
        self.vue_bonhomme.setScene(self.scene)
        self.disposition_principale.addWidget(self.vue_bonhomme)

        # Lecture de la liste de mots complète
        with open("mots.txt", mode="r") as fichier:
            self.mots_dictionnaires = fichier.readlines()

        # Variables pour le jeu
        self.lettres_restantes, self.lettres_utilisees = recommencer_partie()
        self.essais_restants = 6
        self.mot_a_deviner = choisir_mot(self.mots_dictionnaires)

        # Créer les boutons pour les lettres
        self.creer_disposition_lettres()
        self.disposition_principale.addLayout(self.disposition_lettres)

        # Déclarations des items graphiques de base
        # Mot à deviner
        self.g_puzzle = QGraphicsTextItem()
        self.g_puzzle.setPos(150, 250)
        police = self.g_puzzle.font()
        police.setPointSize(20)
        self.g_puzzle.setFont(police)

        # Lettres utilisées
        self.g_lettres_utilisees = QGraphicsTextItem()


        # Potence
        self.g_potence = QGraphicsPixmapItem()
        self.image_potence = QPixmap("./images/potence.png")
        self.image_potence = self.image_potence.scaled(QSize(175, 175))

        # Bonhomme
        self.g_tete = QGraphicsPixmapItem()
        self.image_tete = QPixmap("./images/tete.png")
        self.image_tete = self.image_tete.scaled(QSize(50, 50))
        self.corps = QGraphicsLineItem()
        self.bras_gauche = QGraphicsLineItem()
        self.bras_droit = QGraphicsLineItem()
        self.jambe_gauche = QGraphicsLineItem()
        self.jambe_droite = QGraphicsLineItem()

        # Dessiner le tout pour une nouvelle partie
        self.action_recommencer_partie()


    def lettre_clicked(self):
        origin: QPushButton = self.sender()
        texte_puzzle, self.essais_restants = tour_jeu(origin.text(), self.mot_a_deviner, self.lettres_utilisees, self.lettres_restantes, self.essais_restants)
        self.creer_disposition_lettres()
        self.g_puzzle.setPlainText(texte_puzzle)
        self.g_lettres_utilisees.setPlainText(str(self.lettres_utilisees))

        if "_" not in texte_puzzle:
            scene_gagnant = QGraphicsScene(QRect(0, 0, 400, 300))
            image_gagnant = QPixmap("./images/bravo.png")
            image_gagnant = image_gagnant.scaled(QSize(400, 300))
            scene_gagnant.addPixmap(image_gagnant)
            self.vue_bonhomme.setScene(scene_gagnant)
        elif self.essais_restants == 5:
            self.g_tete = QGraphicsPixmapItem()
            self.g_tete.setPixmap(self.image_tete)
            self.g_tete.setPos(QPoint(195, 95))
            self.scene.addItem(self.g_tete)
        elif self.essais_restants == 4:
            self.corps = QGraphicsLineItem()
            self.corps.setLine(QLine(QPoint(220, 140), QPoint(220, 195)))
            self.scene.addItem(self.corps)
        elif self.essais_restants == 3:
            self.bras_gauche = QGraphicsLineItem(QLine(QPoint(220, 140), QPoint(210, 160)))
            self.scene.addItem(self.bras_gauche)
        elif self.essais_restants == 2:
            self.bras_droit = QGraphicsLineItem(QLine(QPoint(220, 140), QPoint(230, 160)))
            self.scene.addItem(self.bras_droit)
        elif self.essais_restants == 1:
            self.jambe_gauche = QGraphicsLineItem(QLine(QPoint(220, 195), QPoint(210, 215)))
            self.scene.addItem(self.jambe_gauche)
        elif self.essais_restants == 0:
            scene_perdant = QGraphicsScene(QRect(0, 0, 400, 300))
            image_perdant = QPixmap("./images/perdant.png")
            image_perdant = image_perdant.scaled(QSize(400, 300))
            scene_perdant.addPixmap(image_perdant)
            self.vue_bonhomme.setScene(scene_perdant)

    def action_recommencer_partie(self):
        self.lettres_restantes, self.lettres_utilisees = recommencer_partie()
        self.essais_restants = 6

        self.scene = QGraphicsScene(QRect(0, 0, 400, 300))

        self.mot_a_deviner = choisir_mot(self.mots_dictionnaires)

        self.g_puzzle = QGraphicsTextItem()
        self.g_puzzle.setPos(125, 250)
        police = self.g_puzzle.font()
        police.setPointSize(20)
        self.g_puzzle.setFont(police)
        self.g_puzzle.setPlainText("_ " * len(self.mot_a_deviner))
        self.scene.addItem(self.g_puzzle)

        self.g_lettres_utilisees = QGraphicsTextItem()
        police_utilisee = self.g_lettres_utilisees.font()
        police_utilisee.setPointSize(16)
        self.g_lettres_utilisees.setPlainText("[]")
        self.g_lettres_utilisees.setPos(QPoint(150, 15))
        self.scene.addItem(self.g_lettres_utilisees)

        self.g_potence = QGraphicsPixmapItem()
        self.g_potence.setPixmap(self.image_potence)
        self.g_potence.setPos(QPoint(100, 50))
        self.scene.addItem(self.g_potence)

        self.vue_bonhomme.setScene(self.scene)

        self.creer_disposition_lettres()

    def creer_disposition_lettres(self):

        nb_widgets = self.disposition_lettres.count()
        for i in range(nb_widgets):
            if self.disposition_lettres.itemAt(i) is not None:
                self.disposition_lettres.itemAt(i).widget().deleteLater()

        grille_lettres = QGridLayout()
        lettres_a_remplir = self.lettres_restantes.copy()

        for l in range(0, 6):
            for c in range(0, 5):
                if len(lettres_a_remplir) == 0:
                    break
                else:
                    lettre = lettres_a_remplir.pop(0)
                    bouton = QPushButton(lettre)
                    bouton.clicked.connect(self.lettre_clicked)
                    grille_lettres.addWidget(bouton, l, c)
            if len(lettres_a_remplir) == 0:
                break

        self.disposition_lettres = grille_lettres
        self.disposition_principale.addLayout(self.disposition_lettres)


if __name__ == "__main__":
    app = QApplication()
    bp = BonhommePendu()
    bp.show()
    app.exec()
