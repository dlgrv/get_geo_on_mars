from PIL import Image, ImageDraw
from math import sqrt
from attractions import attractions
import db

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


def search_nearest_attraction(uid, gradus_x, gradus_y):
    lang = db.get_language(uid)[0]
    min_distance = 9999999
    for attraction_id in attractions[lang]:
        distance = sqrt((gradus_x-attractions[lang][attraction_id][2][0])**2 +
                        (gradus_y-attractions[lang][attraction_id][2][1])**2)
        if distance < min_distance:
            min_distance = distance
            nearest_attraction_id = attraction_id
    save_user_attractions(uid, nearest_attraction_id, gradus_x, gradus_y)
    return nearest_attraction_id


def save_user_attractions(uid, nearest_attraction_id, gradus_x, gradus_y):
    attractions_list = db.get_attractions(uid)[0].split()
    nearest_attraction_id = str(nearest_attraction_id)
    if nearest_attraction_id not in attractions_list:
        attractions_list.append(nearest_attraction_id)
    attractions_str = ' '.join(map(str, attractions_list))
    db.update_attractions(uid, attractions_str)
    drawing_not_nearest_attractions(uid, nearest_attraction_id, attractions_list, gradus_x, gradus_y)


def drawing_not_nearest_attractions(uid, nearest_attraction_id, attractions_list, gradus_x, gradus_y):
    map = Image.open('./clean_mars_low.png')
    pin_2 = Image.open('./pattern/pin_2.png') # 89x161
    x_centre = 1500
    y_centre = 975
    for attractions_id in attractions_list:
        if attractions_id != nearest_attraction_id:
            attraction_coord_x = attractions['rus'][int(attractions_id)][2][0]
            attraction_coord_y = attractions['rus'][int(attractions_id)][2][1]
            attraction_coord_ypx = int(888 * 4 / 360 * attraction_coord_y)
            attraction_coord_xpx = int((1450 / 360 * attraction_coord_x * 2) * sqrt(1 - (attraction_coord_ypx / 960) ** 2))
            paste_pin_coord = (x_centre + attraction_coord_xpx - 45, y_centre - attraction_coord_ypx - 161)
            map.paste(pin_2, paste_pin_coord, pin_2)
    map.save(f'./ready_map_for_user/{uid}.png')
    drawing_geotag(uid, nearest_attraction_id, gradus_x, gradus_y)


def drawing_geotag(uid, nearest_attraction_id, gradus_x, gradus_y):
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
    if ypx + y_size_geotag >= y_centre:
        over_edge_img = Image.open(f'./ready_map_for_user/{uid}.png') #3000x1953
        map = Image.new('RGB', (3000, 1953 + 2*(ypx + y_size_geotag - y_centre) + 4), (0, 0, 0))
        y_offset = ypx + y_size_geotag - y_centre
        paste_coord = (x_centre + xpx - (x_size_geotag // 2), y_centre - ypx + 5 - y_size_geotag + y_offset)
        map.paste(over_edge_img, (0, y_offset))
    else:
        map = Image.open(f'./ready_map_for_user/{uid}.png') # 3000x1953
        paste_coord = (x_centre + xpx - (x_size_geotag // 2), y_centre - ypx - y_size_geotag)
    map.paste(img, paste_coord, img)
    map.save(f'./ready_map_for_user/{uid}.png')
    drawing_nearest_attraction(uid, nearest_attraction_id)


def drawing_nearest_attraction(uid, nearest_attraction_id):
    map = Image.open(f'./ready_map_for_user/{uid}.png')
    map_size = map.size
    x_centre, y_centre = map_size[0] // 2, map_size[1] // 2
    pin_1 = Image.open('./pattern/pin_1.png')
    attraction_coord_x = attractions['rus'][int(nearest_attraction_id)][2][0]
    attraction_coord_y = attractions['rus'][int(nearest_attraction_id)][2][1]
    attraction_coord_ypx = int(888 * 4 / 360 * attraction_coord_y)
    attraction_coord_xpx = int((1450 / 360 * attraction_coord_x * 2) * sqrt(1 - (attraction_coord_ypx / 960) ** 2))
    paste_pin_coord = (x_centre + attraction_coord_xpx - 45, y_centre - attraction_coord_ypx - 161)
    map.paste(pin_1, paste_pin_coord, pin_1)
    map.save(f'./ready_map_for_user/{uid}.jpg')


#search_nearest_attraction(824956847, 37.656808, 55.822001)