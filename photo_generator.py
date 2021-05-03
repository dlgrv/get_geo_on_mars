from PIL import Image, ImageDraw
from math import sqrt

rad = 30
x_null = 8192 // 2
y_null = 4096 // 2
x_one_degree_in_px = 8192 // 360
y_one_degree_in_px = 4096 // 180

def ava_resize(uid):
    ava_size = (164, 164)
    ava = Image.open(f'./users_profile_photos/{uid}.jpg')
    ava = ava.resize(ava_size)
    ava.save(f'./users_profile_photos/{uid}.jpg')

def create_map_with_geotag(uid, gradus_x, gradus_y):
    try:
        ava = Image.open(f'./users_profile_photos/{uid}.jpg')
    except Exception as e:
        ava = Image.open(f'./users_profile_photos/default_ava.jpg')
    img = Image.open('./pattern/empty_list.png')
    img.paste(ava, (40, 40))
    geotag = Image.open('./pattern/geotag.png')
    img.paste(geotag, (0, 0), geotag)
    ypx = int(888 * 4 / 360 * gradus_y)
    xpx = int((1450 / 360 * gradus_x * 2) * sqrt(1 - (ypx / 960) ** 2))
    x_centre = 1500
    y_centre = 975
    x_size_geotag = 244
    y_size_geotag = 326
    print(ypx, y_size_geotag, y_centre)
    if ypx + y_size_geotag >= y_centre:
        over_edge_img = Image.open('./clean_mars_low.png') #3000x1953
        map = Image.new('RGB', (3000, 1953 + 2*(ypx + y_size_geotag - y_centre) + 4), (0, 0, 0))
        y_offset = ypx + y_size_geotag - y_centre
        paste_coord = (x_centre + xpx - (x_size_geotag // 2), y_centre - ypx + 5 - y_size_geotag + y_offset)
        map.paste(over_edge_img, (0, y_offset))
    else:
        map = Image.open('./clean_mars_low.png') # 3000x1953
        paste_coord = (x_centre + xpx - (x_size_geotag // 2), y_centre - ypx - y_size_geotag)
    map.paste(img, paste_coord, img)
    map.save(f'./ready_map_for_user/{uid}.jpg')

gradus_x = 37.656808
gradus_y = 55.822001