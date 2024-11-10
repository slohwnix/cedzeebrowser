## je vais commenter mon code -> ça vous permet de comprendre à quoi servent mes lignes ;)
#ici j'importe tous les modules nécessaires
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os

#pour éviter de créer des fenêtes supplémentaires, on vérifie si l'application à déjà une instance ouverte
application = QApplication.instance()
#si il n'y a pas d'instance on en crée une
if not application:
    application = QApplication(sys.argv)

# Charge le fichier local index.html
local_path = os.path.abspath("index.html")


##fenêtre
window = QMainWindow()
#titre
window.setWindowTitle("CEDZEE Browser")
#taille
window.resize(1200,800)
#faculatif mais pour un confort: définir la position d'apparition de la fenêtre
window.move(300,50)

##navigateur
#on initialise la vue
browser = QWebEngineView()
browser.setUrl(QUrl.fromLocalFile(local_path)) #page internet où se lance le navigateur
window.setCentralWidget(browser) #on explique que le navigateur est le composant principal de notre fenêtre

##outils de navigation et interface
#barre d'adresse
menu = QToolBar("Menu de navigation") #créer une barre des tâches nommé "menu"
window.addToolBar(menu)

def home():
    adress_input.returnPressed.connect(lambda: browser.setUrl(QUrl.fromLocalFile(local_path))) #lorsque la touche est pressée, on change l'url affichée à l'aide de browser et des données contenues dans adress_input
    browser.urlChanged.connect(lambda url: adress_input.setText(url.toString())) # Met à jour la barre d'adresse lors de la navigation

# Bouton Précédent
back_btn = QAction("←", window)
back_btn.triggered.connect(browser.back)
menu.addAction(back_btn)

# Bouton Suivant
forward_btn = QAction("→", window)
forward_btn.triggered.connect(browser.forward)
menu.addAction(forward_btn)

# Bouton Recharger
reload_btn = QAction("⟳", window)
reload_btn.triggered.connect(browser.reload)
menu.addAction(reload_btn)

#bouton home
home_btn = QAction("⌂", window)
home_btn.triggered.connect(home)
menu.addAction(home_btn)

#barre d'adresse
adress_input = QLineEdit()
adress_input.returnPressed.connect(lambda: browser.setUrl(QUrl(adress_input.text()))) #lorsque la touche est pressée, on change l'url affichée à l'aide de browser et des données contenues dans adress_input
browser.urlChanged.connect(lambda url: adress_input.setText(url.toString())) # Met à jour la barre d'adresse lors de la navigation
menu.addWidget(adress_input) #on ajoute la barre de navigation à notre barre des tâches
window.show()




#on execute
application.exec_()