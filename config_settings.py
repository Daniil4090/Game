from PyQt5 import QtWidgets
from config_settings_design import Ui_Form
import sys


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox.addItem("Полный экран")
        self.ui.comboBox.addItem("[500, 500]")
        self.ui.comboBox.addItem("[1000, 1000]")
        self.ui.comboBox.addItem("[1500, 1500]")
        self.ui.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        file = open("data/config.txt", "w", encoding="utf-8")
        if self.ui.comboBox.currentText() == "Полный экран":
            file.write("[0, 0]\n")
        else:
            file.write(self.ui.comboBox.currentText() + "\n")
        if not self.ui.lineEdit.text():
            file.write("Quest")
        else:
            file.write(self.ui.lineEdit.text())


app = QtWidgets.QApplication([])
application = App()
application.show()
sys.exit(app.exec())
