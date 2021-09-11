from PIL import Image, ImageDraw
from math import log, log2
import progressbar
import threading
import colorsys
import _thread
import queue
import json
import os

MAX_ITER = 450

# Image size (pixels)

WIDTH = 600
HEIGHT = 400
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1
filename = None
THREADS = 20

data = queue.Queue()

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) < 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    if n == MAX_ITER:
        return MAX_ITER
    return n + 1 - log(log2(abs(z)))
"""
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n
"""
DEBUG = []

def thread_worker(thread_id):
    while True:
        try:
            x,y,c = data.get_nowait()
        except queue.Empty:
            break
        m = mandelbrot(c)
        # The color depends on the number of iterations
        hue = int(255 * m / MAX_ITER)
        saturation = 255
        if m < MAX_ITER:
            value = 255
        else:
            value = 0
        # Plot the point
        draw.point([x, y], (hue, saturation, value))
        DEBUG.append("Proccessed point X: "+str(x)+",Y: "+str(y)+",C: "+str(c)+" by thread "+str(thread_id))
    DEBUG.append("Completed thread "+str(thread_id))

def main_thread_worker(thread_id):
    with progressbar.ProgressBar(max_value=WIDTH*HEIGHT) as bar:
        while True:
            try:
                x,y,c = data.get_nowait()
            except queue.Empty:
                break
            m = mandelbrot(c)
            # The color depends on the number of iterations
            hue = int(255 * m / MAX_ITER)
            saturation = 255
            if m < MAX_ITER:
                value = 255
            else:
                value = 0
            # Plot the point
            draw.point([x, y], (hue, saturation, value))
            bar.update((WIDTH*HEIGHT)-data.qsize())
            DEBUG.append("Proccessed point X: "+str(x)+",Y: "+str(y)+",C: "+str(c)+" by main thread")
        DEBUG.append("Completed main thread")
    print("Completed all work on main thread, size of queue is ",data.qsize())

try:
    conf = json.loads(input("Enter JSON configuration: "))
    WIDTH = conf.get("WIDTH")
    HEIGHT = conf.get("HEIGHT")
    RE_START = conf.get("RE_START")
    RE_END = conf.get("RE_END")
    IM_START = conf.get("IM_START")
    IM_END = conf.get("IM_END")
    if conf.get("FILENAME") is not None and type(conf.get("FILENAME")) == str:
        filename = conf.get("FILENAME")
        print("JSON filename loaded!")
    else:
        filename = None
    if conf.get("MAX_ITER") is not None and type(conf.get("MAX_ITER")) == int:
        MAX_ITER = conf.get("MAX_ITER")
        print("JSON MAX_ITER loaded, settings MAX_ITER to",str(conf.get("MAX_ITER"))+"!")
    if conf.get("THREADS") is not None and type(conf.get("THREADS")) == int:
        THREADS = conf.get("THREADS")
    print("JSON conf loaded!")
except:
    print("Failed to load JSON conf, using default one!")


im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

for x in progressbar.progressbar(range(0, WIDTH)):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        data.put([x,y,c])

for i in range(THREADS):
    _thread.start_new_thread(thread_worker, (i,))
    #threading.Thread(target=thread_worker, daemon=True).start()

main_thread_worker(THREADS)
#data.join()


#im.convert('RGB').save('output-rgb.png', 'PNG')
if filename == None:
    filename = input("Enter filename to save image to (must end with .png, image will be saved in the images folder): ")
if not "./images/" in filename:
    filename = os.path.join("./images/" , filename)
imRGB = im.convert("RGB")
imRGB.save(filename, "PNG")
print("RGB image successfully saved!")
code = '{ "WIDTH":'+str(WIDTH)+', "HEIGHT":'+str(HEIGHT)+', "RE_START":'+str(RE_START)+', "RE_END":'+str(RE_END)+', "IM_START":'+str(IM_START)+', "IM_END":'+str(IM_END)+', "FILENAME":"'+str(filename)+'" }'

with open(filename+".conf", "w") as file:
    file.write(str(code))
print()
print("Configuration of the current image:")
print(str(code))

with open("latest.log", "w") as file:
    for i in DEBUG:
        file.write(str(i)+"\n")
print("Debug file writed!")