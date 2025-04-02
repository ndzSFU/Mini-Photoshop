import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import math

imageDisplay = None
ogImage = None
grayImageDisplay = None
grayscaleImage = None

BayerMatrix = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ])

#Normalized the values to 0-255
for i in range(4):
    for j in range(4):
        BayerMatrix[i, j] = (BayerMatrix[i, j] * 255) / 16

def open_and_display_bmp():
    #Allows the global var to be changed by this function
    global imageDisplay, ogImage

    # Open the file dialog when the button is clicked
    filePath = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
    
    ogImage = Image.open(filePath, mode = 'r')

    # Convert the image to the tkinter image format, so we can use the tkinter cnavas to display the img
    imageDisplay = ImageTk.PhotoImage(ogImage)

    # Clear the canvas before displaying a new image
    canvas.delete("all")

    #Display image on the now clear canvas
    #Set canvas width and height to max posssible proportions of the image
    canvas.config(width=(ogImage.width*2), height=ogImage.height) 
    canvas.create_image(0, 0, anchor=tk.NW, image=imageDisplay)
    #canvas.pack()

def make_grayscaled_image():
    global grayImageDisplay, grayscaleImage

    grayscaleImage = Image.new("RGB", ogImage.size)

    pixels = grayscaleImage.load()
    ogPixles = ogImage.load()

    for x in range(ogImage.width):
        for y in range(ogImage.height):
            R, G, B = ogPixles[x, y]
            luminance = int(0.299 * R + 0.587 * G + 0.114 * B)
            
            pixels[x, y] = (luminance, luminance, luminance)

    grayImageDisplay = ImageTk.PhotoImage(grayscaleImage)

def show_grayscale():

    make_grayscaled_image()

    canvas.delete("all")
    
    canvas.create_image(0, 0, anchor=tk.NW, image=imageDisplay)

    canvas.create_image(ogImage.width, 0, anchor=tk.NW, image=grayImageDisplay)

def make_ordered_dither_image():
    global orderedDitherImage, orderedDitherDisplay

    orderedDitherImage = Image.new("L", ogImage.size)

    pixels = orderedDitherImage.load()
    ogPixels = ogImage.load()

    for x in range(grayscaleImage.width):
        for y in range(grayscaleImage.height):
            # Get the grayscale value of the pixel at (x, y)
            lum = (ogPixels[x, y])[0] #returns the L value

            i = x % 4
            j = y % 4

            threshold = BayerMatrix[i , j]

            if (lum > threshold):
                pixels[x, y] = 255  
            else:
                pixels[x, y] = 0    
    
    orderedDitherDisplay = ImageTk.PhotoImage(orderedDitherImage)


def show_ordered_dither():

    make_grayscaled_image()

    canvas.delete("all")

    canvas.create_image(0, 0, anchor=tk.NW, image=grayImageDisplay)

    make_ordered_dither_image()

    canvas.create_image(ogImage.width, 0, anchor=tk.NW, image=orderedDitherDisplay)

def get_min_max_intensity(channel):
    min_intensity = 256
    max_intensity = -1

    for x in range(ogImage.width):
        for y in range(ogImage.height):
            intensity = channel.getpixel((x, y))

            if intensity < min_intensity:
                min_intensity = intensity
            if intensity > max_intensity:
                max_intensity = intensity

    return max_intensity, min_intensity


def make_auto_leveled():
    global autoLeveledImageDisplay

    leveledChannels = []

    colourChannels = ogImage.split()
    
    for colour in colourChannels:
        maxIntensity, minIntensity = get_min_max_intensity(colour)
        
        leveledChannel = Image.new("L", colour.size)

        for x in range(ogImage.width):
            for y in range(ogImage.height):

                lum = colour.getpixel((x, y))

                if minIntensity != maxIntensity:
                    stretched_value = (lum - minIntensity) * 255 // (maxIntensity - minIntensity)
                    leveledChannel.putpixel((x, y), max(0, min(255, stretched_value)))
                else:
                    leveledChannel.putpixel((x, y), 0)

        leveledChannels.append(leveledChannel)

    autoLeveledImage = Image.merge("RGB", leveledChannels)
    autoLeveledImageDisplay = ImageTk.PhotoImage(autoLeveledImage)

def show_auto_level():
    make_auto_leveled()

    canvas.delete("all")
    
    canvas.create_image(0, 0, anchor=tk.NW, image=imageDisplay)
    canvas.create_image(ogImage.width, 0, anchor=tk.NW, image=autoLeveledImageDisplay)

def make_red_image(type):
    global redImageDisplay, redImage

    redImage = Image.new("RGB", ogImage.size)

    pixels = redImage.load()
    ogPixles = ogImage.load()

    for x in range(ogImage.width):
        for y in range(ogImage.height):
            R, G, B = ogPixles[x, y]
            
            if(type == "add"):
                pixels[x, y] = (255, G, B)
            elif(type == "remove"):
                pixels[x, y] = (0, G, B)

    redImageDisplay = ImageTk.PhotoImage(redImage)

def show_red(type):

    make_red_image(type)

    canvas.delete("all")
    
    canvas.create_image(0, 0, anchor=tk.NW, image=imageDisplay)

    canvas.create_image(ogImage.width, 0, anchor=tk.NW, image=redImageDisplay)

def make_green_image(type):
    global greenImageDisplay, greenImage

    greenImage = Image.new("RGB", ogImage.size)

    pixels = greenImage.load()
    ogPixles = ogImage.load()

    for x in range(ogImage.width):
        for y in range(ogImage.height):
            R, G, B = ogPixles[x, y]
            
            if(type == "add"):
                pixels[x, y] = (R, 255, B)
            elif(type == "remove"):
                pixels[x, y] = (R, 0, B)

    greenImageDisplay = ImageTk.PhotoImage(greenImage)

def show_green(type):

    make_green_image(type)

    canvas.delete("all")
    
    canvas.create_image(0, 0, anchor=tk.NW, image=imageDisplay)

    canvas.create_image(ogImage.width, 0, anchor=tk.NW, image=greenImageDisplay)

def make_blue_image(type):
    global blueImageDisplay, blueImage

    blueImage = Image.new("RGB", ogImage.size)

    pixels = blueImage.load()
    ogPixles = ogImage.load()

    for x in range(ogImage.width):
        for y in range(ogImage.height):
            R, G, B = ogPixles[x, y]
            
            if(type == "add"):
                pixels[x, y] = (R, G, 255)
            elif(type == "remove"):
                pixels[x, y] = (R, G, 0)

    blueImageDisplay = ImageTk.PhotoImage(blueImage)

def show_blue(type):

    make_blue_image(type)

    canvas.delete("all")
    
    canvas.create_image(0, 0, anchor=tk.NW, image=imageDisplay)

    canvas.create_image(ogImage.width, 0, anchor=tk.NW, image=blueImageDisplay)

def make_gamma_corrected(type):
    global GammaImageDisplay, GammaImage

    GammaImage = Image.new("RGB", ogImage.size)

    pixels = GammaImage.load()
    ogPixles = ogImage.load()

    for x in range(ogImage.width):
        for y in range(ogImage.height):
            R,G,B = ogPixles[x, y]

            if(type == "reg"):
                GammaValue = 2.2
            elif(type == "inv"):
                GammaValue = 1.0/2.2

            invRed = int(((R / 255) ** GammaValue) * 255)
            invGreen = int(((G / 255) ** GammaValue) * 255)
            invBlue = int(((B / 255) ** GammaValue) * 255)

            pixels[x, y] = (invRed, invGreen, invBlue)
            

    GammaImageDisplay = ImageTk.PhotoImage(GammaImage)

def show_gamma_corrected(type):

    make_gamma_corrected(type)

    canvas.delete("all")
    
    canvas.create_image(0, 0, anchor=tk.NW, image=imageDisplay)

    canvas.create_image(ogImage.width, 0, anchor=tk.NW, image=GammaImageDisplay)



root = tk.Tk()
root.title("Mini Photoshop")

# Set up canvas for image display
canvas = tk.Canvas(root, width=1600, height=900)
canvas.pack()

# Define the menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Core operations menu with a nice font, padding, and separator
coreMenu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 12), bg="lightgray", fg="black")
menu_bar.add_cascade(label="Core Operations", menu=coreMenu)

coreMenu.add_command(label="Open File", command=open_and_display_bmp)
coreMenu.add_separator()
coreMenu.add_command(label="Grayscale", command=show_grayscale)
coreMenu.add_command(label="Ordered Dithering", command=show_ordered_dither)
coreMenu.add_command(label="Auto Level", command=show_auto_level)
coreMenu.add_separator()
coreMenu.add_command(label="Exit", command=root.quit)

optionalMenu = tk.Menu(menu_bar, tearoff=0, font=("Times New Roman", 12), bg="lightgray", fg="black")
menu_bar.add_cascade(label="Optional Operations", menu=optionalMenu)

optionalMenu.add_command(label="Enhance Red", command=lambda:show_red("add"))
optionalMenu.add_command(label="Remove Red", command=lambda:show_red("remove"))

optionalMenu.add_separator()
optionalMenu.add_command(label="Enhance Green", command=lambda:show_green("add"))
optionalMenu.add_command(label="Remove Green", command=lambda:show_green("remove"))

optionalMenu.add_separator()
optionalMenu.add_command(label="Enhance Blue", command=lambda: show_blue("add"))
optionalMenu.add_command(label="Remove Blue", command=lambda: show_blue("remove"))

optionalMenu.add_separator()
optionalMenu.add_command(label="Undo Gamma Correction (Darken)", command=lambda: show_gamma_corrected("reg"))
optionalMenu.add_command(label="re-Gamma Correction (Brighten)", command=lambda: show_gamma_corrected("inv"))

optionalMenu.add_separator()
optionalMenu.add_command(label="Exit", command=root.quit)

root.mainloop()    


