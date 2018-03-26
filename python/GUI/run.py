import tkinter as tk
import time
import threading
import imutils
import argparse
from imutils.video import VideoStream
from PIL import Image
from PIL import ImageTk
import cv2
import serial

#comment out the first if using GPIO, the second if using usb
port = '/dev/ttyACM0'
#port = '/dev/ttyAMA0'

ser = serial.Serial(port, 115200)
ser.close()
ser.open()


LARGE_FONT = ("Times", 90, "bold")
MEDIUM_FONT = ("Times", 60)
SMALL_FONT = ("Times", 30)

BACKGROUND_COLOUR = "#FF1919"
BACKGROUND_COLOUR_BUTTON = "#F79024"

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type = int, default = 0,
                help="whether or not the Raspberry Pi Camera should be used")
args = vars(ap.parse_args())

print("[INFO] Warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] >= 0).start()
time.sleep(2.0)

print("[INFO] Loading Haar Cascades")
baseCascadePath = "/usr/local/share/OpenCV/haarcascades/"

faceCascadePath = baseCascadePath + "haarcascade_frontalface_default.xml"
noseCascadePath = baseCascadePath + "haarcascade_mcs_nose.xml"


faceCascade = cv2.CascadeClassifier(faceCascadePath)
noseCascade = cv2.CascadeClassifier(noseCascadePath)

imgMustache = cv2.imread('mustache.png', -1)

orig_mask = imgMustache[:,:,3]

orig_mask_inv = cv2.bitwise_not(orig_mask)

imgMustache = imgMustache[:,:,0:3]
origMustacheHeight, origMustacheWidth = imgMustache.shape[:2]

class Main(tk.Tk):
    def __init__(self, vs, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.state = True
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = threading.Event()
        
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.kill)
        self.bind("w", self.forward)
        self.bind("a", self.left)
        self.bind("s", self.reverse)
        self.bind("d", self.right)
        
        self.frames = {}

        for f in list_pages:
            frame = f(container, self)

            self.frames[f] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
    def forward(self, event = None):
        ser.write('w'.encode('utf-8'))

    def left(self, event = None):
        ser.write('a'.encode('utf-8'))

    def reverse(self, event = None):
        ser.write('s'.encode('utf-8'))

    def right(self, event = None):
        ser.write('d'.encode('utf-8'))
        
    def toggle_fullscreen(self, event = None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)

    def kill(self, event = None):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        ser.close()
        self.destroy()
        

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        ser.write('l'.encode('utf-8'))

        self.configure(bg = BACKGROUND_COLOUR)

        self.clock = tk.Label(self, text = 'begone', anchor = 'nw', justify = 'left', font = ("system", 20))
        self.clock.configure(bg = BACKGROUND_COLOUR)
        self.clock.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')

        self.l1 = tk.Label(self, text = 'Self Driving\nCar!', font = LARGE_FONT)
        self.l1.configure(bg = BACKGROUND_COLOUR)
        self.l1.grid(row = 3, column = 1, columnspan = 3, sticky = 'nsew')

        self.b1 = tk.Button(self, text = 'Mapping Mode', font = SMALL_FONT, command = lambda:controller.show_frame(MappingMode))
        self.b1.configure(bg = BACKGROUND_COLOUR_BUTTON, relief = 'raised')
        self.b1.grid(row = 6, column = 1, sticky = 'nsew')

        self.b2 = tk.Button(self, text = 'Controlled Mode', font = SMALL_FONT, command = lambda:controller.show_frame(ControlledMode))
        self.b2.configure(bg = BACKGROUND_COLOUR_BUTTON, relief = 'raised')
        self.b2.grid(row = 6, column = 3, sticky = 'nsew')

        self.b3 = tk.Button(self, text = 'Exit', font = SMALL_FONT, command = lambda:controller.kill())
        self.b3.configure(bg = BACKGROUND_COLOUR_BUTTON, relief = 'raised')
        self.b3.grid(row = 7, column = 2)
        
        self.update_clock()

        for i in range(8):
            self.grid_rowconfigure(i, weight = 1)
        for i in range(5):
            self.grid_columnconfigure(i, weight = 1)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock.configure(text = now)
        self.clock.after(200, self.update_clock)


class ControlledMode(tk.Frame):

    def __init__(self, parent, controller):

        ser.write('c'.encode('utf-8'))

        tk.Frame.__init__(self, parent)

        self.mustache_count = 0

        self.configure(bg = BACKGROUND_COLOUR)

        self.clock = tk.Label(self, text = 'begone', anchor = 'nw', justify = 'left', font = ("system", 20))
        self.clock.configure(bg = BACKGROUND_COLOUR)
        self.clock.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')

        self.vs = vs
        self.frame = None
        self.stopEvent = None

        self.panel = None
    
        self.b1 = tk.Button(self, text = 'Mapping Mode', font = SMALL_FONT, command=lambda:controller.show_frame(MappingMode))
        self.b1.configure(bg = BACKGROUND_COLOUR_BUTTON)
        self.b1.grid(row = 8, column = 2, columnspan = 2, sticky = 'nsew')

        self.b2 = tk.Button(self, text = 'Main Menu', font = SMALL_FONT, command = lambda:controller.show_frame(MainPage))
        self.b2.configure(bg = BACKGROUND_COLOUR_BUTTON)
        self.b2.grid(row = 8, column = 5, columnspan = 2, sticky = 'nsew')

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        print("[INFO] started thread = ", self.thread.is_alive())
        
        self.update_clock()


    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock.configure(text = now)
        self.clock.after(200, self.update_clock)

    def videoLoop(self):
        #code adapted from https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/
        #with adjustments made so it works how I want it to
        #facial recognition code adapted from https://sublimerobots.com/2015/02/dancing-mustaches
        try:
            while not self.stopEvent.is_set():

                swidth = self.winfo_screenwidth()
                sheight = self.winfo_screenheight()
                
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width = int(swidth / 1.5), height = int(sheight / 1.5))

                # change image from bgr (opencv) to rgb (PIL) then to PIL and ImageTk format
                img1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    grey,
                    scaleFactor = 1.1,
                    minNeighbors = 5,
                    minSize = (30, 30),
                    flags = cv2.CASCADE_SCALE_IMAGE)
                
                for (x, y, w, h) in faces:
                    #uncomment the next line for debugging faces
                    #face = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    print("[INFO] detected %s" % len(faces) + (" face" if len(faces) == 1 else " faces"))
                    self.mustache_count += len(faces)

                    roi_grey = grey[y:y+h, x:x+w]
                    roi_color = img1[y:y+h, x:x+w]

                    nose = noseCascade.detectMultiScale(roi_grey)

                    for (nx, ny, nw, nh) in nose:
                        #uncomment the next line for debugging noses
                        #cv2.rectangle(roi_color, (nx, ny), (nx+nw, ny+nh), (255, 0, 0), 1)
                        print("[INFO] detected a nose")

                        #mustache should be 3 times the width of the nose
                        mustacheWidth = 3 * nw
                        mustacheHeight = mustacheWidth * origMustacheHeight / origMustacheWidth

                        #center the mustache
                        x1 = nx - (mustacheWidth/4)
                        x2 = nx + nw + (mustacheWidth/4)
                        y1 = ny + nh - (mustacheHeight/2)
                        y2 = ny + nh + (mustacheHeight/2)

                        x1 = int(x1)
                        x2 = int(x2)
                        y1 = int(y1)
                        y2 = int(y2)

                        #check for clipping
                        if x1 < 0:
                            x1 = 0
                        if y1 < 0:
                            y1 = 0
                        if x2 > w:
                            x2 = w
                        if y2 > h:
                            y2 = h

                        #recalculate the width and height
                        mustacheWidth = x2 - x1
                        mustacheHeight = y2 - y1

                        mustacheWidth = int(mustacheWidth)
                        mustacheHeight = int(mustacheHeight)

                        # resize the original image and the masks to the mustache sizes
                        mustache = cv2.resize(imgMustache, (mustacheWidth, mustacheHeight), interpolation = cv2.INTER_AREA)
                        mask = cv2.resize(orig_mask, (mustacheWidth, mustacheHeight), interpolation = cv2.INTER_AREA)
                        mask_inv = cv2.resize(orig_mask_inv, (mustacheWidth, mustacheHeight), interpolation = cv2.INTER_AREA)

                        #take ROI for mustache from background equal to size of mustache image
                        roi = roi_color[y1:y2, x1:x2]

                        #roi_bg contains the original image only where the mustache is not
                        roi_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)

                        #roi_fg contains the original image only where the image is
                        roi_fg = cv2.bitwise_and(mustache, mustache, mask = mask)

                        # join the roi_bg and roi_fg
                        dst = cv2.add(roi_bg, roi_fg)

                        # place the joined image, saved to dst, back over the original image
                        roi_color[y1:y2, x1:x2] = dst

                        break

                img = Image.fromarray(img1)
                img = ImageTk.PhotoImage(img)
                print("[INFO] HAHA you have a mustache now")
                print("[INFO] I have drawn %s mustaches on people" % self.mustache_count)
                
                if self.panel is None:
                    self.panel = tk.Label(self, image = img)
                    self.panel.image = img
                    self.panel.grid(row = 2, rowspan = 5, column = 1, columnspan = 5, sticky = 'nsew')

                else:
                    self.panel.configure(image = img)
                    self.panel.image = img

        except RuntimeError:
            print("[INFO] RuntimeError caught")
                

class MappingMode(tk.Frame):

    def __init__(self, parent, controller):

        ser.write('m'.encode('utf-8'))

        tk.Frame.__init__(self, parent)

        self.configure(bg = BACKGROUND_COLOUR)

        self.clock = tk.Label(self, text = 'begone', anchor = 'nw', justify = 'left', font = ("system", 20))
        self.clock.configure(bg = BACKGROUND_COLOUR)
        self.clock.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')

        self.l1 = tk.Label(self, text = 'Mapping Mode', anchor = 'n', font = MEDIUM_FONT)
        self.l1.configure(bg = BACKGROUND_COLOUR)
        self.l1.grid(row = 0, column = 2, columnspan = 2)

        self.b1 = tk.Button(self, text = 'Controlled Mode', font = SMALL_FONT,
                            command = lambda:controller.show_frame(ControlledMode))
        self.b1.configure(bg = BACKGROUND_COLOUR_BUTTON)
        self.b1.grid(row = 6, column = 2, columnspan = 2)

        self.b2 = tk.Button(self, text = 'Main Menu', font = SMALL_FONT,
                            command = lambda:controller.show_frame(MainPage))
        self.b2.configure(bg = BACKGROUND_COLOUR_BUTTON)
        self.b2.grid(row = 6, column = 5, columnspan = 2)

        self.update_clock()

        for i in range(6):
            self.grid_rowconfigure(i, weight = 1)

        for i in range(6):
            self.grid_rowconfigure(i, weight = 1)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock.configure(text = now)
        self.clock.after(200, self.update_clock)

list_pages = [MainPage, ControlledMode, MappingMode]
main = Main(vs)
main.title("Self Driving Car")
RWidth = main.winfo_screenwidth()
RHeight = main.winfo_screenheight()
main.geometry("%dx%d" % (RWidth / 2, RHeight / 2))
main.attributes('-fullscreen', True)
main.mainloop()
