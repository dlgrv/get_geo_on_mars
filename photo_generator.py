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
ava_size = (164, 164)

def create_geotag(uid):
    img = Image.open(f'./users_profile_photos/{uid}.jpg')
    out = img.resize(ava_size)
    out.save(f'./users_profile_photos/{uid}.jpg')
    img = Image.open()


def photo_generator(user_id,x_degree, y_degree):
    draw.ellipse((x_null + x_degree * x_one_degree_in_px - rad, y_null - y_degree * y_one_degree_in_px - rad,
                  x_null + x_degree * x_one_degree_in_px + rad, y_null - y_degree * y_one_degree_in_px + rad),
                 fill='green')
    img.save(f'{user_id}.png')

create_geotag(824956847)