import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import PruebaWIFI1
from EnjambreMain import Ui_MainWindow
from cam import CameraHandler
from plot import Plothandler

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Iniciar servidor
        PruebaWIFI1.iniciar_servidor()

        # === Cámara ===
        self.camera = CameraHandler()
        self.plano = Plothandler()


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # === Conexiones ===
        self.playButton.clicked.connect(self.encender_robots)
        self.pauseButton.clicked.connect(self.pausar_robots)
        self.stopButton.clicked.connect(self.stop_robots)
        self.enviarButton.clicked.connect(self.enviar_variables)
        self.levelbutton.clicked.connect(self.calibrar_robots)

        # Valores por defecto
        self.Lux_lit.setText("500")
        self.ran_detec.setText("0.8")
        self.vel_motor.setText("150")
        self.thetha_luz.setText("450000")
        self.tiempo_prueba.setText("3")
        self.Tmax_var.setText("60")

    def update_frame(self):
        frame, corners, ids = self.camera.get_frame()
        if frame is None:
            return

        # 1️⃣ Mostrar cámara
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        self.camara.setPixmap(pixmap.scaled(
            self.camara.width(),
            self.camara.height(),
            QtCore.Qt.KeepAspectRatio
        ))

        # 2️⃣ Actualizar plano
        self.plano.actualizar_puntos(corners, ids)
        plano_img = self.plano.generar_plano()

        h2, w2, ch2 = plano_img.shape
        bytes_per_line2 = ch2 * w2
        q_img2 = QtGui.QImage(plano_img.data, w2, h2, bytes_per_line2, QtGui.QImage.Format_RGB888)
        pixmap2 = QtGui.QPixmap.fromImage(q_img2)
        self.plot.setPixmap(pixmap2.scaled(
            self.plot.width(),
            self.plot.height(),
            QtCore.Qt.KeepAspectRatio
        ))



    # Funciones de botones
    def encender_robots(self):
        PruebaWIFI1.encender_robots()

    def pausar_robots(self):
        PruebaWIFI1.pausar_robots()

    def stop_robots(self):
        PruebaWIFI1.stop_robots()

    def calibrar_robots(self):
        PruebaWIFI1.calibrar_robots()

    def enviar_variables(self):
        try:
            L = str(float(self.Lux_lit.text().strip()))
            D = str(float(self.ran_detec.text().strip()))
            V = str(float(self.vel_motor.text().strip()))
            A = str(float(self.thetha_luz.text().strip()))
            M = str(float(self.tiempo_prueba.text().strip()))
            S = str(float(self.Tmax_var.text().strip()))

            comando = f"VARIABLES: L{L} D{D} V{V} A{A} M{M} S{S}"
            print(f"[GUI] Enviando: {comando}")

            for esp_id in list(PruebaWIFI1.clientes.keys()):
                PruebaWIFI1.enviar_mensaje(esp_id, comando)

            QtWidgets.QMessageBox.information(self, "Trama enviada", "Variables enviadas correctamente.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se pudieron enviar las variables:\n{e}")

    def closeEvent(self, event):
        """Liberar la cámara al cerrar."""
        self.camera.release()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
