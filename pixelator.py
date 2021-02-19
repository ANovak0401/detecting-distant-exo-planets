import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

files = ['earth_west.png', 'earth_east.png']

for file in files:
    img_ini = cv.imread(file)  # initialise file by reading it with imread
    pixelated = cv.resize(img_ini, (3, 3), interpolation=cv.INTER_AREA)  # create 3x3 pixelated image
    img = cv.resize(pixelated, (300, 300), interpolation=cv.INTER_AREA)  # bring resolution back to 300 by 300
    cv.imshow('Pixelated {}'.format(file), img)  # show image on screen
    cv.waitKey(2000)  # keep up for 2 seconds

    b, g, r = cv.split(pixelated)  # break out primary color channels
    color_aves = []  # list for color averages
    for array in (b, g, r):
        color_aves.append(np.average(array))  # average colors and add to list

    labels = "Blue", 'Green', 'Red'  # labels for pie chart
    colors = ['blue', 'green', 'red']  # colors used in chart
    fig, ax = plt.subplots(figsize=(3.5, 3.3))  # size in inches
    _, _, autotexts = ax.pie(color_aves,  # create pie chart with color aves as data
                             labels=labels,  # set labels
                             autopct='%1.1f%%',  # set autopct to show numbers with one decimal point
                             colors=colors)  # set colors of chart
    for autotext in autotexts:
        autotext.set_color('white')  # set background color to white
    plt.title('{}\n'.format(file))  # add title to chart

plt.show()  # show chart
