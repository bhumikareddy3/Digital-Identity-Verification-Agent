import cv2
import pytesseract
import easyocr

reader = easyocr.Reader(['en'])

def preprocess(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return thresh

def extract_text(image_path):
    img = preprocess(image_path)
    text1 = pytesseract.image_to_string(img)
    text2 = reader.readtext(image_path, detail=0)
    return text1 + " ".join(text2)
