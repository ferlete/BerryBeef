import sys
import warnings

import matplotlib
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDesktopWidget, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from scipy.signal import savgol_filter

from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error, r2_score

from BEEF.Filter import Filter
from BEEF.FileIO import FileIO
from BEEF.constants import *

# for outlier

warnings.filterwarnings("ignore")


# regression-python/
class PLSR:
    item_predicted = ''


    def __init__(self, width, height, project, filename, Y_column, Y_row, X_column, X_row, ncomponents, max_inter,
                 tab_graphic, tab_prediction, cod_transform, ordem_derivativa=1, ordem_polinominal=0,
                 baseline_method=0, save_model=False):

        self.width = width
        self.height = height
        self.project = project
        self.filename = filename
        self.max_inter = max_inter
        self.save_model = save_model

        self.response_column_init = int(Y_column[0])
        self.response_column_end = int(Y_column[1])
        self.response_row_init = int(Y_row[0])
        self.response_row_end = int(Y_row[1])

        self.prediction_column_init = int(X_column[0])
        self.prediction_column_end = int(X_column[1])
        self.prediction_row_init = int(X_row[0])
        self.prediction_row_end = int(X_row[1])

        self.ncomponents = ncomponents
        self.cod_transform = cod_transform

        self.ordem_derivativa = ordem_derivativa
        self.ordem_polinominal = ordem_polinominal
        self.baseline_method = baseline_method
        # self.tab_prediction = tab_prediction

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas, tab_graphic)

        self.figure.clf()
        self.figure.subplots_adjust(bottom=.10, left=.10, right=.95, top=.95, hspace=.55)

        layout = QVBoxLayout(tab_graphic)
        layout.addWidget(self.canvas)
        layout.addWidget(toolbar)

        self.tbl_view = QTableWidget()
        self.tbl_view.setObjectName("tbl_view")
        self.tbl_view.setFixedWidth(self.width - 280)
        self.tbl_view.setFixedHeight(self.height - 180)
        layout = QVBoxLayout(tab_prediction)
        layout.addWidget(self.tbl_view)

        self.wl = []

        csv_filename = DB_FOLDER + self.project + "/" + self.filename
        self.data = self.load_data_csv(csv_filename)
        self.plsr()

    def load_data_csv(self, filename):
        try:
            df = pd.read_csv(filename, sep=';')
            df.fillna(0, inplace=True)
            return df

        except Exception as ex:
            print(ex)

    def plsr(self):

        try:

            reference_data = self.data.iloc[self.prediction_row_init - 1:self.response_row_end,
                             self.response_column_init - 1:self.response_column_end]
            #print("ref", reference_data)

            # Get reference values
            Y_calib = (reference_data.iloc[self.prediction_row_init - 1:self.prediction_row_end])
            Y_valid = (reference_data.iloc[self.response_row_init - 1:self.response_row_end])

            # Get spectra
            #X_calib = pd.DataFrame.get_values(self.data.iloc[self.prediction_row_init - 1:self.prediction_row_end,
            #                                  self.prediction_column_init: self.prediction_column_end])
            #X_valid = pd.DataFrame.get_values(self.data.iloc[self.response_row_init - 1:self.response_row_end,
            #                                  self.prediction_column_init:self.prediction_column_end])

            X_calib = self.data.iloc[self.prediction_row_init - 1:self.prediction_row_end,
                                              self.prediction_column_init-1: self.prediction_column_end]

            X_valid = self.data.iloc[self.response_row_init - 1:self.response_row_end,
                                              self.prediction_column_init-1:self.prediction_column_end]



            #print(X_calib)
            #print(Y_calib)
            model = pd.concat([Y_calib, X_calib], axis=1)
            #print(self.model)


            # X_train, X_test, y_train, y_test = train_test_split(X_calib, Y_calib, test_size=0.2, random_state=0)
            # print(X_train)

            # Get wavelengths (They are in the first line which is considered a header from pandas)
            self.wl = list(self.data.columns.values)
            # print(wl[self.prediction_column_init-1:self.prediction_column_end])

            # Plot Original spectra
            ax1 = self.figure.add_subplot(231)
            ax1.set_title('Spectro Original')
            ax1.set_xlabel('Wavelength (nm)')
            ax1.set_ylabel('Absorbance')
            ax1.set_xticks([100, 215, 315, 415, 515, 615, 715, 815, 915, 1015, 1115, 1215])
            ax1.plot(self.wl[self.prediction_column_init-1:self.prediction_column_end], X_calib.T)

            # Tranform data
            X_calib = pd.DataFrame(X_calib)
            X_valid = pd.DataFrame(X_valid)
            if self.cod_transform == 1:
                # Calculate derivatives
                self.title = str(self.ordem_derivativa + 1) + "º Derivativa Savitzky Golay"

                X2_calib = savgol_filter(X_calib, 17, polyorder=self.ordem_polinominal, deriv=self.ordem_derivativa)
                X2_valid = savgol_filter(X_valid, 17, polyorder=self.ordem_polinominal, deriv=self.ordem_derivativa)

            elif self.cod_transform == 2:
                self.title = "Standard Normal Variate"

                corr = Filter()
                X2_calib = corr.filter_snv(X_calib)
                X2_valid = corr.filter_snv(X_valid)

            elif self.cod_transform == 3:
                self.title = "Multiplicative Scatter Correction "

                corr = Filter()
                X2_calib = corr.filter_msc(X_calib)
                X2_valid = corr.filter_msc(X_valid)

            elif self.cod_transform == 4:
                corr = Filter()
                if self.baseline_method == 0:
                    self.title = "Baseline Linear"
                    X2_calib = corr.filter_baseline_linear(X_calib)
                    X2_valid = corr.filter_baseline_linear(X_valid)
                elif self.baseline_method == 1:
                    self.title = "Baseline Envelope"
                    X2_calib = corr.filter_baseline_envelope(X_calib)
                    X2_valid = corr.filter_baseline_envelope(X_valid)
                elif self.baseline_method == 2:
                    self.title = "Baseline ALS"
                    X2_calib = corr.filter_baseline_als(X_calib)
                    X2_valid = corr.filter_baseline_als(X_valid)
                elif self.baseline_method == 1:
                    self.title = "Baseline ARPLS"
                    X2_calib = corr.filter_baseline_arpls(X_calib)
                    X2_valid = corr.filter_baseline_arpls(X_valid)
                elif self.baseline_method == 4:
                    self.title = "Baseline AIRPLS"
                    X2_calib = corr.filter_baseline_airpls(X_calib)
                    X2_valid = corr.filter_baseline_airpls(X_valid)

            else:
                self.title = "Sem Transformação"
                X2_calib = X_calib
                X2_valid = X_valid

            # Spectro Transformed
            ax2 = self.figure.add_subplot(232)
            ax2.set_title(self.title)
            ax2.set_xlabel('Wavelength (nm)')
            ax2.set_ylabel('Absorbance')
            ax2.set_xticks([100, 215, 315, 415, 515, 615, 715, 815, 915, 1015, 1115, 1215])
            ax2.plot(self.wl[self.prediction_column_init-1:self.prediction_column_end], X2_calib.T)

            self.prediction(X2_calib, Y_calib, X2_valid, Y_valid)

            if self.save_model:
                self.export_model(model)

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def prediction(self, X_calib, Y_calib, X_valid, Y_valid):
        try:
            # Run PLS including a variable number of components  and calculate MSE
            mse = []

            component = np.arange(1, self.ncomponents)
            for i in component:
                pls = PLSRegression(n_components=i, max_iter=self.max_inter)
                # Fit
                pls.fit(X_calib, Y_calib)
                # Prediction
                Y_pred = pls.predict(X_valid)
                # print("Y_pred",Y_pred)

                mse_p = mean_squared_error(Y_valid, Y_pred)
                mse.append(mse_p)

                # comp = 100 * (i + 1) / 40
                # Trick to update status on the same line
                # sys.stdout.write("\r%d%% completed" % comp)
                # sys.stdout.flush()
            # sys.stdout.write("\n")

            # Calculate and print the position of minimum in MSE
            msemin = np.argmin(mse)
            print("Suggested number of components: ", msemin + 1)
            sys.stdout.write("\n")

            # plot components suggested
            ax3 = self.figure.add_subplot(233)
            ax3.set_title('PLS')
            ax3.set_xlabel('Number of PLS components')
            ax3.set_ylabel('MSE')
            ax3.plot(component, np.array(mse), '-v', color='blue', mfc='blue')
            ax3.plot(component[msemin], np.array(mse)[msemin], 'P', ms=10, mfc='red')

            # Run PLS with suggested number of components
            pls = PLSRegression(n_components=msemin + 1, max_iter=self.max_inter)
            pls.fit(X_calib, Y_calib)
            # print("x_scores")
            # print(pls.x_scores_)
            # print("y_scores")
            # print(pls.y_scores_)
            # print("Coeficiente Y = X coef_ + Err")
            #print("Y = X ", pls.coef_, " + ERR")
            y_intercept = pls.y_mean_ - np.dot(pls.x_mean_, pls.coef_)
            print("Y Intercept: ", y_intercept)
            #print("pls.y_mean_:", pls.y_mean_)
            #print("pls.x_mean_:", pls.x_mean_)


            Y_pred = pls.predict(X_valid)

            ax4 = self.figure.add_subplot(234)
            ax4.set_title('PLS Coefficientes')
            ax4.set_xlabel('Wavelength (nm)')
            ax4.set_ylabel('Absolute value of PLS coefficients')
            ax4.set_xticks([100, 215, 315, 415, 515, 615, 715, 815, 915, 1015, 1115, 1215])
            ax4.plot(self.wl[self.prediction_column_init-1:self.prediction_column_end], np.abs(pls.coef_[:, 0]))

            #
            # # Calculate and print scores
            score_p = r2_score(Y_valid, Y_pred)
            mse_p = mean_squared_error(Y_valid, Y_pred)
            sep = np.std(Y_pred - Y_valid)
            rpd = np.std(Y_valid) / sep
            bias = np.mean(Y_pred - Y_valid)

            # print('R2: %5.3f' % score_p)
            # print('MSE: %5.3f' % mse_p)
            # print('SEP: %5.3f' % sep)
            # print('RPD: %5.3f' % rpd)
            # print('Bias: %5.3f' % bias)

            # Plot regression and figures of merit
            rangey = Y_valid.max() - Y_valid.min()
            rangex = Y_pred.max() - Y_pred.min()

            # print("rangey", rangey)
            # print("rangex", rangex)

            # print("Y_pred len:", len(Y_pred))
            # print("Type", type(Y_pred))  # <class 'numpy.ndarray'>
            # print("Y_pred", Y_pred)

            # print("Y_valid len", len(Y_valid))
            # print("type", type(Y_valid.values))  # class 'pandas.core.frame.DataFrame'>
            # print("Y_valid values", Y_valid)
            # print("item Predito", Y_valid.columns[0])
            self.item_predicted = Y_valid.columns[0]  # item predicted
            Y_valid = Y_valid.values  # convert to 1D vector

            pred = pd.DataFrame(Y_pred)
            valid = pd.DataFrame(Y_valid)
            predicted_measured = pd.concat([pred, valid], axis=1)
            predicted_measured.columns = ['Predicted', 'Measured']
            #print(predicted_measured)
            self.fill_table_result(self.tbl_view, predicted_measured)

            #model_X = pd.DataFrame(X_calib)
            #print(X_calib)
            #model_Y =pd.DataFrame(Y_calib)
            #model = pd.concat([model_Y, model_X])
            #print(model)

            # create and plot models
            z = np.polyfit(Y_valid[0], Y_pred[0], 1)
            # print("z", z)

            ax5 = self.figure.add_subplot(235)
            ax5.set_title(self.item_predicted + ' Predicted X Measured')
            ax5.set_xlabel('Predicted')
            ax5.set_ylabel('Measured')
            ax5.scatter(Y_pred, Y_valid, c='red', edgecolors='k')
            ax5.plot(z[1] + z[0] * Y_valid, Y_valid, c='blue', linewidth=1)
            ax5.plot(Y_valid, Y_valid, color='green', linewidth=1)
            ax5.text(Y_pred.min() + .5 * rangex, Y_valid.max() - 0.1 * rangey, 'R$^{2}=$ %5.3f' % score_p)
            ax5.text(Y_pred.min() + .5 * rangex, Y_valid.max() - 0.15 * rangey, 'MSE: %5.3f' % mse_p)
            ax5.text(Y_pred.min() + .5 * rangex, Y_valid.max() - 0.2 * rangey, 'SEP: %5.3f' % sep)
            ax5.text(Y_pred.min() + .5 * rangex, Y_valid.max() - 0.25 * rangey, 'RPD: %5.3f' % rpd)
            ax5.text(Y_pred.min() + .5 * rangex, Y_valid.max() - 0.3 * rangey, 'Bias: %5.3f' % bias)

            self.canvas.draw()
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def fill_table_result(self, table_name, dados):
        try:

            table_name.setColumnCount(len(dados.columns))
            table_name.setRowCount(len(dados))

            table_name.setHorizontalHeaderLabels(dados.columns)

            for row in range(len(dados.values)):
                for column in range(len(dados.columns)):
                    cellinfo = QTableWidgetItem("%.2f" % dados.iloc[row][column])
                    table_name.setItem(row, column, cellinfo)

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def export_model(self, df_model):

        try:
            filename = DB_FOLDER + self.project + "/" + self.item_predicted + "_" + self.filename[:-4] + "_Model.csv"
            file = FileIO()
            file.save_dataframe_to_csv(dataframe=df_model, filename=filename)

        except Exception as ex:
            print(ex)