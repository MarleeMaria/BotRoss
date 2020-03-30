import cv2
import argparse
import math
import progressbar
import numpy as np


from pointillism import *

# from gui import StartGUI

# GLOBAL PARAMETERS
MIN_HEIGHT_CM = 10
MIN_WIDTH_CM = 10
MAX_HEIGHT_CM = 25
MAX_WIDTH_CM = 25
MIN_STROKE = 1
STROKE_FACTOR = 0.5
STROKE_LENGTH = 5
PIXELS_PER_CM = 50 # used in preview, do not set over 100 due to high processing time

parser = argparse.ArgumentParser(description='...')
parser.add_argument('--palette-size', default=20, type=int, help="Number of colors of the base palette")
# parser.add_argument('--stroke-scale', default=0, type=int, help="Scale of the brush strokes (0 = automatic)")
parser.add_argument('--gradient-smoothing-radius', default=0, type=int, help="Radius of the smooth filter applied to the gradient (0 = automatic)")
parser.add_argument('--limit-image-size', default=0, type=int, help="Limit the image size (0 = no limits)")
# parser.add_argument('--canvas-width', default=-1, type=int, help="Limit the canvas width (cm) (unspecified = scales to fit)")
# parser.add_argument('--canvas-height', default=-1, type=int, help="Limit the canvas height (cm) (unspecified = scales fully)")
# parser.add_argument('img_path', nargs='?', default="images/lake.jpg")

args = parser.parse_args()

class Stroke:
    def __init__(self, start_x, start_y, end_x, end_y, color_well):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color_well = color_well

def sort_strokes(strokes):
    min_stroke = min(strokes, key=lambda x: (x.color_well, x.start_x))
    sorted_strokes = [min_stroke]
    n = len(strokes) - 1
    strokes.remove(min_stroke)
    while n > 0:
        current = sorted_strokes[-1]
        nxt = min(strokes, key=lambda x: (x.color_well, math.pow((x.start_x - current.end_x),2) + math.pow((x.start_y - current.end_y),2)))
        sorted_strokes.append(nxt)
        strokes.remove(nxt)
        n -= 1
    return sorted_strokes


class mainRun:
    # @classmethod
    def run(self, brush, width, height, colors, file):
        res_path = file.rsplit(".", -1)[0] + "_drawing.jpg"
        img = cv2.imread(file)

        if args.gradient_smoothing_radius == 0:
            gradient_smoothing_radius = int(round(max(img.shape) / 100))
            print("Automatically chosen gradient smoothing radius: %d" % gradient_smoothing_radius)
        else:
            gradient_smoothing_radius = args.gradient_smoothing_radius

        if args.limit_image_size > 0:
            img = limit_size(img, args.limit_image_size)

        if brush == 0:
            stroke_scale = int(math.ceil(max(img.shape) / 1000))
            print("Automatically chosen stroke scale: %d" % stroke_scale)
        else:
            stroke_scale = brush

        # determine what the max size of the image is relative to real dimensions
        if height > MAX_HEIGHT_CM or (height < MIN_HEIGHT_CM  and height != -1) or width > MAX_WIDTH_CM or (width < MIN_WIDTH_CM and width != -1):
            print("Invalid canvas dimensions. Resetting to defaults.") #TODO: more descriptive error
            height = -1
            width = -1

        while width == -1 or height == -1:
            # height and width are both unspecified
            if height == -1 and width == -1:
                if img.shape[0] >= img.shape[1]:
                    height = 30
                else:
                    width = 30
            elif height == -1:
                height = img.shape[0] / img.shape[1] * width
                if height > MAX_HEIGHT_CM or gui.height < MIN_HEIGHT_CM:
                    print("Invalid canvas dimensions. Resetting to defaults.")
                    if height > MAX_HEIGHT_CM:
                        height = MAX_HEIGHT_CM
                    elif height < MIN_HEIGHT_CM:
                        height = MIN_HEIGHT_CM
                    width = -1
            elif width == -1:
                width = img.shape[1] / img.shape[0] * height
                if width > MAX_WIDTH_CM or width < MIN_WIDTH_CM:
                    print("Invalid canvas dimensions. Resetting to defaults.")
                    if width > MAX_WIDTH_CM:
                        width = MAX_WIDTH_CM
                    elif width < MIN_WIDTH_CM:
                        width = MIN_WIDTH_CM
                    height = -1

        HEIGHT_CM = height
        WIDTH_CM = width

        print("Your height is %f cm" % HEIGHT_CM)
        print("Your width is %f cm" % WIDTH_CM)


        # convert the image to grayscale to compute the gradient
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        print("Computing color palette...")
        palette = ColorPalette.from_image(img, args.palette_size, colors)

        #add back in the
        # print("Extending color palette...")
        # palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])

        # display the color palette
        # cv2.imshow("palette", palette.to_image())
        # cv2.waitKey(200)

        print("Computing gradient...")
        gradient = VectorField.from_gradient(gray)

        print("Smoothing gradient...")
        gradient.smooth(gradient_smoothing_radius)

        print("Drawing image...")
        # create a "cartonized" version of the image to use as a base for the painting
        #res = cv2.medianBlur(img, 11)

        #create black blank image
        blank_image = np.zeros((img.shape[0],img.shape[0],3), np.uint8)
        res = cv2.medianBlur(blank_image, 11)

        #fill blank image with white
        res.fill(255)

        # define a randomized grid of locations for the brush strokes
        grid = randomized_grid(img.shape[0], img.shape[1], gradient, scale=50)
        batch_size = 10000

        output_file = open("output.txt","w+")
        bar = progressbar.ProgressBar()

        # get list of strokes
        strokes = []
        color_tuple_to_well = {tuple(color): well for well, color in enumerate(colors)}

        #print(colorList)
        for h in bar(range(0, len(grid), batch_size)):

            # get the pixel colors at each point of the grid
            pixels = np.array([img[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])

            # precompute the probabilities for each color in the palette
            # lower values of k means more randomnes
            color_probabilities = compute_color_probabilities(pixels, palette, k=200)

            for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):

                # select color
                color = color_select(color_probabilities[i], palette)
                if color == [255, 255, 255]:
                    continue

                # calculate length and angle
                angle = math.degrees(gradient.direction(y, x)) + 90
                length = int(round(MIN_STROKE + math.sqrt(STROKE_LENGTH* gradient.magnitude(y, x))))

                # calculate start and end points
                start_x = (length / 2 * math.cos(math.radians(angle)) + x) / img.shape[1] * WIDTH_CM
                start_y = (length / 2 * math.sin(math.radians(angle)) + y) / img.shape[0] * HEIGHT_CM + (MAX_HEIGHT_CM - HEIGHT_CM)
                end_x  = (length / 2 * math.cos(math.radians(angle) + math.pi) + x) / img.shape[1] * WIDTH_CM
                end_y = (length / 2 * math.sin(math.radians(angle) + math.pi) + y) / img.shape[0] * HEIGHT_CM + (MAX_HEIGHT_CM - HEIGHT_CM)

                # hacky preview solution for previews
                start_x_preview = (length / 2 * math.cos(math.radians(angle)) + x)
                start_y_preview = (length / 2 * math.sin(math.radians(angle)) + y)
                end_x_preview  = (length / 2 * math.cos(math.radians(angle) + math.pi) + x)
                end_y_preview = (length / 2 * math.sin(math.radians(angle) + math.pi) + y)

                # guards
                if start_x < 0:
                    start_x = 0
                elif start_x > WIDTH_CM:
                    start_x = WIDTH_CM
                if start_y < (MAX_HEIGHT_CM - HEIGHT_CM):
                    start_y = MAX_HEIGHT_CM - HEIGHT_CM
                elif start_y > MAX_HEIGHT_CM:
                    start_y = MAX_HEIGHT_CM
                if end_x < 0:
                    end_x = 0
                elif end_x > WIDTH_CM:
                    end_x = WIDTH_CM
                if end_y < (MAX_HEIGHT_CM - HEIGHT_CM):
                    end_y = MAX_HEIGHT_CM - HEIGHT_CM
                elif end_y > MAX_HEIGHT_CM:
                    end_y = MAX_HEIGHT_CM

                # Round to nearest millimetre for output file purposes
                start_x_rounded = round(start_x, 1)
                start_y_rounded = round(MAX_HEIGHT_CM - start_y, 1)
                end_x_rounded = round(end_x, 1)
                end_y_rounded = round(MAX_HEIGHT_CM - end_y, 1)

                # calculate points for drawing preview
                # start_point = round(start_x * PIXELS_PER_CM), round(start_y * PIXELS_PER_CM)
                # end_point = round(end_x * PIXELS_PER_CM), round(end_y * PIXELS_PER_CM)
                start_point = round(start_x_preview), round(start_y_preview)
                end_point = round(end_x_preview), round(end_y_preview)

                # sketch preview
                cv2.line(res, (start_point), (end_point), color, stroke_scale)

                # append stroke to list
                strokes.append(Stroke(start_x_rounded, start_y_rounded, end_x_rounded, end_y_rounded, color_tuple_to_well[tuple(color)]))

        strokes = sort_strokes(strokes)

        for stroke in strokes:
            output_file.write("{},{},{},{},{}\n".format(stroke.start_x, stroke.start_y, stroke.end_x, stroke.end_y, stroke.color_well))

        output_file.write("#")
        output_file.close()
        # cv2.imshow("res", limit_size(res, 1080))
        cv2.imwrite(res_path, res)
        cv2.waitKey(0)
