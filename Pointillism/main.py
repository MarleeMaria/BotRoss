import cv2
import argparse
import math
import progressbar
import numpy as np
from pointillism import *

parser = argparse.ArgumentParser(description='...')
parser.add_argument('--palette-size', default=20, type=int, help="Number of colors of the base palette")
parser.add_argument('--stroke-scale', default=0, type=int, help="Scale of the brush strokes (0 = automatic)")
parser.add_argument('--gradient-smoothing-radius', default=0, type=int, help="Radius of the smooth filter applied to the gradient (0 = automatic)")
parser.add_argument('--limit-image-size', default=0, type=int, help="Limit the image size (0 = no limits)")
parser.add_argument('img_path', nargs='?', default="images/lake.jpg")

args = parser.parse_args()

res_path = args.img_path.rsplit(".", -1)[0] + "_drawing.jpg"
img = cv2.imread(args.img_path)

if args.limit_image_size > 0:
    img = limit_size(img, args.limit_image_size)

if args.stroke_scale == 0:
    stroke_scale = int(math.ceil(max(img.shape) / 1000))
    print("Automatically chosen stroke scale: %d" % stroke_scale)
else:
    stroke_scale = args.stroke_scale

if args.gradient_smoothing_radius == 0:
    gradient_smoothing_radius = int(round(max(img.shape) / 50))
    print("Automatically chosen gradient smoothing radius: %d" % gradient_smoothing_radius)
else:
    gradient_smoothing_radius = args.gradient_smoothing_radius

# convert the image to grayscale to compute the gradient
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print("Computing color palette...")
palette = ColorPalette.from_image(img, args.palette_size)

# print("Extending color palette...")
# palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])

# display the color palette
#____Commented out so i dont have to see it each time____
cv2.imshow("palette", palette.to_image())
cv2.waitKey(200)

print("Computing gradient...")
gradient = VectorField.from_gradient(gray)

print("Smoothing gradient...")
gradient.smooth(gradient_smoothing_radius)

print("Drawing image...")
# create a "cartonized" version of the image to use as a base for the painting
#res = cv2.medianBlur(img, 11)

#create black blank image
blank_image = np.zeros((img.shape[0], img.shape[1],3), np.uint8)
res = cv2.medianBlur(blank_image, 11)
#fill blank image with white
res.fill(255)

# define a randomized grid of locations for the brush strokes
#LOOOK HERE FUCK WITH THE SCALE
grid = randomized_grid(img.shape[0], img.shape[1], scale=10)
batch_size = 10000

output_file = open("output.txt","w+")
bar = progressbar.ProgressBar()
for h in bar(range(0, len(grid), batch_size)):

    # get the pixel colors at each point of the grid
    pixels = np.array([img[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])

    # precompute the probabilities for each color in the palette
    # lower values of k means more randomnes
    color_probabilities = compute_color_probabilities(pixels, palette, k=200)

    for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):
        #Get colour bellow?
        color = color_select(color_probabilities[i], palette)
        #prints out RBG values for each strokes
        #print(color)
        angle = math.degrees(gradient.direction(y, x)) + 90
        length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))

        # calculate start and end points
        start_point = round(length / 2 * math.cos(math.radians(angle)) + x), round(length / 2 * math.sin(math.radians(angle)) + y)
        end_point  = round(length / 2 * math.cos(math.radians(angle) + math.pi) + x), round(length / 2 * math.sin(math.radians(angle) + math.pi) + y)

        # write to output file
        output_file.write("{}, {}, {}\n".format(str(start_point), str(end_point), str(color)))
        # draw the brush stroke
        cv2.ellipse(res, (x, y), (length, stroke_scale), angle, 0, 360, color, -1, cv2.LINE_AA)
        #append to text file...

        #these are the center x,y's for the start/end of the rectangle
        start_x = length / 2 * math.cos(math.radians(angle)) + x
        start_y = length / 2 * math.sin(math.radians(angle)) + y
        end_x = length / 2 * math.cos(math.radians(angle) + math.pi) + x
        end_y = length / 2 * math.sin(math.radians(angle) + math.pi) + y

        hheight = (start_x - end_x)/2
        hwidth = (start_y - end_y)/2

        #corner points for rect.
        tl_xy = (round(start_x+hheight), round(start_y+hwidth))
        br_xy = (round(end_x-hheight),round(end_y-hwidth))

        #b_code.write("%s, %s %s\n" % (tl_xy,br_xy,color))
        #output_file.write("{}, {}, {}\n".format(str(start_point), str(end_point), str(color)))
        #change into a rect call
        # cv2.rectangle(res, (tl_xy), (br_xy), color, -1)
        # cv2.rectangle(res, (start_point), (end_point), color, -1)

#b_code.close()
cv2.imshow("res", limit_size(res, 1080))
cv2.imwrite(res_path, res)
cv2.waitKey(0)
