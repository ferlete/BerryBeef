import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QFileDialog
from configparser import ConfigParser

from sklearn.cross_decomposition import PLSRegression

from BERRYBEEF.Main_UI import Ui_MainWindow
from BERRYBEEF.Dialog_Real_Time_UI import Ui_Dialog as DRealTime
from BERRYBEEF.Config import Config
from BERRYBEEF.FileIO import FileIO
from BERRYBEEF.Calcule import Calcule
from BERRYBEEF.constants import *


class MainWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, title, width, height, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowIcon(QtGui.QIcon('Imagens/beef.jpg'))
        self.project_selected = ""

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

            prediction_onlineButton = QAction(QIcon('Imagens/prediction.png'), 'Predição Tempo Real', self)
            prediction_onlineButton.setStatusTip('Predição em tempo real')
            prediction_onlineButton.triggered.connect(self.predict_real_time)
            fileMenu.addAction(prediction_onlineButton)

            exitButton = QAction(QIcon('Imagens/exit.png'), 'Sair', self)
            exitButton.setShortcut('Ctrl+Q')
            exitButton.setStatusTip('Exit application')
            exitButton.triggered.connect(self.close)
            fileMenu.addAction(exitButton)

            sobreButton = QAction(QIcon('Imagens/about.png'), 'Sobre', self)
            # sobreButton.triggered.connect(self.open_dialog_about)
            helpMenu.addAction(sobreButton)

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def config(self):
        try:
            conf = Config()
            conf.exec_()

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def predict_real_time(self):
        try:

            file = FileIO()
            config_file = DB_FOLDER  + "/config.ini"

            if file.file_exists(config_file):
                trm_name, _ = QFileDialog.getOpenFileName(self, 'Open TRM File', 'TRM', 'TRM(*.TRM)')
                if trm_name:

                    config = ConfigParser()
                    config.read(config_file)
                    ph_model = DB_FOLDER + self.project_selected + "/" + config.get("Model", "ph")

                    data_predict = file.load_trm_to_dataframe(trm_name)
                    data_model_ph = file.load_csv_pandas(ph_model, sep=';')

                    if data_predict.shape[0] != data_model_ph.shape[1] - 1:
                        QMessageBox.about(self, "Erro", 'Qtde de colunas do modelo deve ser a mesma da predição')
                    else:

                        reference = DB_FOLDER + self.project_selected + "/" + config.get("Reference", "ref")
                        quality = DB_FOLDER + self.project_selected + "/" + config.get("Parameter", "quality_file")

                        data_reference = file.load_csv_pandas(reference, sep=';')
                        data_quality = file.load_csv_pandas(quality, sep=';')

                        X_valid = data_predict['Transmittance']
                        data_reference = data_reference.T
                        calc = Calcule()
                        X_valid = calc.transmittance_to_absorbance(X_valid, data_reference)
                        X_valid = X_valid.T

                        out = "Arquivo: " + os.path.basename(trm_name) + "\n\n"

                        for key, value in config.items('Model'):
                            key_model = DB_FOLDER + self.project_selected + "/" + config.get("Model", key)
                            data_model_key = file.load_csv_pandas(key_model, sep=';')
                            X_calib = data_model_key.iloc[:, 1:]
                            Y_calib = data_model_key.iloc[:, 0:1]  # apenas a coluna de predicao
                            pls = PLSRegression(n_components=2, max_iter=500)
                            pls.fit(X_calib, Y_calib)
                            Y_pred = pls.predict(X_valid)  # valores preditos

                            # print(key, " Valor Predito:", round(float(Y_pred[0]), 1))
                            query = 'Atributo == "' + key + '" & (de <= ' + str(round(float(Y_pred[0]), 3)) + ' <= ate)'
                            rslt_df = data_quality.query(query)
                            out = out + "{} = {} \n".format(key, rslt_df['Descricao'].iloc[0])

                            if (key == "ph"):
                                valor_predito_ph = round(float(Y_pred[0]), 1)

                        if (valor_predito_ph >= 5.3 and valor_predito_ph <= 5.8):
                            apro = "Aprovado"
                            style = "background-color: green; border: 1px solid black;"
                        else:
                            apro = "Reprovado"
                            style = "background-color: red; border: 1px solid black;"

                        dialog = QtWidgets.QDialog()
                        self.dg_realtime = DRealTime()
                        self.dg_realtime.setupUi(dialog)
                        self.dg_realtime.lbl_result.setText(out)
                        self.dg_realtime.lbl_apro.setText(apro)
                        self.dg_realtime.lbl_apro.setStyleSheet(style)
                        dialog.exec_()

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)
