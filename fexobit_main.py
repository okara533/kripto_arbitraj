import time
import threading
from fexobit_socket import Fexobit_socket

socket=Fexobit_socket()
ws=socket.connect_socket()
threading.Thread(target=socket.prepare_data,args=[ws]).start()
threading.Thread(target=socket.print_data).start()
