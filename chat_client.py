# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Elaborato reti: Client per chatroom

@author: Federico Mantoni
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
from tkinter import scrolledtext, messagebox

""" Gestisce la ricezione dei messaggi e la loro visualizzazione a schermo """
def ricevi_messaggio():
    while True:
        try:
            msg = client.recv(BUFSIZ).decode(ENCODING)
            msg_area.config(state=tkt.NORMAL)
            msg_area.insert(tkt.END, msg+"\n")
            msg_area.config(state=tkt.DISABLED)
            msg_area.see(tkt.END)
        except OSError:  
            break
        except ConnectionError as e:
            messagebox.showerror("Errore", "Errore: connessione interrotta")
            print("Errore, connessione interrotta: ", e)
            

""" Gestisce l'invio dei messaggi al server """
def invia_messaggio(event=None):
    try:
        msg = messaggio.get()
        messaggio.set("")
        client.send(msg.encode(ENCODING))
        if msg == QUIT:
            client.close()
            finestra.destroy()
    except (OSError, ConnectionError) as e:
        messagebox.showerror("Errore","Errore nell'invio del messaggio")
        print("errore nell'invio del messaggio", e)
        if msg == QUIT:
            finestra.destroy()

""" Gestisce il comportamento nel momento della chiusura della finestra """
def on_closure(event=None):
    messaggio.set(QUIT)
    invia_messaggio()
    

finestra = tkt.Tk()
finestra.title("Chatroom")

chat_frame = tkt.Frame(finestra)
chat_frame.pack()

msg_area = scrolledtext.ScrolledText(chat_frame, wrap=tkt.WORD, width=60, height=20, state=tkt.DISABLED)
msg_area.pack(side=tkt.LEFT, fill=tkt.BOTH)

messaggio = tkt.StringVar()
entry_field = tkt.Entry(finestra, textvariable=messaggio, width=42)
entry_field.bind("<Return>", invia_messaggio)
entry_field.pack()

send_button = tkt.Button(finestra, text="Invio", command=invia_messaggio)
send_button.pack()


finestra.protocol("WM_DELETE_WINDOW", on_closure)

#----Connessione al Server----
host = input('Inserisci l\'indirizzo IP del server host della chatroom: ')
port = input('Inserire la porta del server: ')

if not port:
    port = 53000
else:
    port = int(port)

BUFSIZ = 1024
address = (host, port)
QUIT = "!quit"
ENCODING = "utf8"

client = socket(AF_INET, SOCK_STREAM)

client.connect(address)

receive_thread = Thread(target=ricevi_messaggio).start()

tkt.mainloop()


