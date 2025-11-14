import cv2
import numpy as np

class TrajectoryGenerator:
    def __init__(self, palette):
        self.palette = palette      # colores de los robots
        self.tracks = {}            # id → lista de posiciones

        # Detector ArUco
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        self.parameters = cv2.aruco.DetectorParameters_create()

    def process_frame(self, frame):
        """Detecta arucos y almacena posiciones."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

        if ids is not None:
            for i, corner in enumerate(corners):
                pts = corner[0]
                cx = int(np.mean(pts[:,0]))
                cy = int(np.mean(pts[:,1]))
                robot_id = int(ids[i][0])

                if robot_id not in self.tracks:
                    self.tracks[robot_id] = []

                self.tracks[robot_id].append((cx, cy))

    def generate_video(self, output_path, w, h, fps):
        """Genera un video con las trayectorias almacenadas."""
        # 1. Validación: si no existen trayectorias, NO generar video
        if not self.tracks or len(self.tracks) == 0:
            print("[PlotGenerator] No se detectaron trayectorias. No se generará video.")
            return False

        # 2. Validación adicional: si existen pero están vacías
        datos_validos = any(len(lista) > 0 for lista in self.tracks.values())
        if not datos_validos:
            print("[PlotGenerator] Las trayectorias existen pero están vacías. No se generará video.")
            return False

        # 3. Obtener la longitud máxima de todas las trayectorias
        max_len = max(len(lista) for lista in self.tracks.values())

        # 4. Crear el objeto VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Más estable en Windows
        video = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

        if not video.isOpened():
            print("[PlotGenerator] ERROR: No se pudo abrir VideoWriter.")
            print("[PlotGenerator] Ruta:", output_path)
            return False

        # 5. Generar los frames del video
        for i in range(max_len):
            frame = np.ones((h, w, 3), dtype=np.uint8) * 255  # Fondo blanco

            # Dibujar la trayectoria de cada robot en el frame actual
            for robot_id, puntos in self.tracks.items():
                if i < len(puntos):
                    x, y = puntos[i]
                    cv2.circle(frame, (int(x), int(y)), 6, (0, 0, 255), -1)

            # Escribir frame al video
            video.write(frame)

        # 6. Cerrar el video
        video.release()

        print(f"[PlotGenerator] Video generado correctamente en: {output_path}")
        return True
