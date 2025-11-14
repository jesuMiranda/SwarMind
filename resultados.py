from PyQt5 import QtWidgets, QtGui
from resultadosVista import Ui_MainWindow
import os

class ResultadosWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, datos, video_path):
        super().__init__()
        self.setupUi(self)

        self.datos = datos
        self.video_path = video_path

        # Conectar botones
        self.guardar.clicked.connect(self.guardar_resultados)
        self.descartar.clicked.connect(self.descartar_video)

        # Llenar tabla
        self.load_table(datos)

    def load_table(self, datos):
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["Variable", "Valor"])
        for k, v in datos.items():
            model.appendRow([QtGui.QStandardItem(k), QtGui.QStandardItem(str(v))])
        self.tableView.setModel(model)

    def guardar_resultados(self):
        # Seleccionar carpeta donde guardar
        ruta = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta para guardar resultados",
            "",
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if ruta:  # Si el usuario no cancela
            # === GUARDAR VIDEO ===
            if os.path.exists(self.video_path):
                nombre_video = os.path.basename(self.video_path)
                destino_video = os.path.join(ruta, nombre_video)
                os.replace(self.video_path, destino_video)

            # === GUARDAR CSV DE DATOS ===
            csv_path = os.path.join(ruta, "datos_experimento.csv")

            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("variable,valor\n")
                for k, v in self.datos.items():
                    f.write(f"{k},{v}\n")

        # Opcional: Cerrar ventana después de guardar
        self.close()


    def descartar_video(self):
        if os.path.exists(self.video_path):
            os.remove(self.video_path)
        QtWidgets.QMessageBox.information(self, "Descartado", "El video ha sido eliminado.")
