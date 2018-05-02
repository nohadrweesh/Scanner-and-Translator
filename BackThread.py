from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore
import cv2
from PIL import Image
import pytesseract
import requests

class BackThread (QObject, Thread):
    process_img = pyqtSignal(str)
    translate_txt = pyqtSignal(str)
    

    def __init__(self,parent=None):
        super(BackThread, self).__init__(parent)
        self.isDone=False
        self.img=''
        self.scannedTxt=""
        self.translatedTxt=""
        

    def processImg(self ):
        print("processImg")
        if self.img != '':
            img =cv2.imread(self.img)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            gray = cv2.medianBlur(gray, 3)
            self.scannedTxt = pytesseract.image_to_string(gray)
            self.process_img.emit(self.scannedTxt)
            self.translateText()
            print("sc "+self.scannedTxt)
        
    def translateText(self ):
        print("translateText")
        content = {"name":self.scannedTxt}
        r = requests.get("https://script.google.com/macros/s/AKfycbyXcCEGICNYUj5Pch1ZQxEnR2E7YBWZ_eVlgSlaUouTdf_XIf0s/exec",verify=True, params=content)
        text=r.text
        str_sucess='("Success")'
        self.translatedTxt=text
        print("tr "+self.translatedTxt)
        if str_sucess in text:
            print ("found")
            self.translatedTxt=text.replace(str_sucess, '')
        self.translate_txt.emit(self.translatedTxt)
        
        
    def run(self):
        print("running")
        while True:
            if self.img != '':
                print("not none")
                self.processImg()
                self.translateText()
                self.img = ''
