from tkinter import *
from PIL import ImageTk, Image

class MainWindow():
    def __init__(self, main):

        # canvas for image
        self.canvas = Canvas(main, width=1850, height=890, bg = 'black')
        self.canvas.grid(row=0, column=0)

        # images
        self.my_images = []
        original = Image.open("owl.jpg")
        img = ImageTk.PhotoImage(original)
        self.my_images.append(img)
        original_1 = Image.open("con.jpg")
        img_1 = ImageTk.PhotoImage(original_1)
        self.my_images.append(img_1)
        original_2 = Image.open("touch.jpg")
        original_2 = original_2.resize((1450,890))
        img_2 = ImageTk.PhotoImage(original_2)
        self.my_images.append(img_2)
        self.my_image_number = 0

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images[self.my_image_number])

        # button to change image
        self.button = Button(main, text="Change", command=self.onButton)
        self.button.grid(row=1, column=0)

    #----------------

    def onButton(self):

        # next image
        self.my_image_number += 1

        # return to first image
        if self.my_image_number == len(self.my_images):
            self.my_image_number = 0

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])

#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
