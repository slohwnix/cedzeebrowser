import sys
import os

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QTabWidget, QWidget, QMenu, QVBoxLayout
    from PyQt6.QtGui import QAction
    from PyQt6.QtCore import QUrl, Qt
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except (ImportError, ImportWarning) as err:
    print(f"Erreur lors de l'importation des modules.\nDétails:\n{err}", file=sys.stderr)
    exit(1)

application = QApplication.instance()
if not application:
    application = QApplication(sys.argv)

home_url = os.path.abspath("./web/index.html")
if not os.path.exists(home_url):
    print("Erreur : La page d'accueil spécifiée est introuvable.", file=sys.stderr)
    exit(1)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CEDZEE Browser")
        self.resize(1200, 800)
        self.move(300, 50)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.menu = QToolBar("Menu de navigation")
        self.addToolBar(self.menu)
        self.add_navigation_buttons()

        # Ajouter un onglet pour la page d'accueil au démarrage
        self.add_homepage_tab()

        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)

        self.new_tab_shortcut = QAction(self)
        self.new_tab_shortcut.setShortcut("Ctrl+T")
        self.new_tab_shortcut.triggered.connect(self.open_new_tab)
        self.addAction(self.new_tab_shortcut)

    def add_navigation_buttons(self):
        back_btn = QAction("←", self)
        back_btn.triggered.connect(lambda: self.current_browser().back() if self.current_browser() else None)
        self.menu.addAction(back_btn)

        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward() if self.current_browser() else None)
        self.menu.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload() if self.current_browser() else None)
        self.menu.addAction(reload_btn)

        home_btn = QAction("⌂", self)
        home_btn.triggered.connect(self.go_home)
        self.menu.addAction(home_btn)

        self.adress_input = QLineEdit()
        self.adress_input.returnPressed.connect(self.navigate_to_url)
        self.menu.addWidget(self.adress_input)

        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(self.open_new_tab)
        self.menu.addAction(new_tab_btn)

    def add_homepage_tab(self):
        """Ajoute un onglet avec la page d'accueil directement après le démarrage."""
        try:
            browser = QWebEngineView()
            browser.setUrl(QUrl.fromLocalFile(home_url))

            # Connexion au signal loadFinished pour s'assurer que la page est chargée correctement
            browser.loadFinished.connect(self.on_homepage_loaded)
            browser.urlChanged.connect(self.update_urlbar)
            browser.page().javaScriptConsoleMessage = self.handle_js_error  

            tab = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(browser)
            tab.setLayout(layout)

            self.tabs.addTab(tab, "Page d'accueil")
            self.tabs.setCurrentWidget(tab)

        except Exception as e:
            print(f"Erreur lors de l'ajout de la page d'accueil : {e}", file=sys.stderr)

    def on_homepage_loaded(self, ok):
        if not ok:
            print("Erreur lors du chargement de la page d'accueil.", file=sys.stderr)
        else:
            print("Page d'accueil chargée avec succès.")

    def current_browser(self):
        try:
            current_tab = self.tabs.currentWidget()
            return current_tab.layout().itemAt(0).widget() if current_tab else None
        except Exception as e:
            print(f"Erreur lors de la récupération du navigateur actuel : {e}", file=sys.stderr)
            return None

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        try:
            url = QUrl(self.adress_input.text())
            if url.scheme() == "":
                url.setScheme("http")
            if self.current_browser():
                self.current_browser().setUrl(url)
        except Exception as e:
            print(f"Erreur lors de la navigation vers une URL : {e}", file=sys.stderr)

    def update_urlbar(self, url):
        try:
            self.adress_input.setText(url.toString())
            self.adress_input.setCursorPosition(0)
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la barre d'adresse : {e}", file=sys.stderr)

    def go_home(self):
        if self.current_browser():
            self.current_browser().setUrl(QUrl.fromLocalFile(home_url))

    def open_new_tab(self):
        self.add_homepage_tab()

    def show_tab_context_menu(self, position):
        try:
            menu = QMenu()
            new_tab_action = menu.addAction("Ouvrir un nouvel onglet")
            close_tab_action = menu.addAction("Fermer cet onglet")

            action = menu.exec(self.tabs.mapToGlobal(position))
            if action == new_tab_action:
                self.open_new_tab()
            elif action == close_tab_action:
                self.close_tab(self.tabs.currentIndex())
        except Exception as e:
            print(f"Erreur lors de l'affichage du menu contextuel : {e}", file=sys.stderr)

    def handle_js_error(self, message, line, sourceID, errorMsg):
        print(f"Erreur JavaScript : {message} à la ligne {line} dans {sourceID}: {errorMsg}", file=sys.stderr)

window = BrowserWindow()
window.show()

try:
    application.exec()
except Exception as e:
    print(f"Erreur critique lors de l'exécution de l'application : {e}", file=sys.stderr)
    exit(1)

