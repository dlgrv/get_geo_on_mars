from PIL import Image, ImageDraw

img = Image.open('photo_mars.jpg') #8192x4096
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
start = time.time()
photo_generator(000, 37.656746, 55.821996)

img.show()
print(time.time()-start)