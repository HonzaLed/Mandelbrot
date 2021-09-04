from PIL import Image, ImageDraw
from mandelbrot import mandelbrot

import progressbar

MAX_ITER = 200

# Image size (pixels)
WIDTH = 600
HEIGHT = 400

# Plot window
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1

palette = []

log = []

im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

for x in progressbar.progressbar(range(0, WIDTH)):
#for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        m = mandelbrot(c)
        # The color depends on the number of iterations
        color = 255 - int(m * 255 / MAX_ITER)

        #if m == MAX_ITER:
            #color = 255
        #else:
        #    color = 0
        
        #print("Matched: ",x,y)
        #print(m)
        #print(color)

        #with open("latest.log", "a") as file:
        #    file.write(str(m))
        log.append(m)

        # Plot the point
        draw.point([x, y], (color, color, color))

im.save('output-bw.png', 'PNG')
print("BW image successfully generated!")

file = open("latest.log", "a")
for i in progressbar.progressbar(log):
    file.write(str(i)+"\n")