
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QLabel, QFileDialog , QMessageBox , QColorDialog
from PyQt5.QtGui import *
## from PyQt5.QtGui import QPainter
import sys
import csv
import sys
import os

import pandas
#import pandas as pd
#from pandasModel import pandasModel

class Ui_Mainwindow(object):

    def tenantcount(self):

        self.label.setText("Tenant Count :")

        try:
            dfs = pandas.read_csv(path, encoding='ISO-8859–1')
            df = pandas.DataFrame(dfs)

            commands = ""
            for i, item in df.iterrows():
                cell = "\\\\reddog\Builds\\branches\git_azure_compute_master_latest\\retail-amd64\Services\Controller\FcShell\scripts\BatchingUpdateForAllNodesOfTenantWhoSkippedHEUpdate.ps1 -clusterName " + str(
                    item["Cluster"]) + " -TenantName " + str(item["TenantName"])
                commands = commands + cell + "\n"
            y = commands.splitlines()
            # le = len(y)
            # print(le)
            # x = self.textEdit.toPlainText()  # anchorAt(Mainwindow)
            # self.label_2.setText("Duplicates :")
            lst = list(y)
            # using regular logic
            data_list = []
            final_list = []
            strd2 = ""
            #self.label.setText("Duplicate Tenants :")
            for item in lst:
                if item not in final_list:
                    final_list.append(item)
                else:
                    data_list.append(item)
            if len(data_list) > 0:
                # print(len(data_list))
                for elem in data_list:
                    # print(elem)
                    elem2 = elem.rstrip().lstrip().split()

                    tenantelem = elem2[4]
                    tenantclust = elem2[2]
                    strd2 = strd2 + tenantclust + "    " + tenantelem + "\n"
                self.textEdit.setText("Total Tenants : " + str(len(y))) #+ "\n" + "Duplicate Tenants : " + str(len(data_list)) + "\n \n \n" + str(strd2))

            else:
                self.textEdit.setText("Total Tenants : " + str(len(y)) + "\n \n" )# + "No Duplicates Found.")
                # print("0")

        except (FileNotFoundError, KeyError, pandas.errors.ParserError, AttributeError, UnicodeDecodeError, NameError,
                TypeError) as error:
            self.textEdit.setText("No File Selected or Wrong file selected")



    def withoutjit(self):

        try:
            # dialog = QFileDialog.getOpenFileName()
            # path = dialog[0]
            #print(path)
            self.label.setText("Commands\nWithNoJIT:\nNoDuplicates")
            #self.textEdit_2.clear()
            dfs = pandas.read_csv(path, encoding= 'ISO-8859–1')
            df = pandas.DataFrame(dfs)



            commands = ""
            for i, item in df.iterrows():

                remosp = item["Cluster"]
                # #finalremo = remosp.str.strip()
                cell = "\\\\reddog\Builds\\branches\git_azure_compute_master_latest\\retail-amd64\Services\Controller\FcShell\scripts\BatchingUpdateForAllNodesOfTenantWhoSkippedHEUpdateWithoutJITAccess.ps1 -clusterName " + str(remosp.strip()) + " -tenantName " + str(item["TenantName"].strip())
                commands = commands + cell + "\n"
            y = commands.rstrip().lstrip().splitlines()
            lst = list(y)
            data_list = []
            final_list = []

            for line in lst:

                if line not in final_list:
                    final_list.append(line)
                else:
                    data_list.append(line)
                str0 = ""
                for elem in final_list:
                    str0 = str0 + elem + "\n                             \n"
                    str2 = str0.rstrip().lstrip()
                    self.textEdit.setText(str(str2))

        except (FileNotFoundError,KeyError,pandas.errors.ParserError,AttributeError,TypeError,UnicodeDecodeError,NameError) as error:
            self.textEdit.setText("No File Selected or Wrong file selected")
            print(error)

    def withjit(self):

        try:
            # dialog = QFileDialog.getOpenFileName()
            # path = dialog[0]
            # #print(path)
            self.label.setText("Commands\nWithJIT:\nNoDuplicates")
            #self.textEdit_2.clear()

            text ,incident_id = QtWidgets.QInputDialog.getText(Mainwindow, 'Incident details', 'Enter incident ID :')
            if text and incident_id:
                incident_id = text
            dfs = pandas.read_csv(path , encoding= 'ISO-8859–1')
            df = pandas.DataFrame(dfs)

            commands = ""
            for i, item in df.iterrows():
                remosp = item["Cluster"]
                cell = "\\\\reddog\Builds\\branches\git_azure_compute_master_latest\\retail-amd64\Services\Controller\FcShell\scripts\BatchingUpdateForAllNodesOfTenantWhoSkippedHEUpdate.ps1 -clusterName " + str(remosp.strip()) + " -incidentId " + str(incident_id) + " -TenantName " + str(item["TenantName"].strip())
                commands = commands + cell + "\n"
            y = commands.splitlines()
            lst = list(y)
            final_list = []

            for line in lst:
                if line not in final_list:
                    final_list.append(line)
                else:
                    pass
                str0 = ""
                for elem in final_list:
                    str0 = str0 + elem + "\n                             \n"
                    str2 = str0.rstrip().lstrip()
                    self.textEdit.setText(str(str2))

        except (FileNotFoundError,KeyError,pandas.errors.ParserError,AttributeError,TypeError,UnicodeDecodeError,NameError) as error:
            self.textEdit.setText("No File Selected or Wrong file selected")
            print(error)
    def checkcsv(self):
        global commands
        global path
        try:
            dialog = QFileDialog.getOpenFileName()

            path = dialog[0]
            print(os.path.basename(path))
            print(path)
            self.label.setText("Commands :")
            #self.textEdit.setText(str(path))
            # self.pathlabel.setText(str(os.path.basename(path)))
            self.pathlabel.setText("File Path : " + str(path))
            self.textEdit.clear()
            #self.textEdit_2.clear()
            #self.label.setText("File Path :")
            # text, incident_id = QtWidgets.QInputDialog.getText(Mainwindow, 'Incident details', 'Enter incident ID :')
            # if text and incident_id:
            #     incident_id = text
            # dfs = pandas.read_csv(path)
            # df = pandas.DataFrame(dfs)
            # #self.textEdit.setText(str(df))
            #
            # commands = ""
            # for i,item in df.iterrows():
            #     cell = "\\\\reddog\Builds\\branches\git_azure_compute_master_latest\\retail-amd64\Services\Controller\FcShell\scripts\BatchingUpdateForAllNodesOfTenantWhoSkippedHEUpdate.ps1 -clusterName " + str(item["Cluster"]) + " -incidentId " + str(incident_id) + " -TenantName " + str(item["TenantName"])
            #
            #     commands = commands + cell + "\n"
            # print(commands)
            #     #data = self.textEdit.setText(str(commands))


        except (FileNotFoundError,KeyError,pandas.errors.ParserError,AttributeError,UnicodeDecodeError) as error:
            self.textEdit.setText(str(error))#"No File Selected or Wrong file selected")

    def duplicate_check(self):
        self.label.setText("Duplicate Tenants :")

        try:
            dfs = pandas.read_csv(path, encoding='ISO-8859–1')
            df = pandas.DataFrame(dfs)


            commands = ""
            for i, item in df.iterrows():
                cell = "\\\\reddog\Builds\\branches\git_azure_compute_master_latest\\retail-amd64\Services\Controller\FcShell\scripts\BatchingUpdateForAllNodesOfTenantWhoSkippedHEUpdate.ps1 -clusterName " + str(
                    item["Cluster"]) + " -TenantName " + str(item["TenantName"])
                commands = commands + cell + "\n"
            y = commands.splitlines()
            #le = len(y)
            #print(le)
            #x = self.textEdit.toPlainText()  # anchorAt(Mainwindow)
            #self.label_2.setText("Duplicates :")
            lst = list(y)
            # using regular logic
            data_list = []
            final_list = []
            strd2 = ""
            self.label.setText("Duplicate Tenants :")
            for item in lst:
                if item not in final_list:
                    final_list.append(item)
                else:
                    data_list.append(item)
            if len(data_list) > 0:
                #print(len(data_list))
                for elem in data_list:
                    #print(elem)
                    elem2 = elem.rstrip().lstrip().split()

                    tenantelem = elem2[4]
                    tenantclust = elem2[2]
                    strd2 = strd2 + tenantclust + "    " + tenantelem + "\n"
                self.textEdit.setText( "Duplicate Tenants : " + str(len(data_list)) + "\n \n \n" + " Clusters                   Tenants \n" + str(strd2)) #"Total Tenants : " + str(len(y)) + "\n" +

            else:
                self.textEdit.setText( "No Duplicates Found.") # "Total Tenants : " + str(len(y)) + "\n \n" +)
                #print("0")

        except (FileNotFoundError,KeyError,pandas.errors.ParserError,AttributeError,UnicodeDecodeError,NameError, TypeError) as error:
            self.textEdit.setText("No File Selected or Wrong file selected")


    def clear(self):
        self.textEdit.clear()
        #self.textEdit_2.clear()
        self.label.setText("Commands :")
        # self.pathlabel.clear()
        # self.pathlabel.setText("")

    # def Tenants(self):
    #
    #     try:
    #         x = self.textEdit.toPlainText()  # anchorAt(Mainwindow)
    #         self.label_2.setText("Duplicates :")
    #         y = x.splitlines()
    #         lst = list(y)
    #         # using regular logic
    #         data_list = []
    #         final_list = []
    #         for item in lst:
    #             if item not in final_list:
    #                 final_list.append(item)
    #             else:
    #                 data_list.append(item)
    #             strd2 = ""
    #             for elem in data_list:
    #                 elem2 = elem.rstrip().lstrip().split()
    #                 finalelem = elem2[6]
    #                 strd = finalelem + "\n \n"
    #                 strd2 = strd2 + strd
    #                 self.textEdit_2.setText(str(strd2))
    #
    #     except (IndexError,KeyError,pandas.errors.ParserError,TypeError,IndexError,UnicodeDecodeError,NameError) as error:
    #         self.textEdit_2.setText(error)

    # def NoDuplicates(self):
    #     try:
    #         x = self.textEdit.toPlainText()  # anchorAt(Mainwindow)  #text()
    #         y = x.splitlines()
    #         lst = list(y)
    #         # using regular logic
    #         data_list = []
    #         final_list = []
    #         for item in lst:
    #             if item not in final_list:
    #                 final_list.append(item)
    #             else:
    #                 data_list.append(item)
    #             str0 = ""
    #             for elem in final_list:
    #                 str0 = str0 + elem + "\n   \n"
    #                 str2 = str0.rstrip().lstrip()
    #                 self.textEdit_2.setText(str(str2))
    #         self.label_2.setText("NoDuplicates :")
    #     except (IndexError,KeyError,pandas.errors.ParserError,TypeError,IndexError,UnicodeDecodeError) as error:
    #         self.textEdit_2.setText("Check format of the data table")



    def setupUi(self, Mainwindow):
        Mainwindow.setObjectName("Mainwindow")
        Mainwindow.resize(1270, 775)

        # w=Mainwindow
        # p = w.palette()
        # p.setColor(w.backgroundRole(), Qt.red)
        # w.setPalette(p)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), Qt.white)
        # self.setPalette(p)
        Mainwindow.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(0, 0, 0, 255));\n"
            "background-color: rgb(200, 200, 200);"
            "border-top-color: rgb(0, 0, 0);"
            #"font: 75 11pt \"Palatino Linotype\";"
            "border-color: rgb(0, 0, 0);")

        app.setStyle("Fusion")



        # Now use a palette to switch to dark colors:
        # palette = QPalette()
        # palette.setColor(QPalette.Window, QColor(53, 53, 53))
        # #palette.setColor(QPalette.WindowText, Qt.white)
        # palette.setColor(QPalette.Base, QColor(25, 25, 25))
        # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        # #palette.setColor(QPalette.ToolTipBase, Qt.white)
        # #palette.setColor(QPalette.ToolTipText, Qt.white)
        # #palette.setColor(QPalette.Text, Qt.white)
        # palette.setColor(QPalette.Button, QColor(53, 53, 53))
        # #palette.setColor(QPalette.ButtonText, Qt.white)
        # #palette.setColor(QPalette.BrightText, Qt.red)
        # palette.setColor(QPalette.Link, QColor(42, 130, 218))
        # palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        # #palette.setColor(QPalette.HighlightedText, Qt.black)
        # app.setPalette(palette)






        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        Mainwindow.setFont(font)
        Mainwindow.setFocusPolicy(QtCore.Qt.TabFocus)
        icon = QtGui.QIcon.fromTheme("CD")
        Mainwindow.setWindowIcon(icon)
        Mainwindow.setAnimated(True)
        Mainwindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        Mainwindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(Mainwindow)
        self.centralwidget.setObjectName("centralwidget")
 #
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(1100, 250, 130, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("checkduplicates")

        self.pushButton.clicked.connect(self.duplicate_check)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 250, 150, 121))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic Semilight")
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setMouseTracking(False)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setObjectName("label")
        # self.label_2 = QtWidgets.QLabel(self.centralwidget)
        # self.label_2.setGeometry(QtCore.QRect(10, 510, 141, 131))
        # font = QtGui.QFont()
        # font.setFamily("Malgun Gothic Semilight")
        # font.setPointSize(11)
        # font.setBold(True)
        # font.setWeight(75)
        # self.label_2.setFont(font)
        # self.label_2.setObjectName("label_2")
###
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(180, 30, 900, 600))#160, 10, 661, 341))

        #self.textEdit = QtWidgets.QTextEdit(Mainwindow)
        self.textEdit.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0568182 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
            "font: 75 10pt \"Calibri\";"
            "background-color: rgb(255, 255, 255);")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.textEdit.setFont(font)
        #self.textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
#####
        # self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        # self.textEdit_2.setGeometry(QtCore.QRect(180, 410, 900, 341))
        # font = QtGui.QFont()
        # font.setStyleStrategy(QtGui.QFont.PreferDefault)
        # self.textEdit_2.setFont(font)
        # self.textEdit_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        # self.textEdit_2.setObjectName("textEdit_2")
        Mainwindow.setCentralWidget(self.centralwidget)       ## to display
        # self.menubar = QtWidgets.QMenuBar(Mainwindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 22))
        # self.menubar.setObjectName("menubar")
        # self.menuFile = QtWidgets.QMenu(self.menubar)
        # self.menuFile.setObjectName("menuFile")
        # self.menuexit = QtWidgets.QMenu(self.menubar)
        # self.menuexit.setObjectName("menuexit")
        # Mainwindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(Mainwindow)
        # self.statusbar.setObjectName("statusbar")
        # Mainwindow.setStatusBar(self.statusbar)
        # self.menuexit.addSeparator()
        # self.menuexit.addSeparator()
        # self.menubar.addAction(self.menuFile.menuAction())
        # self.menubar.addAction(self.menuexit.menuAction())
##########
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setEnabled(True)
        self.pushButton1.setGeometry(QtCore.QRect(1100, 400, 130, 31))
        # self.pushButton1.setStyleSheet(
        #     "font: 75 11pt \"Calibri\";")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton1.setFont(font)
        self.pushButton1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton1.setFlat(False)
        self.pushButton1.setObjectName("clear")
        self.pushButton1.clicked.connect(self.clear)

#############################

        self.pushButtontenantcount = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtontenantcount.setEnabled(True)
        self.pushButtontenantcount.setGeometry(QtCore.QRect(1100, 325, 130, 31))
        # self.pushButton1.setStyleSheet(
        #     "font: 75 11pt \"Calibri\";")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtontenantcount.setFont(font)
        self.pushButtontenantcount.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtontenantcount.setFlat(False)
        self.pushButtontenantcount.setObjectName("Tenant Count")
        self.pushButtontenantcount.clicked.connect(self.tenantcount)

###############No duplicates button
        # self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton3.setEnabled(True)
        # self.pushButton3.setGeometry(QtCore.QRect(920, 360, 121, 31))
        # font = QtGui.QFont()
        # font.setFamily("Calibri")
        # font.setPointSize(9)
        # font.setBold(True)
        # font.setWeight(75)
        # self.pushButton3.setFont(font)
        # self.pushButton3.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.pushButton3.setFlat(False)
        # self.pushButton3.setObjectName("checkduplicates")
        # self.pushButton3.clicked.connect(self.NoDuplicates)
##############
        self.checkingcsv = QtWidgets.QPushButton(self.centralwidget)
        self.checkingcsv.setEnabled(True)
        self.checkingcsv.setGeometry(QtCore.QRect(180, 700, 130, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkingcsv.setFont(font)
        self.checkingcsv.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkingcsv.setFlat(False)
        self.checkingcsv.setObjectName("checkduplicates")
        self.checkingcsv.clicked.connect(self.checkcsv)
#################
        self.jitcommands = QtWidgets.QPushButton(self.centralwidget)
        self.jitcommands.setEnabled(True)
        self.jitcommands.setGeometry(QtCore.QRect(1100, 100, 130, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.jitcommands.setFont(font)
        self.jitcommands.setFocusPolicy(QtCore.Qt.NoFocus)
        self.jitcommands.setFlat(False)
        self.jitcommands.setObjectName("checkduplicates")
        self.jitcommands.clicked.connect(self.withjit)

####################
        self.nojitcommands = QtWidgets.QPushButton(self.centralwidget)
        self.nojitcommands.setEnabled(True)
        self.nojitcommands.setGeometry(QtCore.QRect(1100, 175, 130, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nojitcommands.setFont(font)
        self.nojitcommands.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nojitcommands.setFlat(False)
        self.nojitcommands.setObjectName("checkduplicates")
        self.nojitcommands.clicked.connect(self.withoutjit)

####################
        self.pathlabel = QtWidgets.QLabel(self.centralwidget)
        self.pathlabel.setGeometry(QtCore.QRect(180, 640, 1210, 31))
        # self.pathlabel.setStyleSheet(
        #     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0568182 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
        #     "font: 75 10pt \"Calibri\";"
        #     "background-color: rgb(255, 255, 255);")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.pathlabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic Semilight")
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.pathlabel.setFont(font)
        self.pathlabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pathlabel.setMouseTracking(False)
        self.pathlabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pathlabel.setObjectName("pathlabel")

        self.retranslateUi(Mainwindow)   ## to other function
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

    def retranslateUi(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("Mainwindow", "WADE - Batch Update Commands"))
        self.pushButton.setText(_translate("Mainwindow", "Duplicate Tenants"))
        self.pushButton1.setText(_translate("Mainwindow", "Clear Data"))
        #self.pushButton2.setText(_translate("Mainwindow", "Duplicate Tenants"))
        #self.pushButton3.setText(_translate("Mainwindow", "NoDuplicates"))
        self.label.setText(_translate("Mainwindow", "Commands :"))
        #self.label_2.setText(_translate("Mainwindow", "Duplicates :"))
        #self.menuFile.setTitle(_translate("Mainwindow", "File"))
        #self.menuexit.setTitle(_translate("Mainwindow", "exit"))
        self.checkingcsv.setText(_translate("Mainwindow", "Browse .csv"))
        self.jitcommands.setText(_translate("Mainwindow","Batch Update\nWithJit"))
        self.nojitcommands.setText(_translate("Mainwindow", "Batch Update\nWithoutJit"))
        # self.Updatebatch.setText(_translate("Mainwindow", "Mark Update\nBatch"))
        # self.UpdatebatchUM.setText(_translate("Mainwindow", "UnMark Update\nBatch"))
        self.pathlabel.setText(_translate("Mainwindow","File Path :"))
        self.pushButtontenantcount.setText(_translate("Mainwindow", "Tenant Count"))
        # self.textEdit.setHtml(_translate("Dialog",
        #                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        #                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        #                                  "p, li { white-space: pre-wrap; }\n"
        #                                  "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        #                                  "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Mainwindow = QtWidgets.QMainWindow()
    ui = Ui_Mainwindow()
    ui.setupUi(Mainwindow)
    #QColorDialog.getColor()
    Mainwindow.show()
    app.exec_()
    #sys.exit(app.exec_())
