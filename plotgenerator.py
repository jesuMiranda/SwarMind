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

    def generate_video(self, output_path, width, height, fps=30):
        """Genera video de las trayectorias."""
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Crear fondo blanco
        base = np.ones((height, width, 3), dtype=np.uint8) * 255

        # reproducir las trayectorias frame por frame
        max_len = max(len(lista) for lista in self.tracks.values())

        for t in range(max_len):
            frame = base.copy()

            for robot_id, points in self.tracks.items():
                color = self.palette.get(robot_id, (50, 50, 50))

                # Dibujar punto y líneas hasta el frame t
                for i in range(1, min(t, len(points)-1)):
                    cv2.line(frame, points[i-1], points[i], color, 3)

                if t < len(points):
                    cv2.circle(frame, points[t], 8, color, -1)

            out.write(frame)

        out.release()
