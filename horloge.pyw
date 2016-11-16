#!/usr/bin/env python
#-*- coding:latin-1 -*- 
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import (QApplication, QMainWindow, QGraphicsItem,QGraphicsScene, QGraphicsView, QPen, QStyle)
from PyQt4.QtCore import QObject, pyqtSignal, SLOT, Qt, QCoreApplication
from collections import defaultdict
from threading import Thread
from threading import BoundedSemaphore, Lock, Thread
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qtcore
from datetime import date
#from tkinter import *

import time,sys,os,logging,subprocess,re,socket,threading,datetime 

#Version
VERSION="v004"

app = qt.QApplication(sys.argv)


def main():
	w = widget()
	w.show()
	sys.exit(app.exec_())
	
class widget(qt.QWidget):
	
	def __init__(self, parent=None):
		qt.QWidget.__init__(self)
		
		self.TempsAssi_min = 15
		self.RAZChrono = True
		
		# Récupération de l'heure actuel
		self.Hcurent= datetime.datetime(int(time.strftime("20%y")),int(time.strftime("%m")),int(time.strftime("%d")),int(time.strftime("%H")), int(time.strftime("%M")),  int(time.strftime("%S")))

		# SET HEURE IN
		self.Hin = self.Hcurent
		# SET HEURE OUT
		self.Hout = self.Hin

		self.Reseize_pointSize=True
		self.Reseize_refHeight=768
		
		# Fenêtre principal
		self.MainWindow_backgroundColor="background-color:rgb(0, 0, 0);"
		self.MainWindow_backgroundColorTop=QColor(44,102,126)
		self.MainWindow_backgroundYTop=110
		self.MainWindow_backgroundColorBottom=QColor(212,207,203)
		self.MainWindow_windowTitle="Horloge"
		self.MainWindow_lineSup=QPen(QColor(228,115,33),30)
		self.MainWindow_lineInf=QPen(QColor(83,84,89),30)
		self.MainWindow_logoPath=sys.path[0]+"\\"+"logo.png"
		self.MainWindow_logoBackgroundColor="rgba(0,0,0,0%)"
		self.MainWindow_logoWidth=300
		self.MainWindow_logoHeight=100	
		
		# Label text pilote
		self.Pilote_textColor="rgb(255, 255, 255)"
		self.Pilote_textBackgroundColor="rgba(0,0,0,0%)"
		self.Pilote_textFont_Police="Arial Unicode MS"
		self.Pilote_textFont_PointSize=40
		self.Pilote_textFont_Bold=True
		self.Pilote_textBorderRadius=""
		self.Pilote_textY=10
		# Label Heure réel
		self.Hreel_textColor="rgb(255, 255, 255)"
		self.Hreel_backgroundColor="rgba(0,0,0,0%)"
		self.Hreel_police="arial"
		self.Hreel_bold=True
		self.Hreel_pointSize=60
		self.Hreel_textBorderRadius=""
		# Heure IN
		self.Hin_text="Service in"
		self.Hin_textColor="rgb(0, 0, 0)"
		self.Hin_backgroundColor="rgba(0,0,0,0%)"
		self.Hin_police="Arial Unicode MS"
		self.Hin_bold=True
		self.Hin_pointSize=45
		self.Hin_textBorderRadius=""
		# Heure OUT
		self.Hout_text="Service out"
		self.Hout_textColor="rgb(0, 0, 0)"
		self.Hout_backgroundColor="rgba(0,0,0,0%)"
		self.Hout_police="Arial Unicode MS"
		self.Hout_bold=True
		self.Hout_pointSize=45
		self.Hout_textBorderRadius=""
		self.Hout_textY=10
		# Heure Decompte
		self.Hdec_textColor="rgb(0, 0, 0)"
		self.Hdec_backgroundColor="rgba(0,0,0,0%)"
		self.Hdec_police="Arial Unicode MS"
		self.Hdec_bold=True
		self.Hdec_pointSize=250
		self.Hdec_textBorderRadius=""

		# Fenêtre principal
		self.setWindowTitle(self.MainWindow_windowTitle)
		self.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1))
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet(self.MainWindow_backgroundColor)

		# Event painter
		rec = qt.QDesktopWidget().screenGeometry(screen=1)
		x=rec.x()
		y=rec.y()
		width=rec.width()
		height=rec.height()
		rec.setX(0)
		rec.setY(0)
		rec.setHeight(height)
		rec.setWidth(width)

		event = QtGui.QPaintEvent(rec)
		self.paintEvent(event)

		mainLayout = QtGui.QGridLayout(self)
		
		# Reseize pointSize
		if self.Reseize_pointSize:
			self.MainWindow_backgroundYTop = qt.QApplication.desktop().height() * self.MainWindow_backgroundYTop / self.Reseize_refHeight
			self.Pilote_textFont_PointSize=qt.QApplication.desktop().height() * self.Pilote_textFont_PointSize / self.Reseize_refHeight
			self.Hreel_pointSize=qt.QApplication.desktop().height() * self.Hreel_pointSize / self.Reseize_refHeight
			self.Hout_pointSize = qt.QApplication.desktop().height() * self.Hout_pointSize / self.Reseize_refHeight
			self.Hin_pointSize = qt.QApplication.desktop().height() * self.Hin_pointSize / self.Reseize_refHeight
			self.Hdec_pointSize = qt.QApplication.desktop().height() * self.Hdec_pointSize / self.Reseize_refHeight
			self.Pilote_textY = qt.QApplication.desktop().height() * self.Pilote_textY / self.Reseize_refHeight
			self.MainWindow_logoWidth = qt.QApplication.desktop().height() * self.MainWindow_logoWidth / self.Reseize_refHeight
			self.MainWindow_logoHeight = qt.QApplication.desktop().height() * self.MainWindow_logoHeight / self.Reseize_refHeight

		# Label nom pilote
		self.labelTextPilote= QtGui.QLabel("M. FREINE / M. TARD")
		self.labelTextPilote.setParent(self)
		font = QFont(self.Pilote_textFont_Police)
		font.setPointSize(self.Pilote_textFont_PointSize)
		font.setBold(self.Pilote_textFont_Bold)
		self.labelTextPilote.setFont(font)
		self.labelTextPilote.setStyleSheet('background-color: '+self.Pilote_textBackgroundColor+'; color: '+self.Pilote_textColor+';')
		self.labelTextPilote.setGeometry(10, self.Pilote_textY, 1000, 100)

		# Label heure
		self.labelHeureReel = QtGui.QLabel(time.strftime('%H:%M:%S',time.localtime()))
		font = QFont(self.Hreel_police)
		font.setPointSize(self.Hreel_pointSize)
		font.setBold(self.Hreel_bold)
		self.labelHeureReel.setFont(font)
		self.labelHeureReel.setStyleSheet('background-color: '+self.Hreel_backgroundColor+'; color:'+self.Hreel_textColor+'; border-radius: '+self.Hreel_textBorderRadius+';')
		mainLayout.addWidget(self.labelHeureReel,0,3,1,1,Qt.AlignTop|Qt.AlignRight)

		# Label decompte
		self.labelDec = QtGui.QLabel("0:00:00")
		font = QFont(self.Hdec_police)
		font.setPointSize(self.Hdec_pointSize)
		font.setBold(self.Hdec_bold)
		self.labelDec.setFont(font)
		self.labelDec.setStyleSheet('background-color: '+self.Hdec_backgroundColor+'; color:'+self.Hdec_textColor+'; border-radius: '+self.Hdec_textBorderRadius+';')
		mainLayout.addWidget(self.labelDec,3,0,10,4,Qt.AlignCenter|Qt.AlignTop)

		# Label text heure in
		self.labelTextHeureIn = QtGui.QLabel(self.Hin_text)
		font = QFont(self.Hin_police)
		font.setPointSize(self.Hin_pointSize)
		font.setBold(self.Hin_bold)
		self.labelTextHeureIn.setFont(font)
		self.labelTextHeureIn.setStyleSheet('background-color: '+self.Hin_backgroundColor+'; color:'+self.Hin_textColor+'; border-radius: '+self.Hin_textBorderRadius+';')
		mainLayout.addWidget(self.labelTextHeureIn,13,0,Qt.AlignLeft|Qt.AlignBottom)
		# Label heure in
		self.labelHeureIn = QtGui.QLabel()
		font = QFont(self.Hin_police)
		font.setPointSize(self.Hin_pointSize)
		font.setBold(self.Hin_bold)
		self.labelHeureIn.setFont(font)
		self.labelHeureIn.setStyleSheet('background-color: '+self.Hin_backgroundColor+'; color:'+self.Hin_textColor+'; border-radius: '+self.Hin_textBorderRadius+';')
		mainLayout.addWidget(self.labelHeureIn,13,1,Qt.AlignLeft|Qt.AlignBottom)
		
		# Label text heure out
		self.labelTextHeureOut = QtGui.QLabel(self.Hout_text)
		font = QFont(self.Hout_police)
		font.setPointSize(self.Hout_pointSize)
		font.setBold(self.Hout_bold)
		self.labelTextHeureOut.setFont(font)
		self.labelTextHeureOut.setStyleSheet('background-color: '+self.Hout_backgroundColor+'; color:'+self.Hout_textColor+'; border-radius: '+self.Hout_textBorderRadius+';')
		mainLayout.addWidget(self.labelTextHeureOut,14,0,Qt.AlignLeft|Qt.AlignBottom)

		# Label heure out
		self.labelHeureOut = QtGui.QLabel()
		font = QFont(self.Hout_police)
		font.setPointSize(self.Hout_pointSize)
		font.setBold(self.Hout_bold)
		self.labelHeureOut.setFont(font)
		self.labelHeureOut.setStyleSheet('background-color: '+self.Hout_backgroundColor+'; color:'+self.Hout_textColor+'; border-radius: '+self.Hout_textBorderRadius+';')
		mainLayout.addWidget(self.labelHeureOut,14,1,Qt.AlignLeft|Qt.AlignBottom)
		
		# Label Logo
		self.labelLogo = QtGui.QLabel(self)
		pix = QtGui.QPixmap(self.MainWindow_logoPath)
		self.labelLogo.setPixmap(pix.scaled(self.MainWindow_logoWidth, self.MainWindow_logoHeight,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
		self.labelLogo.setStyleSheet('background-color: '+self.MainWindow_logoBackgroundColor)
		mainLayout.addWidget(self.labelLogo,14,3,Qt.AlignRight|Qt.AlignBottom)

		# Set de la fenêtre principal
		self.setLayout(mainLayout)
		# Création d'un timer 1000ms qui génére un signal
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.updateLabel)
		self.timer.start(1000)
		
		self.razChrono()
		self.setWindow1()
		self.setWindow2()

	def paintEvent(self, event):
		self.painter=QPainter(self)
		r_topRec= qt.QDesktopWidget().screenGeometry(screen=1)
		x=r_topRec.x()
		y=r_topRec.y()
		width=r_topRec.width()
		height=r_topRec.height()
		r_topRec.setX(0)
		r_topRec.setY(0)
		r_topRec.setHeight(height)
		r_topRec.setWidth(width)
		r_topRec.setHeight(self.MainWindow_backgroundYTop)

		r_bottomRec= qt.QDesktopWidget().screenGeometry(screen=1)
		x=r_bottomRec.x()
		y=r_bottomRec.y()
		width=r_bottomRec.width()
		height=r_bottomRec.height()
		r_bottomRec.setX(0)
		r_bottomRec.setY(0)
		r_bottomRec.setHeight(height)
		r_bottomRec.setWidth(width)
		r_bottomRec.setY(self.MainWindow_backgroundYTop+3)
		r_bottomRec.setHeight(qt.QDesktopWidget().screenGeometry(screen=1).height()-r_topRec.height()-2)

		self.painter.fillRect(r_topRec,self.MainWindow_backgroundColorTop)
		self.painter.fillRect(r_bottomRec,self.MainWindow_backgroundColorBottom)

		# Line sup
		x1=qt.QDesktopWidget().screenGeometry(screen=1).width()
		x2=qt.QDesktopWidget().screenGeometry(screen=1).width()*12/20
		y1=qt.QDesktopWidget().screenGeometry(screen=1).height()*12/20
		y2=qt.QDesktopWidget().screenGeometry(screen=1).height()
		self.painter.setPen(self.MainWindow_lineSup)
		self.painter.drawLine(x1,y1,x2,y2)
		# Line inf
		x1=qt.QDesktopWidget().screenGeometry(screen=1).width()
		x2=qt.QDesktopWidget().screenGeometry(screen=1).width()*13/20
		y1=qt.QDesktopWidget().screenGeometry(screen=1).height()*13/20
		y2=qt.QDesktopWidget().screenGeometry(screen=1).height()
		self.painter.setPen(self.MainWindow_lineInf)
		self.painter.drawLine(x1,y1,x2,y2)

		self.painter.end()

	def updateLabel(self):
		# Mise à jour du label heure
		year=time.strftime("20%y")
		month=time.strftime("%m")
		day=time.strftime("%d")
		hour=time.strftime("%H")
		minute=time.strftime("%M")
		second=time.strftime("%S")
		self.Hcurent= datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
		
		self.labelHeureReel.setText(hour+":"+minute+":"+second)
		
		# Mise à jour du compte à rebour
		if self.Hout>=self.Hcurent and not self.RAZChrono:
			font = QFont(self.Hdec_police)
			font.setPointSize(self.Hdec_pointSize)
			font.setBold(self.Hdec_bold)
			self.labelDec.setFont(font)
			if self.Hout-self.Hcurent <=  datetime.timedelta(hours=0,minutes=3,seconds=0):
				self.Hdec_textColor="rgb(181, 0, 0)"
				self.labelDec.setStyleSheet('background-color: '+self.Hdec_backgroundColor+'; color:'+self.Hdec_textColor+'; border-radius: '+self.Hdec_textBorderRadius+';')
			else:
				self.Hdec_textColor="rgb(0, 0, 0)"
				self.labelDec.setStyleSheet('background-color: '+self.Hdec_backgroundColor+'; color:'+self.Hdec_textColor+'; border-radius: '+self.Hdec_textBorderRadius+';')
			if self.Hout-self.Hcurent > datetime.timedelta(hours=0,minutes=int(self.editorTempsAssi.text()),seconds=0):
				self.labelDec.setText(str(datetime.timedelta(hours=0,minutes=int(self.editorTempsAssi.text()),seconds=0)))
			else:
				self.labelDec.setText(str(self.Hout-self.Hcurent))

		elif self.Hcurent>self.Hout and not self.RAZChrono:
			self.Hdec_textColor="rgb(181, 0, 0)"
			self.labelDec.setStyleSheet('background-color: '+self.Hdec_backgroundColor+'; color:'+self.Hdec_textColor+'; border-radius: '+self.Hdec_textBorderRadius+';')
			font = QFont(self.Hdec_police)
			font.setPointSize(self.Hdec_pointSize-30)
			font.setBold(self.Hdec_bold)
			self.labelDec.setFont(font)
			self.labelDec.setText("+"+str(self.Hcurent-self.Hout))
	
	def setWindow1(self):
		self.window1 = None  # Initialisation
		self.window1 = QtGui.QWidget()
		self.window1.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1).x()+100, qt.QDesktopWidget().screenGeometry(screen=1).y()+100,100,100)
		self.window1.setWindowTitle("Reglages")
		self.mainLayoutwindow1 = QtGui.QGridLayout(self.window1)

		self.GroupBoxNomPilote= QtGui.QGroupBox("Nom pilote / copilote")
		layoutInfoNom = QtGui.QVBoxLayout()
		self.GroupBoxNomPilote.setLayout(layoutInfoNom)
		self.mainLayoutwindow1.addWidget(self.GroupBoxNomPilote,0,0,1,2)

		self.editorNom = QtGui.QLineEdit()
		self.editorNom.setFocusPolicy(Qt.TabFocus)
		self.editorNom.setFixedSize(500,30)
		layoutInfoNom.addWidget(self.editorNom)

		self.GroupBoxHin= QtGui.QGroupBox("Heure entree")
		layoutHin = QtGui.QGridLayout()
		self.GroupBoxHin.setLayout(layoutHin)
		self.mainLayoutwindow1.addWidget(self.GroupBoxHin,1,0,1,2)
		
		self.labelTextHin = QtGui.QLabel("Heure")
		layoutHin.addWidget(self.labelTextHin,0,0,1,1)

		self.labelTextHin = QtGui.QLabel("Minute")
		layoutHin.addWidget(self.labelTextHin,0,1,1,1)
		
		self.labelTextHin = QtGui.QLabel("Seconde")
		layoutHin.addWidget(self.labelTextHin,0,2,1,1)

		self.editorHin_h = QtGui.QLineEdit()
		self.editorHin_h.setFocusPolicy(Qt.TabFocus)
		layoutHin.addWidget(self.editorHin_h,1,0,1,1)

		self.editorHin_m = QtGui.QLineEdit()
		self.editorHin_m.setFocusPolicy(Qt.TabFocus)
		layoutHin.addWidget(self.editorHin_m,1,1,1,1)
		
		self.editorHin_s = QtGui.QLineEdit()
		self.editorHin_s.setFocusPolicy(Qt.TabFocus)
		layoutHin.addWidget(self.editorHin_s,1,2,1,1)

		self.GroupBoxTempsAssi= QtGui.QGroupBox("Temps assistance (en min)")
		layoutTempsAssi = QtGui.QGridLayout()
		self.GroupBoxTempsAssi.setLayout(layoutTempsAssi)
		self.mainLayoutwindow1.addWidget(self.GroupBoxTempsAssi,2,0,1,2)

		self.editorTempsAssi = QtGui.QLineEdit()
		self.editorTempsAssi.setFocusPolicy(Qt.TabFocus)
		layoutTempsAssi.addWidget(self.editorTempsAssi)
		
		self.buttonRAZ = QtGui.QPushButton("RAZ Chrono")
		self.buttonRAZ.setFocusPolicy(Qt.TabFocus)
		self.buttonRAZ.setAutoDefault(True)
		self.mainLayoutwindow1.addWidget(self.buttonRAZ,3,0,1,1)
		self.connect(self.buttonRAZ, QtCore.SIGNAL("clicked()"), self.sigWindow1ButtonRAZ)

		self.buttonOk = QtGui.QPushButton("Valider")
		self.buttonOk.setFocusPolicy(Qt.TabFocus)
		self.buttonOk.setAutoDefault(True)
		self.mainLayoutwindow1.addWidget(self.buttonOk,4,0,1,1)
		self.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), self.sigWindow1ButtonOk)
		
		self.buttonAnn = QtGui.QPushButton("Annuler")
		self.buttonAnn.setFocusPolicy(Qt.TabFocus)
		self.buttonAnn.setAutoDefault(True)
		self.mainLayoutwindow1.addWidget(self.buttonAnn,4,1,1,1)
		self.connect(self.buttonAnn, QtCore.SIGNAL("clicked()"), self.sigWindow1ButtonAnn)

	def setWindow2(self):
		self.window2 = None  # Initialisation
		self.window2 = QtGui.QWidget()
		self.window2.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1).x()+100, qt.QDesktopWidget().screenGeometry(screen=1).y()+100,400,100)
		self.window2.setWindowTitle("Infos systemes")
		
		self.mainLayoutwindow2 = QtGui.QGridLayout(self.window2)
		
		self.GroupBoxReglageH= QtGui.QGroupBox("Reglage heure systeme")
		layoutReglageH = QtGui.QGridLayout()
		self.GroupBoxReglageH.setLayout(layoutReglageH)
		self.mainLayoutwindow2.addWidget(self.GroupBoxReglageH,1,0,1,2)
		
		self.labelText = QtGui.QLabel("Heure")
		layoutReglageH.addWidget(self.labelText,0,0,1,1)

		self.labelText = QtGui.QLabel("Minute")
		layoutReglageH.addWidget(self.labelText,0,1,1,1)
		
		self.labelText  = QtGui.QLabel("Seconde")
		layoutReglageH.addWidget(self.labelText,0,2,1,1)

		self.editorSetH_h = QtGui.QLineEdit()
		self.editorSetH_h.setFocusPolicy(Qt.TabFocus)
		layoutReglageH.addWidget(self.editorSetH_h,1,0,1,1)

		self.editorSetH_m = QtGui.QLineEdit()
		self.editorSetH_m.setFocusPolicy(Qt.TabFocus)
		layoutReglageH.addWidget(self.editorSetH_m,1,1,1,1)
		
		self.editorSetH_s = QtGui.QLineEdit()
		self.editorSetH_s.setFocusPolicy(Qt.TabFocus)
		layoutReglageH.addWidget(self.editorSetH_s,1,2,1,1)

		self.buttonOk_w2 = QtGui.QPushButton("Valider")
		self.buttonOk_w2.setFocusPolicy(Qt.TabFocus)
		self.buttonOk_w2.setAutoDefault(True)
		self.mainLayoutwindow2.addWidget(self.buttonOk_w2,2,0,1,1)
		self.connect(self.buttonOk_w2, QtCore.SIGNAL("clicked()"), self.sigWindow2ButtonOk)
		
		self.buttonAnn_w2 = QtGui.QPushButton("Annuler")
		self.buttonAnn_w2.setFocusPolicy(Qt.TabFocus)
		self.buttonAnn_w2.setAutoDefault(True)
		self.mainLayoutwindow2.addWidget(self.buttonAnn_w2,2,1,1,1)
		self.connect(self.buttonAnn_w2, QtCore.SIGNAL("clicked()"), self.sigWindow2ButtonAnn)

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_F1:
			self.editorNom.setText(self.labelTextPilote.text())
			self.editorHin_h.setText(time.strftime("%H"))
			self.editorHin_m.setText(time.strftime("%M"))
			self.editorHin_s.setText("0")
			self.editorTempsAssi.setText(str(self.TempsAssi_min))

			self.window1.show()
			self.editorNom.setFocus()
		
		if e.key() == QtCore.Qt.Key_F2:
			self.editorSetH_h.setText(time.strftime("%H"))
			self.editorSetH_m.setText(time.strftime("%M"))
			self.editorSetH_s.setText(time.strftime("%S"))
		
			self.window2.show()
			self.editorNom.setFocus()
		
	def sigWindow1ButtonOk(self):
		self.window1.hide()
		#self.Hcurent= datetime.datetime(int(time.strftime("20%y")),int(time.strftime("%m")),int(time.strftime("%d")),int(time.strftime("%H")), int(time.strftime("%M")),  int(time.strftime("%S")))
		# SET HEURE IN
		self.Hin = datetime.datetime(int(time.strftime("20%y")),int(time.strftime("%m")),int(time.strftime("%d")),int(self.editorHin_h.text()),int(self.editorHin_m.text()), int(self.editorHin_s.text()))
		# SET HEURE OUT
		self.Hout = self.Hin+datetime.timedelta(hours=0,minutes=int(self.editorTempsAssi.text()),seconds=0) # (heure,minute,seconde)
		
		self.labelHeureOut.setText(" :   " +self.Hout.strftime("%H")+":"+self.Hout.strftime("%M")+":"+self.Hout.strftime("%S"))
		self.labelHeureIn.setText(" :   " + self.Hin.strftime("%H")+":"+ self.Hin.strftime("%M")+":"+self.Hin.strftime("%S"))
		self.labelTextPilote.setText(self.editorNom.text())
		self.RAZChrono = False
		
	def sigWindow1ButtonAnn(self):
		self.window1.hide()
	
	def sigWindow1ButtonRAZ(self):
		self.razChrono()
		self.window1.hide()

	def sigWindow2ButtonOk(self):
		self.window2.hide()
		
	def sigWindow2ButtonAnn(self):
		self.window2.hide()

	def razChrono(self):
		self.RAZChrono = True
		font = QFont(self.Hdec_police)
		font.setPointSize(self.Hdec_pointSize)
		font.setBold(self.Hdec_bold)
		self.labelDec.setFont(font)
		self.Hdec_textColor="rgb(0, 0, 0)"
		self.labelDec.setStyleSheet('background-color: '+self.Hdec_backgroundColor+'; color:'+self.Hdec_textColor+'; border-radius: '+self.Hdec_textBorderRadius+';')
		self.labelHeureOut.setText(" :   00:00:00")
		self.labelHeureIn.setText(" :   00:00:00")
		self.labelDec.setText("0:00:00")
		
main()
