from PyQt4 import QtCore, QtGui
import csv
import getpass
import sys
import os
import cfscrape
from bs4 import BeautifulSoup as bs
import requests
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
class WTF_EXCPTN(Exception):
    pass

class parser (object):
    def __init__ (self, src):
        self.soup_obj = src
        self.output   = None
        pass

    def prepare (self):
        try:
            prep = lambda x,y=0: self.soup_obj.select (x)[y].text.encode ('utf-8')
            self.output = ( { 'date'     : prep ("div.td a[href^=/date/]"),
                      'id'       : self.soup_obj.select ("div.td h3 a[href^=/exploit/description/]")[0]['href'].lstrip \
                            ('/exploit/description/'),
                      'name'     : prep ("div.td h3 a[href^=/exploit/description/]"),
                      'platform' : prep ("div.td a[href^=/platforms/]"),
                      'level'    : prep ("div.TipText", 1).lstrip ('\nSecurity Risk')[:-1],
                      'verified' : ("check" in self.soup_obj.select ("div.allow_tip.td img[src$=.png]")[0]['src']),
                      'author'   : prep ("div.allow_tip.td a[href^=/author/]")
                } )

        except (Exception):
            pass

        finally:
            return (True)
            
    def __call__ (self):
        self.prepare ()
        return (self.output)

class zero_day (object):
    def __init__ (self, kw=None):
        (self.site, self.kw, self.app) = \
        ("https://en.0day.today/", kw, "search?search_request=")
        self.session = cfscrape.create_scraper()
        pass

    
    def onayla(self):
        self.session.post(self.site, data={'agree' : 'Yes, I agree'})
        return (True)

    def ara (self):
        resp = self.session.get("{0.site}{0.app}{0.kw}".format (self)).text.encode ('utf-8')
        src  = bs (resp, 'html.parser')
        exps = src.findAll ('div', attrs={ 'class':'ExploitTableContent' })
        return (filter(None, list (map (lambda x: parser(x)(), exps))))

    def surdur (self):
        self.onayla ()
        exps = self.ara ()
        return ('\n'.join ([str (pretty_out (EXP)) for EXP in exps]))
        #for EXP in exps:
            #print (pretty_out (EXP))
            #self.textBrowser.append(pretty_out(EXP))
         
            
        

    @classmethod
    def __call__ (cls, kw):
        return (cls (kw=kw).surdur ())

class pretty_out (object):
    def __init__ (self, liste):
        self.liste = """<0day.today>
[{name}]-[{id}]
<[{date} - {platform} - {level}]>
Yazar: @{author}\n""".format (**liste)
        
    def __str__ (self):
        return (self.liste)

    def __repr__ (self):
        return (self.liste)
     
class arama:
    def __init__(self,kw=None):
            
        self.kw = kw
        self.session = cfscrape.create_scraper()
        pass

    def update(self):
            
        try:
                os.remove("files.csv")
        except:
                pass
        r = requests.get("https://raw.githubusercontent.com/offensive-security/exploit-database/master/files.csv")
        benim_dosyam = open("files.csv", "w")
        benim_dosyam.write(r.text.encode('utf-8'))
    def bul(self):
        self.update()
        with open('files.csv', 'r') as f:
            self.r = csv.reader(f)
            for row in self.r:
                for i in row:
                    if str(self.kw) in i.lower():
                        yield (
                            '<exploit.db>\n' \
                            '[{r[2]}]-[{r[0]}]\n' \
                            '<[{r[3]} - {r[5]} - {r[6]}]>\n' \
                            'Yazar: @{r[4]}\n <[http://www.exploit-db.com/exploits/{r[0}]>\n\n'.format(r=row)
                        )
                        
    
    @classmethod
    def __call__(cls,kw):
        return (cls (kw=kw).bul())

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(769, 624)
        self.line = QtGui.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(220, 0, 41, 421))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(240, 60, 531, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(350, 10, 221, 21))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(250, 10, 41, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Norse"))
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(25, 230, 560, 190))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        pixmap = QtGui.QPixmap('images.jpg')
        self.label_2.setPixmap(pixmap)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(590, 10, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        Form.connect(self.pushButton, QtCore.SIGNAL("clicked()"),self.b_click)
        self.textBrowser = QtGui.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(290, 80, 431, 331))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(5, 422, 761, 201))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        pixmap1 = QtGui.QPixmap('ravennlogo.jpg')
        self.label_3.setPixmap(pixmap1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def b_click(self):
        kw = self.lineEdit.text()
        (edb, zday) = ('\n'.join ([exp for exp in arama()(kw)]), zero_day()(kw))
        map(self.textBrowser.append, [edb, zday])
        
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "RAVEN", None))
        self.label.setText(_translate("Form", "Ara:", None))
        #self.label_2.setText(_translate("Form", "Resim", None))
        self.pushButton.setText(_translate("Form", "Ara!", None))
        #self.label_3.setText(_translate("Form", "TextLabel", None))

def main ():
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

if (__name__ == "__main__"): main()
