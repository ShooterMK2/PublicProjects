# Editor Description



"""
UI: symbol set: - | ⌄ < 

        {horizontal supp index}
          {horizontal index}
       ⌄            ⌄      
    ---------------------------------  
    |                               |  1
    |                               |  2
    |                               |  3
    |   ############                |< 4
    |   ############                |  5
    |   ############                |< 6
    --------------------------------- 

"""
#---------------------------------------------------------------------------------#
from tqdm import tqdm
import numpy as np
from PIL import Image
import os

class PhotoEditor():
    #file handling variable
    extensions = ["*.jpg", "*.bmp", "*.jpeg"]
    ImagePath_template = "{userPath}\\{fileName}"
    modifiedFileName = "modified_{}"
    User_directory = ""
    Output_directory = ""
    Image_Name = {}
    Chosen_Image = ""
    
    #Image Variable
    im = Image.Image
    imArray = []
    image_width = 0
    image_height = 0
    image_WidthRatio = 0.0
    image_HeightRatio = 0.0

    editedIm = Image.Image

    #UI Variable
    standard_width = standard_height = 9

    UI_image_width = 0
    UI_image_height = 0
    Left_indicator_index = 1
    Right_indicator_index = 0
    Top_indicator_index = 1
    Bottom_indicator_index = 0

    UI_Box = []
    UserImage = []

    #initial settings
    def initial_settings(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        try:
            os.makedirs(os.path.join(directory, "Modified"))
            os.makedirs(os.path.join(directory, "Raw"))
            print("Editor Initialization finished, Please put photo that you want to edit in \"Raw\" Folder.")
        except FileExistsError:
            pass
        
        return(directory)
        
    #file opening functions
    def ListDirectory(self, path):
        imgfiles = {}

        for file, count in enumerate(os.listdir(path)):                
            imgfiles[file] = count

        return imgfiles

    def ChooseFile(self, fileNames = dict):

        print("File list:")
        
        for count in range(len(fileNames)):
            print(str(count)+ ":", fileNames[count])

        userInput = int(input(f"Input file index(0-{len(fileNames)-1}):"))
        
        while fileNames.get(userInput) == -1:
            print("Invilad index!")
            userInput = input(f"Input file index(0-{len(fileNames)-1}):")
        
        return fileNames.get(userInput)
        
    def __init__(self) -> None:
        
        self.User_directory = os.path.join(self.initial_settings(),"Raw")
        self.Output_directory = os.path.join(self.User_directory, "Modified")
        self.Image_Name = self.ListDirectory(self.User_directory) 
        self.Chosen_Image = self.ChooseFile(self.Image_Name)

        self.im = Image.open(self.ImagePath_template.format(userPath = self.User_directory, fileName = self.Chosen_Image))
        self.image_width = self.im.width
        self.image_height = self.im.height
        
        self.imArray = np.array(self.im)
        
        ratio = self.image_width/self.image_height

        self.UI_image_width = round(self.standard_width * ratio)
        self.UI_image_height = round(round(self.standard_height) / ratio)
        self.Right_indicator_index = self.UI_image_width
        self.Bottom_indicator_index = self.UI_image_height

        self.image_WidthRatio = self.image_width / self.UI_image_width
        self.image_HeightRatio = self.image_height / self.UI_image_height

    #Box UI functions    
    def generateUIBox(self):
        self.UI_Box = []
        #top index number
    
        temp_tenth = []
        temp = []
        tenthCount = -1
        for i in range(self.UI_image_width+2):
            if i % 10 == 0:
                tenthCount += 1
                temp_tenth.append(str(tenthCount))
                temp_tenth.append(" ")
            else:
                temp_tenth.append("  ")
            
            temp.append(str((i) - 10*tenthCount))
            temp.append(" ") 
        self.UI_Box.append(temp_tenth)
        self.UI_Box.append(temp)

        #initial top indicator
        tempRow = []
        tempRow.append("⌄ ")

        for j in range(self.UI_image_width):
            tempRow.append("  ")     
        tempRow.append(" ⌄")
        self.UI_Box.append(tempRow)
        
        #Box generation
        for row in range(self.UI_image_height+2):
            tempRow = []
            if row == 0 or row == self.UI_image_height + 2 - 1:
                tempRow.append(" -")
                for i in range(self.UI_image_width):
                    tempRow.append("--")
                tempRow.append("-")
                tempRow.append("<")
                tempRow.append(" "+str(row))                
            else:
                tempRow.append(" |")
                for j in range(self.UI_image_width):
                    tempRow.append("  ")     
                tempRow.append("|")
                tempRow.append(" ")
                tempRow.append(" "+str(row))
            
            self.UI_Box.append(tempRow)
        


    def PrintBox(self):
        for row, count in enumerate(self.UI_Box):
            print("".join(self.UI_Box[row]))

    def MoveLeftRightIndicator(self, L, R):
        #get input
        
        while L < 1 or L > self.UI_image_width:
            print("ERROR: Invalid left index")
            return False
        
        while R < 1 or R > self.UI_image_width or R < L:
            print("ERROR: Invalid right index")
            return False
            
        #switch Left Indicator
        self.UI_Box[2][self.Left_indicator_index], self.UI_Box[2][L] = self.UI_Box[2][L], self.UI_Box[2][self.Left_indicator_index]
        
        #switch Right Indicator
        self.UI_Box[2][self.Right_indicator_index+1], self.UI_Box[2][R] = self.UI_Box[2][R], self.UI_Box[2][self.Right_indicator_index+1]

        #update old index
        self.Left_indicator_index = L
        self.Right_indicator_index = R

    def MoveTopBottomIndicator(self, T, D):
        #get input
        
        while T < 0 or T >= self.UI_image_height:
            print("ERROR: Invalid index")
            return False
         
        while D < 0 or D > self.UI_image_height:
            print("ERROR: Invalid index")
            return False
            
        #switch Top Indicator
        self.UI_Box[self.Top_indicator_index+3][-2], self.UI_Box[T+3][-2] = self.UI_Box[T+3][-2], self.UI_Box[self.Top_indicator_index+3][-2]
        
        #switch Bottom Indicator
        self.UI_Box[self.Bottom_indicator_index+4][-2], self.UI_Box[D+3][-2] = self.UI_Box[D+3][-2], self.UI_Box[self.Bottom_indicator_index+4][-2]

        #update old index
        
        self.Top_indicator_index = T 
        self.Bottom_indicator_index = D
    # Show selection    
    def selection(self):
        #get selection method(ALL or custom)
        # new selection input method: all at one seperated by,
        selectionInput = input("Input selection coordinates(left, right, top, down, seperate with \",\"), press enter for select all: ").split(",")
        
        if selectionInput != [""]:
            while len(selectionInput) != 4 or selectionInput[0].isdigit() == False or selectionInput[1].isdigit() == False or selectionInput[2].isdigit() == False or selectionInput[3].isdigit() == False:
                print("Four integer is required")
                selectionInput = input("Input selection coordinates(left, right, top, down, seperate with \",\"), press enter for select all: ").split(",")
                
            if self.MoveLeftRightIndicator(int(selectionInput[0]), int(selectionInput[1])) == False:
                return False
            if self.MoveTopBottomIndicator(int(selectionInput[2]), int(selectionInput[3])) == False:
                return False
            
        left = self.Left_indicator_index
        Right = self.Right_indicator_index
        Top = self.Top_indicator_index
        Bottom = self.Bottom_indicator_index
        
        for row in range(Top+3, Bottom+4):
                        
            for grid in range(left, Right+1):
                
                self.UI_Box[row][grid] = "##"

    #Box UI functions end        
    def getTrueSelectedArea(self):
        trueL = round((self.Left_indicator_index-1) * self.image_WidthRatio)
        trueR = round(self.Right_indicator_index * self.image_WidthRatio)
        trueT = round((self.Top_indicator_index-1) * self.image_HeightRatio)
        trueB = round(self.Bottom_indicator_index * self.image_HeightRatio) 

        return (trueL, trueT, trueR, trueB)      
    #Image Handling
    def saveImage(self, path = None, fileName = None):
        safePath = self.User_directory
        safeName = f"modified_{self.Chosen_Image}"
        if path != None:
            safeName = path
        
        if fileName != None:
            safeName = fileName
        
        self.editedIm.save(self.ImagePath_template.format(userPath = safePath, fileName = safeName))
    
    def CropImage(self,boundary):

        Left, Top, Right, Bottom = boundary
        
        cropped_imArray = self.imArray[Top:Bottom, Left:Right]

        cropped_im = Image.fromarray(cropped_imArray)

        cropped_im.show()  # test code
        
    def AdjustImageBrightness(self):

        addjustment = int(input("Brightness addjustment: "))

        adjusted_image_data = self.imArray + addjustment
        adjusted_image_data = np.clip(0, adjusted_image_data, 255)
        adjusted_image = Image.fromarray(adjusted_image_data.astype('uint8'), 'RGB')

        self.editedIm = adjusted_image

    def selectionBlur(self, selection_area ,radius):
        L, T, R, D = selection_area
    
        sub_imArray = self.imArray[T:D,L:R]
        height, width, _ = sub_imArray.shape

        integral_image = np.cumsum(np.cumsum(sub_imArray, axis=0), axis=1)
        with tqdm(total=(self.image_height*self.image_width), desc='Bluring', position=0, unit= "pixel") as progressBar:
            for y in range(height):
                for x in range(width):
                    
                    x1 = max(0, x - radius)
                    y1 = max(0, y - radius)
                    x2 = min(width - 1, x + radius)
                    y2 = min(height - 1, y + radius)

                    count = (x2 - x1 + 1) * (y2 - y1 + 1)
                    box_sum = integral_image[y2, x2] - integral_image[y1, x2] - integral_image[y2, x1] + integral_image[y1, x1]
                    average = box_sum // count
                    sub_imArray[y, x] = average
                    
                    progressBar.update(1)

            self.imArray[T:D, L:R] = sub_imArray
        return Image.fromarray(self.imArray)

 
    def box_blur(self, radius, selection_area = None):

        if selection_area:
            blurred_image = self.selectionBlur(selection_area, radius)

        else:
            pixels = self.imArray
            height, width, _ = pixels.shape
            integral_image = np.cumsum(np.cumsum(pixels, axis=0), axis=1)
            with tqdm(total=(self.image_height*self.image_width), desc='Outer Loop', position=0) as progressBar: 
                for y in range(height):
                    for x in range(width):
                        
                        x1 = max(0, x - radius)
                        y1 = max(0, y - radius)
                        x2 = min(width - 1, x + radius)
                        y2 = min(height - 1, y + radius)

                        count = (x2 - x1 + 1) * (y2 - y1 + 1)

                        box_sum = integral_image[y2, x2] - integral_image[y1, x2] - integral_image[y2, x1] + integral_image[y1, x1]

                        average = box_sum // count

                        pixels[y, x] = average

                        progressBar.update(1)

            blurred_image = Image.fromarray(pixels)
        
        self.editedIm = blurred_image

        


    #Command Handler
    #Command Handler


        
# standard_BoxWidth = 9
# standard_BoxHeight = 9
    
# UserImage = Image.open("C:/Programs/Python/photo_editor/temp1.jpg")
# Width_Height_ratio = round(UserImage.width/UserImage.height)
# estimated_Box_Width = round(standard_BoxHeight * Width_Height_ratio)
# estimated_Box_Height = round(round(standard_BoxHeight * Width_Height_ratio) / Width_Height_ratio)

editor = PhotoEditor()
# #editor = PhotoEditor(r"C:\Programs\Python\photo_editor\modified.jpg") # test code
editor.generateUIBox()
# editor.AdjustImageBrightness()
editor.PrintBox()
editor.selection()
editor.PrintBox()
print(editor.image_width)
print(editor.image_height)
print(editor.Left_indicator_index, editor.Right_indicator_index, editor.Top_indicator_index, editor.Bottom_indicator_index)
editor.CropImage(editor.getTrueSelectedArea())
editor.box_blur(25, editor.getTrueSelectedArea())
editor.saveImage()
