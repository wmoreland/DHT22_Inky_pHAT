import time
import inky
import board
import datetime
import numpy as np
import adafruit_dht
from PIL import Image, ImageDraw, ImageFont


# Function to convert temperature to pixel position
def convert_T(x):
    return int(round((59 - ((x - 10) * (59 / 20))) + 15))


# Function to convert temperature to pixel position
def convert_H(x):
    return int(round((59 - (x * (59 / 100))) + 15))


# Function to measure mean T and H
def measure_mean(time_period=10):
    wait_time = 2
    time_passed = 0
    T_list = np.array([])
    H_list = np.array([])

    while time_passed < time_period:
        time_passed += wait_time

        try:
            T_list = np.append(T_list, dht.temperature)
            H_list = np.append(H_list, dht.humidity)
        except RuntimeError as e:
            print("Reading from DHT failure: ", e.args)
        time.sleep(wait_time)
    try:
        T_mean = T_list.mean()
        H_mean = H_list.mean()
    except:
        print('Error')
    return T_mean, H_mean


# Function to create plot
def draw_plot():
    # Axis titles
    font = ImageFont.truetype(fontname, 12)
    draw.text((5, 24), 'T', black, font)
    draw.text((195, 24), 'H', black, font)

    # Y-axis (temperature)
    font = ImageFont.truetype(fontname, 10)
    draw.line([(34, 15), (34, 75)], width=1, fill=black)
    for y in [15, 45, 75]:
        draw.line([(30, y), (34, y)], width=1, fill=black)
    for y, message in zip([9, 39, 69], ['30', '20', '10']):
        draw.text((15, y), message, black, font)

    # Y-axis (humidity)
    draw.line([(178, 15), (178, 75)], width=1, fill=black)
    for y in [15, 27, 38, 50, 62, 75]:
        draw.line([(178, y), (182, y)], width=1, fill=black)
    draw.text((185, 69), '0', black, font)
    draw.text((185, 9), '100', black, font)

    # X-axis
    draw.line([(34, 75), (178, 75)], width=1, fill=black)
    for x in [34, 46, 58, 70, 82, 94, 106, 118, 130, 142, 154, 166, 178]:
        draw.line([(x, 75), (x, 79)], width=1, fill=black)

    # Clean the plot area
    for x in np.arange(35, 178, 1):
        for y in np.arange(15, 74, 1):
            img.putpixel((x, y), white)

    # Add today's date as title
    message = datetime.datetime.now().strftime('%d %B %Y')
    font = ImageFont.truetype(fontname, 15)
    w, h = font.getsize(message)
    x = (inkyphat.WIDTH / 2) - (w / 2)
    draw.text((x, 0), message, black, font)

    inkyphat.set_image(img)
    inkyphat.show()


# Function to update data
def arrange_data(T, H, T_list_plot, H_list_plot):
    T_list_plot = np.delete(T_list_plot, 0)
    T_list_plot = np.append(T_list_plot, T)
    H_list_plot = np.delete(H_list_plot, 0)
    H_list_plot = np.append(H_list_plot, H)
    return T_list_plot, H_list_plot


# Function to plot the temperature and humidity data
def plot_data(T_list_plot, H_list_plot):
    x_coordinate = np.arange(35, 178, 1)
    h_coordinate = [convert_H(h) for h in H_list_plot]
    h_points = []
    for x, h in zip(x_coordinate, h_coordinate):
        if h < 74:
            h_points.append((x, h))
    t_coordinate = [convert_T(t) for t in T_list_plot]
    t_points = []
    for x, t in zip(x_coordinate, t_coordinate):
        if t < 74:
            t_points.append((x, t))

    if len(h_points) > 1:
        draw.line(h_points, fill=black, width=1)
        draw.line(t_points, fill=red, width=1)
    else:
        img.putpixel(h_points[0], black)
        img.putpixel(t_points[0], red)

    inkyphat.set_image(img)
    inkyphat.show()


# Initialise the inky phat
inkyphat = inky.InkyPHAT('red')
inkyphat.set_border(inky.BLACK)
img = Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
draw = ImageDraw.Draw(img)
fontname = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
dht = adafruit_dht.DHT22(board.D4)
white = 0
black = 1
red = 2
T_list_plot = np.zeros_like(np.arange(143))
H_list_plot = np.zeros_like(np.arange(143))

while True:
    print("*** Measuring the average temperature and humidity ***")
    T, H = measure_mean()

    print("*** Arranging the data ***")
    T_list_plot, H_list_plot = arrange_data(T, H, T_list_plot, H_list_plot)

    print("*** Drawing the graph ***")
    draw_plot()

    print("*** Plotting the data ***")
    plot_data(T_list_plot, H_list_plot)

    print("*** Sleep... ***")
    time.sleep(10)
