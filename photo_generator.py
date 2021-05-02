from PIL import Image, ImageDraw

img = Image.open('clean_mars_low.png') #3000x1953
draw = ImageDraw.Draw(img)
import time

rad = 30
x_null = 8192 // 2
y_null = 4096 // 2
x_one_degree_in_px = 8192 // 360
y_one_degree_in_px = 4096 // 180
rad = 30

def photo_generator(user_id,x_degree, y_degree):
    draw.ellipse((x_null + x_degree * x_one_degree_in_px - rad, y_null - y_degree * y_one_degree_in_px - rad,
                  x_null + x_degree * x_one_degree_in_px + rad, y_null - y_degree * y_one_degree_in_px + rad),
                 fill='green')
    img.save(f'{user_id}.png')
start = time.time()