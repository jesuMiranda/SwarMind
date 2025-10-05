import cv2
import cv2.aruco as aruco

def main():
    # Iniciar la cámara
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Definir el diccionario de marcadores ArUco
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
    parameters = aruco.DetectorParameters_create()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los marcadores
        corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            # Dibujar los contornos y los IDs detectados
            aruco.drawDetectedMarkers(frame, corners, ids)

            # Opcional: Dibujar un contorno más grueso manualmente
            for corner in corners:
                pts = corner.reshape((4, 2)).astype(int)
                cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

        # Mostrar la imagen
        cv2.imshow("Detección de ArUco", frame)

        # Salir con tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
