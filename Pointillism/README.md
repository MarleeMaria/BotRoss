![example](images/landscape_drawing.jpg)

# Pointillism
This repo contains a python application that converts a photo to a pointillist painting.

You can find informations about the algorithm [here](https://medium.com/@matteoronchetti/https-medium-com-matteoronchetti-pointillism-with-python-and-opencv-f4274e6bbb7b)

## Installation
```
cd Pointillism
pip3 install -r requirements.txt
python3 main.py images/landscape.jpg --palette-size=20 --stroke-scale=10 --gradient-smoothing-radius=20
```

YOU ALSO NEED FOR GUI:
python3 -m pip install Pillow

# How to use GUI
find picture
choose colour or b/w
B/W: hit submit and watch her go
COLOUR:
select the number of colours
select each colour (ONE BY ONE)
DO NOT HIT SUBMIT
Close??? the interface???

# Known errors:
Errors say that the canvas size is always changed.....
