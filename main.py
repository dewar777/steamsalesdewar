import requests
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel
from bs4 import BeautifulSoup
from ui import Ui_MainWindow
import sys
import re
from natsort import natsorted, ns
lst = []
lst2 = []
lst3 = []
finlist = []


def main(count):
    surl = 'https://store.steampowered.com/search/?sort_by=&sort_order=0&specials=1&filter=topsellers&page='
    for k in range(count + 1):
        url = surl + str(k)
        get_data(gethtml(url))


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet("background-image: url(binaries/backgroundmain.png);")
        self.setWindowIcon(QIcon('binaries/icon.png'))
        self.setWindowTitle('Steam Sales Finder by dewar')
        self.ui.listWidget.setStyleSheet("background-image: url(binaries/background.png);color: rgb(255, 255, 255);")
        self.ui.pushButton.setStyleSheet("background-image: url(binaries/background.png);color: rgb(255, 255, 255);")
        self.ui.pushButton_2.setStyleSheet("background-image: url(binaries/background.png);color: rgb(255, 255, 255);")
        self.ui.spinBox.setStyleSheet("background-image: url(binaries/background.png); color: rgb(0, 39, 75);")
        self.ui.pushButton.clicked.connect(self.btnClicked)
        self.ui.pushButton_2.clicked.connect(self.btnClicked_2)

    def btnClicked(self):
        count = self.ui.spinBox.value()
        main(count)
        text = str(self.ui.comboBox.currentText())
        if text == "По порядку":
            for h in range(len(finlist)):
                self.ui.listWidget.addItem(finlist[h])
        elif text == "По алфавиту":
            for h in range(len(finlist)):
                self.ui.listWidget.addItem(natsorted(finlist)[h])

    def btnClicked_2(self):
        self.close()


def gethtml(url):
    r = requests.get(url)
    return r.text


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    name_tags = soup.find_all('div')
    for i in range(len(name_tags)):
        if 'class="responsive_search_name_combined"' in str(name_tags[i]):
            if 'class="col search_name ellipsis">' in str(name_tags[i]):
                if '<strike>' in str(name_tags[i]):
                    name = re.search(r'<span class="title">(.*)</span>', str(name_tags[i]))
                    if name.group(0) is not None:
                        lst.append(name.group(0))
            if 'class="col search_price_discount_combined responsive_secondrow" data-price-final=' in str(name_tags[i]):
                if 'style="color: #888888;"' in str(name_tags[i]):
                    price = re.search(r'<strike>(.*)</strike>', str(name_tags[i]))
                    if price is not None:
                        lst2.append(price.group(0))
                    newprice = re.search(r'<span(.*)</div>', str(name_tags[i]))
                    if newprice is not None:
                        lst3.append(newprice.group(0))

    for j in range(len(lst)):
        line = str(lst[j][20:-7]) + ", старая цена - " + str(lst2[j][8:-9]) + ", новая цена - " + str(lst3[j][67:-6])
        if str(lst3[j][67]) == ">":
            line = str(lst[j][20:-7]) + ", старая цена - " + str(lst2[j][8:-9]) + ", новая цена - " + str(lst3[j][68:-6])
        if len(str(lst3[j][68:-6])) > 1 and line not in finlist:
            finlist.append(line)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
