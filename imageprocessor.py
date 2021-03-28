from PIL import Image
from PIL import ImageFilter
from PIL import ImageStat
import numpy as np
from scipy import ndimage
import cv2
class ImageProcessor:
    
    def __init__(self, img_path):
        self.img = Image.open(img_path)
        self.file_name = img_path

    def process(self):
        # GrayScale
        self.img = self.img.convert('LA')
        # self.img = self.img.filter(ImageFilter.ModeFilter(2))
        

        # Thresholding
        
        
        self.img = self.faster_bradley_threshold(self.img, threshold=100)


        # Noise Removal
        # self.img = self.img.filter(ImageFilter.UnsharpMask(1, 200, 4))
        #self.img = self.img.filter(ImageFilter.BoxBlur(1))

        threshold = sum(ImageStat.Stat(self.img).mean)/2
        self.img = self.img.point(lambda p: p > threshold and 255) 

        #self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        self.img.save(self.file_name)
        # self.line_removal(self.file_name)
        self.img = Image.open(self.file_name)
        # Edge detection
        # self.img = self.img.filter(ImageFilter.FIND_EDGES)



    def save(self, path):
        self.img.save(path)

    # https://stackoverflow.com/questions/33091755/bradley-roth-adaptive-thresholding-algorithm-how-do-i-get-better-performance
    def faster_bradley_threshold(self, image, threshold=75, window_r=5):
        percentage = threshold / 100.
        window_diam = 2*window_r + 1
        # convert image to numpy array of grayscale values
        img = np.array(image.convert('L')).astype(np.float) # float for mean precision 
        # matrix of local means with scipy
        means = ndimage.uniform_filter(img, window_diam)
        # result: 0 for entry less than percentage*mean, 255 otherwise 
        height, width = img.shape[:2]
        result = np.zeros((height,width), np.uint8)   # initially all 0
        result[img >= percentage * means] = 128       # numpy magic :)
        
        # convert back to PIL image
        return Image.fromarray(result)

    def line_removal(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Remove horizontal
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,10))
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255,255,255), 2)

        # Repair image
        repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,1))
        #image = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel, iterations=1)

        # Other stuff to play around with
        
        image = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_OPEN, repair_kernel, iterations=1)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,2))
        image = cv2.erode(image,kernel,iterations = 1)

        cv2.imwrite(self.file_name, image)