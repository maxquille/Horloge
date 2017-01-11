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
import ConfigParser
import sys

#Reglage
SCRIPT_VERSION="1.0.0"
path_fileParam = "paramAppli.ini"
path_fileConf = "confAppli.ini"
logo_name = "logo.png"
pictureDriver_name = "photo_pilote.png"
archive_name = "patch_horloge.tar.gz"

class window(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self)
		self.sig = qtcore.SIGNAL("sig")
		self.Hcurent = datetime.datetime(int(2016),int(1),int(1),int(1),int(0),int(0))

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_F9:
			self.emit(self.sig,e)
		else:
			self.keyPressEventOverload(e)

	def updateCurrentDate(self):
		self.year=time.strftime("%Y")
		self.month=time.strftime("%m")
		self.day=time.strftime("%d")
		self.hour=time.strftime("%H")
		self.minute=time.strftime("%M")
		self.second=time.strftime("%S")
		
		self.Hcurent= datetime.datetime(int(self.year),int(self.month),int(self.day),int(self.hour),int(self.minute),int(self.second))

		self.labelHeureReel.setText(self.hour+":"+self.minute+":"+self.second)
		self.currentHlabelPopup2.setText(	self.hour + ":" +\
											self.minute + ":"+\
											self.second+ "  "+\
											self.day+ "/"+
											self.month+ "/"+\
											self.year +\
											"    (hh:mm:ss  jj/mm/aaaa)")

	def writeFileParam(self):
		fconfig = ConfigParser.ConfigParser()
		# Test presence du fichier de conf
		#try:
		#	with open(os.path.join(sys.path[0],path_fileParam)): 
		#		fconfig.read(os.path.join(sys.path[0],path_fileParam))
		#except IOError:
		fconfig.add_section('General')
		fconfig.add_section('Decompte')
		
		fconfig.set('General','nom_pilote_copilote',self.TextPilote)
		fconfig.set('General','duree_assistance_min',self.TempsAssi_min)
		fconfig.set('General','affichage_photo_pilote',self.displayPictureDriver)
		fconfig.set('Decompte','basculement1_min',self.decompteBasculement1_min)
		fconfig.set('Decompte','basculement2_min',self.decompteBasculement2_min)

		try:
			fconfig.write(open(os.path.join(sys.path[0],path_fileParam),'w'))
		except:
			False

	def readFileParam(self):
		fconfig = ConfigParser.ConfigParser()
		try:
			fconfig.read(os.path.join(sys.path[0],path_fileParam))
			self.TextPilote = fconfig.get('General','nom_pilote_copilote')
		except:
			self.TextPilote = "M. NomPilote / M. NomCopilote"
		
		try:
			self.TempsAssi_min = fconfig.getint('General','duree_assistance_min')
		except:
			self.TempsAssi_min = 15
		
		try:
			self.displayPictureDriver = fconfig.getboolean('General','affichage_photo_pilote')
		except:
			self.displayPictureDriver = False
		
		try:
			self.decompteBasculement1_min = fconfig.getint('Decompte','basculement1_min')
		except:
			self.decompteBasculement1_min = 5
		
		try:
			self.decompteBasculement2_min = fconfig.getint('Decompte','basculement2_min')
		except:
			self.decompteBasculement2_min = 0


	def readFileConf(self):
		fconfig = ConfigParser.ConfigParser()
		try:
			fconfig.read(os.path.join(sys.path[0],path_fileConf))
			self.version_Config = fconfig.get('General','version_config')
			self.version_Logo = fconfig.get('General','version_logo')
			temp = fconfig.get('General','couleur_fenetre_principal_haut')
			self.MainWindow_backgroundColorTop = QColor(int(temp.split(",")[0]),\
														int(temp.split(",")[1]),\
														int(temp.split(",")[2]))	
			temp = fconfig.get('General','couleur_fenetre_principal_bas')
			self.MainWindow_backgroundColorBottom = QColor(	int(temp.split(",")[0]),\
															int(temp.split(",")[1]),\
															int(temp.split(",")[2]))
			temp = fconfig.get('General','couleur_fenetre_principal_ligne_haut')
			self.MainWindow_lineSup = QPen(QColor(	int(temp.split(",")[0]),\
													int(temp.split(",")[1]),\
													int(temp.split(",")[2])),30)
			temp = fconfig.get('General','couleur_fenetre_principal_ligne_bas')
			self.MainWindow_lineInf = QPen(QColor(	int(temp.split(",")[0]),\
													int(temp.split(",")[1]),\
													int(temp.split(",")[2])),30)
			self.PoliceFont = fconfig.get('General','police_ecriture')
			self.Pilote_textFont_PointSize = fconfig.getint('LabelNomPilote','taille_police')
			self.Pilote_textColor = fconfig.get('LabelNomPilote','couleur_police')
			self.Pilote_textFont_Bold = fconfig.getboolean('LabelNomPilote','gras_police')
			self.Hreel_textColor = fconfig.get('LabelHeureReel','couleur_police')
			self.Hreel_bold = fconfig.getboolean('LabelHeureReel','gras_police')
			self.Hreel_pointSize = fconfig.getint('LabelHeureReel','taille_police')
			self.Hin_textColor = fconfig.get('LabelHinHout','couleur_police')
			self.Hout_textColor = fconfig.get('LabelHinHout','couleur_police')
			self.Hin_bold = fconfig.getboolean('LabelHinHout','gras_police')
			self.Hout_bold = fconfig.getboolean('LabelHinHout','gras_police')
			self.Hin_pointSize = fconfig.getint('LabelHinHout','taille_police')
			self.Hout_pointSize = fconfig.getint('LabelHinHout','taille_police')
			self.Hdec_pointSize = fconfig.getint('LabelDecompte','taille_police')
			self.Hdec_reducePointSize = fconfig.getint('LabelDecompte','reduction_taille_police_avec_signe')
			self.Hdec_textColor_nominal = fconfig.get('LabelDecompte','couleur_police_nominal')
			self.Hdec_textColor_phase1 = fconfig.get('LabelDecompte','couleur_police_phase1')
			self.Hdec_textColor_phase2 = fconfig.get('LabelDecompte','couleur_police_phase2')
			
		except:
			self.MainWindow_backgroundColorTop = QColor(44,102,126)
			self.MainWindow_backgroundColorBottom=QColor(212,207,203)
			self.MainWindow_lineSup=QPen(QColor(228,115,33),30)
			self.MainWindow_lineInf=QPen(QColor(83,84,89),30)
			self.PoliceFont = "Droid Sans"
			self.Pilote_textFont_PointSize=30
			self.Pilote_textColor="rgb(255, 255, 255)"
			self.Pilote_textFont_Bold=True
			self.Hreel_textColor="rgb(255, 255, 255)"
			self.Hreel_bold=True
			self.Hreel_pointSize=50
			self.Hin_textColor="rgb(0, 0, 0)"
			self.Hin_bold=True
			self.Hin_pointSize=45
			self.Hout_textColor="rgb(255, 0, 0)"
			self.Hout_bold=True
			self.Hout_pointSize=45
			self.Hdec_pointSize=280
			self.Hdec_reducePointSize=30
			self.Hdec_textColor_nominal = "rgb(0, 0, 0)"
			self.Hdec_textColor_phase1 = "rgb(212,207,203)"
			self.Hdec_textColor_phase2 = "rgb(181, 0, 0)"

	def setPictureDriverAndName(self, displayPicture):
		if displayPicture:
			try:
				with open(self.PhotoPilote_Path): 
					self.labelPhotoPilote = QtGui.QLabel(self)
					pix = QtGui.QPixmap(self.PhotoPilote_Path)
					self.labelPhotoPilote.setPixmap(pix.scaled(400, self.MainWindow_backgroundYTop-20,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))

					self.labelPhotoPilote.setStyleSheet('border:2px solid black; background-color: '+self.PhotoPilotePath_BackgroundColor)
					self.mainLayout.addWidget(self.labelTextPilote,0,1,1,5,Qt.AlignLeft)
					self.mainLayout.addWidget(self.labelPhotoPilote,0,0,1,1,Qt.AlignCenter)
			except IOError:
				self.mainLayout.addWidget(self.labelTextPilote,0,0,1,6,Qt.AlignLeft)
		else:
			
			self.mainLayout.addWidget(self.labelTextPilote,0,0,1,6,Qt.AlignLeft)
			try:
				if self.labelPhotoPilote:
					self.labelPhotoPilote.deleteLater()
			except:
				False

	def templateWindow(self):
		# Ajustement en fonction de la taille
		self.Reseize_pointSize=True
		self.Reseize_refHeight=768
		
		# Police d'ecriture
		#self.PoliceFont = "Droid Sans"

		# Fenêtre principal
		self.MainWindow_backgroundColor="background-color:rgb(0, 0, 0);"
		#self.MainWindow_backgroundColorTop=QColor(44,102,126)
		self.MainWindow_backgroundYTop=110
		#self.MainWindow_backgroundColorBottom=QColor(212,207,203)
		self.MainWindow_windowTitle="Horloge"
		#self.MainWindow_lineSup=QPen(QColor(228,115,33),30)
		#self.MainWindow_lineInf=QPen(QColor(83,84,89),30)
		self.MainWindow_logoPath=os.path.join(sys.path[0],logo_name)
		self.MainWindow_logoBackgroundColor="rgba(0,0,0,0%)"
		self.MainWindow_logoWidth=300
		self.MainWindow_logoHeight=100
		# Label text pilote
		#self.Pilote_textColor="rgb(255, 255, 255)"
		self.Pilote_textBackgroundColor="rgba(0,0,0,0%)"
		self.Pilote_textFont_Police=self.PoliceFont
		#self.Pilote_textFont_PointSize=30
		#self.Pilote_textFont_Bold=True
		self.Pilote_textBorderRadius=""
		self.Pilote_textY=10
		# Photo pilote
		self.PhotoPilote_Path = os.path.join(sys.path[0],pictureDriver_name)
		self.PhotoPilotePath_BackgroundColor="rgba(255,0,0,0%)"
		self.PhotoPilotePath_logoWidth=300
		self.PhotoPilotePath_logoHeight=100
		# Label Heure réel
		#self.Hreel_textColor="rgb(255, 255, 255)"
		self.Hreel_backgroundColor="rgba(0,0,0,0%)"
		self.Hreel_police=self.PoliceFont
		#self.Hreel_bold=True
		#self.Hreel_pointSize=50
		self.Hreel_textBorderRadius=""
		
		# Fenêtre principal
		self.setWindowTitle(self.MainWindow_windowTitle)
		self.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1))
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet(self.MainWindow_backgroundColor)


		# Event painter
		rec = qt.QDesktopWidget().screenGeometry(screen=0)
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
	
		self.mainLayout = QtGui.QGridLayout(self)

		# Reseize pointSize
		if self.Reseize_pointSize:
			self.MainWindow_backgroundYTop = qt.QApplication.desktop().height() * self.MainWindow_backgroundYTop / self.Reseize_refHeight
			self.Pilote_textFont_PointSize=qt.QApplication.desktop().height() * self.Pilote_textFont_PointSize / self.Reseize_refHeight
			self.Hreel_pointSize=qt.QApplication.desktop().height() * self.Hreel_pointSize / self.Reseize_refHeight
			self.Pilote_textY = qt.QApplication.desktop().height() * self.Pilote_textY / self.Reseize_refHeight
			self.MainWindow_logoWidth = qt.QApplication.desktop().height() * self.MainWindow_logoWidth / self.Reseize_refHeight
			self.MainWindow_logoHeight = qt.QApplication.desktop().height() * self.MainWindow_logoHeight / self.Reseize_refHeight
		

		# Label nom pilote
		self.labelTextPilote= QtGui.QLabel(self.TextPilote)
		self.labelTextPilote.setParent(self)
		font = QFont(self.Pilote_textFont_Police)
		font.setPointSize(self.Pilote_textFont_PointSize)
		font.setBold(self.Pilote_textFont_Bold)
		self.labelTextPilote.setFont(font)
		self.labelTextPilote.setStyleSheet('background-color: '+self.Pilote_textBackgroundColor+'; color: '+self.Pilote_textColor+';')
		#self.mainLayout.addWidget(self.labelTextPilote,0,1,1,5,Qt.AlignLeft)
		#self.mainLayout.addWidget(self.labelTextPilote,0,0,1,3,Qt.AlignLeft)

		# Label heure
		self.labelHeureReel = QtGui.QLabel(time.strftime('%H:%M:%S',time.localtime()))
		font = QFont(self.Hreel_police)
		font.setPointSize(self.Hreel_pointSize)
		font.setBold(self.Hreel_bold)
		self.labelHeureReel.setFont(font)
		self.labelHeureReel.setStyleSheet('background-color: '+self.Hreel_backgroundColor+'; color:'+self.Hreel_textColor+'; border-radius: '+self.Hreel_textBorderRadius+';')
		self.mainLayout.addWidget(self.labelHeureReel,0,6,1,1,Qt.AlignRight)
		#self.mainLayout.addWidget(self.labelHeureReel,0,3,1,1,Qt.AlignTop|Qt.AlignRight)

		# Label Logo
		try:
			with open(self.MainWindow_logoPath): 
				self.labelLogo = QtGui.QLabel(self)
				pix = QtGui.QPixmap(self.MainWindow_logoPath)
				self.labelLogo.setPixmap(pix.scaled(self.MainWindow_logoWidth, self.MainWindow_logoHeight,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
				self.labelLogo.setStyleSheet('background-color: '+self.MainWindow_logoBackgroundColor)
				self.mainLayout.addWidget(self.labelLogo,14,6,1,1,Qt.AlignBottom)
				#self.mainLayout.addWidget(self.labelLogo,14,3,1,1,Qt.AlignRight|Qt.AlignBottom)
		except IOError:
			False
		
		self.setPictureDriverAndName(self.displayPictureDriver)
		
		self.setLayout(self.mainLayout)
		

	def paintEvent(self, event):
		self.painter=QPainter(self)
		r_topRec= qt.QDesktopWidget().screenGeometry(screen=0)
		x=r_topRec.x()
		y=r_topRec.y()
		width=r_topRec.width()
		height=r_topRec.height()
		r_topRec.setX(0)
		r_topRec.setY(0)
		r_topRec.setHeight(height)
		r_topRec.setWidth(width)
		r_topRec.setHeight(self.MainWindow_backgroundYTop)

		r_bottomRec= qt.QDesktopWidget().screenGeometry(screen=0)
		x=r_bottomRec.x()
		y=r_bottomRec.y()
		width=r_bottomRec.width()
		height=r_bottomRec.height()
		r_bottomRec.setX(0)
		r_bottomRec.setY(0)
		r_bottomRec.setHeight(height)
		r_bottomRec.setWidth(width)
		r_bottomRec.setY(self.MainWindow_backgroundYTop+3)
		r_bottomRec.setHeight(qt.QDesktopWidget().screenGeometry(screen=0).height()-r_topRec.height()-2)

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

class window1(window):
	def __init__(self, parent=None):
		super(window1, self).__init__(parent)

		# Declaration des variables
		self.Hin = datetime.datetime(int(2016),int(1),int(1),int(1),int(0),int(0))
		self.Hout = datetime.datetime(int(2016),int(1),int(1),int(1),int(0),int(0))
		
		self.readFileParam()
		self.readFileConf()
		self.templateWindow()
		self.overload_window()
		self.setPopUp1()
		self.setPopUp2()
		self.setPopUp3()
		self.setPopUp4()
		self.setTimer()
		
		self.DisplayRAZChrono = True
		self.razChrono()
			
		self.show()	

	def setTimer(self):
		# Création d'un timer 1000ms qui génére un signal
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.updateLabel)
		self.timer.start(1000)	

	def updateFontLabelDec(self, pointSize, textColor):

		font = QFont(self.Hdec_police)
		font.setPointSize(int(pointSize))
		font.setBold(True)
		self.labelDec.setFont(font)
	
		self.labelDec.setStyleSheet('background-color: rgba(0,0,0,0%); color:'+str(textColor)+'; border-radius: ;')


	def updateLabel(self):
		# Mise à jour de l'heure courrante
		self.updateCurrentDate()

		t_remaining_min = self.Hout-self.Hcurent
		t_basc1_min = datetime.timedelta(hours=0,minutes=self.decompteBasculement1_min,seconds=0)
		t_basc2_min = datetime.timedelta(hours=0,minutes=self.decompteBasculement2_min,seconds=0)
		point_size = 0
		color = ""
		
		if not self.DisplayRAZChrono:
			
			# Choix de la couleur du decompte
			if 	(t_remaining_min > t_basc1_min\
				and t_remaining_min > t_basc2_min):
				
				color=self.Hdec_textColor_nominal

			elif 	(self.TempsAssi_min < self.decompteBasculement1_min \
					or self.TempsAssi_min < self.decompteBasculement2_min)\
					and t_remaining_min > datetime.timedelta(hours=0,minutes=self.TempsAssi_min,seconds=0):
				
				color=self.Hdec_textColor_nominal

			elif t_remaining_min <= t_basc1_min\
				and t_remaining_min > t_basc2_min:

				color=self.Hdec_textColor_phase1
			
			elif t_remaining_min <= t_basc1_min\
				and t_remaining_min <= t_basc2_min:

				color=self.Hdec_textColor_phase2
			
			else:
				color=self.Hdec_textColor_nominal

			# Choix de taille du decompte
			if self.Hcurent>=self.Hout:
				point_size = self.Hdec_pointSize-self.Hdec_reducePointSize

			elif t_remaining_min > datetime.timedelta(hours=0,minutes=self.TempsAssi_min,seconds=0):
				point_size = self.Hdec_pointSize-self.Hdec_reducePointSize

			else:
				point_size = self.Hdec_pointSize

			self.updateFontLabelDec(point_size,color)

			# Affichage du label
		
			if t_remaining_min>datetime.timedelta(hours=0,minutes=0,seconds=0):

				if t_remaining_min > datetime.timedelta(hours=0,minutes=self.TempsAssi_min,seconds=0):
					self.labelDec.setText(self.labelHeureReel.text())
				else :
					self.labelDec.setText(str(self.Hout-self.Hcurent))

			else :

				if self.Hcurent-self.Hout > datetime.timedelta(hours=9,minutes=59,seconds=59):
					self.labelDec.setText("+9:99:99")
				else :
					self.labelDec.setText("+"+str(self.Hcurent-self.Hout))
		
		elif self.DisplayRAZChrono:
			self.updateFontLabelDec(self.Hdec_pointSize, self.Hdec_textColor_nominal)
			self.labelHeureOut.setText(" :   00:00:00")
			self.labelHeureIn.setText(" :   00:00:00")
			self.labelDec.setText("0:00:00")

	def overload_window(self):
		# Heure IN
		self.Hin_text="Service in"
		#self.Hin_textColor="rgb(0, 0, 0)"
		self.Hin_backgroundColor="rgba(0,0,0,0%)"
		self.Hin_police=self.PoliceFont
		#self.Hin_bold=True
		#self.Hin_pointSize=45
		self.Hin_textBorderRadius=""
		# Heure OUT
		self.Hout_text="Service out"
		#self.Hout_textColor="rgb(0, 0, 0)"
		self.Hout_backgroundColor="rgba(0,0,0,0%)"
		self.Hout_police=self.PoliceFont
		#self.Hout_bold=True
		#self.Hout_pointSize=45
		self.Hout_textBorderRadius=""
		self.Hout_textY=10
		# Heure Decompte
		self.Hdec_police=self.PoliceFont
		#self.Hdec_pointSize=280
		
		# Reseize pointSize
		if self.Reseize_pointSize:
			self.Hout_pointSize = qt.QApplication.desktop().height() * self.Hout_pointSize / self.Reseize_refHeight
			self.Hin_pointSize = qt.QApplication.desktop().height() * self.Hin_pointSize / self.Reseize_refHeight
			self.Hdec_pointSize = qt.QApplication.desktop().height() * self.Hdec_pointSize / self.Reseize_refHeight
			
		# Label decompte
		self.labelDec = QtGui.QLabel("0:00:00")
		self.mainLayout.addWidget(self.labelDec,3,0,10,7,Qt.AlignCenter|Qt.AlignTop)
		#self.mainLayout.addWidget(self.labelDec,3,0,10,4,Qt.AlignCenter|Qt.AlignTop)

		# Label text heure in
		self.labelTextHeureIn = QtGui.QLabel(self.Hin_text)
		font = QFont(self.Hin_police)
		font.setPointSize(self.Hin_pointSize)
		font.setBold(self.Hin_bold)
		self.labelTextHeureIn.setFont(font)
		self.labelTextHeureIn.setStyleSheet('background-color: '+self.Hin_backgroundColor+'; color:'+self.Hin_textColor+'; border-radius: '+self.Hin_textBorderRadius+';')
		self.mainLayout.addWidget(self.labelTextHeureIn,13,0,1,2,Qt.AlignLeft|Qt.AlignBottom)
		#self.mainLayout.addWidget(self.labelTextHeureIn,13,0,Qt.AlignLeft|Qt.AlignBottom)

		# Label heure in
		self.labelHeureIn = QtGui.QLabel()
		font = QFont(self.Hin_police)
		font.setPointSize(self.Hin_pointSize)
		font.setBold(self.Hin_bold)
		self.labelHeureIn.setFont(font)
		self.labelHeureIn.setStyleSheet('background-color: '+self.Hin_backgroundColor+'; color:'+self.Hin_textColor+'; border-radius: '+self.Hin_textBorderRadius+';')
		self.mainLayout.addWidget(self.labelHeureIn,13,2,1,3,Qt.AlignLeft|Qt.AlignBottom)
		#self.mainLayout.addWidget(self.labelHeureIn,13,1,Qt.AlignLeft|Qt.AlignBottom)
		
		# Label text heure out
		self.labelTextHeureOut = QtGui.QLabel(self.Hout_text)
		font = QFont(self.Hout_police)
		font.setPointSize(self.Hout_pointSize)
		font.setBold(self.Hout_bold)
		self.labelTextHeureOut.setFont(font)
		self.labelTextHeureOut.setStyleSheet('background-color: '+self.Hout_backgroundColor+'; color:'+self.Hout_textColor+'; border-radius: '+self.Hout_textBorderRadius+';')
		self.mainLayout.addWidget(self.labelTextHeureOut,14,0,1,2,Qt.AlignLeft|Qt.AlignBottom)
		#self.mainLayout.addWidget(self.labelTextHeureOut,14,0,Qt.AlignLeft|Qt.AlignBottom)

		# Label heure out
		self.labelHeureOut = QtGui.QLabel()
		font = QFont(self.Hout_police)
		font.setPointSize(self.Hout_pointSize)
		font.setBold(self.Hout_bold)
		self.labelHeureOut.setFont(font)
		self.labelHeureOut.setStyleSheet('background-color: '+self.Hout_backgroundColor+'; color:'+self.Hout_textColor+'; border-radius: '+self.Hout_textBorderRadius+';')
		self.mainLayout.addWidget(self.labelHeureOut,14,2,1,3,Qt.AlignLeft|Qt.AlignBottom)
		#self.mainLayout.addWidget(self.labelHeureOut,14,1,Qt.AlignLeft|Qt.AlignBottom)
		
	def razChrono(self):
		self.DisplayRAZChrono = True
		
	def setPopUp1(self):
		self.popup1 = QtGui.QWidget()
		self.popup1.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1).x()+100, qt.QDesktopWidget().screenGeometry(screen=1).y()+100,100,100)
		self.popup1.setWindowTitle("Reglages")
		self.mainLayoutPopup1 = QtGui.QGridLayout(self.popup1)
		
		self.GroupBoxNomPilote= QtGui.QGroupBox("Nom pilote / copilote")
		layoutInfoNom = QtGui.QVBoxLayout()
		self.GroupBoxNomPilote.setLayout(layoutInfoNom)
		self.mainLayoutPopup1.addWidget(self.GroupBoxNomPilote,0,0,1,2)

		self.editorNom = QtGui.QLineEdit()
		self.editorNom.setFocusPolicy(Qt.TabFocus)
		self.editorNom.setFixedSize(400,30)
		layoutInfoNom.addWidget(self.editorNom)
		
		self.checkBoxPhotoPilote = QtGui.QCheckBox('Afficher photo pilote (cocher avec la touche Espace)')
		self.checkBoxPhotoPilote.setFocusPolicy(Qt.TabFocus)
		layoutInfoNom.addWidget(self.checkBoxPhotoPilote)

		self.GroupBoxHin= QtGui.QGroupBox("Heure entree")
		layoutHin = QtGui.QGridLayout()
		self.GroupBoxHin.setLayout(layoutHin)
		self.mainLayoutPopup1.addWidget(self.GroupBoxHin,1,0,1,2)
		
		layoutHin.addWidget(QtGui.QLabel("Jour"),0,0,1,1)
		layoutHin.addWidget(QtGui.QLabel("Mois"),0,1,1,1)
		layoutHin.addWidget(QtGui.QLabel("Heure"),2,0,1,1)
		layoutHin.addWidget(QtGui.QLabel("Minute"),2,1,1,1)
		layoutHin.addWidget(QtGui.QLabel("Seconde"),2,2,1,1)
		
		self.editorHin_day = QtGui.QLineEdit()
		self.editorHin_month = QtGui.QLineEdit()
		self.editorHin_h = QtGui.QLineEdit()
		self.editorHin_m = QtGui.QLineEdit()
		self.editorHin_s = QtGui.QLineEdit()

		self.editorHin_day.setFocusPolicy(Qt.TabFocus)
		self.editorHin_month.setFocusPolicy(Qt.TabFocus)
		self.editorHin_h.setFocusPolicy(Qt.TabFocus)
		self.editorHin_m.setFocusPolicy(Qt.TabFocus)
		self.editorHin_s.setFocusPolicy(Qt.TabFocus)
		
		layoutHin.addWidget(self.editorHin_day,1,0,1,1)
		layoutHin.addWidget(self.editorHin_month,1,1,1,1)
		layoutHin.addWidget(self.editorHin_h,3,0,1,1)	
		layoutHin.addWidget(self.editorHin_m,3,1,1,1)
		layoutHin.addWidget(self.editorHin_s,3,2,1,1)


		self.GroupBoxTempsAssi= QtGui.QGroupBox("Temps assistance (en min)")
		layoutTempsAssi = QtGui.QGridLayout()
		self.GroupBoxTempsAssi.setLayout(layoutTempsAssi)
		self.mainLayoutPopup1.addWidget(self.GroupBoxTempsAssi,2,0,1,2)

		self.editorTempsAssi = QtGui.QLineEdit()
		self.editorTempsAssi.setFocusPolicy(Qt.TabFocus)
		layoutTempsAssi.addWidget(self.editorTempsAssi)
		
		self.buttonRAZ = QtGui.QPushButton("RAZ Chrono")
		self.buttonRAZ.setFocusPolicy(Qt.TabFocus)
		self.buttonRAZ.setAutoDefault(True)
		self.mainLayoutPopup1.addWidget(self.buttonRAZ,3,0,1,1)
		#self.connect(self.buttonRAZ, QtCore.SIGNAL("clicked()"), self.sigPopup1ButtonRAZ)
		self.buttonRAZ.clicked.connect(lambda: self.sigPopup1ButtonOk_RAZ("RAZ"))

		self.buttonOkPopup1 = QtGui.QPushButton("Valider")
		self.buttonOkPopup1.setFocusPolicy(Qt.TabFocus)
		self.buttonOkPopup1.setAutoDefault(True)
		self.mainLayoutPopup1.addWidget(self.buttonOkPopup1,4,0,1,1)
		#self.connect(self.buttonOkPopup1, QtCore.SIGNAL("clicked()"), self.sigPopup1ButtonOk)
		self.buttonOkPopup1.clicked.connect(lambda: self.sigPopup1ButtonOk_RAZ("Ok"))
		
		self.buttonAnnPopup1 = QtGui.QPushButton("Annuler")
		self.buttonAnnPopup1.setFocusPolicy(Qt.TabFocus)
		self.buttonAnnPopup1.setAutoDefault(True)
		self.mainLayoutPopup1.addWidget(self.buttonAnnPopup1,4,1,1,1)
		self.connect(self.buttonAnnPopup1, QtCore.SIGNAL("clicked()"), self.sigPopup1ButtonAnn)
		

		self.labelInfoUser1 = QtGui.QLabel()
		self.labelInfoUser1.setStyleSheet('background-color: rgba(0,0,0,0%); color:rgb(181, 0, 0); border-radius: '+self.Hreel_textBorderRadius+';')
		self.mainLayoutPopup1.addWidget(self.labelInfoUser1,5,0,1,3)

	def setPopUp2(self):
		self.popup2 = QtGui.QWidget()
		self.popup2.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1).x()+100, qt.QDesktopWidget().screenGeometry(screen=1).y()+100,300,200)
		self.popup2.setWindowTitle("Regalge de l'heure interne")
		self.mainLayoutPopup2 = QtGui.QGridLayout(self.popup2)
		
		self.GroupBoxCurrentH= QtGui.QGroupBox("Heure actuelle du systeme")
		layoutCurrentH = QtGui.QGridLayout()
		self.GroupBoxCurrentH.setLayout(layoutCurrentH)
		self.mainLayoutPopup2.addWidget(self.GroupBoxCurrentH,0,0,1,2)
		
		self.currentHlabelPopup2 = QtGui.QLabel()
		layoutCurrentH.addWidget(self.currentHlabelPopup2,0,0,1,2)


		self.GroupBoxReglageH= QtGui.QGroupBox("Reglage de l'heure interne")
		layoutReglageH = QtGui.QGridLayout()
		self.GroupBoxReglageH.setLayout(layoutReglageH)
		self.mainLayoutPopup2.addWidget(self.GroupBoxReglageH,1,0,1,2)
		
		layoutReglageH.addWidget(QtGui.QLabel("Jour"),0,0,1,1)
		layoutReglageH.addWidget(QtGui.QLabel("Mois"),0,1,1,1)
		layoutReglageH.addWidget(QtGui.QLabel("Annee(YYYY)"),0,2,1,1)
		layoutReglageH.addWidget(QtGui.QLabel("Heure"),2,0,1,1)
		layoutReglageH.addWidget(QtGui.QLabel("Minute"),2,1,1,1)
		layoutReglageH.addWidget(QtGui.QLabel("Seconde"),2,2,1,1)

		self.editorSetH_day = QtGui.QLineEdit()
		self.editorSetH_month = QtGui.QLineEdit()
		self.editorSetH_year = QtGui.QLineEdit()
		self.editorSetH_h = QtGui.QLineEdit()
		self.editorSetH_m = QtGui.QLineEdit()
		self.editorSetH_s = QtGui.QLineEdit()

		self.editorSetH_day.setFocusPolicy(Qt.TabFocus)
		self.editorSetH_month.setFocusPolicy(Qt.TabFocus)
		self.editorSetH_year.setFocusPolicy(Qt.TabFocus)
		self.editorSetH_h.setFocusPolicy(Qt.TabFocus)
		self.editorSetH_m.setFocusPolicy(Qt.TabFocus)
		self.editorSetH_s.setFocusPolicy(Qt.TabFocus)
		
		layoutReglageH.addWidget(self.editorSetH_day,1,0,1,1)
		layoutReglageH.addWidget(self.editorSetH_month,1,1,1,1)
		layoutReglageH.addWidget(self.editorSetH_year,1,2,1,1)
		layoutReglageH.addWidget(self.editorSetH_h,3,0,1,1)
		layoutReglageH.addWidget(self.editorSetH_m,3,1,1,1)
		layoutReglageH.addWidget(self.editorSetH_s,3,2,1,1)

		self.buttonOkPopup2 = QtGui.QPushButton("Valider")
		self.buttonOkPopup2.setFocusPolicy(Qt.TabFocus)
		self.buttonOkPopup2.setAutoDefault(True)
		self.mainLayoutPopup2.addWidget(self.buttonOkPopup2,4,0,1,1)
		self.connect(self.buttonOkPopup2, QtCore.SIGNAL("clicked()"), self.sigPopup2ButtonOk)
		
		self.buttonAnnPopup2 = QtGui.QPushButton("Annuler")
		self.buttonAnnPopup2.setFocusPolicy(Qt.TabFocus)
		self.buttonAnnPopup2.setAutoDefault(True)
		self.mainLayoutPopup2.addWidget(self.buttonAnnPopup2,4,1,1,1)
		self.connect(self.buttonAnnPopup2, QtCore.SIGNAL("clicked()"), self.sigPopup2ButtonAnn)
		

	def setPopUp3(self):
		self.popup3 = QtGui.QWidget()
		self.popup3.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1).x()+100, qt.QDesktopWidget().screenGeometry(screen=1).y()+100,500,500)
		self.popup3.setWindowTitle("Versions")
		self.mainLayoutPopup3 = QtGui.QGridLayout(self.popup3)

		addrMacEth0 = os.popen("ifconfig eth0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'").read()
		distribVersion = os.popen("cat /distrib_version.txt").read().strip()
		versionGlobalProjet = os.popen("cat /version_global_projet.txt").read().strip()
		try :
			textVersion = 	"Version Global PROJET : "+versionGlobalProjet+"\n\n"+\
							"Version script : "+SCRIPT_VERSION+"\n"+\
							"Version conf    : "+self.version_Config+"\n"+\
							"Version logo    : "+self.version_Logo+"\n"+\
							"Version OS      : "+distribVersion+"\n"+\
							"HWaddr          : "+addrMacEth0
		except:
			textVersion = 	"Version Global PROJET : "+versionGlobalProjet+"\n\n"+\
							"Version script : "+SCRIPT_VERSION+"\n"+\
							"Version logo    : "+self.version_Logo+"\n"+\
							"Version OS      : "+distribVersion+"\n"+\
							"HWaddr          : "+addrMacEth0

		self.mainLayoutPopup3.addWidget(QtGui.QLabel(textVersion),0,0,1,2,Qt.AlignTop)
		
		self.buttonFermerPopup3 = QtGui.QPushButton("Fermer")
		self.buttonFermerPopup3.setFocusPolicy(Qt.TabFocus)
		self.buttonFermerPopup3.setAutoDefault(True)
		self.mainLayoutPopup3.addWidget(self.buttonFermerPopup3,1,0,1,1)
		self.connect(self.buttonFermerPopup3, QtCore.SIGNAL("clicked()"), self.sigPopup3ButtonFermer)
	
	def setPopUp4(self):
		self.popup4 = QtGui.QWidget()
		self.popup4.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1).x()+100, qt.QDesktopWidget().screenGeometry(screen=1).y()+100,300,200)
		self.popup4.setWindowTitle("Basculement couleur")
		self.mainLayoutPopup4 = QtGui.QGridLayout(self.popup4)
		
		self.GroupBoxBasculCouleur= QtGui.QGroupBox("Basculement couleur")
		layoutBasculCouleur = QtGui.QGridLayout()
		self.GroupBoxBasculCouleur.setLayout(layoutBasculCouleur)
		self.mainLayoutPopup4.addWidget(self.GroupBoxBasculCouleur,0,0,1,2)
		
		layoutBasculCouleur.addWidget(QtGui.QLabel("* 'Basculement 1 : changement couleur noir vers orange\n* 'Basculement 2 : changement couleur orange vers rouge\n* La valeur 'Basculement 2' doit etre <= 'Basculement 1'"),0,0,1,2)
		layoutBasculCouleur.addWidget(QtGui.QLabel("Basculement 1 (min)"),1,0,1,1)
		layoutBasculCouleur.addWidget(QtGui.QLabel("Basculement 2 (min)"),1,1,1,1)
		self.editorBascul1 = QtGui.QLineEdit()
		self.editorBascul2 = QtGui.QLineEdit()
		layoutBasculCouleur.addWidget(self.editorBascul1,2,0,1,1)
		layoutBasculCouleur.addWidget(self.editorBascul2,2,1,1,1)
		
		self.buttonOkPopup4 = QtGui.QPushButton("Valider")
		self.buttonOkPopup4.setFocusPolicy(Qt.TabFocus)
		self.buttonOkPopup4.setAutoDefault(True)
		self.mainLayoutPopup4.addWidget(self.buttonOkPopup4,4,0,1,1)
		self.connect(self.buttonOkPopup4, QtCore.SIGNAL("clicked()"), self.sigPopup4ButtonOk)
		
		self.buttonAnnPopup4 = QtGui.QPushButton("Annuler")
		self.buttonAnnPopup4.setFocusPolicy(Qt.TabFocus)
		self.buttonAnnPopup4.setAutoDefault(True)
		self.mainLayoutPopup4.addWidget(self.buttonAnnPopup4,4,1,1,1)
		self.connect(self.buttonAnnPopup4, QtCore.SIGNAL("clicked()"), self.sigPopup4ButtonAnn)
		
		self.labelInfoUser4 = QtGui.QLabel()
		self.labelInfoUser4.setStyleSheet('background-color: rgba(0,0,0,0%); color:rgb(181, 0, 0); border-radius: '+self.Hreel_textBorderRadius+';')
		self.mainLayoutPopup4.addWidget(self.labelInfoUser4,5,0,1,2)


	def sigPopup1ButtonOk_RAZ(self, buttonType):

		self.labelInfoUser1.setText("")
		if len(self.editorNom.text()) > 60 and not self.displayPictureDriver:
			self.labelInfoUser1.setText("Le texte du pilote est trop grand : "+str(len(self.editorNom.text()))+" characteres\r\nNombre maximum : 36")
			return
		elif len(self.editorNom.text()) > 60 and self.displayPictureDriver:
			self.labelInfoUser1.setText("Le texte du pilote est trop grand : "+str(len(self.editorNom.text()))+" characteres\r\nNombre maximum : 25")
			return

		if buttonType == "Ok":
		
			try:
				datetime.datetime(	int(time.strftime("20%y")),\
									int(self.editorHin_month.text()),\
									int(1),\
									int(1),\
									int(1),\
									int(1))
			except:
				self.labelInfoUser1.setText("Mois incorrect")
				return
			
			try:
				datetime.datetime(	int(time.strftime("20%y")),\
									int(self.editorHin_month.text()),\
									int(self.editorHin_day.text()),\
									int(1),\
									int(1),\
									int(1))
			except:
				self.labelInfoUser1.setText("Jour incorrect")
				return
			try:
				datetime.datetime(	int(time.strftime("20%y")),\
									int(self.editorHin_month.text()),\
									int(self.editorHin_day.text()),\
									int(self.editorHin_h.text()),\
									int(1),\
									int(1))
			except:
				self.labelInfoUser1.setText("Heure incorrect")
				return
			try:
				datetime.datetime(	int(time.strftime("20%y")),\
									int(self.editorHin_month.text()),\
									int(self.editorHin_day.text()),\
									int(self.editorHin_h.text()),\
									int(self.editorHin_m.text()),\
									int(1))
			except:
				self.labelInfoUser1.setText("Minute incorrect")
				return
			try:
				datetime.datetime(	int(time.strftime("20%y")),\
									int(self.editorHin_month.text()),\
									int(self.editorHin_day.text()),\
									int(self.editorHin_h.text()),\
									int(self.editorHin_m.text()),\
									int(self.editorHin_s.text()))
			except:
				self.labelInfoUser1.setText("Seconde incorrect")
				return
		
			if int(self.editorTempsAssi.text()) > 599 :
				self.labelInfoUser1.setText("Duree assistance trop grande : "+self.editorTempsAssi.text()+" minutes\r\nMinutes maximum : 599")
				return

			
			self.Hin = datetime.datetime(	int(time.strftime("%Y")),\
											int(self.editorHin_month.text()),\
											int(self.editorHin_day.text()),\
											int(self.editorHin_h.text()),\
											int(self.editorHin_m.text()),\
											int(self.editorHin_s.text()))

			self.TempsAssi_min = int(self.editorTempsAssi.text())
			self.Hout = self.Hin + datetime.timedelta(hours=0,minutes=self.TempsAssi_min,seconds=0)
			
			self.labelHeureOut.setText(	" :   " + self.Hout.strftime("%H") + \
										":" + self.Hout.strftime("%M") + \
										":" + self.Hout.strftime("%S"))

			self.labelHeureIn.setText(	" :   " + self.Hin.strftime("%H") + \
										":" + self.Hin.strftime("%M") + \
										":" +self.Hin.strftime("%S"))
			
			self.DisplayRAZChrono = False
		
		else:
			self.razChrono()

		self.TextPilote = self.editorNom.text()
		self.labelTextPilote.setText(self.TextPilote)
		
		if self.checkBoxPhotoPilote.isChecked():
			self.displayPictureDriver = True
		else:
			self.displayPictureDriver = False
		self.setPictureDriverAndName(self.displayPictureDriver)
		
		self.popup1.hide()
		self.writeFileParam()
		
	def sigPopup1ButtonAnn(self):
		self.popup1.hide()
	
	#def sigPopup1ButtonRAZ(self):
	#	self.razChrono()
	#	self.popup1.hide()

	def sigPopup2ButtonOk(self):
		cmd = 	'sudo date --set "'\
				+ str(self.editorSetH_month.text()) + "/" \
				+ str(self.editorSetH_day.text()) + "/" \
				+ str(self.editorSetH_year.text()) + " " \
				+ str(self.editorSetH_h.text()) + ":" \
				+ str(self.editorSetH_m.text()) + ":" \
				+ str(self.editorSetH_s.text()) + '"'

		os.system(cmd)
		time.sleep(3)
		subprocess.check_output(["sudo","hwclock","-w"])

	 	self.popup2.hide()
		
	def sigPopup2ButtonAnn(self):
		self.popup2.hide()

	def sigPopup3ButtonFermer(self):
		self.popup3.hide()
	
	def sigPopup4ButtonOk(self):
		self.labelInfoUser4.setText("")
		try:
			if 	int(self.editorBascul1.text()) < 0 \
				or int(self.editorBascul2.text()) < 0:
				self.labelInfoUser4.setText("Les valeurs de basculements doivent etre >=0")
				return
		except:
			self.labelInfoUser4.setText("Les valeurs sont incorrects")

		if int(self.editorBascul1.text()) < int(self.editorBascul2.text()):
			self.labelInfoUser4.setText("La valeur 'Basculement 2' doit etre < 'Basculement 1'")
			return
	
		self.decompteBasculement1_min = int(self.editorBascul1.text())
		self.decompteBasculement2_min = int(self.editorBascul2.text())
		self.popup4.hide()
		self.writeFileParam()

	def sigPopup4ButtonAnn(self):
		self.popup4.hide()

	def keyPressEventOverload(self,e):
		if e.key() == QtCore.Qt.Key_F1:
			self.editorNom.setText(self.TextPilote)
			self.editorHin_day.setText(time.strftime("%d"))
			self.editorHin_month.setText(time.strftime("%m"))
			self.editorHin_h.setText(time.strftime("%H"))
			self.editorHin_m.setText(time.strftime("%M"))
			self.editorHin_s.setText("0")
			self.editorTempsAssi.setText(str(self.TempsAssi_min))
			if self.displayPictureDriver:
				self.checkBoxPhotoPilote.setCheckState(Qt.Checked)
			else:
				self.checkBoxPhotoPilote.setCheckState(Qt.Unchecked)
			self.popup1.show()
			self.editorNom.setFocus()

		elif e.key() == QtCore.Qt.Key_F2:
			self.editorBascul1.setText(str(self.decompteBasculement1_min))
			self.editorBascul2.setText(str(self.decompteBasculement2_min))

			self.popup4.show()
			self.editorBascul1.setFocus()

		elif e.key() == QtCore.Qt.Key_F3:
			self.editorSetH_day.setText(self.day)
			self.editorSetH_month.setText(self.month)
			self.editorSetH_year.setText(self.year)
			self.editorSetH_h.setText(self.hour)
			self.editorSetH_m.setText(self.minute)
			self.editorSetH_s.setText(self.second)
	
			self.popup2.show()
			
			self.editorSetH_day.setFocus()

		elif e.key() == QtCore.Qt.Key_F4:
			self.popup3.show()

class window2(window):
	def __init__(self, parent=None):
		super(window2, self).__init__(parent)
		self.readFileParam()
		self.readFileConf()
		self.templateWindow()

def signal(e):
	if e.key() == QtCore.Qt.Key_F9:
		w1.hide()
		#w2.show()

class thradMaint(qtcore.QThread, QWidget):
	def __init__(self, parent=None):
		qtcore.QThread.__init__(self, parent=app)
		self.rebootRequest = False
	def run(self):
		while True:
			time.sleep(5)
			
			
			res = self.USBKeyPresent()
			if res != None:
				print "\nCle USB detecte"
				time.sleep(5)
				self.copyDriverPicture(res)
				self.executePatch(res)
				
				subprocess.check_output(["umount",res])
				if self.rebootRequest:
					self.rebootScript(res)
				
			else:
				time.sleep(3)
				print "Attente key"

	def USBKeyPresent(self):
		#
		res = subprocess.check_output(["cat","/etc/mtab"])
		
		for line in res.splitlines():
			if "/dev/" in line and "/media/" in line :
				return line.split(" ")[1]

		return None
	
	def initWindow(self):
		self.popupUpdate.setGeometry(qt.QDesktopWidget().screenGeometry(screen=1).x()+100, qt.QDesktopWidget().screenGeometry(screen=1).y()+100,1000,900)
		self.popupUpdate.setWindowTitle("Mise a jour")
		self.mainlayoutPopupUpdate = QtGui.QGridLayout(self.popupUpdate)
		
		self.mainlayoutPopupUpdate.addWidget(QtGui.QLabel("********************\n* Cle USB detecte *\n********************"),0,0,1,2)

		self.GroupBoxUpdateFw= QtGui.QGroupBox("Mise a jour script et conf")
		layoutUpdateFw= QtGui.QVBoxLayout()
		self.GroupBoxUpdateFw.setLayout(layoutUpdateFw)
		self.mainlayoutPopupUpdate.addWidget(self.GroupBoxUpdateFw,1,0,30,2,Qt.AlignTop)


		self.LabelTextUpdate = QLabel()
		layoutUpdateFw.addWidget(self.LabelTextUpdate)
	
		self.LabelTextUpdate.setWordWrap(True)
		
	def updateText(self, text):
		self.LabelTextUpdate.setText(self.LabelTextUpdate.text()+text)

	def executePatch(self, path):
		try:
			print "\nDebut fonction executePatch()"
			subprocess.check_output(["cp",os.path.join(path,archive_name),"/tmp"])
			subprocess.check_output(["tar","pxvzf",os.path.join("/tmp",archive_name),"-C","/tmp","-m"])
			subprocess.check_output(["/bin/bash",os.path.join("/tmp","patch-me.sh")])
			self.rebootRequest = True
			print "Fin fonction executePatch()"
		except:
			print "Erreur fonction executePatch()"

	def copyDriverPicture(self, path):
		print "\nDebut fonction copyDriverPicture()"
		try:
			subprocess.check_output(["cp",os.path.join(path,pictureDriver_name),os.path.join(sys.path[0],pictureDriver_name)])
			self.rebootRequest = True
			print "Fin fonction copyDriverPicture()"
		except:
			print "Erreur fonction copyDriverPicture()"
					
	def rebootScript(self, path):
		print "\nDebut fonction rebootScript()"
		os.system('echo "#! /bin/bash" > /tmp/rebootScript.sh')
		os.system("""echo kill -9 "$PPID" >> /tmp/rebootScript.sh""")
		os.system('echo "sleep 1" >> /tmp/rebootScript.sh')
		os.system('echo "python /home/pi/Horloge/soft/horloge.pyw &" >> /tmp/rebootScript.sh')
		
		subprocess.check_output(["/bin/bash",os.path.join("/tmp","rebootScript.sh")])


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	subprocess.check_output(["setxkbmap","fr"])

	w1 = window1()
	QObject.connect(w1,w1.sig, signal)

	#w2 = window2()
	#QObject.connect(w2,w2.sig, signal)
		
	t1 = thradMaint() 
	t1.start()

	sys.exit(app.exec_())


