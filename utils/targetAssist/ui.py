#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project  gAutoy
gAutoy Copyright (C) 2015 SGogolenko
All rights reserved

This file is part of gAutoy.

gAutoy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gAutoy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gAutoy.  If not, see <http://www.gnu.org/licenses/>.

######################################################################
@package      gAutoy
@file         ui.py
@author       Sergiy Gogolenko
@license      GPLv3

GUI for targetAssist.
######################################################################
"""
from __future__ import print_function
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

def message(*objs):
    import sys
    #print("MESSAGE: ", *objs, file=sys.stderr)
def error(*objs):
    import sys
    print("ERROR: ", *objs, file=sys.stderr)

import sys, os
# sys.path = [os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))] + sys.path
import gautoy

from PyQt4 import QtGui, QtCore

class CustomComboBox(QtGui.QComboBox):
    signal_hided = QtCore.pyqtSignal()
    signal_shown = QtCore.pyqtSignal()
    def hideEvent(self, event):
        super(CustomComboBox, self).hideEvent(event)
        self.signal_hided.emit()

    def showEvent(self, event):
        super(CustomComboBox, self).showEvent(event)
        self.signal_shown.emit()

class CustomLineEdit(QtGui.QLineEdit):
    signal_hided = QtCore.pyqtSignal()
    signal_shown = QtCore.pyqtSignal()
    def hideEvent(self, event):
        super(CustomLineEdit, self).hideEvent(event)
        self.signal_hided.emit()

    def showEvent(self, event):
        super(CustomLineEdit, self).showEvent(event)
        self.signal_shown.emit()

class GUITartetApp(QtGui.QWidget):
    
    def __init__(self, app, 
                 targets, uid, pwd,
                 ssh_shell_path, ssh_client_path,
                 actions, targetDirs,
                 defaultLocalWD, defaultTargetWD, 
                 defaultLocalProduction, defaultTargetBackup):
        super(GUITartetApp, self).__init__()
        self.application = app
        self.setWindowIcon(QtGui.QIcon('targetAssist.ico'))

        self.__targets = targets
        self.targetDirs = targetDirs

        self.uid, self.pwd   = uid, pwd
        self.ssh_shell_path  = ssh_shell_path
        self.ssh_client_path = ssh_client_path

        self.__actions = actions

        self.defaultLocalProduction = defaultLocalProduction
        self.defaultLocalWD  = defaultLocalWD

        self.defaultTargetWD = defaultTargetWD
        self.defaultTargetBackup  = defaultTargetBackup

        self.initUI()

        # self.qleLocalWD.setText(self.defaultLocalWD)
        # self.qleLocalProduction.setText(self.defaultLocalProduction)
        # self.qleTargetWD.setText(self.)
        # self.qleTargetBackup.setText(self.targetDirs['Default'])

        self.setAcceptDrops(True)

    def initUI(self):      

        self.lblTarget = QtGui.QLabel('Target:', self)
        self.lblTarget.move(10, 22)

        comboTarget = QtGui.QComboBox(self)
        for target in self.__targets:
            comboTarget.addItem(target)
        comboTarget.move(50, 20)
        comboTarget.activated[str].connect(self.targetChanged)

        self.cbWriteable = QtGui.QCheckBox('Write bin', self)
        self.cbWriteable.move(175, 22)
        #cbWriteable.toggle()
        self.cbWriteable.stateChanged.connect(self.changeReadability)

        btnConsole = QtGui.QPushButton('Console', self)
        btnConsole.setToolTip('Run PUTTY console for the selected target')
        btnConsole.resize(btnConsole.sizeHint())
        btnConsole.move(275, 20)
        btnConsole.clicked.connect(self.openConsole)

        ############################################################
        # Action section
        ############################################################

        lblAction = QtGui.QLabel('Action:', self)
        lblAction.move(10, 50)

        self.comboAction = QtGui.QComboBox(self)
        for target in self.__actions.keys():
            self.comboAction.addItem(target)
        self.comboAction.move(50, 50)
        self.comboAction.activated[str].connect(self.actionChanged)

        self.btnAction = QtGui.QPushButton('Do', self) #QtGui.QIcon('open.png')
        self.btnAction.setToolTip('Select folder with source files')
        self.btnAction.resize(btnConsole.sizeHint())
        self.btnAction.move(275, 50)
        self.btnAction.clicked.connect(self.actionExecute)
        self.btnAction.setDisabled(True)

        self.qleParameter = CustomLineEdit(self)
        self.qleParameter.move(140, 50)

        self.qleParameter.signal_hided.connect(self.qleParameter.hide)
        self.qleParameter.signal_shown.connect(self.qleParameter.show)
        self.qleParameter.setFixedWidth(125)
        self.qleParameter.hide()

        self.comboParameter = CustomComboBox(self)
        self.comboParameter.move(140, 50)
        self.comboParameter.setFixedWidth(125)
        # self.comboParameter.activated[str].connect(self.targetChanged)
        self.comboParameter.hide()

        self.comboParameter.signal_hided.connect(self.comboParameter.hide)
        self.comboParameter.signal_shown.connect(self.comboParameter.show)

        ############################################################
        # Work directory section
        ############################################################

        lblTargetWD = QtGui.QLabel('Target work directory', self)
        lblTargetWD.move(10, 100)
        self.qleTargetWD = QtGui.QLineEdit(self)
        self.qleTargetWD.move(125, 100)
        self.qleTargetWD.setText(self.defaultTargetWD)

        lblLocalWD = QtGui.QLabel('Local work directory', self)
        lblLocalWD.move(10, 125)
        self.qleLocalWD = QtGui.QLineEdit(self)
        self.qleLocalWD.move(125, 125)
        self.qleLocalWD.setText(self.defaultLocalWD)

        btnLocalWD = QtGui.QPushButton('Open', self) #QtGui.QIcon('open.png')
        btnLocalWD.setToolTip('Select folder with source files')
        btnLocalWD.resize(btnConsole.sizeHint())
        btnLocalWD.move(275, 125)
        btnLocalWD.clicked.connect(self.dialogueLocalWD)

        comboTargetWD = QtGui.QComboBox(self)
        comboTargetWD.addItem('Default')
        for folder in self.targetDirs:
            comboTargetWD.addItem(folder)
        comboTargetWD.move(275, 100)
        comboTargetWD.activated[str].connect(self.targetWDChanged)

        ############################################################
        # Binaries directory section
        ############################################################

        lblTargetBackup = QtGui.QLabel('Target backup directory', self)
        lblTargetBackup.move(10, 150)
        self.qleTargetBackup = QtGui.QLineEdit(self)
        self.qleTargetBackup.move(125, 150)
        self.qleTargetBackup.setText(self.defaultTargetBackup)

        lblLocalProduction = QtGui.QLabel('Production directory', self)
        lblLocalProduction.move(10, 175)
        self.qleLocalProduction = QtGui.QLineEdit(self)
        self.qleLocalProduction.move(125, 175)
        self.qleLocalProduction.setDisabled(True)
        self.qleLocalProduction.setText(self.defaultLocalProduction)

        btnLocalProduction = QtGui.QPushButton('Open', self) #QtGui.QIcon('open.png')
        btnLocalProduction.setToolTip('Select folder with binaries')
        btnLocalProduction.resize(btnConsole.sizeHint())
        btnLocalProduction.move(275, 175)
        btnLocalProduction.clicked.connect(self.dialogueLocalProduction)

        comboTargetBackup = QtGui.QComboBox(self)
        comboTargetBackup.addItem('Default')
        for folder in self.targetDirs:
            comboTargetBackup.addItem(folder)
        comboTargetBackup.move(275, 150)
        comboTargetBackup.activated[str].connect(self.targetBackupChanged)

        ############################################################
        # Geometry section
        ############################################################

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('No active target')
        self.show()
        
    def targetChanged(self, text):
        self.cbWriteable.setCheckState(False)
        self.setTarget(text, 
                       uid = self.uid, pwd = self.pwd,
                       ssh_shell_path  = self.ssh_shell_path,
                       ssh_client_path = self.ssh_client_path)
        self.setWindowTitle('{0} (ReadOnly)'.format(text))

    def actionChanged(self, text):
        actName = self.__actions[str(text)]
        if hasattr(self, actName):
            import inspect
            args = inspect.getargspec(eval('self.{0}'.format(actName))).args
            if len(args) == 1:
                self.comboParameter.hide()
                self.qleParameter.hide()
            else:
                default_param = eval('self.{0}(None)'.format(actName))
                if hasattr(default_param, '__iter__'):
                    self.comboParameter.clear()
                    for param in default_param:
                        self.comboParameter.addItem(param)
                    self.comboParameter.show()
                    self.qleParameter.hide()
                else:
                    self.qleParameter.setText(str(default_param))
                    self.comboParameter.hide()
                    self.qleParameter.show()
            self.btnAction.setDisabled(False)
        else:
            self.btnAction.setDisabled(True)
            
        message('Selected action: {0}'.format(str(text)))

    def actionExecute(self, text):
        actName = self.__actions[str(self.comboAction.currentText())]
        if hasattr(self, actName):
            self.btnAction.setText('In progress')
            self.btnAction.setDisabled(True)
            self.application.processEvents()
            message("self.btnAction.setText('In progress')")
            if   not self.comboParameter.isHidden():
                eval('self.{0}(str(self.comboParameter.currentText()))'.format(actName))
                message('Execute action: {0}({1})'.format(self.currentAction, self.comboParameter.currentText()))
            elif not self.qleParameter.isHidden():
                eval('self.{0}(str(self.qleParameter.text()))'.format(actName))
                message('Execute action: {0}({1})'.format(self.currentAction, self.qleParameter.text()))
            else:
                eval('self.{0}()'.format(actName))
                message('Execute action: {0}()'.format(actName))
            self.btnAction.setText('Do')
            self.btnAction.setDisabled(False)
            self.application.processEvents()

    def targetBackupChanged(self, text):
        folder = self.targetDirs.get(str(text),self.defaultTargetBackup)
        self.qleTargetBackup.setText(folder)
        message('Changed target bin to {0}'.format(folder))

    def targetWDChanged(self, text):
        folder = self.targetDirs.get(str(text),self.defaultTargetWD)
        self.qleTargetWD.setText(folder)
        message('Changed target WD to {0}'.format(folder))

    def changeReadability(self, state):
        self.setWindowTitle('{0} {1}'.format(self.target.ip,
                                             '' if state == QtCore.Qt.Checked else '(ReadOnly)'))
        self.mountRead(state)

    def dialogueLocalWD(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, 'Choose Directory', self.localWD)
        localWD = str(folder) if len(folder) > 0 else self.localWD
        self.qleLocalWD.setText(localWD)

    def dialogueLocalProduction(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, 'Choose Directory', self.localProduction)
        localProduction = str(folder) if len(folder) > 0 else self.localProduction
        self.qleLocalProduction.setText(localProduction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile().toLocal8Bit().data()
            self.putTargetWD(path)

    ############################################################
    @property
    def localWD(self):
        return str(self.qleLocalWD.text())

    @property
    def localProduction(self):
        return str(self.qleLocalProduction.text())

    @property
    def localBin(self):
        return os.path.join(self.localProduction, r'hu_ctrl\exe\imp')

    @property
    def targetWD(self):
        return str(self.qleTargetWD.text()) #self.comboTargetWD.currentText())

    @property
    def targetBackup(self):
        return str(self.qleTargetBackup.text()) #self.comboTargetBackup.currentText())

    @property
    def targetBin(self):
        return self.targetDirs['Navigation Bin']

    @property
    def currentAction(self):
        return str(self.comboAction.currentText())

    ############################################################

    def putTargetWD(self, path):
        if os.path.isfile(path):
            message(path)

    def setTarget(self, text):
        message('Set target {0}'.format(text))

    def mountRead(self, is_readable):
        pass

    def openConsole(self):
        message('Open console')
        

