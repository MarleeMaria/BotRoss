import tkinter
import _tkinter
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

class StartGUI:
    def __init__(self):

        # Create the main window
        root = tkinter.Tk()
        root.title("Customise your painting")
        welcome = tkinter.Label(root, text="Welcome to Bot Ross the painter bot that changes png and jpeg files to a painting.")
        welcome.pack()

        # root.minsize(640, 400)

        root.labelFrame = ttk.LabelFrame(root, text = "Choose a Photo")
        root.labelFrame.pack()

        def fileDialog():
            root.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
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
            root.quit()


        button_submit = tkinter.Button(root, text="Submit", command=submit)

        # Pack

        radiobutton_1.pack(padx=5)
        radiobutton_2.pack(padx=5)
        button_submit.pack()

        # Run forever or until submit!
        root.mainloop()

        if selection == 2:
            print( "Colored.")

            level2 = tkinter.Tk()
            level2.title("My colors")
            scale_option = tkinter.IntVar()

            # Create some widgets to put in the level2 widget (window)
            top_label = tkinter.Label(level2, text="How large is your palette it can be up to 20 colors")
            top_scale = tkinter.Scale(level2, orient=tkinter.HORIZONTAL, from_=1, to=20)

            def confirm():
                print( "Confim Color amount")
                top_scale.get()
                global colorNum
                colorNum = top_scale.get()
                root.quit()

            # top_button = tkinter.Button(level2, text="OK")
            top_submit = tkinter.Button(level2, text="Confirm", command=confirm)

            top_label.pack()
            top_scale.pack()
            top_submit.pack()

            level2.mainloop()


        elif selection == 1:
            print( "Black & White.")
            self.colors = [[255,255,255], [0,0,0]]
            print(self.colors)


        try: confirm
        except NameError: confirm = None
        if confirm is None:
            print("colorless")
        else:
            print( "Pick colors.")

            level3 = tkinter.Tk()
            level3.title("Browse colors")
            scale_option = tkinter.IntVar()

            # Create some widgets to put in the level2 widget (window)
            top_label = tkinter.Label(level3, text="TESTLEVEL")
            for x in range(colorNum):
                tkinter.Scale(level3, orient=tkinter.HORIZONTAL, from_=0, to=20)


            top_label.pack()
            top_scale.pack()
            top_submit.pack()
            level3.mainloop()

    def color(self):
        return self.colors

    def file(self):
        return self.file




#
#
# __all__ = ["Chooser", "askcolor"]
#
# # color chooser class
#
# class Chooser(Dialog):
#
#     "Ask for a color"
#
#     command = "tk_chooseColor"
#
#     def _fixoptions(self):
#         try:
#             # make sure initialcolor is a tk color string
#             color = self.options["initialcolor"]
#             if isinstance(color, tuple):
#                 # assume an RGB triplet
#                 self.options["initialcolor"] = "#%02x%02x%02x" % color
#         except KeyError:
#             pass
#
#     def _fixresult(self, widget, result):
#         # result can be somethings: an empty tuple, an empty string or
#         # a Tcl_Obj, so this somewhat weird check handles that
#         if not result or not str(result):
#             return None, None # canceled
#
#         # to simplify application code, the color chooser returns
#         # an RGB tuple together with the Tk color string
#         r, g, b = widget.winfo_rgb(result)
#         return (b/256, g/256, r/256)
#
#
#
# # convenience stuff
#
# def askcolor(color = None, **options):
#     "Ask for a color"
#
#     if color:
#         options = options.copy()
#         options["initialcolor"] = color
#
#     return Chooser(**options).show()
#
#
# # --------------------------------------------------------------------
# # test stuff
#
# if __name__ == "__main__":
#     print("color", askcolor())
