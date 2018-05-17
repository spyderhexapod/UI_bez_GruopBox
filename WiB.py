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
