import sys
import signal
import http.server
import socketserver

#Se passato un numero di porta da riga di comando utilizza quello, altrimenti di default usa la porta 8080
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080

#ThreadingTCPServer serve per gestire più richieste
server = socketserver.ThreadingTCPServer(('',port), http.server.SimpleHTTPRequestHandler )

#Assicura che Ctrl+C termini in modo pulito tutti i thread generati
server.daemon_threads = True

#acconsente il riutilizzo del socket anche se non ancora rilasciato
server.allow_reuse_address = True  

#funzione che permette di uscire dal processo tramite Ctrl+C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

#interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

# entra nel loop infinito
try:
  while True:
    server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close()