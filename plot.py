import cv2
import numpy as np
import time
import random

class Plothandler:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.last_update = 0
        self.refresh_interval = 5  # segundos
        self.current_points = {}
        self.colors = {}  # ← Diccionario para guardar color de cada ID

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

            # === COLOR ÚNICO POR ID ===
            if robot_id not in self.colors:
                # Generar color aleatorio y guardarlo
                self.colors[robot_id] = tuple(random.randint(50, 255) for _ in range(3))
            color = self.colors[robot_id]

            # === DIBUJO DEL PUNTO Y ETIQUETA ===
            cv2.circle(img, (sx, sy), 25, color, -1)  # radio ↑ (antes 20)
            cv2.putText(
                img,
                f"ID:{robot_id}",
                (sx + 15, sy - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,           # tamaño ↑ (antes 0.9)
                color,         # usa el mismo color del punto
                3              # grosor ↑ (antes 2)
            )

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
