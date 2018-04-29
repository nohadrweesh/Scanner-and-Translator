from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import pytesseract
import cv2
import matplotlib.pyplot as plt
import requests
import imutils


class GuiForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.scannedText=""
        self.translatedText=""
        self.img=None
        self.ui = Ui_Scanner()
        self.ui.setupUi(self)
        #open file
        self.ui.actionOpen.triggered.connect(self.file_save_scanned)
        self.ui.actionSave.triggered.connect(self.file_save_translated)

        
        
        self.ui.btnStart.clicked.connect(self.choose_captured)
        self.ui.btnCapture.clicked.connect(self.take_pic)
        # self.ui.lineEdit.textChanged.connect(self.set_filter_val)
        
    
    

    def choose_captured(self):
        print("start_capturing_packets")
        name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        print('opend file '+name)
        if name != '':
            #resize to show
            imgOrigin=cv2.imread(name)
            img = imutils.resize(imgOrigin,width=270,height=400)
            image = QtGui.QImage(img, img.shape[1],\
                            img.shape[0], img.shape[1] * 3,QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap(image)
            pixmap = QtGui.QPixmap(pix)
            self.ui.imgLabel.setPixmap(pixmap)
            self.ui.imgLabel.show()
            
            print("img named "+name)
            stext=process_img(name)
            self.ui.scanned_view.setText(stext)
            print(stext)
            trText=translate(stext)
            
            print("===================")
            print(trText)
            self.ui.translated_view.setText(trText)
            self.scannedText=stext
            self.translatedText=trText
            self.img=img


    
    def take_pic(self):
        cam = cv2.VideoCapture(0)
        frame = cam.read()[1]
        cv2.imwrite(filename='img.jpg', img=frame)
        cam.release()
        imgOrigin=cv2.imread('img.jpg')
        img = imutils.resize(imgOrigin,width=270,height=400)
        image = QtGui.QImage(img, img.shape[1],\
                        img.shape[0], img.shape[1] * 3,QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
        pixmap = QtGui.QPixmap(pix)
        self.ui.imgLabel.setPixmap(pixmap)
        self.ui.imgLabel.show()
            
            
        stext=process_img('img.jpg')
        self.ui.scanned_view.setText(stext)
        print(stext)
        trText=translate(stext)
            
        print("===================")
        print(trText)
        self.ui.translated_view.setText(trText)
        self.scannedText=stext
        self.translatedText=trText
        self.img=img

    def file_save_scanned(self):
        print("file_open")
        name, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Scanned', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        print('opend file '+name)
        if name != '':
                
            f = open(name+'.txt','w')
            f.write(self.scannedText)
            f.close()
        

    
        
            


    def file_save_translated(self):
        print("file_save")
        name, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Translated', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        print('opend file '+name)
        if name != '':
                
            f = open(name+'.txt','w')
            f.write(self.translatedText)
            f.close()
            
def process_img(imgName):
    img=cv2.imread(imgName)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 

    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray)
    #search for ("Success")
    return text
    
def translate(text):
    content = {"name":text}


    r = requests.get("https://script.google.com/macros/s/AKfycbyXcCEGICNYUj5Pch1ZQxEnR2E7YBWZ_eVlgSlaUouTdf_XIf0s/exec",verify=True, params=content)
    text=r.text
    str_sucess='("Success")'
    newText=text
    if str_sucess in text:
        print ("found")
        newText=text.replace(str_sucess, '')
    return newText
    #return r.text

class Ui_Scanner(object):
    def setupUi(self, Scanner):
        Scanner.setObjectName("Scanner")
        Scanner.resize(1360, 693)
        self.centralwidget = QtWidgets.QWidget(Scanner)
        self.centralwidget.setObjectName("centralwidget")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(20, 10, 270, 30))
        self.btnStart.setObjectName("btnStart")
        self.btnCapture = QtWidgets.QPushButton(self.centralwidget)
        self.btnCapture.setGeometry(QtCore.QRect(20, 50, 270, 30))
        self.btnCapture.setObjectName("btnCapture")
        
        self.imgLabel=QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setGeometry(QtCore.QRect(20, 90, 270, 400))
        self.imgLabel.setObjectName("imgLabel")
        
        
        

        #scanned view
        self.scanned_view = QtWidgets.QTextBrowser(self.centralwidget)
        self.scanned_view.setGeometry(QtCore.QRect(300, 10, 520, 693))
        self.scanned_view.setObjectName("scanned_view")
        self.scanned_view.setText("Scanned Text")
        
        #translated view
        self.translated_view = QtWidgets.QTextBrowser(self.centralwidget)
        self.translated_view.setGeometry(QtCore.QRect(830, 10, 520, 693))
        self.translated_view.setObjectName("translated_view")
        self.translated_view.setText("Translated Text")


        



        Scanner.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Scanner)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 708, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        Scanner.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Scanner)
        self.statusbar.setObjectName("statusbar")
        Scanner.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(Scanner)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(Scanner)
        self.actionSave.setObjectName("actionSave")
        
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        
        self.menubar.addAction(self.menuFile.menuAction())

        

        self.retranslateUi(Scanner)
        QtCore.QMetaObject.connectSlotsByName(Scanner)

    def retranslateUi(self, Scanner):
        _translate = QtCore.QCoreApplication.translate
        Scanner.setWindowTitle(_translate("Scanner", "Document Scanner and Translator"))
        self.btnStart.setText(_translate("Scanner", "Choose Picture"))
        self.btnCapture.setText(_translate("Scanner", "Capture Picture"))
        
        self.menuFile.setTitle(_translate("Scanner", "File"))
        self.actionOpen.setText(_translate("Scanner", "Save Scanned"))
        self.actionSave.setText(_translate("Scanner", "Save Translated"))
        







from PyQt5.QtCore import QObject, pyqtSignal

if __name__ == "__main__":
    # sniffer = Sniffer()
    # sniffer.start()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Scanner = GuiForm()

    Scanner.show()

    sys.exit(app.exec_())