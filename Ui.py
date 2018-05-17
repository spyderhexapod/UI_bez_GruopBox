from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QLineEdit, QSlider,QMessageBox, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTextEdit, QCheckBox, QLCDNumber, QGroupBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QByteArray
from SerialMonitor import SerialMonitor_class
from IK import IK_class
from elipsa import Elipsa_class
import sys, time, threading, random, math, os

#Bartek wtykał kabelki 26.04.2018

class Sterowanie(QWidget):
	global IK, monitor, katyVar, elipsa
	
	IK = IK_class()
	monitor = SerialMonitor_class()
	elipsa = Elipsa_class()
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.interfejs()
		self.x_label_camera.setText("X: {0}".format(str(self.x_slider_camera.value())))
		self.y_label_camera.setText("Y: {0}".format(str(self.y_slider_camera.value())))
		self.yLabelSpyder.setText("Y: {0} %".format(IK.mapFunction(self.y_slider_spyder.value(), -180, -40, 0, 100)))
		self.xLabelSpyder.setText("Y: {0} %".format(IK.mapFunction(self.x_slider_spyder.value(), -180, -40, 0, 100)))
		self.zLabelSpyder.setText("Z: {0} %".format(IK.mapFunction(self.z_slider_spyder.value(), -180, -40, 0, 100)))
		
		self.distanceLabel.setText("Odległość: Nieznana")
		
		self.LP_line.setText("LP: {0} {1} {2}".format(IK.katy[0], IK.katy[1], IK.katy[2]))
		self.LS_line.setText("LS: {0} {1} {2}".format(IK.katy[3], IK.katy[4], IK.katy[5]))
		self.LT_line.setText("LT: {0} {1} {2}".format(IK.katy[6], IK.katy[7], IK.katy[8]))
		self.PP_line.setText("PP: {0} {1} {2}".format(IK.katy[9], IK.katy[10], IK.katy[11]))
		self.PS_line.setText("PS: {0} {1} {2}".format(IK.katy[12], IK.katy[13], IK.katy[14]))
		self.PT_line.setText("PT: {0} {1} {2}".format(IK.katy[15], IK.katy[16], IK.katy[17]))
		thread = threading.Thread(target = self.default)
		#thread = threading.Thread(target = self.test)
		thread.start()
		self.katyVar = False
		
		self.sliderTab = [self.sliderX1, self.sliderY1, self.sliderZ1, 
				self.sliderX2, self.sliderY2, self.sliderZ2,
				self.sliderX3, self.sliderY3, self.sliderZ3, 
				self.sliderX4, self.sliderY4, self.sliderZ4,
				self.sliderX5, self.sliderY5, self.sliderZ5, 
				self.sliderX6, self.sliderY6, self.sliderZ6]
		
		for i in range(0, len(self.sliderTab)):
			self.sliderTab[i].setTickPosition(QSlider.TicksBelow)
			self.sliderTab[i].setTickInterval(10)
			#~ #self.sliderTab[i].valueChanged.connect(self.sliderValueChanged)
		
		self.x_slider_spyder.setTickPosition(QSlider.TicksBelow)
		self.x_slider_spyder.setTickInterval(10)
		self.y_slider_spyder.setTickPosition(QSlider.TicksBothSides)
		self.y_slider_spyder.setTickInterval(10)
		self.z_slider_spyder.setTickPosition(QSlider.TicksBelow)
		self.z_slider_spyder.setTickInterval(10)
		self.x_slider_camera.setTickPosition(QSlider.TicksBelow)
		self.x_slider_camera.setTickInterval(10)
		self.y_slider_camera.setTickPosition(QSlider.TicksBothSides)
		self.y_slider_camera.setTickInterval(10)
		
	def test(self):
		time.sleep(2.5)
		self.noga1('|')
		self.noga2('|')
		self.noga3('|')
		self.noga4('|')
		self.noga5('|')
		self.noga6('#')
		print("dziala")

	def default(self):
		time.sleep(2.5)
		elipsa.tablica("LP", IK.katy[0], IK.katy[1], IK.katy[2], 254, False)
		elipsa.tablica("LS", IK.katy[3], IK.katy[4], IK.katy[5], 254, False)
		elipsa.tablica("LT", IK.katy[6], IK.katy[7], IK.katy[8], 254, False)
		elipsa.tablica("PP", IK.katy[9], IK.katy[10], IK.katy[11], 254, False)
		elipsa.tablica("PS", IK.katy[12], IK.katy[13], IK.katy[14], 254, False)
		elipsa.tablica("PT", IK.katy[15], IK.katy[16], IK.katy[17], 255, True)
		
	def kinematyka_wartosci(self):
		self.sliderX1.setRange(-200, 100)
		self.sliderX1.setValue(-59)
		
		self.sliderY1.setRange(-150, 0)
		self.sliderY1.setValue(-118)
		
		self.sliderZ1.setRange(-150, 100)
		self.sliderZ1.setValue(-60)

		self.sliderX2.setRange(-200, 100)
		self.sliderX2.setValue(-85)
		
		self.sliderY2.setRange(-150, 0)
		self.sliderY2.setValue(-118)
		
		self.sliderZ2.setRange(-80, 80)
		self.sliderZ2.setValue(0)

		self.sliderX3.setRange(-200, 100)
		self.sliderX3.setValue(-60)

		self.sliderY3.setRange(-161, 0)
		self.sliderY3.setValue(-118)

		self.sliderZ3.setRange(-200, 100)
		self.sliderZ3.setValue(60)

		self.sliderX4.setRange(0, 170)
		self.sliderX4.setValue(60)

		self.sliderY4.setRange(-150, 0)
		self.sliderY4.setValue(-118)

		self.sliderZ4.setRange(-100, 100)
		self.sliderZ4.setValue(-60)

		self.sliderX5.setRange(-200, 100)
		self.sliderX5.setValue(85)

		self.sliderY5.setRange(-150, 0)
		self.sliderY5.setValue(-118)

		self.sliderZ5.setRange(-80, 80)
		self.sliderZ5.setValue(0)

		self.sliderX6.setRange(0, 170)
		self.sliderX6.setValue(60)

		self.sliderY6.setRange(-150, 0)
		self.sliderY6.setValue(-118)

		self.sliderZ6.setRange(-100, 100)
		self.sliderZ6.setValue(60)
		
	def interfejs(self):
		# Slidery
		self.sliderX1 = QSlider(Qt.Horizontal, self)
		self.xLabel1 = QLabel("X = -60")

		self.sliderY1 = QSlider(Qt.Horizontal, self)
		self.yLabel1 = QLabel("Y = -118")

		self.sliderZ1 = QSlider(Qt.Horizontal, self)
		self.zLabel1 = QLabel("Z = -60")

		self.sliderX2 = QSlider(Qt.Horizontal, self)
		self.xLabel2 = QLabel("X = -85")

		self.sliderY2 = QSlider(Qt.Horizontal, self)
		self.yLabel2 = QLabel("Y = -118")

		self.sliderZ2 = QSlider(Qt.Horizontal, self)
		self.zLabel2 = QLabel("Z = 0")

		self.sliderX3 = QSlider(Qt.Horizontal, self)
		self.xLabel3 = QLabel("X = -60")

		self.sliderY3 = QSlider(Qt.Horizontal, self)
		self.yLabel3 = QLabel("Y = -118")

		self.sliderZ3 = QSlider(Qt.Horizontal, self)
		self.zLabel3 = QLabel("Z = 60")

		self.sliderX4 = QSlider(Qt.Horizontal, self)
		self.xLabel4 = QLabel("X = 60")

		self.sliderY4 = QSlider(Qt.Horizontal, self)
		self.yLabel4 = QLabel("Y = -118")

		self.sliderZ4 = QSlider(Qt.Horizontal, self)
		self.zLabel4 = QLabel("Z = -60")

		self.sliderX5 = QSlider(Qt.Horizontal, self)
		self.xLabel5 = QLabel("X = 85")
	 
		self.sliderY5 = QSlider(Qt.Horizontal, self)
		self.yLabel5 = QLabel("Y = -118")
	
		self.sliderZ5 = QSlider(Qt.Horizontal, self)
		self.zLabel5 = QLabel("Z = 0")

		self.sliderX6 = QSlider(Qt.Horizontal, self)
		self.xLabel6 = QLabel("X = 60")

		self.sliderY6 = QSlider(Qt.Horizontal, self)
		self.yLabel6 = QLabel("Y = -118")
 
		self.sliderZ6 = QSlider(Qt.Horizontal, self)
		self.zLabel6 = QLabel("Z = 60")
		
		self.kinematyka_wartosci()

		self.sliderX1.valueChanged.connect(self.valueChangedX1)
		self.sliderY1.valueChanged.connect(self.valueChangedY1)
		self.sliderZ1.valueChanged.connect(self.valueChangedZ1)
		self.sliderX2.valueChanged.connect(self.valueChangedX2)
		self.sliderY2.valueChanged.connect(self.valueChangedY2)
		self.sliderZ2.valueChanged.connect(self.valueChangedZ2)
		self.sliderX3.valueChanged.connect(self.valueChangedX3)
		self.sliderY3.valueChanged.connect(self.valueChangedY3)
		self.sliderZ3.valueChanged.connect(self.valueChangedZ3)
		self.sliderX4.valueChanged.connect(self.valueChangedX4)
		self.sliderY4.valueChanged.connect(self.valueChangedY4)
		self.sliderZ4.valueChanged.connect(self.valueChangedZ4)
		self.sliderX5.valueChanged.connect(self.valueChangedX5)
		self.sliderY5.valueChanged.connect(self.valueChangedY5)
		self.sliderZ5.valueChanged.connect(self.valueChangedZ5)
		self.sliderX6.valueChanged.connect(self.valueChangedX6)
		self.sliderY6.valueChanged.connect(self.valueChangedY6)
		self.sliderZ6.valueChanged.connect(self.valueChangedZ6)

		self.auto_checkbox = QCheckBox("Automatyczne wysyłanie", self)
		self.auto_checkbox.setChecked(True)
		self.auto_checkbox.clicked.connect(self.checkboxFunction)
		
		self.execution_Button = QPushButton("&Wykonaj", self)
		self.execution_Button.clicked.connect(self.execution)
		
		self.forward_Button = QPushButton("&Do przodu", self)
		self.forward_Button.clicked.connect(self.front)
		
		self.reset_button = QPushButton("&Reset", self)
		self.reset_button.clicked.connect(self.resetButtonClicked)
		
		self.naKatyButton = QPushButton("&Zamień na kąty", self)
		self.naKatyButton.clicked.connect(self.katy)
		
		self.distanceButton = QPushButton("&Odczytaj odległość")
		self.distanceButton.clicked.connect(self.distance)
		
		self.wheelButton = QPushButton("&Rysuj koło", self)
		self.wheelButton.clicked.connect(elipsa.wheel)
		
		self.elipse1Button = QPushButton("&Rysowanie elipsy1", self)
		self.elipse1Button.clicked.connect(elipsa.ellipse1)
		
		self.elipse2Button = QPushButton("&Rysowanie elipsy2", self)
		self.elipse2Button.clicked.connect(elipsa.ellipse2)
		
		self.elipse3Button = QPushButton("&Rysowanie elipsy3", self)
		self.elipse3Button.clicked.connect(elipsa.ellipse3)
		
		self.elipse4Button = QPushButton("&Rysowanie elipsy4", self)
		self.elipse4Button.clicked.connect(elipsa.ellipse4)
		
		self.elipse5Button = QPushButton("&Rysowanie elipsy5", self)
		self.elipse5Button.clicked.connect(elipsa.ellipse5)
		
		self.elipse6Button = QPushButton("&Rysowanie elipsy6", self)
		self.elipse6Button.clicked.connect(elipsa.ellipse6)
		
		self.walk1Button = QPushButton("&ChodźR", self)
		self.walk1Button.clicked.connect(elipsa.walkR)
		
		self.walk2Button = QPushButton("&ChodźL", self)
		self.walk2Button.clicked.connect(elipsa.walkL)
		
		self.OffButton = QPushButton("&Off RPi", self)
		self.OffButton.clicked.connect(self.Shutdown)
		
		self.RestartButton = QPushButton("&Restart RPi", self)
		self.RestartButton.clicked.connect(self.Reboot)
		
		self.ResetArduinoButton = QPushButton("&Reset arduino", self)
		self.ResetArduinoButton.clicked.connect(self.ResetArduino)
		
		self.distanceLabel = QLabel(self)

		self.monitor_receiver = QTextEdit(self)
		
		#slidery i labely do kamery
		self.y_slider_camera = QSlider(Qt.Vertical, self)
		self.y_slider_camera.setRange(1,180)
		self.y_slider_camera.setValue(20)
		self.y_slider_camera.valueChanged.connect(self.valueChangedYc)
		self.x_slider_camera = QSlider(Qt.Horizontal, self)
		self.x_slider_camera.setRange(1, 180)
		self.x_slider_camera.setValue(90)
		self.x_slider_camera.valueChanged.connect(self.valueChangedXc)
		self.x_label_camera = QLabel(self)
		self.y_label_camera = QLabel(self) 
		self.camera_labelY = QLabel("OkoY: ", self)
		self.camera_labelX = QLabel("OkoX: ", self)

		#slider gora_dol
		self.y_slider_spyder = QSlider(Qt.Vertical, self)
		self.y_slider_spyder.setRange(-180, -40)
		self.y_slider_spyder.setValue(-118)
		self.y_slider_spyder.valueChanged.connect(self.valueChangedSpyderY)
		self.yLabelSpyder = QLabel(self)
		self.yLabel = QLabel("Pion: ", self)
		
		#slider przod_tyl
		self.x_slider_spyder = QSlider(Qt.Horizontal, self)
		self.x_slider_spyder.setRange(-180, -40)
		self.x_slider_spyder.setValue(-118)
		self.x_slider_spyder.valueChanged.connect(self.valueChangedSpyderX)
		self.xLabelSpyder = QLabel(self)
		self.xLabel = QLabel("Poziomo: ", self)
		
		#slider prawo_lewo
		self.z_slider_spyder = QSlider(Qt.Horizontal, self)
		self.z_slider_spyder.setRange(-180, -40)
		self.z_slider_spyder.setValue(-118)
		self.z_slider_spyder.valueChanged.connect(self.valueChangedSpyderZ)
		self.zLabelSpyder = QLabel(self)
		self.zLabel = QLabel("Prawo - Lewo: ", self)
		
		#wysiwetlacze i label LCD do czujnikow nacisku
		self.Pressure_button = QPushButton("&Odczytaj nacisk", self)
		self.Pressure_button.clicked.connect(self.pressFunction)
		self.LcdN1 = QLCDNumber()
		self.LcdN2 = QLCDNumber()
		self.LcdN3 = QLCDNumber()
		self.LcdN4 = QLCDNumber()
		self.LcdN5 = QLCDNumber()
		self.LcdN6 = QLCDNumber()
		
		self.LcdN1_label = QLabel("LP")
		self.LcdN2_label = QLabel("LS")
		self.LcdN3_label = QLabel("LT")
		self.LcdN4_label = QLabel("PP")
		self.LcdN5_label = QLabel("PS")
		self.LcdN6_label = QLabel("PT")

		self.LP_line = QLineEdit(self)
		self.LS_line = QLineEdit(self)
		self.LT_line = QLineEdit(self)
		self.PP_line = QLineEdit(self)
		self.PS_line = QLineEdit(self)
		self.PT_line = QLineEdit(self)

		ukladMonitor = QVBoxLayout()
		ukladMonitor.addWidget(self.LP_line, 0)
		ukladMonitor.addWidget(self.LS_line, 1)
		ukladMonitor.addWidget(self.LT_line, 2)
		ukladMonitor.addWidget(self.PP_line, 3)
		ukladMonitor.addWidget(self.PS_line, 4)
		ukladMonitor.addWidget(self.PT_line, 5)
		ukladMonitor.addWidget(self.monitor_receiver, 6)
		
		#opcje
		ukladOpcje = QVBoxLayout()
		ukladOpcje.addWidget(self.OffButton, 1)
		ukladOpcje.addWidget(self.RestartButton, 2)
		ukladOpcje.addWidget(self.ResetArduinoButton, 3)
		
		#dystans
		ukladDystans = QGridLayout()
		ukladDystans.addWidget(self.distanceButton, 0, 0)
		ukladDystans.addWidget(self.distanceLabel, 1, 0)

		#Nogi
		
		LegLayout = QGridLayout()
		LegLayout.addWidget(self.auto_checkbox, 0, 0)
		LegLayout.addWidget(self.naKatyButton, 0, 1)
		LegLayout.addWidget(self.CreateLTGroupBox(), 3, 0)
		LegLayout.addWidget(self.CreateLSGroupBox(), 2, 0)
		LegLayout.addWidget(self.CreateLPGroupBox(), 1, 0)
		LegLayout.addWidget(self.CreatePPGroupBox(), 1, 1)
		LegLayout.addWidget(self.CreatePSGroupBox(), 2, 1)
		LegLayout.addWidget(self.CreatePTGroupBox(), 3, 1)
		
		#slidery pionowe (OkoY i pion)
		ukladT1 = QGridLayout()
		ukladT1.addWidget(self.camera_labelY, 0, 0)
		ukladT1.addWidget(self.yLabel, 0, 1)
		ukladT1.addWidget(self.y_slider_camera, 1, 0)
		ukladT1.addWidget(self.y_slider_spyder, 1, 1)
		
		#wartości ze sliderow pionowych (OkoY i pion)
		ukladT12 = QGridLayout()
		ukladT12.addWidget(self.y_label_camera, 0, 0)
		ukladT12.addWidget(self.yLabelSpyder, 0, 1)
		
		#slidery poziome(OkoX i poziom) i prawo-lewo
		ukladXZ = QGridLayout()
		ukladXZ.addWidget(self.camera_labelX, 0, 0)
		ukladXZ.addWidget(self.x_slider_camera, 0, 1)
		ukladXZ.addWidget(self.x_label_camera, 0, 2)
		ukladXZ.addWidget(self.xLabel, 1, 0)
		ukladXZ.addWidget(self.x_slider_spyder, 1, 1)
		ukladXZ.addWidget(self.xLabelSpyder, 1, 2)
		ukladXZ.addWidget(self.zLabel, 2, 0)
		ukladXZ.addWidget(self.z_slider_spyder, 2, 1)
		ukladXZ.addWidget(self.zLabelSpyder, 2, 2)
		
		#elipsy
		ukladT5 = QVBoxLayout()
		ukladT5.addWidget(self.wheelButton, 0)
		ukladT5.addWidget(self.elipse1Button, 1)
		ukladT5.addWidget(self.elipse2Button, 2)
		ukladT5.addWidget(self.elipse3Button, 3)
		ukladT5.addWidget(self.elipse4Button, 4)
		ukladT5.addWidget(self.elipse5Button, 5)
		ukladT5.addWidget(self.elipse6Button, 6)
		ukladT5.addWidget(self.walk1Button, 7)
		ukladT5.addWidget(self.walk2Button, 8)
		
		#reset, wykonaj, do przodu
		ukladB = QVBoxLayout()
		ukladB.addWidget(self.reset_button, 1)
		ukladB.addWidget(self.execution_Button, 2)
		ukladB.addWidget(self.forward_Button, 3)

		#Czujniki nacisku
		ukladT2 = QGridLayout()
		ukladT2.addWidget(self.LcdN1, 0, 0)
		ukladT2.addWidget(self.LcdN2, 0, 1)
		ukladT2.addWidget(self.LcdN3, 0, 2)
		ukladT2.addWidget(self.LcdN4, 0, 3)
		ukladT2.addWidget(self.LcdN5, 0, 4)
		ukladT2.addWidget(self.LcdN6, 0, 5)
		ukladT2.addWidget(self.Pressure_button, 0 ,6)
		ukladT2.addWidget(self.LcdN1_label, 0, 0)
		ukladT2.addWidget(self.LcdN2_label, 0, 1)
		ukladT2.addWidget(self.LcdN3_label, 0, 2)
		ukladT2.addWidget(self.LcdN4_label, 0, 3)
		ukladT2.addWidget(self.LcdN5_label, 0, 4)
		ukladT2.addWidget(self.LcdN6_label, 0, 5)

		MainLayout = QGridLayout()
		MainLayout.addLayout(LegLayout, 0, 0)
		MainLayout.addLayout(ukladMonitor, 0, 1)
		MainLayout.addLayout(ukladDystans, 1, 1)
		MainLayout.addLayout(ukladT1, 0, 2)
		MainLayout.addLayout(ukladT2, 1, 0)
		MainLayout.addLayout(ukladT5, 0, 3)
		MainLayout.addLayout(ukladT12, 1, 2)
		MainLayout.addLayout(ukladB, 2, 1)
		MainLayout.addLayout(ukladXZ, 2, 0)
		MainLayout.addLayout(ukladOpcje, 2, 2)

		self.setLayout(MainLayout)

		self.setGeometry(20, 20, 800, 400)
		self.setWindowTitle("Sterowanie - Spyder")

		monitor.bufferUpdated.connect(self.RSRead)

		self.show()

		monitor.start()
		
	def sliderValueChanged(self, value, segment):
		self.lcd[int(segment)].display(value)
		
	def CreatePPGroupBox(self):
		groupBox = QGroupBox("Prawy Przód")
		
		ukladPP = QGridLayout()
		ukladPP.addWidget(self.sliderX4, 0, 0)
		ukladPP.addWidget(self.xLabel4, 0, 1)
		ukladPP.addWidget(self.sliderY4, 2, 0)
		ukladPP.addWidget(self.yLabel4, 2, 1)
		ukladPP.addWidget(self.sliderZ4, 3, 0)
		ukladPP.addWidget(self.zLabel4, 3, 1)
		
		groupBox.setLayout(ukladPP)
		
		return groupBox
			
	def CreatePSGroupBox(self):
		groupBox = QGroupBox("Prawy Środek")
		
		ukladPS = QGridLayout()
		ukladPS.addWidget(self.sliderX5, 0, 0)
		ukladPS.addWidget(self.xLabel5, 0, 1)
		ukladPS.addWidget(self.sliderY5, 2, 0)
		ukladPS.addWidget(self.yLabel5, 2, 1)
		ukladPS.addWidget(self.sliderZ5, 3, 0)
		ukladPS.addWidget(self.zLabel5, 3, 1)
		
		groupBox.setLayout(ukladPS)
		
		return groupBox
		
	def CreatePTGroupBox(self):
		groupBox = QGroupBox("Prawy Tył")
		
		ukladPT = QGridLayout()
		ukladPT.addWidget(self.sliderX6, 0, 0)
		ukladPT.addWidget(self.xLabel6, 0, 1)
		ukladPT.addWidget(self.sliderY6, 2, 0)
		ukladPT.addWidget(self.yLabel6, 2, 1)
		ukladPT.addWidget(self.sliderZ6, 3, 0)
		ukladPT.addWidget(self.zLabel6, 3, 1)
		
		groupBox.setLayout(ukladPT)
		
		return groupBox
			
	def CreateLPGroupBox(self):
		groupBox = QGroupBox("Lewy Przód")
		
		ukladLP = QGridLayout()
		ukladLP.addWidget(self.sliderX1, 1, 0)
		ukladLP.addWidget(self.xLabel1, 1, 1)
		ukladLP.addWidget(self.sliderY1, 2, 0)
		ukladLP.addWidget(self.yLabel1, 2, 1)
		ukladLP.addWidget(self.sliderZ1, 3, 0)
		ukladLP.addWidget(self.zLabel1, 3, 1)
		
		groupBox.setLayout(ukladLP)
		
		return groupBox
		
	def CreateLSGroupBox(self):
		groupBox = QGroupBox("Lewy Środek")
		
		ukladLS = QGridLayout()
		ukladLS.addWidget(self.sliderX2, 0, 0)
		ukladLS.addWidget(self.xLabel2, 0, 1)
		ukladLS.addWidget(self.sliderY2, 2, 0)
		ukladLS.addWidget(self.yLabel2, 2, 1)
		ukladLS.addWidget(self.sliderZ2, 3, 0)
		ukladLS.addWidget(self.zLabel2, 3, 1)
		
		groupBox.setLayout(ukladLS)
		
		return groupBox	
		
	def CreateLTGroupBox(self):
		groupBox = QGroupBox("Lewy Tył")
		
		ukladLT = QGridLayout()
		ukladLT.addWidget(self.sliderX3, 0, 0)
		ukladLT.addWidget(self.xLabel3, 0, 1)
		ukladLT.addWidget(self.sliderY3, 2, 0)
		ukladLT.addWidget(self.yLabel3, 2, 1)
		ukladLT.addWidget(self.sliderZ3, 3, 0)
		ukladLT.addWidget(self.zLabel3, 3, 1)
		
		groupBox.setLayout(ukladLT)
		
		return groupBox
	
	def Shutdown(self):
		odp = QMessageBox.question(self,
									"Pytanie", "Czy na pewno? ",
									QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if odp == QMessageBox.Yes:
			os.system("sudo shutdown -h now")
		
	def Reboot(self):
		odp = QMessageBox.question(self,
									"Pytanie", "Czy na pewno? ",
									QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if odp == QMessageBox.Yes:
			os.system("sudo reboot")
		
	def ResetArduino(self):
		odp = QMessageBox.question(self,
									"Pytanie", "Czy na pewno? ",
									QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if odp == QMessageBox.Yes:
			array = QByteArray()
			array.append('*')
			monitor.serialWrite(array)
			
			time.sleep(3)
			
			thread = threading.Thread(target = self.default)
			#thread = threading.Thread(target = self.test)
			thread.start()
	
	def valueChangedSpyderX(self):
		self.xLabelSpyder.setText("X: {0} %".format(IK.mapFunction(self.x_slider_spyder.value(), -180, -40, 0, 100)))
		
	def valueChangedSpyderZ(self):
		self.zLabelSpyder.setText("Z: {0} %".format(IK.mapFunction(self.z_slider_spyder.value(), -180, -40, 0, 100)))

	def valueChangedSpyderY(self):
		i = 1
		while i <= 17:
			self.auto_checkbox.setChecked(False)
			self.sliderTab[i].setValue(self.y_slider_spyder.value())
			self.yLabelSpyder.setText("Y: {0} %".format(IK.mapFunction(self.y_slider_spyder.value(), -180, -40, 0, 100)))
			i += 3
		self.execution()

	def distance(self):
		array = QByteArray()
		array.append('%')
		monitor.serialWrite(array)
		
	def front(self):
		ft = threading.Thread(target = self.front_thread)
		ft.start()
		
	def front_thread(self):
		delay = 0.75
		self.sliderY2.setValue(-80)
		self.sliderY4.setValue(-80)
		self.sliderY6.setValue(-80)
		#monitor.Czy_ready()
		time.sleep(delay)
		self.execution()
		
		self.sliderZ2.setValue(-50)
		self.sliderX2.setValue(-60)
		self.sliderZ4.setValue(-100)
		self.sliderX4.setValue(5)
		self.sliderZ6.setValue(0)
		self.sliderX6.setValue(85)
		#monitor.Czy_ready()
		time.sleep(delay)
		self.execution()
		
		self.sliderY2.setValue(-118)
		self.sliderY4.setValue(-118)
		self.sliderY6.setValue(-118)
		self.sliderX2.setValue(-70)
		#monitor.Czy_ready()
		time.sleep(delay)
		self.execution()
		
	def execution(self):
		self.auto_checkbox.setChecked(True)
		self.noga1(254)
		self.noga2(254)
		self.noga3(254)
		self.noga4(254)
		self.noga5(254)
		self.noga6(255)
		self.auto_checkbox.setChecked(False)
		
	def katy(self):
		if self.katyVar:            
			self.naKatyButton.setText("Kąty")
			self.katyVar = False
			self.kinematyka_wartosci()
		elif not self.katyVar:
			self.naKatyButton.setText("Kinematyka")
			self.katyVar = True
			for i in range(0, len(self.sliderTab)):
				self.sliderTab[i].setRange(0, 180)
				self.sliderTab[i].setValue(IK.katy[i])
					   
	def pressFunction(self):
		self.thread = threading.Thread(target = self.pressFunctionThread)
		self.thread.start()
		
	def pressFunctionThread(self):
		while True:
			array = QByteArray()
			array.append('@')
			monitor.serialWrite(array)
			time.sleep(0.09)
	   
	def valueChangedYc(self):
		array = QByteArray()
		array.append(chr(20))
		array.append('|')
		if self.y_slider_camera.value() != 124:
			array.append(chr(self.y_slider_camera.value()))
		else:
			array.append(chr(200))
		array.append('|')
		array.append(chr(255))
		array.append('#')
		
		self.y_label_camera.setText("Y: " + str(self.y_slider_camera.value()))
			  
		monitor.serialWrite(array)
		
	def valueChangedXc(self):
		array = QByteArray()
		array.append(chr(19))
		array.append('|')
		array.append(chr(self.x_slider_camera.value()))
		array.append('|')
		array.append(chr(255))
		array.append('#')
		
		self.x_label_camera.setText("X: " + str(self.x_slider_camera.value()))
		
		monitor.serialWrite(array)
		 
	def resetButtonClicked(self):      
		self.x_slider_camera.setValue(90)
		self.y_slider_camera.setValue(20)
		
		if not self.katyVar:
			self.sliderX1.setValue(-85)
			self.sliderY1.setValue(-118)
			self.sliderZ1.setValue(-90)

			self.sliderX2.setValue(-85)
			self.sliderY2.setValue(-118)
			self.sliderZ2.setValue(0)

			self.sliderX3.setValue(-85)
			self.sliderY3.setValue(-120)
			self.sliderZ3.setValue(50)

			self.sliderX4.setValue(85)
			self.sliderY4.setValue(-118)
			self.sliderZ4.setValue(-80)

			self.sliderX5.setValue(85)
			self.sliderY5.setValue(-118)
			self.sliderZ5.setValue(0)

			self.sliderX6.setValue(85)
			self.sliderY6.setValue(-118)
			self.sliderZ6.setValue(100)
			
		else:
			for i in range(0, len(self.sliderTab)):
				self.sliderTab[i].setValue(IK.katy[i])
			
	def closeEvent(self, QCloseEvent):
		odp = QMessageBox.question(self,
								   "Pytanie", "Czy na pewno? ",
								   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if odp == QMessageBox.Yes:
			QCloseEvent.accept()
		else:
			QCloseEvent.ignore()
			
	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.close()
		elif e.key() == Qt.Key_W:
			self.front()
		elif e.key() == Qt.Key_S:
			print("Dziala s")
		elif e.key() == Qt.Key_A:
			print("Dziala a")
		elif e.key() == Qt.Key_D:
			print("Dziala D")

	def koniec(self):
		self.close()
		
	def noga1(self, znak):
		value = IK.IK_LP(self.sliderX1.value(), self.sliderY1.value(), self.sliderZ1.value())
		if self.auto_checkbox.isChecked() and not self.katyVar:
			try:               
				elipsa.tablica("LP", value[0], value[1], value[2], znak, True)
			except:
				print("Poza zakresem")    
		self.LP_line.setText("LP: " + str(value[0]) + "  " + str(value[1]) + "  " + str(value[2]))
			
	def noga2(self, znak):
		value = IK.IK_LS(self.sliderX2.value(), self.sliderY2.value(), self.sliderZ2.value())
		if self.auto_checkbox.isChecked() and not self.katyVar:
			try:
				elipsa.tablica("LS", value[0], value[1], value[2], znak, True)
			except:
				print("Poza zakresem")
		self.LS_line.setText("LS: " + str(value[0]) + "  " + str(value[1]) + "  " + str(value[2]))       
		 
	def noga3(self, znak):
		value = IK.IK_LT(self.sliderX3.value(), self.sliderY3.value(), self.sliderZ3.value())
		if self.auto_checkbox.isChecked() and not self.katyVar:
			#try:              
			elipsa.tablica("LT", value[0], value[1], value[2], znak, True)  
		   # except:
			   # print("Poza zakresem")
		self.LT_line.setText("LT: " + str(value[0]) + "  " + str(value[1]) + "  " + str(value[2]))

	def noga4(self, znak):
		value = IK.IK_PP(self.sliderX4.value(), self.sliderY4.value(), self.sliderZ4.value())
		if self.auto_checkbox.isChecked() and not self.katyVar:
			try:                
				elipsa.tablica("PP", value[0], value[1], value[2], znak, True)
			except:
				print("Poza zakresem")
		self.PP_line.setText("PP: " + str(value[0]) + "  " + str(value[1]) + "  " + str(value[2]))

	def noga5(self, znak):
		value = IK.IK_PS(self.sliderX5.value(), self.sliderY5.value(), self.sliderZ5.value())
		if self.auto_checkbox.isChecked() and not self.katyVar:
			try:
				elipsa.tablica("PS", value[0], value[1], value[2], znak, True)
			except:
				print("Poza zakresem")
		self.PS_line.setText("PS: " + str(value[0]) + "  " + str(value[1]) + "  " + str(value[2]))

	def noga6(self, znak):
		value = IK.IK_PT(self.sliderX6.value(), self.sliderY6.value(), self.sliderZ6.value())
		if self.auto_checkbox.isChecked() and not self.katyVar:
			try:
				elipsa.tablica("PT", value[0], value[1], value[2], znak, True)
			except:
				print("Poza zakresem")
		self.PT_line.setText("PT: " + str(value[0]) + "  " + str(value[1]) + "  " + str(value[2]))
		
	def valueChangedX1(self):
		size = self.sliderX1.value()
		if not self.katyVar:
			self.xLabel1.setText("X = " + str(size))
			self.noga1('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(16))
				array.append('|')
				if self.sliderX1.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderX1.value()))
				array.append('#')
				self.xLabel1.setText("LP1 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedY1(self):
		size = self.sliderY1.value()
		if not self.katyVar:
			self.yLabel1.setText("Y = " + str(size))
			self.noga1('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(17))
				array.append('|')
				if self.sliderY1.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderY1.value()))
				array.append('#')
				self.yLabel1.setText("LP2 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedZ1(self):
		size = self.sliderZ1.value()
		if not self.katyVar:
			self.zLabel1.setText("Z = " + str(size))
			self.noga1('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(18))
				array.append('|')
				if self.sliderZ1.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderZ1.value()))
				array.append('#')
				self.zLabel1.setText("LP3 = " + str(size))
				monitor.serialWrite(array)
		
	def valueChangedX2(self):
		size = self.sliderX2.value()
		if not self.katyVar:
			size = self.sliderX2.value()
			self.xLabel2.setText("X = " + str(size))
			self.noga2('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(13))
				array.append('|')
				if self.sliderX2.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderX2.value()))
				array.append('#')
				self.xLabel2.setText("LS1 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedY2(self):
		size = self.sliderY2.value()
		if not self.katyVar:
			self.yLabel2.setText("Y = " + str(size))
			self.noga2('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(14))
				array.append('|')
				if self.sliderY2.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderY2.value()))
				array.append('#')
				self.yLabel2.setText("LS2 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedZ2(self):
		size = self.sliderZ2.value()
		if not self.katyVar:
			self.zLabel2.setText("Z = " + str(size))
			self.noga2('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(15))
				array.append('|')
				if self.sliderZ2.value() == 35:
					array.append(chr(-57))
				else:                   
					array.append(chr(self.sliderZ2.value()))
				array.append('#') 
				self.zLabel2.setText("LS3 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedX3(self):
		size = self.sliderX3.value()
		if not self.katyVar:
			self.xLabel3.setText("X = " + str(size))
			self.noga3('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(10))
				array.append('|')
				if self.sliderX3.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderX3.value()))
				array.append('#')
				self.xLabel3.setText("LT1 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedY3(self):
		size = self.sliderY3.value()
		if not self.katyVar:
			self.yLabel3.setText("Y = " + str(size))
			self.noga3('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(11))
				array.append('|')
				if self.sliderY3.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderY3.value()))
				array.append('#')
				self.yLabel3.setText("LT2 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedZ3(self):
		size = self.sliderZ3.value()
		if not self.katyVar:
			self.zLabel3.setText("Z = " + str(size))
			self.noga3('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(12))
				array.append('|')
				if self.sliderZ3.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderZ3.value()))
				array.append('#')
				self.zLabel3.setText("LT3 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedX4(self):
		size = self.sliderX4.value()
		if not self.katyVar:
			self.xLabel4.setText("X = " + str(size))
			self.noga4('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(7))
				array.append('|')
				if self.sliderX4.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderX4.value()))
				array.append('#')
				self.xLabel4.setText("PP1 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedY4(self):
		size = self.sliderY4.value()
		if not self.katyVar:
			self.yLabel4.setText("Y = " + str(size))
			self.noga4('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(8))
				array.append('|')
				if self.sliderY4.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderY4.value()))
				array.append('#')
				self.yLabel4.setText("PP2 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedZ4(self):
		size = self.sliderZ4.value()
		if not self.katyVar:
			self.zLabel4.setText("Z = " + str(size))
			self.noga4('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(9))
				array.append('|')
				if self.sliderZ4.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderZ4.value()))
				array.append('#')
				self.zLabel4.setText("PP3 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedX5(self):
		size = self.sliderX5.value()
		if not self.katyVar:
			size = self.sliderX5.value()
			self.xLabel5.setText("X = " + str(size))
			self.noga5('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(4))
				array.append('|')
				if self.sliderX5.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderX5.value()))
				array.append('#')
				self.xLabel5.setText("PS1 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedY5(self):
		size = self.sliderY5.value()
		if not self.katyVar:
			size = self.sliderY5.value()
			self.yLabel5.setText("Y = " + str(size))
			self.noga5('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(5))
				array.append('|')
				array.append(chr(self.sliderY5.value()))
				if self.sliderY5.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderY5.value()))
				array.append('#')
				self.yLabel5.setText("PS2 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedZ5(self):
		size = self.sliderZ5.value()
		if not self.katyVar:
			self.zLabel5.setText("Z = " + str(size))
			self.noga5('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(6))
				array.append('|')
				if self.sliderZ5.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderZ5.value()))
				array.append('#')
				self.zLabel5.setText("PS3 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedX6(self):
		size = self.sliderX6.value()
		if not self.katyVar:
			self.xLabel6.setText("X = " + str(size))
			self.noga6('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(1))
				array.append('|')
				if self.sliderX6.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderX6.value()))
				array.append('#')
				self.xLabel6.setText("PT1 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedY6(self):
		size = self.sliderY6.value()
		if not self.katyVar:
			self.yLabel6.setText("Y = " + str(size))
			self.noga6('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(2))
				array.append('|')
				if self.sliderY6.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderY6.value()))
				array.append('#')
				self.yLabel6.setText("PT2 = " + str(size))
				monitor.serialWrite(array)

	def valueChangedZ6(self):
		size = self.sliderZ6.value()
		if not self.katyVar:
			self.zLabel6.setText("Z = " + str(size))
			self.noga6('#')
		else:
			if self.auto_checkbox.isChecked(): 
				array = QByteArray()
				array.append('$')
				array.append(chr(3))
				array.append('|')
				if self.sliderZ6.value() == 35:
					array.append(chr(-57))
				else:
					array.append(chr(self.sliderZ6.value()))
				self.zLabel6.setText("PT3 = " + str(size))
				array.append('#')
				monitor.serialWrite(array)

	def checkboxFunction(self):
		print("oK")
		
	def RSRead(self, msg):
		#print(msg)
		if msg[2] == '@':
			tab = msg[3 : -6].split('|')
			self.LcdN1.display(int((int(tab[0]) * 100) / 255))
			self.LcdN2.display(int((int(tab[1]) * 100) / 255))
			self.LcdN3.display(int((int(tab[2]) * 100) / 255))
			self.LcdN4.display(int((int(tab[3]) * 100) / 255))
			self.LcdN5.display(int((int(tab[4]) * 100) / 255))
			self.LcdN6.display(int((int(tab[5]) * 100) / 255))
		elif  msg[2] == '%':
			self.distanceLCD.display(int(msg[3: -5]))
		else:
			self.monitor_receiver.append(str(msg[2 : -5])) 
