# Desenvolvido por Luiz F. R. Pimentel <-- KanekiZLF

import pyautogui
import time
import threading
import sys
import subprocess
from tkinter import *
from queue import Queue
from tkinter import messagebox
import os

programOpen = False
imgFound = False
buttonClick = False
emailClick = False
passwordClick = False
buttonContinue = False
buttonIgnore = False
stopThread = False
imgSearch = "FirstClick.png"
imgIcon = "iconCorel.ico"
os.chdir(os.path.dirname(os.path.realpath(__file__)))
# Criar uma fila para passar mensagens da thread secundária para a thread principal
message_queue = Queue()

def openProgram():
    global programOpen, stopThread, window

    if not programOpen and not stopThread:
        try:
            subprocess.Popen(r"CorelDRW.exe")
            programOpen = True
            return True
        except FileNotFoundError:
            messagebox.showerror("CorelRobotLogin by KanekiZLF",
                                 "O arquivo CorelDRW.exe não pôde ser localizado. Certifique-se de que o programa está na pasta executável do CorelDraw !",
                                 icon="error",
                                 type="ok",)
            sys.exit()

def searchStrings():
    global buttonClick, emailClick, passwordClick, buttonContinue, buttonIgnore, stopThread, text2, text3, text4, text5, text6

    while not stopThread:
        try:
            img = pyautogui.locateCenterOnScreen(imgSearch, confidence=0.8)
            if img:
                if not buttonClick:
                    pyautogui.click(img.x - 200, img.y + 120)
                    text2["text"] = "Corel Found !"
                    buttonClick = True

                if not emailClick:
                    pyautogui.click(img.x - 200, img.y + 160)
                    text3["text"] = "Found Email"
                    pyautogui.write("superKanekiZLF@fala.com")
                    emailClick = True

                if not passwordClick:
                    pyautogui.click(img.x - 200, img.y + 200)
                    text4["text"] = "Found Password"
                    pyautogui.write("omelhorsemduvidas")
                    passwordClick = True

                if not buttonContinue:
                    pyautogui.click(img.x + 200, img.y + 520)
                    text5["text"] = "Found Continue"
                    buttonContinue = True

                if not buttonIgnore:
                    pyautogui.click(img.x + 150, img.y + 520)
                    text6["text"] = "Found Ignore"
                    buttonIgnore = True

                if all([buttonClick, emailClick, passwordClick, buttonContinue, buttonIgnore]):
                    # Enviar mensagem para fechar o programa para a thread principal
                    message_queue.put("closeProgram")
                    break

        except pyautogui.ImageNotFoundException:
            if not stopThread:
                time.sleep(.5)
                # Enviar mensagem para atualizar a GUI com "Not Found" para a thread principal
                message_queue.put("notFound")

def showGui():
    global window, text2, text3, text4, text5, text6
    window = Tk()
    window.resizable(False, False)

    try:
        window.iconbitmap(imgIcon)
    except FileNotFoundError:
        messagebox.showerror("CorelRobot by KanekiZLF", f"Ícone não encontrado: {imgIcon}", type="ok")
    except TclError:
        messagebox.showerror("CorelRobot by KanekiZLF", "Erro ao definir o ícone !", type="ok")

    window.title("CorelRobot")
    text1 = Label(window, text="Iniciando Corel Login...")
    text1.grid(column=0, row=0)
    #button = Button(window, text="?")
    #button.grid(column=0, row=1)
    text2 = Label(window, text="Waiting for CorelDRW")
    text2.grid(column=0, row=2)
    text3 = Label(window, text="Waiting for CorelDRW")
    text3.grid(column=0, row=3)
    text4 = Label(window, text="Waiting for CorelDRW")
    text4.grid(column=0, row=4)
    text5 = Label(window, text="Waiting for CorelDRW")
    text5.grid(column=0, row=5)
    text6 = Label(window, text="Waiting for CorelDRW")
    text6.grid(column=0, row=6)
    window.protocol("WM_DELETE_WINDOW", closeProgram)

    # Inicia a thread após o programa ser aberto
    threading.Thread(target=searchStrings).start()

    # Verifica a fila de mensagens da thread secundária e atualiza a GUI
    window.after(100, checkMessageQueue)

    window.mainloop()

def checkMessageQueue():
    # Verifica se há mensagens na fila e atualiza a GUI conforme necessário
    while not message_queue.empty():
        message = message_queue.get()
        if message == "closeProgram":
            closeProgram()
        elif message == "notFound":
            text2["text"] = "Waiting for CorelDRW"
            text3["text"] = "Waiting for CorelDRW"
            text4["text"] = "Waiting for CorelDRW"
            text5["text"] = "Waiting for CorelDRW"
            text6["text"] = "Waiting for CorelDRW"
    
    # Agenda a verificação novamente após um curto período
    window.after(100, checkMessageQueue)

def closeProgram(*args):
    global stopThread
    if not stopThread:
        if window:
            window.destroy()
            stopThread = True
            sys.exit()

# Abre o programa antes de iniciar a thread
openProgram()

# Inicia a thread após o programa ser aberto
threading.Thread(target=showGui).start()
