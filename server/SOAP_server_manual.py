from http.server import (
    BaseHTTPRequestHandler,  # обработка HTTP-запросов.
    HTTPServer,
)
from xml.etree import ElementTree as ET


class SimpleSoapServer(BaseHTTPRequestHandler):

    def do_POST(self):
        # Обязательный заголовок HTTP, указывающий на длину тела запроса.
        content_length = int(self.headers['Content-Length'])
        # Данные из тела запроса.
        soap_request = self.rfile.read(content_length).decode('utf-8')

        # Парсим SOAP-запрос.
        root = ET.fromstring(soap_request)
        name = root.find('.//{urn:HelloWorldService}name').text
        times = int(root.find('.//{urn:HelloWorldService}times').text)

        # Формирование SOAP-ответа
        soap_response = """<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="urn:HelloWorldService">
               <soapenv:Header/>
               <soapenv:Body>
                  <web:say_helloResponse>
                     <return>Hello, %s, %d times!</return>
                  </web:say_helloResponse>
               </soapenv:Body>
            </soapenv:Envelope>
        """ % (name, times)

        # Отправка ответа
        self.send_response(200)
        self.send_header('Content-Type', 'text/xml; charset=utf-8')
        self.send_header('Content-Length', len(soap_response))
        self.end_headers()
        self.wfile.write(soap_response.encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleSoapServer)
    print("SOAP server started on http://0.0.0.0:8000/")
    httpd.serve_forever()
