import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

clientes = {}  # Diccionario {ID: conexión}
callback_mensaje = None  # Aquí guardaremos una función que será llamada cuando llegue un mensaje


def set_callback(func):
    """Permite que la interfaz registre una función para recibir mensajes."""
    global callback_mensaje
    callback_mensaje = func

def handle_client(conn, addr):
    print(f"[+] Nueva conexión: {addr}")


    try:
        # Recibir ID de ESP al conectarse
        esp_id = conn.recv(1024).decode("utf-8").strip()
        clientes[esp_id] = conn
        print(f"[Servidor] Registrado {esp_id} desde {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode("utf-8").strip()
            print(f"[{esp_id}] => {mensaje}")
    except:
        pass

    print(f"[-] Conexión cerrada: {addr}")
    conn.close()
    if esp_id in clientes:
        del clientes[esp_id]

def enviar_mensaje(esp_id, mensaje):
    if esp_id in clientes:
        try:
            clientes[esp_id].sendall((mensaje + "\n").encode("utf-8"))
            print(f"[Servidor] Enviado a {esp_id}: {mensaje}")
        except:
            print(f"[Servidor] Error enviando a {esp_id}")
    else:
        print(f"[Servidor] {esp_id} no está conectado")

# Configuración del servidor
def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Servidor] Escuchando en {HOST}:{PORT}")

# Acepta múltiples clientes
    def aceptar_clientes():
        while True:
            conn, addr = server.accept()
            hilo = threading.Thread(target=handle_client, args=(conn, addr))
            hilo.start()
            
    hilo_server = threading.Thread(target=aceptar_clientes, daemon=True)
    hilo_server.start()

# -----------------------------
# Funciones de control
# -----------------------------
def encender_robots():
    for esp in list(clientes.keys()):
        enviar_mensaje(esp, "ON")

def apagar_robots():
    for esp in list(clientes.keys()):
        enviar_mensaje(esp, "OFF")
def calibrar_robots():
    for esp in list(clientes.keys()):
        enviar_mensaje(esp, "calibrate")



"""
# Ejemplo: mandar mensajes
while True:
    
    enviar_mensaje("ESP1", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP2", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP3", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP4", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP5", "ON")   # LED encendido
    time.sleep(2)

    enviar_mensaje("ESP6", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP7", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP8", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP9", "ON")   # LED encendido
    time.sleep(2)
    enviar_mensaje("ESP10", "ON")   # LED encendido
    time.sleep(2)

    enviar_mensaje("ESP1", "OFF")  # LED apagado
    enviar_mensaje("ESP2", "OFF")  # LED apagado
    enviar_mensaje("ESP3", "OFF")  # LED apagado
    enviar_mensaje("ESP4", "OFF")  # LED apagado
    enviar_mensaje("ESP5", "OFF")  # LED apagado
    '''
    enviar_mensaje("ESP6", "OFF")  # LED apagado
    enviar_mensaje("ESP7", "OFF")  # LED apagado
    enviar_mensaje("ESP8", "OFF")  # LED apagado
    enviar_mensaje("ESP9", "OFF")  # LED apagado
    enviar_mensaje("ESP10", "OFF")  # LED apagado
    '''
    time.sleep(2)
   

"""



