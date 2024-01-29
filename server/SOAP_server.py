from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello(ctx, name, times):
        return "Hello, %s, %d times!" % (name, times)


if __name__ == '__main__':
    # Создаем SOAP-приложение
    soap_app = Application([HelloWorldService], 'urn:HelloWorldService', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())

    # Создаем WSGI-приложение
    wsgi_app = WsgiApplication(soap_app)

    # Запускаем сервер на порту 8000
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("SOAP server started on http://0.0.0.0:8000/")
    server.serve_forever()

