from PyQt5.QtWidgets import *
from BERRYBEEF.Config_UI import Ui_Dialog
from BERRYBEEF.Client import Client


class Config(QDialog):

    def __init__(self, parent=None):
        super(Config, self).__init__(parent)
        self.setWindowTitle("Configure")
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_signals()
        self.init()
        self.show()

    def init(self):
        pass

    def center(self):
        try:

            frameGm = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            frameGm.moveCenter(centerPoint)
            self.move(frameGm.topLeft())

        except Exception as ex:
            print(ex)

    def setup_signals(self):
        self.ui.btn_fechar.clicked.connect(self.close)
        self.ui.btn_sincronizar.clicked.connect(self.sincronizar)

    def sincronizar(self):

        ip = self.ui.txt_ip.text()
        port = self.ui.txt_port.text()
        Client(str(ip), port)
