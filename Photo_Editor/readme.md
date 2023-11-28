# Photo Editor
by Jimmy Yau, Cory Chan, Paul Tsang
## Introduction
This is a console-based image editor with 3 editing functions: Blur, Crop, and Adjust Brightness.<br>
User can select part of the image for Blur and Crop function.<br> 

## How to use
### Initial setup
After downloaded the editorUI script, place it into a empty folder and excute it.
The first run will be a auto initialization run for setting the folder it required.
After the first run, place your images in the new "Raw" folder. Then it is ready to use.<br>

### Using the editor
There should be a clear instruction in every steps. Please read those before taking any action to prevent errors.<br>

The modified image will be stored in the new "Modified" folder in default. You can edit the saving path during the editing.

## Remindar
- **Please make sure that Tqdm, Numpy, and Pillow is installed.** 
- The editor should be able to handle common image types like PNG, JPG and BMP. However, Since the file scanning filter is not working right now, 
- please **DON'T** put any non-image file in the "Raw" folder. Or errors may pop out when you accidentally select those file in the editor.<br/>
- Please make sure that your input is **CORRECT AND FULFILL THE REQUIRMENTS** when you are using the editor. **TRY NOT TO CHALLENGE** the program - or you may encounter an error that may lead to progress loss.<br/>
- It is not recommended to use a weak bluring strength for selection blur due to the unnatural edge after processing. This is related to our blur algorithm which will not blur the boundary of the selected area. This maybe fixed in future update.<br/>

##
Feel free to copy and use this code if you found it necessary for your project but please remember to give credits.