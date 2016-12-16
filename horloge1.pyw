#!/usr/bin/env python
#-*- coding:latin-1 -*- 
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import (QApplication, QMainWindow, QGraphicsItem,QGraphicsScene, QGraphicsView, QPen, QStyle)
from PyQt4.QtCore import QObject, pyqtSignal, SLOT, Qt, QCoreApplication
from collections import defaultdict
from threading import Thread
from PyQt4.QtCore import QThread
from threading import BoundedSemaphore, Lock, Thread
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qtcore
from datetime import date
import time,sys,os,logging,subprocess,re,socket,threading,datetime 
import signal
from PyQt4.QtCore import QObject, pyqtSignal, SLOT, Qt, QCoreApplication

#Reglage
VERSION="v004"


class window(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(window, self).__init__(parent)
		self.sig = qtcore.SIGNAL("sig")

	def keyPressEvent(self, e):
		self.emit(self.sig,e)
	
	def initWindow(self):
		self.setWindowTitle("Horloge")
		self.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1))
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet("background-color:rgb(0, 0, 0);")
		

class window1(window, QtGui.QWidget):
	def __init__(self, parent=None):
		super(window1, self).__init__(parent)
		self.initWindow()
		self.show()

	
class window2(window, QtGui.QWidget):
	def __init__(self, parent=None):
		super(window2, self).__init__(parent)
		self.initWindow()

def signal(e):
	if e.key() == QtCore.Qt.Key_F1:
		w1.show()
		w2.hide()
	elif e.key() == QtCore.Qt.Key_F2:
		w2.show()
		w1.hide()
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	w1 = window1()
	QObject.connect(w1,w1.sig, signal)

	w2 = window2()
	QObject.connect(w2,w2.sig, signal)

	sys.exit(app.exec_())


