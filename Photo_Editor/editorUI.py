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

General UI:
===================================================


                    {content}


===================================================

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
    UI_seperator = "======================================================="

    UI_Box = []
    UserImage = []

    # Operation Variable
    FunctionsDict = {0: "Adjust Brightness", 1: "Crop image", 2: "Blur image"}
    ModifiedImage_Headings = {0: "Adjusted_Brightness", 1: "Cropped", 2: "Blured"}
    isRunning = True

    #initial settings
    def initial_settings(self):
        
        directory = os.path.dirname(os.path.realpath(__file__))
        try:
            os.makedirs(os.path.join(directory, "Modified"))
            os.makedirs(os.path.join(directory, "Raw"))
            print("Initialization for first excution")
            print("Editor Initializing...")
            print("Editor Initialization finished, Modified files will be store in \"Modified\" folder.\nPlease put photo that you want to edit in the new \"Raw\" Folder in this directory. Then, restart the editor.")
            print("Press AnyKey to exit")
            input()
            quit()
        except FileExistsError:
            pass
        
        return directory
        
    #file opening functions
    def ListDirectory(self, path):
        imgfiles = {}

        for file, count in enumerate(os.listdir(path)):                
            imgfiles[file] = count

        return imgfiles

    def ChooseFile(self, fileNames = dict):
        print(self.UI_seperator)
        print("File list:")
        
        for count in range(len(fileNames)):
            print(str(count)+ ":", fileNames[count])

        userInput = int(input(f"\nInput file index(0-{len(fileNames)-1}):"))
        
        while fileNames.get(userInput) == -1:
            print("Invilad index!")
            userInput = input(f"Input file index(0-{len(fileNames)-1}):")
        
        print(self.UI_seperator)
        return fileNames.get(userInput)
    
    def initImage(self, image):
        
        self.im = image
        self.image_width = image.width
        self.image_height = image.height
        
        self.imArray = np.array(self.im)
        
        ratio = self.image_width/self.image_height

        self.UI_image_width = round(self.standard_width * ratio)
        self.UI_image_height = round(round(self.standard_height) / ratio)
        self.Right_indicator_index = self.UI_image_width
        self.Bottom_indicator_index = self.UI_image_height

        self.image_WidthRatio = self.image_width / self.UI_image_width
        self.image_HeightRatio = self.image_height / self.UI_image_height
        
    def __init__(self) -> None:
        
        self.User_directory = self.initial_settings()
        self.Raw_directory = os.path.join(self.initial_settings(),"Raw")
        self.Output_directory = os.path.join(self.User_directory, "Modified")
        self.Image_Name = self.ListDirectory(self.Raw_directory) 
        self.Chosen_Image = self.ChooseFile(self.Image_Name)

        self.im = Image.open(self.ImagePath_template.format(userPath = self.Raw_directory, fileName = self.Chosen_Image))

        self.CommandHandler()

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
        self.generateUIBox()
        self.PrintBox()
        
        #get selection method(ALL or custom)
        # new selection input method: all at one seperated by ","
        print("Input selection coordinates(left, right, top, down, seperate with \",\")")
        selectionInput = input(f"Limit:(Left: {self.Left_indicator_index}-Right: {self.Right_indicator_index}, Top: {self.Top_indicator_index}-Bottom: {self.Bottom_indicator_index}) Press enter for select all: ").split(",")
        
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

        self.PrintBox()

    #Box UI functions end        
    def getTrueSelectedArea(self):
        trueL = round((self.Left_indicator_index-1) * self.image_WidthRatio)
        trueR = round(self.Right_indicator_index * self.image_WidthRatio)
        trueT = round((self.Top_indicator_index-1) * self.image_HeightRatio)
        trueB = round(self.Bottom_indicator_index * self.image_HeightRatio) 

        return (trueL, trueT, trueR, trueB)      
    #Image Handling
    def saveImage(self, path = None, fileName = None):
        safePath = self.Output_directory
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

        self.editedIm = cropped_im

    def AdjustImageBrightness(self):

        addjustment = int(input("Brightness adjustment: "))

        adjusted_image_data = self.imArray.astype('int16') + addjustment #change type to int16 to prevent overflow

        adjusted_image_data = np.where(adjusted_image_data > 255, 255, adjusted_image_data) 
        adjusted_image_data = np.where(adjusted_image_data < 0, 0, adjusted_image_data)
        adjusted_image_data = adjusted_image_data.astype('uint8')
        adjusted_image = Image.fromarray(adjusted_image_data, 'RGB')
        
        self.editedIm = adjusted_image 

    def selectionBlur(self, selection_area ,radius):
        L, T, R, D = selection_area
    
        sub_imArray = self.imArray[T:D,L:R]
        height, width, _ = sub_imArray.shape

        integral_image = np.cumsum(np.cumsum(sub_imArray, axis=0), axis=1)
        with tqdm(total=((R-L)*(D-T)), desc='Bluring', position=0, unit= "pixel") as progressBar:
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

 
    def BlurHandler(self, selection_area, radius = 15):

        blurred_image = self.selectionBlur(selection_area, radius)
        
        self.editedIm = blurred_image

    #Command Handler
    def CommandHandler(self):
        
        while self.isRunning:

            self.initImage(self.im)

            print("Function list:")
            for count in range(len(self.FunctionsDict)):
                print(str(count)+ ":", self.FunctionsDict[count])

            userInput = input("Choose a Function by index: ")
            while not userInput.isdigit() or self.FunctionsDict.get(int(userInput))  == -1:
                print("Invaild Index!")
                userInput = input("Choose a Function by index: ")
            
            userInput = int(userInput)
            print(self.UI_seperator)
            print(f"Choosed: {self.FunctionsDict.get(userInput)}")
            if userInput == 0:
                self.AdjustImageBrightness()
                print("Brightness adjusted")
            elif userInput == 1:
                if self.selection() == False:
                    print("Invliad Selection!, please Try again!")
                    continue

                self.CropImage(self.getTrueSelectedArea())
                
                print("Image Cropped")
            else:                
                if self.selection() == False:
                    print("Invliad Selection!, please Try again!")
                    continue

                BlurStrength = input("Input Blur Strength(default = 15): ")
                if BlurStrength:
                    while not BlurStrength.isdigit() or int(BlurStrength) < 0:
                        print("Invaild Input!")
                        BlurStrength = int(input("Input Blur Strength(default = 15, press enter for default): "))
                    self.BlurHandler(self.getTrueSelectedArea(), int(BlurStrength))
                else:
                    self.BlurHandler(self.getTrueSelectedArea())
                
                print("Image blured")
            
            self.editedIm.show("Preview")

            userInput2 = input("Any Further edit(Y/N)?")

            while userInput2.lower() != "y" and userInput2.lower() != "n":
                print("Invalid input!")
                userInput2 = input("Any Further edit(Y/N)?")

            if userInput2.lower() == "y":
                self.im = self.editedIm

            else:
                filename = input("Input desire filename, press enter for default:")
                if filename:  
                    self.saveImage(filename)
                else:
                    self.saveImage()
                print("Thanks for using")
                self.isRunning = False

    #Command Handler

editor = PhotoEditor()
