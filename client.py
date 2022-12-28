import tkinter as tk
from itertools import count
from PIL import Image, ImageTk
import threading, pyaudio, wave, socketio

sio = socketio.Client()

go = False

#Setup GUI
root = tk.Tk()
root['bg']='#000000'
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title('Epic Sax Guy')
fs = []
def e_i_f_g(p):
    global gd
    image = Image.open(p)
    for r in count(1):
        try:
            fs.append(image.copy().resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS))
            image.seek(r)
        except Exception as e:
            print(e)
            break
    print(len(fs))
x = 0
def p_g():
    global x, c_i
    try:
        x += 1
        r_i = fs[x]
        c_i = ImageTk.PhotoImage(r_i)
        g_l.config(image=c_i)
        root.after(50, p_g)
    except Exception as e:
        print(e)
        x = 0
        root.after(50, p_g)
g_l = tk.Label(root)
g_l.pack()
e_i_f_g("vibe.gif")
p_g()

# Setup Audio
def play_audio():
        global is_playing
        global my_thread
        CHUNK = 1024
        wf = wave.open('aud.wav', 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
        while True:
            wf.rewind()
            data = wf.readframes(CHUNK)
            while data:
                stream.write(data)
                data = wf.readframes(CHUNK)
def aoodiu():
    aud = threading.Thread(target=play_audio, name="Audio Playback Thread")
    aud.start()
root.after(1, aoodiu)

#Listen for the go time message from server
@sio.event
def connect():
    print('Connected')
@sio.event
def time(data):
    global go
    print("Server said go time "+str(data))
    go = data
@sio.event
def disconnect():
    print('Disconnected')
def conserv():
    try:
        sio.connect('https://epicsaxguy.trsc25.repl.co/')
    except Exception as e:
        print(e)
        print("Connection Failed. Retrying...")
        conserv()
conserv()
while True:
    if go:
        root.mainloop()
sio.wait()