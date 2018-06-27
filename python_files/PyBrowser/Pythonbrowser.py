#from PyQt5.QtCore import QUrl
#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtWebKitWidgets import QWebView, sys

#app = QApplication(sys.argv)
#view = QWebView()
#view.show()
#view.setUrl(QUrl(“http://www.google.com”))
#app.exec()


from PyQt5.QtWidgets import QApplication, QWidget
from ui_output import Ui_Form

class MainWindow(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pressed)

    def pressed(self):
        self.webView.setUrl(QUrl(self.lineEdit.displayText()))

view = MainWindow()
