import random
import math
from tkinter import filedialog
import hashlib
import datetime
from PIL import Image, ImageDraw

class MoasicPass():

    #region Image Generation
    #Block = A Block of Pixels 64x64
    
    hexValues = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    def makeBlock(self) -> Image.Image: 
        hexColor = "#"
        for x in range(0,6):
            hexColor += self.hexValues[random.randint(0,15)]
        imgChunk = ImageDraw.Image.new("RGB", (64,64), hexColor)
        return imgChunk
    
    def makeImage(self) -> Image.Image:
        # "--------START MAKING BLOCKS--------")
        chunklist: list[Image.Image]
        chunklist = []
        for x in range(0, 2116): #Making 64x64 solid BLOCKS, one color only
            chunklist.append(self.makeBlock())

        imgWidth = 0 # Check if SquareRoot is fitting for a PERFECT SQUARE
        while not math.sqrt(len(chunklist)).is_integer():
            chunklist.append(self.makeBlock())
        imgWidth = int(math.sqrt(len(chunklist))*64)
        imgHeight = imgWidth            
      
        #"--------END MAKING BLOCKS--------")

        #"--------START CREATING IMAGE--------")
        img = Image.new("RGB", (imgWidth, imgHeight), "#ffffff")
        blocks_per_row = imgWidth // 64

        #Pasting all Blocks into the Canvas
        for idx, chunk in enumerate(chunklist):
            x = int((idx % blocks_per_row) * 64)
            y = int((idx // blocks_per_row) * 64)
            img.paste(chunk, (x, y))      
            
        #"--------END CREATING IMAGE--------")
        return img
    #endregion

    #region FileDialog Methods
    def getImage(self) -> Image.Image:
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*")])
        if file != None and file != '' and file.endswith(".png"):
            IMG = Image.open(file)
            if IMG.height != 2944 or IMG.width != 2944:
                print("Invalid Image selected")
                return None
            else:
                print("Invalid Filetype selected")
                return IMG
        else:
            return None
        

    def saveImage(self, IMG:Image.Image) -> bool: 
        fileName = hashlib.sha256("".join([str(datetime.datetime.now), str(random.randint(0, 999999999999))]).encode()).hexdigest()
        path = filedialog.asksaveasfile(filetypes=[("PNG files", "*.png")], title="Save Image", initialfile= fileName + ".png")
        if path == None or len(path.name) <= 0 or not path.name.endswith(".png"): 
            print("Invalid path or filetype given")
            return False
        else:
            IMG.save(path.name)
            print("Image saved at '" + path.name + "'")
            return True
    #endregion

    #region generate or read Password
    def getPassWord(self, IMG: Image.Image) -> str:
        #Start in the middle of the first block
        rgbList = []
        block_size = 64
        blocks_per_row = 46  #2944 / 64 = 46

        for row in range(blocks_per_row):
            for col in range(blocks_per_row):
                x = col * block_size + block_size // 2
                y = row * block_size + block_size // 2
                rgb = IMG.getpixel((x, y))
                rgbList.append(rgb)

        hex_string = ''.join(f'{r:02x}{g:02x}{b:02x}' for r, g, b in rgbList)
        password = hashlib.sha256(hex_string.encode()).hexdigest()
        return password
    #endregion

    #region User Interface
    def User_loop(self):
        needsInput = True
        print("\n-----------------------------------------")
        print("Welcome to the Mosaic Password Generator!")
        print("-----------------------------------------")
        print("Usage: ")
        print("'create' | generates a new Image and Password")
        print("'read'   | for reading a Password from a generated Image")
        print("'exit'   | for exiting the script")
        print("-----------------------------------------\n")
        while needsInput:

            uInput = input(": ")

            if uInput != None and uInput != '':
                match uInput:
                    case "create":
                        IMG = self.makeImage()
                        imageSaved = self.saveImage(IMG)
                        if imageSaved:
                            IMG.show()
                        else:
                            print("Error saving the Image")
                    case "read":
                        IMG = self.getImage()
                        if IMG is not None:
                            password = self.getPassWord(IMG)
                            print("Password: " + password)
                        else:
                            print("Error reading the Password")
                    case "exit":
                        needsInput = False

    #endregion

    def main(self):
        self.User_loop()

if __name__ == "__main__":
    moasicPass = MoasicPass()
    moasicPass.main()

#moasicPass = MoasicPass()
#moasicPass.main()