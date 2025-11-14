# plano.py
import cv2
import numpy as np
import time

class Plothandler:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.last_update = 0
        self.refresh_interval = 5  # segundos
        self.current_points = {}

        #  PALETA de colores suaves PARA IDs 1-10
        self.PALETTE = {
            1:  (0, 0, 255),      # Rojo fuerte
            2:  (0, 255, 0),      # Verde fuerte
            3:  (255, 0, 0),      # Azul fuerte
            4:  (0, 255, 255),    # Amarillo fuerte
            5:  (255, 0, 255),    # Magenta
            6:  (255, 255, 0),    # Cyan
            7:  (0, 128, 255),    # Naranja
            8:  (128, 0, 255),    # Morado
            9:  (255, 0, 128),    # Rosa fuerte
            10: (0, 255, 128),    # Lima brillante
        }


    def actualizar_puntos(self, corners, ids):
        if ids is None:
            self.current_points = {}
            return

        puntos = {}
        for i, corner in enumerate(corners):
            pts = corner[0]
            cx = int(np.mean(pts[:, 0]))
            cy = int(np.mean(pts[:, 1]))
            puntos[int(ids[i][0])] = (cx, cy)

        self.current_points = puntos

    def generar_plano(self):
        current_time = time.time()

        # Reiniciar imagen cada X segundos
        if current_time - self.last_update > self.refresh_interval:
            self.last_update = current_time
            img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        else:
            img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

        # Dibujar puntos
        for robot_id, (x, y) in self.current_points.items():

            # Escalar posiciones
            sx = int((x / 1920) * self.width)
            sy = int((y / 1080) * self.height)

            #  Seleccionar color suave según ID
            color = self.PALETTE.get(robot_id, (200, 200, 200))  # gris si ID > 10

            # Dibujar punto
            cv2.circle(img, (sx, sy), 25, color, -1)

            # Dibujar etiqueta
            cv2.putText(
                img,
                f"ID:{robot_id}",
                (sx + 15, sy - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                color,
                3,
                cv2.LINE_AA
            )

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
