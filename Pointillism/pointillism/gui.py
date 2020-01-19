import tkinter
import _tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.commondialog import Dialog
from tkinter import colorchooser

class StartGUI:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.brush = 5
        self.colors = ""
        self.file = ""


    def run(self):
        # Create the main window
        root = tkinter.Tk()
        root.title("Customise Your Painting")
        welcome = tkinter.Label(root, text="Welcome to Bot Ross the painter bot that changes png and jpeg files to a painting.")
        welcome.grid(row=0)


        root.labelFrame = ttk.LabelFrame(root, text = "Choose a Photo").grid(row=1)

        def fileDialog():
            root.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select An Image", filetype =
            (("jpeg files","*.jpg"),("png files","*.png"),("jpeg files","*.jpeg")) )

            global filePath
            self.file =  root.filename

            img = Image.open(root.filename)
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            root.panel = ttk.Label(root.labelFrame, image=img)
            root.panel.image = img
            root.panel.grid(row=3)

        root.label = ttk.Label(root.labelFrame, text = "")
        root.label.grid(row=4)
        root.label.configure(text = self.file)


        root.button = ttk.Button(root.labelFrame, text = "Browse A File",command = fileDialog)
        root.button.grid(row=2)

        # Create cavas Size
        canvas_size = tkinter.Label(root, text="Specify Canvas Size")
        label_height = tkinter.Label(root, text="Height(cm): ").grid(row=6, sticky=W)
        label_width = tkinter.Label(root,  text="Width(cm): ").grid(row=7, sticky=W)
        canvas_height = tkinter.Spinbox(root, from_=10, to=25)
        canvas_width = tkinter.Spinbox(root, from_=10, to=25)



        brush_size = tkinter.IntVar()

        brush_label = tkinter.Label(root, text="Specify Brush Size")
        brush_size_1 = tkinter.Radiobutton( root,
                                        text="Small",
                                        variable=brush_size,
                                        value=5)
        brush_size_2 = tkinter.Radiobutton( root,
                                        text="Medium",
                                        variable=brush_size,
                                        value=10)
        brush_size_3 = tkinter.Radiobutton( root,
                                        text="Large",
                                        variable=brush_size,
                                        value=20)

        canvas_size.grid(row=5)
        canvas_height.grid(row=6)
        canvas_width.grid(row=7)

        brush_label.grid()
        brush_size_1.grid()
        brush_size_2.grid()
        brush_size_3.grid()

        # Create label
        label = tkinter.Label(root, text="Pick Your Pallette")


        # Lay out label
        radio_option = tkinter.IntVar()

        radiobutton_1 = tkinter.Radiobutton( root,
                                        text="Black And White",
                                        variable=radio_option,
                                        value=1)
        radiobutton_2 = tkinter.Radiobutton( root,
                                        text="Color",
                                        variable=radio_option,
                                        value=2)

        # Lay out widgets in the level2 pop-up window

        def preview():
            height_value = int(canvas_height.get())
            width_value = int(canvas_width.get())

            self.height = height_value
            self.width = width_value

            root.panel.grid_remove()
            img =  Image.open(self.file)
            img = img.resize((self.width*25, self.height*25), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            root.panel = ttk.Label(root.labelFrame, image=img)
            root.panel.image = img
            root.panel.grid(row=3)

        root.preview = ttk.Button(root, text = "Preview",command = preview).grid()

        def next():
            label.grid()


            radiobutton_1.grid()
            radiobutton_2.grid()
            button_submit.grid()

        # root.next = ttk.Button(root, text = "Next",command = next).grid()


        def submit():
            label.grid()


            # radiobutton_1.grid()
            # radiobutton_2.grid()


            print( "Selection:")
            radio_option.get()
            global selection
            selection = radio_option.get()


            print( "Brush Size:")
            brush_size.get()
            self.brush = brush_size.get()
            print(self.brush)
            # button_submit.config(state="disabled")


            height_value = int(canvas_height.get())
            width_value = int(canvas_width.get())

            self.height = height_value
            self.width = width_value
            root.quit()
            print( "Black & White.")
            self.colors = [[255,255,255], [0,0,0]]

            # try: selection
            # except NameError: selection = None
            # if selection is None:
            #     print("colorless")
            # elif selection == 2:
            #     print( "Colored.")
            #     scale_option = tkinter.IntVar()
            #
            #     # Create some widgets to put in the level2 widget (window)
            #     top_label = tkinter.Label(root, text="How large is your palette it can be up to 20 colors")
            #
            #     top_scale = tkinter.Spinbox(root, from_=1, to=10)
            #
            #
            #     def confirm():
            #         print( "Confim Color amount")
            #         # top_scale.get()
            #         global colorNum
            #         colorNum = int(top_scale.get())
            #         self.colors = []
            #         index = 0
            #         # e = tkinter.Label(root, text="test")
            #         # e.grid(side=LEFT)
            #
            #
            #         for color in range(colorNum):
            #           # self.colors.append([255, 255, 255])
            #           print(self.colors)
            #
            #           index += 1
            #           button_text = "Well " + str(index)
            #           # buttonColor = tkinter.Button(root, text="Pick Color", command= call_me(index))
            #           buttonColor = tkinter.Button(root, text=button_text, command= call_me)
            #           buttonColor.grid()
            #
            #
            #     def call_me():
            #         clr = colorchooser.askcolor(title="select color")
            #         root.label2 = ttk.Label(root, text = clr[1])
            #         root.label2.grid()
            #         root.label2.configure(background=clr[1])
            #         strip = clr[1].lstrip('#')
            #         value = list(int(strip[j:j+2], 16) for j in (4, 2, 0))
            #         # print(index)
            #         self.colors.append(value)
            #
            #         # root.quit()
            #
            #     # top_button = tkinter.Button(level2, text="OK")
            #     top_submit = tkinter.Button(root, text="Confirm", command=confirm)
            #
            #     top_label.grid()
            #     top_scale.grid()
            #     top_submit.grid()
            #
            # elif selection == 1:
            #     root.quit()
            #     print( "Black & White.")
            #     self.colors = [[255,255,255], [0,0,0]]
            #     print(self.colors)


        button_submit = ttk.Button(root, text="Submit", command=submit).grid()





        # Run forever or until submit!
        root.mainloop()

        print(self.colors)
        try: confirm
        except NameError: confirm = None
        if confirm is None:
            print("colorless")
        else:
            print( "Pick colors.")

    def brush(self):
        return self.brush

    def width(self):
        return self.width

    def height(self):
        return self.height

    def color(self):
        return self.colors

    def file(self):
        return self.file
