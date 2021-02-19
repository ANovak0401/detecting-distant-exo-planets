import math
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# constants
IMG_HT = 400
IMG_WIDTH = 500
BLACK_IMG = np.zeros((IMG_HT, IMG_WIDTH, 1), dtype='uint8')  # opencv uses numpy arrays as the image format
STAR_RADIUS = 165
EXO_RADIUS = 7
EXO_DX = 3
EXO_START_X = 40
EXO_START_Y = 230
NUM_FRAMES = 145


def main():
    intensity_samples = record_transit(EXO_START_X, EXO_START_Y)  # create list of measured light intensities
    print('intensity sample complete')
    relative_brightness = calc_rel_brightness(intensity_samples)  # intensity relative to maximum intensity
    print("relative brightness complete")
    print('\nestimated exoplanet radius = {:.2f}\n'
          .format(STAR_RADIUS * math.sqrt(max(relative_brightness)
                                          - min(relative_brightness))))  # print radius of detected planet
    plot_light_curve(relative_brightness)  # plot light curve with matplotlib
    print('plot complete')


def record_transit(exo_x, exo_y):
    """Draw planet transiting star and return list of intensity changes."""
    intensity_samples = []  # list for intensity measurements
    for _ in range(NUM_FRAMES):  # for entry based on number of frames
        temp_img = BLACK_IMG.copy()  # create temp image
        cv.circle(temp_img, (int(IMG_WIDTH / 2), int(IMG_HT / 2)),
                  STAR_RADIUS, 255, -1)  # draw circle te represent star
        cv.circle(temp_img, (exo_x, exo_y), EXO_RADIUS, 0, -1)  # draw circle representing exo planet
        intensity = temp_img.mean()  # get light intensity from frame
        cv.putText(temp_img, 'Mean intensity = {}'.format(intensity), (5, 390),
                   cv.FONT_HERSHEY_PLAIN, 1, 255)  # title for image
        cv.imshow('Transit', temp_img)  # show image
        cv.waitKey(30)  # keep window for 30 seconds
        intensity_samples.append(intensity)  # add intensity to the list of samples
        exo_x += EXO_DX  # advance exoplanet circle by constant
    return intensity_samples  # return the samples list


def calc_rel_brightness(intensity_samples):
    """Return list of relative brightness from list of intensity values."""
    rel_brightness = []  # list for relative brightness values
    max_brightness = max(intensity_samples)  # find brightest sample from group
    for intensity in intensity_samples:  # for each entry in list
        rel_brightness.append(intensity / max_brightness)  # add intensity divided by max brightness
    return rel_brightness  # return of function


def plot_light_curve(rel_brightness):
    """Plot changes in relative brightness vs. time."""
    plt.plot(rel_brightness, color='red', linestyle='dashed',
             linewidth=2, label='Relative Brightness')  # create pyplot plot
    plt.legend(loc='upper center')  # create legend for plot
    plt.title('Relative Brightness vs. Time')  # create title for plot
    plt.show()  # show plot


if __name__ == '__main__':
    main()
