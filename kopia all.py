try:
   import threading
   import os
   import sys
   import socket
   import time
   import RPi.GPIO as GPIO
   import serial
   from PyQt5.QtWidgets import QApplication, QWidget
   from PyQt5.QtGui import QIcon
   from PyQt5.QtWidgets import QLabel, QGridLayout, QLineEdit
   from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QTextEdit
   from PyQt5.QtCore import Qt, QObject, pyqtSignal, QByteArray
   from IK import IK_class
   from Ui import Sterowanie

except ImportError:
   print("Problem z importowaniem bibliotek")

Rsread = "1"
global okno

wifiport = 8888
polaczeniewifi = False

bluetoothport = 0
BluetoothRPi = 'B8:27:EB:F8:2F:2A'

polaczeniebluetooth = False

qwerty = 0

timer_czas = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Ard_in = 4

class Programator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()
    
    def interfejs(self):
        #Etykieta
        self.etykieta1 = QLabel("Monitor RS232", self)
        self.Odbior = QTextEdit(self)
        
        self.monitor = SerialMonitor()
              
        # przypisanie widgetów do układu tabelarycznego
        ukladT = QGridLayout()
        ukladT.addWidget(self.etykieta1, 0, 0)
        ukladT.addWidget(self.Odbior, 1, 0)
        
        # przyciski
        StartBtn = QPushButton("&Start", self)
        StopBtn = QPushButton("&Stop", self)
        koniecBtn = QPushButton("&Koniec", self)
        koniecBtn.resize(koniecBtn.sizeHint())
        koniecBtn.setToolTip('naciśnij <b>przycisk</b> aby zakończyć program')
        
        ukladH = QHBoxLayout()
        ukladH.addWidget(StartBtn)
        ukladH.addWidget(StopBtn)
        
        ukladT.addLayout(ukladH, 2, 0, 1, 3)
        ukladT.addWidget(koniecBtn, 3, 0, 1, 3)
        
        # przypisanie utworzonego układu do okna 
        self.setLayout(ukladT)
        self.monitor.bufferUpdated.connect(self.RSRead)
        koniecBtn.clicked.connect(self.koniec)
        StartBtn.clicked.connect(self.monitor.start)
        StopBtn.clicked.connect(self.monitor.stop)
        #self.Odbior.setReadOnly(True)
        
        self.setGeometry(20, 20, 300, 600)
        self.setWindowTitle("RS323 - Spyder")
        self.show()
        self.monitor.start() # uruchomienie procesu - automatyczne zamiast przycisku START
        
    def RSRead(self, msg):
        self.Odbior.append(str(msg))
                                     
    def koniec(self):
        self.monitor.stop() #zatrzymanie procesu
        self.close()

class SerialMonitor(QObject):
    pom = ''
    bufferUpdated = pyqtSignal(str)
    ser = serial.Serial('/dev/ttyACM0', baudrate=57600, # ttyAMA0
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)

    def __init__(self):
        super(SerialMonitor, self).__init__()
        self.running = False
        self.thread = threading.Thread(target=self.serial_monitor_thread)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.ser.close()

    def serialWrite(self, serialIn):
        #print("dziala")
        self.ser.write(serialIn)

    def Czy_ready(self):
        if self.pom == b'!\r\n':
             return True
        else: 
            return False

    def serial_monitor_thread(self):       
        while self.running is True:
            msg = self.ser.readline()
            if msg:
                try:
                    self.bufferUpdated.emit(str(msg))
                    self.pom = msg
                    msg = ''
                except ValueError:
                    print('Wrong data')
            else:
                pass
                #self.ser.close()
        
def Czytaj():
   try:
      dane = bus.read_byte(adres_i2c)
      print(dane)
      return dane
   except OSError:
      os.system("exit")
         
def dane(data):
   global qwerty
   if data[0] == 0 or data[0] == 8:
      qwerty = 0
      
   elif data[0] == 6:
      qwerty = -6

   elif data[0] != 0 or data[0] != 8 or data[0] != 6:
      qwerty = 10
      
   print(data[0])
   if data[0] >= 0 and data[0] <= 8:
      pisz(data[0])
   if data[0] == 10:   
       pisz(7)
       os.system("sudo shutdown -h now")
   if data[0] == 9:
      pisz(7)
      os.system("sudo reboot")
  
def WiFi():
   global qwerty
   wifi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      wifi.bind(('', wifiport))

   except socket.error as err:
       print("Error")
       print(err)
       sys.exit()

   wifi.listen(10)
   pisz(8)

   conn, addr = wifi.accept()
   qwerty = 0
   file = open("plik.txt", "a")
   print("Polaczono z: {0} : {1} (WiFi)".format(addr[0], str(addr[1])))
   print("Polaczenie nastapilo: {0}".format(czas()))
   file.write("Polaczono z: {0} : {1} (WiFi)  {2}".format(addr[0], str(addr[1]), czas()) + '\n')
   file.close()
   pisz(8)

   polaczeniewifi = True

   while True:  
       if polaczeniewifi == False:
          conn, addr = wifi.accept()
          file = open("plik.txt", "a")
          print("Polaczono z: {0} : {1} (WiFi)".format(addr[0], str(addr[1])))
          print("Polaczenie nastapilo: {0}".format(czas()))
          file.write("Polaczono z: {0} : {1} (WiFi)  {2}".format(addr[0], str(addr[1]), czas()) + '\n')
          file.close()
          pisz(8)
          polaczeniewifi = True
       data = conn.recv(64)

       try:
          dane(data)
                
       except:
            file = open("plik.txt", "a")
            print("Rozlaczono z: {0} : {1} (WiFi)".format(addr[0], str(addr[1])))
            pisz(7)
            print("Rozlaczenie nastapilo: {0}".format(czas()))
            file.write("Rozlaczono z: {0} : {1} (WiFi) {2}".format(addr[0], str(addr[1]), czas()) + '\n')
            file.close()
            print("Oczekiwanie na polaczenie WiFi lub Bluetooth")
            polaczeniewifi = False

   wifi.close()

def Bluetooth():
   global qwerty
   bluetooth = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
   try:
      bluetooth.bind((BluetoothRPi, bluetoothport))

   except socket.error as err:
      print("Error")
      print(err)
      sys.exit()

   bluetooth.listen(1)
   print("Oczekiwanie na polaczenie WiFi lub Bluetooth")
   client, addr = bluetooth.accept()
   pisz(8)
   qwerty = 0
   file = open("plik.txt", "a")
   print("Polaczono z: {0} (Bluetooth)".format(addr[0]))
   print("Polaczenie nastapilo: {0}".format(czas()))
   file.write("Polaczono z: {0} (Bluetooth)  {1}".format(addr[0], czas()) + '\n')
   file.close()

   polaczeniebluetooth = True

   while True:
      if polaczeniebluetooth == False:
          client, addr = bluetooth.accept()
          pisz(8)
          file = open("plik.txt", "a")
          print("Polaczono z: {0} (Bluetooth)".format(addr[0]))
          print("Polaczenie nastapilo: {0}".format(czas()))
          file.write("Polaczono z: {0} (Bluetooth)  {1}".format(addr[0], czas()) + '\n')
          file.close()
          polaczeniebluetooth = True

      try:
          data = client.recv(1024)
          dane(data)     
            
      except:
          file = open("plik.txt", "a")
          print("Rozlaczono z: {0} (Bluetooth)".format(addr[0]))
          pisz(7)
          print("Rozlaczenie nastapilo: {0}".format(czas()))
          file.write("Rozlaczono z: {0} (Bluetooth)  {1}".format(addr[0], czas()) + '\n')
          file.close()
          print("Oczekiwanie na polaczenie WiFi lub Bluetooth")
          polaczeniebluetooth = False

   bluetooth.close()

def czas():
   return time.strftime('%d/%m/%Y, %X')

def licznik():
   global qwerty
   while True:
      qwerty += 1
      time.sleep(1)
      if qwerty == 9:
         pisz(7)

def W():
         IK = IK_class()
         time.sleep(2.5) 
         for i in range(-90, 60):
            test = IK.IK_PT(70, -118, i)
            array = QByteArray()
            array.append(chr(1))
            array.append('|')
            array.append(chr(int(test[0])))
            array.append('|')
            array.append(chr(254))
            array.append('#')
            array.append(chr(2))
            array.append('|')
            array.append(chr(int(test[1])))
            array.append('|')
            array.append(chr(254))
            array.append('#')
            array.append(chr(3))
            array.append('|')
            array.append(chr(int(test[2])))
            array.append('|')
            array.append(chr(255))
            array.append('#')
            
            print(array)
            
           # time.sleep(0.01)
            
            while okno.monitor.Czy_ready() == False:
               time.sleep(1)
            
            okno.monitor.serialWrite(array)

def Ustaw90():
    
    IK = IK_class()
    time.sleep(2.5) 
    
    array = QByteArray()
           
    test = IK.IK_LP(-85, -118, 0)
    
    print("{1}, {0}".format(test, "LP"))
    
    array.append(chr(16))
    array.append('|')
    array.append(chr(int(test[0])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(17))
    array.append('|')
    array.append(chr(int(test[1])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(18))
    array.append('|')
    array.append(chr(int(test[2])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    
    test = IK.IK_LS(-85, -118, 0)
    
    print("{1}, {0}".format(test, "LS"))
    
    array.append(chr(13))
    array.append('|')
    array.append(chr(int(test[0])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(14))
    array.append('|')
    array.append(chr(int(test[1])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(15))
    array.append('|')
    array.append(chr(int(test[2])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    
    test = IK.IK_LT(-85, -118, 0)
    
    print("{1}, {0}".format(test, "LT"))
    
    array.append(chr(10))
    array.append('|')
    array.append(chr(int(test[0])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(11))
    array.append('|')
    array.append(chr(int(test[1])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(12))
    array.append('|')
    array.append(chr(int(test[2])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    
    test = IK.IK_PP(85, -118, 0)
    
    print("{1}, {0}".format(test, "PP"))
        
    array.append(chr(7))
    array.append('|')
    array.append(chr(int(test[0])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(8))
    array.append('|')
    array.append(chr(int(test[1])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(9))
    array.append('|')
    array.append(chr(int(test[2])))
    array.append('|')
    array.append(chr(254))
    array.append('#')  
    
    test = IK.IK_PS(85, -118, 0)
    
    print("{1}, {0}".format(test, "PS"))
     
    array.append(chr(4))
    array.append('|')
    array.append(chr(int(test[0])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(5))
    array.append('|')
    array.append(chr(int(test[1])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(6))
    array.append('|')
    array.append(chr(int(test[2])))
    array.append('|')
    array.append(chr(254))
    array.append('#')

     
    test = IK.IK_PT(85, -118, 0)
     
    print("{1}, {0}".format(test, "PT"))
     
    array.append(chr(1))
    array.append('|')
    array.append(chr(int(test[0])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(2))
    array.append('|')
    array.append(chr(int(test[1])))
    array.append('|')
    array.append(chr(254))
    array.append('#')
    array.append(chr(3))
    array.append('|')
    array.append(chr(int(test[2])))
    array.append('|')
    array.append(chr(255))
    array.append('#')
     

    
    okno.monitor.serialWrite(array)
    
    
    time.sleep(2)
    
    for i in range (0, 1):
    
        array.clear()
        
        test = IK.IK_PP(85, -118, -40)
        
        print("{1}, {0}".format(test, "PT"))
        
        array.append(chr(7))
        array.append('|')
        array.append(chr(int(test[0])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(8))
        array.append('|')
        array.append(chr(int(test[1])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(9))
        array.append('|')
        array.append(chr(int(test[2])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        
        test = IK.IK_PS(85, -118, -40)
        
        print("{1}, {0}".format(test, "PT"))
        
        array.append(chr(4))
        array.append('|')
        array.append(chr(int(test[0])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(5))
        array.append('|')
        array.append(chr(int(test[1])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(6))
        array.append('|')
        array.append(chr(int(test[2])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
    
        test = IK.IK_PT(85, -118, -40)
    
        print("{1}, {0}".format(test, "PT"))
    
        array.append(chr(1))
        array.append('|')
        array.append(chr(int(test[0])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(2))
        array.append('|')
        array.append(chr(int(test[1])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(3))
        array.append('|')
        array.append(chr(int(test[2])))
        array.append('|')
        array.append(chr(255))
        array.append('#')
    
        okno.monitor.serialWrite(array)
    
    
        time.sleep(1)
    
        array.clear()
        
        test = IK.IK_PP(85, -118, 40)
    
        print("{1}, {0}".format(test, "PT"))
    
        array.append(chr(7))
        array.append('|')
        array.append(chr(int(test[0])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(8))
        array.append('|')
        array.append(chr(int(test[1])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(9))
        array.append('|')
        array.append(chr(int(test[2])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        
    
        test = IK.IK_PS(85, -118, 40)
    
        print("{1}, {0}".format(test, "PT"))
    
        array.append(chr(4))
        array.append('|')
        array.append(chr(int(test[0])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(5))
        array.append('|')
        array.append(chr(int(test[1])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(6))
        array.append('|')
        array.append(chr(int(test[2])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        
    
        test = IK.IK_PT(85, -118, 40)
    
        print("{1}, {0}".format(test, "PT"))
    
        array.append(chr(1))
        array.append('|')
        array.append(chr(int(test[0])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(2))
        array.append('|')
        array.append(chr(int(test[1])))
        array.append('|')
        array.append(chr(254))
        array.append('#')
        array.append(chr(3))
        array.append('|')
        array.append(chr(int(test[2])))
        array.append('|')
        array.append(chr(255))
        array.append('#')
        
        okno.monitor.serialWrite(array)
        
        time.sleep(1)
    
    #~ test = IK.IK_LS(-55, -80, 0)
    #~ 
    #~ print("{1}, {0}".format(test, "LS"))
    #~ 
    #~ array.append(chr(13))
    #~ array.append('|')
    #~ array.append(chr(int(test[0])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(14))
    #~ array.append('|')
    #~ array.append(chr(int(test[1])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(15))
    #~ array.append('|')
    #~ array.append(chr(int(test[2])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ 
    #~ test = IK.IK_LT(-55, -80, 0)
    #~ 
    #~ print("{1}, {0}".format(test, "LT"))
    #~ 
    #~ array.append(chr(10))
    #~ array.append('|')
    #~ array.append(chr(int(test[0])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(11))
    #~ array.append('|')
    #~ array.append(chr(int(test[1])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(12))
    #~ array.append('|')
    #~ array.append(chr(int(test[2])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ 
    #~ test = IK.IK_PP(55, -80, 0)
    #~ 
    #~ print("{1}, {0}".format(test, "PP"))
        #~ 
    #~ array.append(chr(7))
    #~ array.append('|')
    #~ array.append(chr(int(test[0])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(8))
    #~ array.append('|')
    #~ array.append(chr(int(test[1])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(9))
    #~ array.append('|')
    #~ array.append(chr(int(test[2])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')  
    #~ 
    #~ test = IK.IK_PS(55, -80, 0)
    #~ 
    #~ print("{1}, {0}".format(test, "PS"))
    #~ 
    #~ array = QByteArray()
    #~ array.append(chr(4))
    #~ array.append('|')
    #~ array.append(chr(int(test[0])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(5))
    #~ array.append('|')
    #~ array.append(chr(int(test[1])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(6))
    #~ array.append('|')
    #~ array.append(chr(int(test[2])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
#~ 
    #~ 
    #~ test = IK.IK_PT(55, -80, 0)
    #~ 
    #~ print("{1}, {0}".format(test, "PT"))
    #~ 
    #~ array.append(chr(1))
    #~ array.append('|')
    #~ array.append(chr(int(test[0])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(2))
    #~ array.append('|')
    #~ array.append(chr(int(test[1])))
    #~ array.append('|')
    #~ array.append(chr(254))
    #~ array.append('#')
    #~ array.append(chr(3))
    #~ array.append('|')
    #~ array.append(chr(int(test[2])))
    #~ array.append('|')
    #~ array.append(chr(255))
    #~ array.append('#')
    
    #okno.monitor.serialWrite(array)

    
       
if __name__ == '__main__':

   app = QApplication(sys.argv)
   okno = Programator()
   okno1 = Sterowanie()

   a = threading.Thread(name = 'WiFi', target = WiFi)
   b = threading.Thread(name = 'Bluetooth', target = Bluetooth)
   c = threading.Thread(name = 'licznik', target = licznik)
   d = threading.Thread(name = 'Ustaw90', target = Ustaw90)

   #d.start()

 #  a.start()
 #  b.start()
 #  c.start()
 #  d.start()
 #  e.start()
 #  f.start()
 #  g.start()
 #  h.start()
 #  i.start()

   sys.exit(app.exec_())
  
