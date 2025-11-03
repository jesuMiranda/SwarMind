import sys
import cv2
import PruebaWIFI1  
from PyQt5 import QtWidgets, QtCore, QtGui
from EnjambreMain import Ui_MainWindow



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # =========================
        # Funciones del servidor
        # =========================
        # Iniciar servidor de comunicación con ESPs
        PruebaWIFI1.iniciar_servidor()

       


        # === Inicializar cámara ===
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # usa 0 si es la cámara principal
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        # Timer para actualizar frames
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # cada 30 ms (~33 fps)

        # === Conexiones de botones ===
        self.playButton.clicked.connect(self.encender_robots)
        self.pauseButton.clicked.connect(self.pausar_robots)
        self.stopButton.clicked.connect(self.stop_robots)
        # === Botones de conexión y calibración ===
        self.enviarButton.clicked.connect(self.enviar_variables)
        self.levelbutton.clicked.connect(self.calibrar_robots)



    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Procesar frame (ejemplo: detección ArUco)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Convertir a QImage
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)

        # Mostrar en QLabel (ajustar tamaño)
        self.camara.setPixmap(pixmap.scaled(
            self.camara.width(), self.camara.height(),
            QtCore.Qt.KeepAspectRatio
        ))

    # =========================
    # Funciones de los botones
    # =========================
    def encender_robots(self):
        print("[GUI] Enviando comando play a los robots")
        PruebaWIFI1.encender_robots()

    def pausar_robots(self):
        print("[GUI] Enviando comando pause a los robots")
        PruebaWIFI1.pausar_robots()

    def stop_robots(self):
        print("[GUI] Enviando comando STOP a los robots")
        PruebaWIFI1.stop_robots()

    def calibrar_robots(self):
        print("[GUI] Enviando comando CALIBRATE a los robots")
        PruebaWIFI1.calibrar_robots()

    def enviar_variables(self):
        try:
            # Leer valores de los QLineEdit
            L = self.Lux_lit.text().strip() 
            D = self.ran_detec.text().strip() 
            V = self.vel_motor.text().strip() 
            A = self.thetha_luz.text().strip() 
            M = self.tiempo_prueba.text().strip() 
            S = self.Tmax_var.text().strip() 

            # Convertir a formato decimal limpio
            L = str(float(L))
            D = str(float(D))
            V = str(float(V))
            A = str(float(A))
            M = str(float(M))
            S = str(float(S))

            # Construir trama
            comando = f"VARIABLES: L{L} D{D} V{V} A{A} M{M} S{S}"
            print(f"[GUI] Enviando: {comando}")

            # Enviar a todos los robots conectados
            for esp_id in list(PruebaWIFI1.clientes.keys()):
                PruebaWIFI1.enviar_mensaje(esp_id, comando)

            QtWidgets.QMessageBox.information(self, "Trama enviada", "Variables enviadas correctamente.")

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudieron enviar las variables:\n{e}")


    def closeEvent(self, event):
        """Liberar la cámara al cerrar la ventana."""
        if self.cap.isOpened():
            self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
