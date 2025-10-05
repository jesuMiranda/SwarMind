import sys
from PyQt5 import QtWidgets, QtCore
from EnjambreMain import Ui_MainWindow
import PruebaWIFI1

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # Señal Qt para actualizar la interfaz desde hilos externos
    mensaje_recibido = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Iniciar servidor de comunicación con ESPs
        PruebaWIFI1.iniciar_servidor()

        # Registrar la función callback para recibir mensajes
        PruebaWIFI1.set_callback(self.recibir_mensaje)

        # Conectar botones
        self.playButton.clicked.connect(self.encender_robots)
        self.stopButton.clicked.connect(self.apagar_robots)
        self.levelbutton.clicked.connect(self.calibrar_robots)

        # Conectar la señal Qt a la función que actualiza el label
        self.mensaje_recibido.connect(self.actualizar_label)

    # --------------------
    # Funciones de botones
    # --------------------
    def encender_robots(self):
        print("[GUI] Enviando comando ON a los robots")
        PruebaWIFI1.encender_robots()

    def apagar_robots(self):
        print("[GUI] Enviando comando OFF a los robots")
        PruebaWIFI1.apagar_robots()

    def calibrar_robots(self):
        print("[GUI] Enviando comando CALIBRATE a los robots")
        PruebaWIFI1.calibrar_robots()

    # --------------------
    # Recepción de mensajes desde ESP
    # --------------------
    def recibir_mensaje(self, esp_id, mensaje):
        """
        Esta función la llama el servidor cuando recibe un mensaje de un ESP.
        No puede modificar la GUI directamente (va en otro hilo),
        así que emitimos una señal Qt.
        """
        print(f"[GUI] Mensaje recibido de {esp_id}: {mensaje}")
        if mensaje.lower() == "calibrado":
            texto = f"{esp_id} calibrado correctamente"
            self.mensaje_recibido.emit(texto)

    def actualizar_label(self, texto):
        """
        Esta función sí se ejecuta en el hilo principal,
        por lo que puede actualizar widgets sin problemas.
        """
        self.levellabel.setText(texto)
        print(f"[GUI] Mostrando en label: {texto}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
