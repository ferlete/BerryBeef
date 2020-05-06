# -*- coding: utf-8 -*-
import sys

import math  # This will import math module
import numpy as np
import pandas as pd

from BERRYBEEF.FileIO import FileIO


class Calcule(object):
    wave = []
    transmittance = []
    reference = []
    absorbances = []
    result = []
    TRUE = True
    FALSE = False

    def __init__(self):
        """Initializes the data."""
        pass

    def transmittance_to_absorbance(self, dataframe, reference):
        try:
            abs = []
            dataframe.astype(float)
            reference.astype(float)
            for i in range(dataframe.shape[0]):
                #print(dataframe.iloc[i].astype(float))
                #print(reference.iloc[i].astype(float))
                #sys.exit()
                trans = dataframe.iloc[i].astype(float) - (reference.iloc[i].astype(float))
                #print(trans)
                abs.append(self.absorbance(trans))

            ret = pd.DataFrame(abs)
            ret.replace({np.inf: 0}, inplace=True)

            return ret

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def absorbance(self, transmittance):
        try:
            return math.log10(1 / (abs(transmittance) / 100))

        except ZeroDivisionError:
            return 0

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def calcular(self, file1, file2, file3, ref):

        file = FileIO()

        # Amostra 1
        lines1 = file.load_trm(file1)

        # Amostra 2
        lines2 = file.load_trm(file2)

        # Amostra 3
        lines3 = file.load_trm(file3)

        # Arquivo de Referencia
        linesref = file.load_trm(ref)

        # Calcular a transmitancia

        # Verifica se os tres arquivos possui a mesma quantidade de linhas
        if lines1.__len__() == lines2.__len__() == lines3.__len__():
            for i in range(lines1.__len__()):
                splitline1 = lines1[i].split("  ")  # Primeira Amostra
                splitline2 = lines2[i].split("  ")  # Segunda Amostra
                splitline3 = lines3[i].split("  ")  # Terceira Amostra
                splitlineref = linesref[i].split("  ")  # Referencia

                wavelength = float(splitline1[0])  # comprimento de onda
                reference = float(splitlineref[1])  # referencia

                # verifica se comprimento de onda das tres amostras sao iguais, ou seja,
                # em cada linha verifica se comprimento de onda eh igual
                if splitline1[0] == splitline2[0] == splitline3[0]:
                    # subtrai a tranmitancia de cada amostra com o valor de referencia
                    if float(splitline1[1]) != reference:
                        transmittance1 = float(splitline1[1]) - reference
                    else:
                        transmittance1 = float(1)

                    if float(splitline2[1]) != reference:
                        transmittance2 = float(splitline3[1]) - reference
                    else:
                        transmittance2 = float(1)

                    if float(splitline3[1]) != reference:
                        transmittance3 = float(splitline3[1]) - reference
                    else:
                        transmittance3 = float(1)

                    transmittance = (transmittance1 + transmittance2 + transmittance3) / 3  # media da transmitancia
                    absorb = self.absorbance(transmittance)

                    self.wave.append(wavelength)
                    self.reference.append(reference)
                    self.transmittance.append(transmittance)
                    self.absorbances.append(absorb)
                else:
                    print("wavelength different")

        else:
            print("sample error")

    def getresult(self):
        return self.result

    def gettranmittance(self):
        return self.transmittance

    def getabsorbancia(self):
        return self.absorbances

    def get_columncount(self):
        return len(self.absorbances)

