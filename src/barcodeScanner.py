import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import sys

"""
Attempts to decode image or frame data 
---
Args: image to be analyzed
Return: barcodeData -> list, or None
"""
def decode(image):
    barcodeData = pyzbar.decode(image)
    if barcodeData != []:
        return barcodeData
    else:
        return None


"""
Start video from default camera on sys, 
attempt to capture barcode in frame and call to decode frame
---
Args: None
Return: barcodeData -> list, or None
"""
def videoIn():

    input = cv2.VideoCapture(0)

    if not input.isOpened():
        print("Error opening default camera")
        return None
    
    print("Video capture started, press 'q' to quit manually")
    try:
        while True:
            live, frame = input.read()

            if not live:
                print("Error, failure to capture frame")

            cv2.imshow('Point camera at barcode to scan!', frame)

            barcodeData = decode(frame)
            
            if barcodeData != None:
                return barcodeData
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        input.release()
        cv2.destroyAllWindows()

    return None

"""
Takes an image path either uploaded or caputred, 
and attempts to read file
---
Args: path -> str (path to some img file)
Return:
"""
def read(path: str):
    if path == "" or None:
        print ("Path not provided")
        return None
    
    image = cv2.imread(path)
    if image is None:
        print(f"cv2 failed to open image on path: {path}")
        return None
    
    return image

"""
outputting data from list based on input flags, 
if working with a different objective in mind than I/O, 
just change the prints to return values, 
and pass that data to next step.
---
Args: barcodeData -> list, flag -> str,
Return: None (cur functionality prints to console)
"""
def dataOut(barcodeData: list, flag: str):
    match flag:
        case "-d":
            print(barcodeData[0].data)
            return None
        case "-dt":
            print(barcodeData[0].data)
            print(barcodeData[0].type)
            return None
        case "-r":
            print(barcodeData[0])
            return None
        case _:
            print("Invalid flag, run the following for options: python3 <filename>.py -help")
            return None



if __name__ == "__main__":
    argLen = len(sys.argv)
    if (argLen == 1) or (argLen < 3):
        print("\n     ---------------  \n     Barcode Scanner  \n     ---------------  ")
        print("     Default usage is denoted below:")
        print("      - Video Input: python3 <filename>.py -v -<output specifier flag>")
        print("      - Image Input: python3 <filename>.py -i -<output specifier flag> <path to image>")
        print("     Output specifiers:")
        print("      - Data Chars: python3 <filename.py> -<input> -d ...")
        print("      - Data Chars and Type: python3 <filename.py> -<input> -dt ...")
        print("      - Raw list, all data: python3 <filename.py> -<input> -r ...\n")
        print("     To display this again: python3 <filename>.py -help, (or pass no flags and files)\n")
        exit(0)

    elif sys.argv[1] == "-i":
        if argLen == 3:
            print("A flag was not provided, run with no flags or -help for options")
            exit(1)
        image = read(sys.argv[3])
        data = decode(image)
        dataOut(data, sys.argv[2])

    elif sys.argv[1] == "-v":
        data = videoIn()
        if data:
            print(f"Video out")
            dataOut(data, sys.argv[2])
        else:
            exit(1)

    else:
        print("Incorrect usage, run with no flags or -help for options")
        exit(1)
    
    exit(0)
