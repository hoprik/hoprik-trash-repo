import http.server
import socketserver
import threading

# Указываем порт, на котором будет работать сервер
port = 8000

# Создаем обработчик запросов и указываем директорию
handler = http.server.SimpleHTTPRequestHandler
handler.directory = "F:\сайт\hoprikru"

def handle_request(handler, path, client_address, server):
    if path == "/exit":
        print("Получен запрос на выход. Сервер отключается.")
        server.shutdown()  # Отключаем сервер
        exit()
    else:
        handler(server, client_address, server)

def start():
    # Запускаем HTTP-сервер на указанном порту
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Сервер запущен на порту {port}")
        httpd.handle_request = lambda *args: handle_request(handler, *args)
        httpd.serve_forever()

thread = threading.Thread(target=start)
thread.start()
