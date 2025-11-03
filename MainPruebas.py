import sys
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from SwarMind.EnjambreMain import Ui_MainWindow
import PruebaWIFI1  # si no lo necesitas aún, puedes comentar esta línea

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # =========================
        # Funciones del servidor
        # =========================
        # Iniciar servidor de comunicación con ESPs
        PruebaWIFI1.iniciar_servidor()
        # Registrar la función callback para recibir mensajes
       # PruebaWIFI1.set_callback(self.recibir_mensaje)


        # === Inicializar cámara ===
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # usa 0 si es la cámara principal
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Timer para actualizar frames
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # cada 30 ms (~33 fps)

        # === Conexiones de botones ===
        self.playButton.clicked.connect(self.encender_robots)
        self.pauseButton.clicked.connect(self.pausar_robots)
        self.stopButton.clicked.connect(self.stop_robots)
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