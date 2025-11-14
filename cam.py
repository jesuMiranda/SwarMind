# camara.py
import cv2

class CameraHandler:
    def __init__(self, camera_index=0):
        #------------capturar video------------
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        #------------definir diccionario aruco------------
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        self.parameters = cv2.aruco.DetectorParameters_create()

        # ===== Grabación =====
        self.recording = False
        self.video_writer = None

    def start_recording(self, filename):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(filename, fourcc, 30.0, (1920, 1080))
        self.recording = True

    def stop_recording(self):
        self.recording = False
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

    def write_frame(self, frame_bgr):
        if self.recording and self.video_writer is not None:
            self.video_writer.write(frame_bgr)
            
    def get_frame(self):
        """Lee un frame de la cámara y devuelve la imagen procesada."""
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Invertir la imagen 180° (de cabeza)
        frame = cv2.flip(frame, -1)

        # Detección de marcadores ArUco
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Convertir a RGB para Qt
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame_rgb, corners, ids

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
