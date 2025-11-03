# ventana_conexion.py
from PyQt5 import QtWidgets
from ConexVista import Ui_conexWindow
import PruebaWIFI1

class VentanaConexion(QtWidgets.QMainWindow, Ui_conexWindow):
    def __init__(self):
        super(VentanaConexion, self).__init__()
        self.setupUi(self)

        # Valores por defecto (puedes ajustar desde Qt Designer también)
        self.Lux_lit.setText("500")
        self.ran_detec.setText("200")
        self.vel_motor.setText("150")
        self.thetha_luz.setText("7000")
        self.tiempo_prueba.setText("3")
        self.Tmax_var.setText("50")

        # Conectar botones
        self.levelbutton.clicked.connect(self.calibrar)
        self.enviarButton.clicked.connect(self.enviar_variables)

    def calibrar(self):
        """Envia comando de calibración."""
        print("[Ventana Conexión] Enviando comando CALIBRATE")
        PruebaWIFI1.calibrar_robots()

    def enviar_variables(self):
        """Crea y envía la trama con los valores ingresados."""
        # Obtener valores
        L = self.Lux_lit.text().strip()
        D = self.ran_detec.text().strip()
        V = self.vel_motor.text().strip()
        A = self.thetha_luz.text().strip()
        M = self.tiempo_prueba.text().strip()
        S = self.Tmax_var.text().strip()

        # Construir trama
        comando = f"VARIABLES: L{L} D{D} V{V} A{A} M{M} S{S}"
        print(f"[Ventana Conexión] Enviando: {comando}")

        # Enviar a todos los robots conectados
        for esp_id in list(PruebaWIFI1.clientes.keys()):
            PruebaWIFI1.enviar_mensaje(esp_id, comando)

        # Feedback visual
        QtWidgets.QMessageBox.information(self, "Enviado", "Trama enviada correctamente")
