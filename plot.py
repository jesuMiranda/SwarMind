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

    def actualizar_puntos(self, corners, ids):
        """Recibe esquinas e IDs detectados por la cámara y guarda sus posiciones."""
        if ids is None:
            self.current_points = {}
            return

        puntos = {}
        for i, corner in enumerate(corners):
            pts = corner[0]
            # Calcular centro del marcador
            cx = int(np.mean(pts[:, 0]))
            cy = int(np.mean(pts[:, 1]))
            puntos[int(ids[i][0])] = (cx, cy)

        self.current_points = puntos

    def generar_plano(self):
        """Genera una imagen con los puntos actuales. Se limpia cada 5 s."""
        current_time = time.time()

        # Cada refresh_interval segundos, se limpia el plano
        if current_time - self.last_update > self.refresh_interval:
            self.last_update = current_time
            img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255  # fondo blanco
        else:
            img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

        # Dibujar puntos (centros)
        for robot_id, (x, y) in self.current_points.items():
            # Escalar coordenadas si vienen en resolución de cámara
            sx = int((x / 1920) * self.width)
            sy = int((y / 1080) * self.height)
            cv2.circle(img, (sx, sy), 8, (0, 0, 255), -1)
            cv2.putText(img, f"ID:{robot_id}", (sx + 10, sy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
