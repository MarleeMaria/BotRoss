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

        # Create the main window
        root = tkinter.Tk()
        root.title("Customise Your Painting")
        welcome = tkinter.Label(root, text="Welcome to Bot Ross the painter bot that changes png and jpeg files to a painting.")
        welcome.pack()

        root.labelFrame = ttk.LabelFrame(root, text = "Choose a Photo")
        root.labelFrame.pack()

        def fileDialog():
            root.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select An Image", filetype =
            (("jpeg files","*.jpg"),("png files","*.png"),("jpeg files","*.jpeg")) )
            root.label = ttk.Label(root.labelFrame, text = "")
            root.label.pack()
            root.label.configure(text = root.filename)

            global filePath
            self.file =  root.filename

            img = Image.open(root.filename)
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel = tkinter.Label(root, image=img)
            panel.image = img
            panel.pack()

        root.button = ttk.Button(root.labelFrame, text = "Browse A File",command = fileDialog)
        root.button.pack()

        # Create label
        label = tkinter.Label(root, text="Pick Your Pallette")

        # Lay out label
        label.pack()
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


        def submit():
            print( "Selection:")
            radio_option.get()
            global selection
            selection = radio_option.get()


            try: selection
            except NameError: selection = None
            if selection is None:
                print("colorless")
            elif selection == 2:
                print( "Colored.")
                scale_option = tkinter.IntVar()

                # Create some widgets to put in the level2 widget (window)
                top_label = tkinter.Label(root, text="How large is your palette it can be up to 20 colors")

                top_scale = tkinter.Scale(root, orient=tkinter.HORIZONTAL, from_=1, to=20)


                def confirm():
                    print( "Confim Color amount")
                    top_scale.get()
                    global colorNum
                    colorNum = top_scale.get()
                    self.colors = []
                    index = 0
                    # e = tkinter.Label(root, text="test")
                    # e.pack(side=LEFT)


                    for color in range(colorNum):
                      # self.colors.append([255, 255, 255])
                      print(self.colors)


                      # buttonColor = tkinter.Button(root, text="Pick Color", command= call_me(index))
                      buttonColor = tkinter.Button(root, text="Pick Color", command= call_me)
                      buttonColor.pack(side=LEFT)
                      index += 1


                def call_me():
                    clr = colorchooser.askcolor(title="select color")
                    root.label2 = ttk.Label(root, text = clr[1])
                    root.label2.pack()
                    root.label2.configure(background=clr[1])
                    strip = clr[1].lstrip('#')
                    value = tuple(int(strip[j:j+2], 16) for j in (4, 2, 0))
                    # print(index)
                    self.colors.append(value)

                    # root.quit()

                # top_button = tkinter.Button(level2, text="OK")
                top_submit = tkinter.Button(root, text="Confirm", command=confirm)

                top_label.pack()
                top_scale.pack()
                top_submit.pack()

            elif selection == 1:
                print( "Black & White.")
                self.colors = [[255,255,255], [0,0,0]]
                print(self.colors)


        button_submit = tkinter.Button(root, text="Submit", command=submit)
        # Pack

        radiobutton_1.pack(padx=5)
        radiobutton_2.pack(padx=5)
        button_submit.pack()



        # Run forever or until submit!
        root.mainloop()

        #
        # if selection == 2:
        #     print( "Colored.")
        #
        #     level2 = tkinter.Tk()
        #     level2.title("My colors")
        #     scale_option = tkinter.IntVar()
        #
        #     # Create some widgets to put in the level2 widget (window)
        #     top_label = tkinter.Label(level2, text="How large is your palette it can be up to 20 colors")
        #
        #     top_scale = tkinter.Scale(level2, orient=tkinter.HORIZONTAL, from_=1, to=20)
        #
        #     def call_me():
        #         clr = colorchooser.askcolor(title="select color")
        #         level2.e.configure(background=clr[1])
        #
        #     def confirm():
        #         print( "Confim Color amount")
        #         top_scale.get()
        #         global colorNum
        #         colorNum = top_scale.get()
        #
        #
        #         row = 0
        #         col = 0
        #         for color in range(colorNum):
        #           e = tkinter.Label(level2, text="test")
        #           buttonColor = tkinter.Button(level2, text="Pick Color", command=call_me)
        #           buttonColor.pack()
        #           e.pack()
        #           row += 1
        #           if (row > 36):
        #             row = 0
        #             col += 1
        #
        #         # root.quit()
        #
        #     # top_button = tkinter.Button(level2, text="OK")
        #     top_submit = tkinter.Button(level2, text="Confirm", command=confirm)
        #
        #     top_label.pack()
        #     top_scale.pack()
        #     top_submit.pack()
        #
        #     level2.mainloop()
        #
        #
        # elif selection == 1:
        #     print( "Black & White.")
        #     self.colors = [[255,255,255], [0,0,0]]
        #     print(self.colors)
        #
        print(self.colors)
        try: confirm
        except NameError: confirm = None
        if confirm is None:
            print("colorless")
        else:
            print( "Pick colors.")

            # level3 = tkinter.Tk()
            # level3.title("Browse colors")
            # scale_option = tkinter.IntVar()
            #
            # # Create some widgets to put in the level2 widget (window)
            # top_label = tkinter.Label(level3, text="TESTLEVEL")
            # for x in range(colorNum):
            #     tkinter.Scale(level3, orient=tkinter.HORIZONTAL, from_=0, to=20)
            #
            # top_label.pack()
            # top_scale.pack()
            # top_submit.pack()
            # level3.mainloop()

    def color(self):
        return self.colors

    def file(self):
        return self.file
