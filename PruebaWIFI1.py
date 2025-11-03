import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes = {}  # Diccionario {ID: conexión}
ips_clientes = {}  # Relación IP → ID (para detección de reconexión)
callback_mensaje = None


# ---------------------------------------------
# Permitir que la interfaz registre un callback
# ---------------------------------------------
def set_callback(func):
    global callback_mensaje
    callback_mensaje = func


# ---------------------------------------------
# Enviar mensaje a un robot
# ---------------------------------------------
def enviar_mensaje(esp_id, mensaje):
    if esp_id in clientes:
        conn = clientes[esp_id]
        try:
            conn.sendall((mensaje + "\n").encode("utf-8"))
            print(f"[Servidor] Enviado a {esp_id}: {mensaje}")
        except Exception as e:
            print(f"[Servidor] Error enviando a {esp_id}: {e}")
            try:
                conn.close()
            except:
                pass
            del clientes[esp_id]
    else:
        print(f"[Servidor] {esp_id} no está conectado")


# ---------------------------------------------
# Hilo que maneja a cada cliente
# ---------------------------------------------
def handle_client(conn, addr):
    ip = addr[0]
    esp_id = None
    print(f"[+] Nueva conexión desde {ip}")

    try:
        # Recibir ID de la ESP32
        esp_id = conn.recv(1024).decode("utf-8").strip()
        if not esp_id:
            print(f"[Servidor] Conexión sin ID desde {ip}, cerrando...")
            conn.close()
            return

        # Si ya hay un cliente con la misma IP o ID, lo reemplazamos
        for key, c in list(clientes.items()):
            try:
                if c.getpeername()[0] == ip or key == esp_id:
                    print(f"[Servidor] Reemplazando conexión previa de {key} ({ip})")
                    try:
                        c.close()
                    except:
                        pass
                    del clientes[key]
            except:
                pass

        # Guardar conexión actual
        clientes[esp_id] = conn
        ips_clientes[ip] = esp_id
        print(f"[Servidor] Registrado {esp_id} ({ip})")

        # Bucle principal de recepción
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                mensaje = data.decode("utf-8").strip()
                print(f"[{esp_id}] => {mensaje}")

                # Notificar a la interfaz si hay callback
                if callback_mensaje:
                    callback_mensaje(esp_id, mensaje)

            except ConnectionResetError:
                print(f"[Servidor] Conexión reiniciada por {esp_id}")
                break
            except OSError as e:
                print(f"[Servidor] Error de red con {esp_id}: {e}")
                break

    except Exception as e:
        print(f"[Error general con {addr}]: {e}")

# Limpieza con tolerancia a reconexiones
    print(f"[-] Conexión cerrada: {addr}")
    try:
        conn.close()
    except:
        pass

    # No borres inmediatamente: espera posible reconexión
    import time
    def limpiar_cliente_luego(esp_id, ip):
        time.sleep(2)  # tiempo para reconectarse
        if esp_id in clientes and clientes[esp_id]._closed:
            print(f"[Servidor] Eliminando registro obsoleto de {esp_id}")
            clientes.pop(esp_id, None)
        ips_clientes.pop(ip, None)

    threading.Thread(target=limpiar_cliente_luego, args=(esp_id, ip), daemon=True).start()


# ---------------------------------------------
# Control de robots
# ---------------------------------------------
def encender_robots():
    for esp in list(clientes.keys()):
        enviar_mensaje(esp, "PLAY")

def pausar_robots():
    for esp in list(clientes.keys()):
        enviar_mensaje(esp, "PAUSE")

def stop_robots():
    for esp in list(clientes.keys()):
        enviar_mensaje(esp, "STOP")

def calibrar_robots():
    for esp in list(clientes.keys()):
        enviar_mensaje(esp, "CALIBRATE")


# ---------------------------------------------
# Servidor principal
# ---------------------------------------------
def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Servidor] Escuchando en {HOST}:{PORT}")

    def aceptar_clientes():
        while True:
            conn, addr = server.accept()
            hilo = threading.Thread(target=handle_client, args=(conn, addr))
            hilo.daemon = True
            hilo.start()

    hilo_server = threading.Thread(target=aceptar_clientes, daemon=True)
    hilo_server.start()


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



