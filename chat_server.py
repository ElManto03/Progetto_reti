# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Elaborato reti: Server per chatroom

@author: Federico Mantoni
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

""" Stabilisce la connessione con i client richiedenti """
def accetta_connessione_client():
    while True:
        try:
            client, indirizzo_client = server.accept()
            print("Connessione da %s, porta %s" % indirizzo_client)
            client.send(("Inserisci il tuo nickname").encode(ENCODING))
            indirizzi[client] = indirizzo_client
            Thread(target=gestione_client, args=(client,)).start()
        except OSError as e:
             print("errore nella connessione al client:", e)
             
""" Gestisce l'ingresso di un client alla chatroom e di ricevere i messaggi inviati """
def gestione_client(client):
    try:
        nome = client.recv(BUFSIZ).decode(ENCODING)
        clients[client] = nome
        benvenuto = 'Benvenuto nella chatroom %s! Se vuoi lasciare la chatroom, scrivi %s per uscire.' % (nome, QUIT)
        client.send(benvenuto.encode(ENCODING))
        messaggio = "%s si è unito all chat!" % nome
        broadcast(messaggio.encode(ENCODING))
    
        while True:
            messaggio = client.recv(BUFSIZ)
            if messaggio.decode(ENCODING) != QUIT:
                broadcast(messaggio, nome+": ")
            else:
                client.close()
                del clients[client]
                broadcast((nome+" ha abbandonato la chat").encode(ENCODING))
                break
    except ConnectionError as e:
        print("Connessione interrotta col client indirizzo: {} porta: {}, errore: {}".format(indirizzi[client][0], indirizzi[client][1], e))
        if client in clients:
            del clients[client]
        if nome:
            broadcast((nome+" ha abbandonato la chat a causa di un errore").encode(ENCODING))
    except OSError as e:
        print("errore nella comunicazione col client", e)
    

""" Invia un messaggio a tutti i client collegati alla chatroom """
def broadcast(messaggio, nome=""):
    for client in clients:
        try:
            client.send(nome.encode(ENCODING)+messaggio)
        except (OSError, ConnectionError) as e:
            print("errore nell'invio del messaggio", e)
        

clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)
QUIT = "!quit"
ENCODING = "utf8"

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)

if __name__ == "__main__":
    server.listen(5)
    print("In attesa di connessioni...")
    accept_thread = Thread(target=accetta_connessione_client)
    accept_thread.start()
    try:
        accept_thread.join()
    except RuntimeError as e:
        print("Errore durante il join del thread: ", e)
    except KeyboardInterrupt:
        print("Esecuzione interrotta dall'utente")
    finally:
        server.close()
