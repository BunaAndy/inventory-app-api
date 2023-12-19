from waitress import serve
from controller.app import app
from paste.translogger import TransLogger
print('Beginning Server')
serve(TransLogger(app, setup_console_handler=False), listen='*:8080')