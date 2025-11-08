# camara.py
import cv2

class CameraHandler:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        self.parameters = cv2.aruco.DetectorParameters_create()

    def get_frame(self):
        """Lee un frame de la cámara y devuelve la imagen procesada."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        if not ret:
            return None, None, None

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Convertir a RGB antes de enviarlo a PyQt
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame_rgb, corners, ids
        



    def release(self):
        if self.cap.isOpened():
            self.cap.release()
