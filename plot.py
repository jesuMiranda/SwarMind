# plano.py
import cv2
import numpy as np
import time

class Plothandler:
    def __init__(self, width=500, height=500, refresh_interval=5, cam_width=1920, cam_height=1080):
        self.width = width
        self.height = height
        self.refresh_interval = refresh_interval
        self.cam_width = cam_width
        self.cam_height = cam_height
        self.last_update = 0
        self.current_points = {}  # {id: (cx, cy)}

    def actualizar_puntos(self, corners=None, ids=None):
        """
        corners: lista de arrays, o None
        ids: array numpy (Nx1) o None
        Guarda los centros detectados en self.current_points.
        Esta función es tolerante a entradas inesperadas.
        """
        try:
            if ids is None or corners is None:
                # No hay detecciones: vaciamos puntos (o mantener últimos?
                # aquí vaciamos porque quieres que no deje rastros fuera del intervalo de 5s)
                self.current_points = {}
                # debug
                # print("[PlanoHandler] No hay detecciones: current_points limpiado")
                return

            # Asegurar tipos
            # ids puede ser array Nx1, convertir a lista simple
            try:
                ids_list = [int(i[0]) if (hasattr(i, "__len__") and len(i) > 0) else int(i) for i in ids]
            except Exception:
                # Fallback si ids ya está en formato 1D
                ids_list = [int(i) for i in ids]

            puntos = {}
            for idx, corner in enumerate(corners):
                if idx >= len(ids_list):
                    continue
                robot_id = ids_list[idx]
                # corner esperado como array (1,4,2) o (4,2)
                arr = np.array(corner).reshape(-1, 2)
                cx = int(np.mean(arr[:, 0]))
                cy = int(np.mean(arr[:, 1]))
                puntos[robot_id] = (cx, cy)

            self.current_points = puntos
            # print(f"[PlanoHandler] Actualizado puntos: {self.current_points}")
        except Exception as e:
            print(f"[PlanoHandler] Error en actualizar_puntos: {e}")
            # no levantar para no romper la GUI

    def generar_plano(self):
        """Genera la imagen del plano con los puntos actuales, limpiando cada refresh_interval segundos."""
        try:
            current_time = time.time()
            # Creamos siempre una imagen limpia al momento de generar,
            # pero respetando el comportamiento de "limpiar cada 5s" simplemente
            # dejamos que current_points sea la fuente de verdad (ya se limpia en actualizar_puntos).
            img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255  # fondo blanco

            # Opcional: dibujar una cuadrícula simple
            step_x = 50
            step_y = 50
            for x in range(0, self.width, step_x):
                cv2.line(img, (x, 0), (x, self.height), (230, 230, 230), 1)
            for y in range(0, self.height, step_y):
                cv2.line(img, (0, y), (self.width, y), (230, 230, 230), 1)

            # Dibujar puntos escalando desde resolución de cámara
            for robot_id, (x, y) in self.current_points.items():
                sx = int((x / float(self.cam_width)) * self.width)
                sy = int((y / float(self.cam_height)) * self.height)
                cv2.circle(img, (sx, sy), 8, (0, 0, 255), -1)
                cv2.putText(img, f"ID:{robot_id}", (sx + 10, sy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"[PlanoHandler] Error en generar_plano: {e}")
            # devolver una imagen en blanco si falla
            img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
