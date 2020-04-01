import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox

from BERRYBEEF.Main_UI import Ui_MainWindow
from BERRYBEEF.Config import Config


class MainWindow(QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self, title, width, height, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowIcon(QtGui.QIcon('Imagens/beef.jpg'))

        self.title = title
        self.left = 0
        self.top = 0
        self.width = width
        self.height = height

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initial_setup()
        self.setup_signals()
        self.window_setup()

        self.statusBar().showMessage(title)
        self.resized.connect(self.adjust_objects_window)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def window_setup(self):
        # window setup
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.move(self.left, self.top)

    def setup_signals(self):
        pass

    def initial_setup(self):
        self.make_menu()

    def adjust_objects_window(self):
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()

    def make_menu(self):
        try:

            menubar = self.menuBar()
            fileMenu = menubar.addMenu('&Sistema')
            helpMenu = menubar.addMenu('A&juda')

            configButton = QAction(QIcon('Imagens/exit.png'), 'Configurar', self)
            configButton.setShortcut('Ctrl+C')
            configButton.setStatusTip('Sincronizar com Softbeef')
            configButton.triggered.connect(self.config)
            fileMenu.addAction(configButton)

            exitButton = QAction(QIcon('Imagens/exit.png'), 'Sair', self)
            exitButton.setShortcut('Ctrl+Q')
            exitButton.setStatusTip('Exit application')
            exitButton.triggered.connect(self.close)
            fileMenu.addAction(exitButton)

            sobreButton = QAction(QIcon('Imagens/about.png'), 'Sobre', self)
            #sobreButton.triggered.connect(self.open_dialog_about)
            helpMenu.addAction(sobreButton)

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def config(self):
        conf = Config()
        conf.exec_()
