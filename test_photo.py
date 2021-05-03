from PIL import Image, ImageDraw

img = Image.open('clean_mars_low.png')
draw = ImageDraw.Draw(img)
from math import sqrt, trunc, ceil

rad = 2
colour = 'red'
#centre_x=1500 y=975
x = 1500
y = 975
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)
# centre right
x = 2950
y = 975
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)
# centre left
x = 50
y = 975
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)
# centre bottom
x = 1500
y = 1860
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)
# centre top
x = 1500
y = 90
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)

# left top corner
x = 935
y = 90
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)

# left bottom corner
x = 935
y = 1860
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)

# right top corner
x = 2065
y = 90
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)

# right bottom corner
x = 2065
y = 1860
draw.ellipse((x-rad, y-rad, x+rad, y+rad),
           fill=colour)
#centre_x=1500 y=975
x_centre = 1500
y_centre = 975
max_x = 1450
a = 1450
b = 960
x = 180
y = 180
#x = 37.656808
#y = 55.822001
xpx = x * 8.056
ypx = y * 5.195
gradus_x = 37.656808
gradus_y = 55.822001
a = int(a / 360 * gradus_x * 2)


for x in range(-a, a+1):
    ypx = b * (sqrt(1 - ((x / a)**2)))
    xpx = x
    #y = int(b * (sqrt(1-((xpx / a)**2))))
    draw.ellipse((x_centre + xpx - rad, y_centre - ypx - rad, x_centre + xpx + rad, y_centre - ypx + rad),
                 fill='red')
    draw.ellipse((x_centre + xpx - rad, y_centre + ypx - rad, x_centre + xpx + rad, y_centre + ypx + rad),
                 fill='red')

b = -int(b * 4 / 360 * gradus_y)
a = 1450
for i in range(-a, a):
    draw.ellipse((x_centre + i - rad, y_centre + b - rad, x_centre + i + rad, y_centre + b + rad),
                 fill='blue')

rad = 10
ypx = -int(960 * 4 / 360 * gradus_y)
xpx = (1450 / 360 * gradus_x * 2) * sqrt(1 - (ypx/960)**2)
draw.ellipse((x_centre + xpx - rad, y_centre + ypx - rad, x_centre + xpx + rad, y_centre + ypx + rad),
                 fill='yellow')



'''
x = 360
a = 1450
a = int((a / 180) * x)
print(a, '!!!!!!!!!!!!!!!!!!')
offset = 0
for x in range(-a, a+1):
    ypx = b * (sqrt(1 - ((x / a)**2)))
    xpx = x
    #y = int(b * (sqrt(1-((xpx / a)**2))))
    draw.ellipse((x_centre + xpx - rad, y_centre - ypx - rad, x_centre + xpx + rad, y_centre - ypx + rad),
                 fill='green')
    draw.ellipse((x_centre + xpx - rad, y_centre + ypx - rad, x_centre + xpx + rad, y_centre + ypx + rad),
                 fill='green')
'''

img.show()