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
import numpy as np
from PIL import Image

class PhotoEditor():
    #Image Variable
    im = Image.Image
    image_width = 0
    image_height = 0
    image_WidthRatio = 0.0
    image_HeightRatio = 0.0

    #UI Variable
    standard_width = standard_height = 9

    UI_image_width = 0
    UI_image_height = 0
    Left_indicator_index = 0
    Right_indicator_index = 0
    Top_indicator_index = 0
    Bottom_indicator_index = 0

    UI_Box = []
    UserImage = []

    def __init__(self, path) -> None:
        self.im = Image.open(path)
        self.image_width = self.im.width
        self.image_height = self.im.height
        
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

    def MoveLeftRightIndicator(self):
        #get input
        L = int(input(f"input bound box start index(1-{self.UI_image_width}):"))
        while L < 1 or L > self.UI_image_width:
            print("ERROR: Invalid index")
            L = int(input(f"input bound box start index(1-{self.UI_image_width}):"))
        
        R = int(input(f"input bound box end index(1-{self.UI_image_width}):"))
        while R < 1 or R > self.UI_image_width or R < L:
            print("ERROR: Invalid index")
            R = int(input(f"input bound box end index(1-{self.UI_image_width}):"))
            
        #switch Left Indicator
        self.UI_Box[2][self.Left_indicator_index], self.UI_Box[2][L] = self.UI_Box[2][L], self.UI_Box[2][self.Left_indicator_index]
        
        #switch Right Indicator
        self.UI_Box[2][self.Right_indicator_index+1], self.UI_Box[2][R] = self.UI_Box[2][R], self.UI_Box[2][self.Right_indicator_index+1]

        #update old index
        self.Left_indicator_index = L
        self.Right_indicator_index = R

    def MoveTopBottomIndicator(self):
        #get input
        T = int(input(f"input bound box start index(1-{self.UI_image_height}):"))
        
        while T < 0 or T >= self.UI_image_height:
            print("ERROR: Invalid index")
            T = int(input(f"input bound box start index(1-{self.UI_image_height}):"))
        
        D = int(input(f"input bound box end index(1-{self.UI_image_height}):")) 
        while D < 0 or D > self.UI_image_height:
            print("ERROR: Invalid index")
            D = int(input(f"input bound box end index(1-{self.UI_image_height}):"))
            
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

        self.MoveLeftRightIndicator()
        self.MoveTopBottomIndicator()
            
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
    def saveImage():
        pass
    
    def CropImage(self,boundary):
        croppedImage = self.im.crop(boundary)

        croppedImage.show()


    #Command Handler
    #Command Handler


        
# standard_BoxWidth = 9
# standard_BoxHeight = 9
    
# UserImage = Image.open("C:/Programs/Python/photo_editor/temp1.jpg")
# Width_Height_ratio = round(UserImage.width/UserImage.height)
# estimated_Box_Width = round(standard_BoxHeight * Width_Height_ratio)
# estimated_Box_Height = round(round(standard_BoxHeight * Width_Height_ratio) / Width_Height_ratio)

# editor = PhotoEditor(estimated_Box_Width, estimated_Box_Height)
editor = PhotoEditor(r"C:\Programs\Python\photo_editor\temp1.jpg")
editor.generateUIBox()

editor.PrintBox()
editor.selection()
editor.PrintBox()
print(editor.image_width)
print(editor.image_height)
print(editor.Left_indicator_index, editor.Right_indicator_index, editor.Top_indicator_index, editor.Bottom_indicator_index)
editor.CropImage(editor.getTrueSelectedArea())
