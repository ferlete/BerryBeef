import csv
import sys
import math
import pandas as pd

from BERRYBEEF.constants import *


class FileIO(object):
    delimit = ';'

    def __init__(self):
        pass

    def load_trm_to_dataframe(self, filename, convert_to_abs=False):
        line_data = []
        header = []
        df = []
        try:
            with open(filename, 'rU') as inFile:
                line = inFile.readline()
                cnt = 1
                while line:
                    if cnt > 2:  # ignore two first lines
                        line_data.append(line.strip())
                    line = inFile.readline()
                    cnt += 1
            for i in range(len(line_data)):
                splitlineref = line_data[i].split("  ")
                header.append(str(splitlineref[0]))
                if convert_to_abs:
                    trans = float(splitlineref[1])
                    absorbance = 2 - math.log10(abs(trans))
                    df.append(absorbance)
                else:
                    df.append(float(splitlineref[1]))

            dataframe = pd.DataFrame()
            dataframe['COnda'] = header
            dataframe['Transmittance'] = df

            #rint(df)
            #sys.exit()

            return dataframe

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def load_trm(self, filename):
        line_data = []
        try:
            with open(filename, 'rU') as inFile:
                line = inFile.readline()
                cnt = 1
                while line:
                    if cnt > 2:  # ignore two first lines
                        line_data.append(line.strip())
                    line = inFile.readline()
                    cnt += 1
            return line_data

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def load_csv_pandas(self, filename, sep):
        try:
            data = pd.read_csv(filename, sep)
            pd.set_option('precision', 3)
            pd.options.display.float_format = '{:,.3f}'.format
            return data

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def load_csv(self, directory, filename):
        try:
            __data = []
            __header = []

            file_csv = DB_FOLDER + directory + "/" + filename
            lines = 0
            if file_csv:
                f = open(file_csv, 'r', encoding='utf-8')
                mystring = f.read()
                ### comma
                if mystring.count(",") > mystring.count('\t'):
                    if mystring.count(",") > mystring.count(';'):
                        self.delimit = ","
                    elif mystring.count(";") > mystring.count(','):
                        self.delimit = ";"
                    else:
                        self.delimit = "\t"
                elif mystring.count(";") > mystring.count('\t'):
                    self.delimit = ';'
                else:
                    self.delimit = "\t"

                f.close()
                with open(file_csv, 'r', newline='\n') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=self.delimit, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for rowdata in csvreader:
                        if lines == 0:
                            __header.append(rowdata)
                        else:
                            __data.append(rowdata)
                        lines += 1

            return __header, __data
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def load_xls(self, filename):
        try:
            df = pd.read_excel(filename)
            return df
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def save_config_range(self, tbl, directory, filename):
        try:
            file = DB_FOLDER + directory + "/" + filename
            with open(file, 'w', newline='\n') as csvfile:
                writer = csv.writer(csvfile, delimiter=self.delimit,
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                header = ["Range_Name", "Range"]
                writer.writerow(header)
                for row in range(tbl.rowCount()):
                    rowdata = []
                    for column in range(tbl.columnCount()):
                        item = tbl.item(row, column)
                        if item is not None:
                            rowdata.append(str(item.text()))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def delete_file(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)

    def file_exists(self, filename):
        return os.path.isfile(filename)

    def get_list_files(self, project, extension, addnull=False):
        try:
            files_csv = []
            if addnull:
                files_csv.append(None)
            for root, dirs, files in os.walk(DB_FOLDER + project):
                for file in files:
                    if file.endswith(extension):
                        files_csv.append(file)

            return files_csv

        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def save_dataframe_to_csv(self, dataframe, filename):
        try:
            dataframe.to_csv(filename, index=False, sep=';', float_format='%.3f')
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def save_trm_to_csv(self, filename, header_labels, data):
        try:
            with open(filename, 'a', newline='\n') as csvfile:
                writer = csv.writer(csvfile, delimiter=self.delimit,
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header_labels)
                writer.writerow(data.iloc[0, :])
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

    def save_array_to_csv(self, filename, header_labels, tbl):
        try:
            with open(filename, 'a', newline='\n') as csvfile:
                writer = csv.writer(csvfile, delimiter=self.delimit,
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header_labels)
                for row in tbl:
                    writer.writerow(row)
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)


