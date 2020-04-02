from PyQt5.QtWidgets import *
from BERRYBEEF.Config_UI import Ui_Dialog
from BERRYBEEF.Client import Client

import sys

class Config(QDialog):

    def __init__(self, parent=None):
        super(Config, self).__init__(parent)
        self.setWindowTitle("Configure")

        #self.progress = QProgressBar(self)
        #self.progress.setGeometry(0, 0, 300, 25)
        #self.progress.setMaximum(5)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_signals()
        self.init()
        self.center()
        self.show()

    def init(self):
        self.ui.progressBar.setVisible(False)

    def center(self):
        try:

            frameGm = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            frameGm.moveCenter(centerPoint)
            self.move(frameGm.topLeft())

        except Exception as ex:
            print(ex)

    def setup_signals(self):
        try:
            self.ui.btn_fechar.clicked.connect(self.close)
            self.ui.btn_sincronizar.clicked.connect(self.sincronizar)
        except Exception as ex:
            print(ex)

    def sincronizar(self):

        try:

            ip = self.ui.txt_ip.text()
            port = self.ui.txt_port.text()
            client = Client()
            self.ui.progressBar.setVisible(True)
            client.countChanged.connect(self.onCountChanged)
            if not client.connect(ip, port):
                QMessageBox.about(self, "Erro", 'Servidor Indisponivel')
            else:
                if client.retr_file():
                    QMessageBox.about(self, "Info", 'Sincronismo Finalizada')
                else:
                    QMessageBox.about(self, "Erro", 'Sincronismo Incompleto')
                self.ui.progressBar.setVisible(False)

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def onCountChanged(self, value):
        self.ui.progressBar.setValue(value)
