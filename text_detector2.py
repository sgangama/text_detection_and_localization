from pytesseract import Output  #you need all these libraries preinstalled...use the pip command
import pytesseract
import argparse
import cv2

#argparser
#is argument has a required=true label, then you need to provide that argument in the command prompt
ap=argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path")
ap.add_argument("-c", "--min-conf", type=int, default=0, help="min confidence to filter weak detections")
args=vars(ap.parse_args())

#read image and convert BGR TO RGB and the localize area of text
image= cv2.imread(args["image"])
rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #you need to install tesseract ocr for this and this line of code whill encompass the path to tesseract.exe file of yours...
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

#loop over text localizations
for i in range(0, len(results["text"])):
    #extract bounding box coordinates from current iteration
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]
    #extract confidence and extracted texts
    text = results["text"][i]
    conf = int(results["conf"][i])
    #filter
    if conf>args["min_conf"]:
        #display
        print("Confidence:{}".format(conf))   #confidence as in probability as to how likely that a given portion of text is a character.
        print("Text:{}".format(text))         #whats written
        print("")
        #strip out non-ASCII text adn draw bounding boxes with texts
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 3)  #text to appear around the detected portion above

        #show output
cv2.imshow("Image", image)
cv2.waitKey(0)
