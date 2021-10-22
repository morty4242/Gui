import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pickle
from PyQt5 import QtCore, QtWidgets, QtGui
from ui_main import Ui_MainWindow
from datamodels.PandasDataModel import PandasDataModel, NewPandasDataModel
from datamodels.UniversalDataModel import UniversalDataModel


class MainApp(Ui_MainWindow):
    def __init__(self, parent):
        self.setupUi(parent)
        parent.setWindowTitle('MRMC Model Manager')
        self.tableView_1.horizontalHeader().setStyleSheet("::section {""background-color: rgb(0, 143, 150);}")

        # initialize variables
        self.df = pd.read_excel('model_data_file/model_inventory.xlsx', engine='openpyxl')

        # load data
        self.load_data()

        self.tableView_1.setModel(self.data_model)
        #
        # self.data_model.layoutChanged.connect(self.tableView.resizeColumnsToContents)

    def load_data(self):
        self.data_model = PandasDataModel(self.df)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainApp(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
