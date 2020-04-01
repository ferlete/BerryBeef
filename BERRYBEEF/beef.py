"""berrybeef.beef: provides entry point main()."""

import sys
from PyQt5.QtWidgets import  QApplication


from .Info import Info
from BERRYBEEF.Main import MainWindow
from BERRYBEEF.constants import *


def main():

    try:

        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        print('Screen: %s' % screen.name())
        size = screen.size()
        print('Size: %d x %d' % (size.width(), size.height()))
        rect = screen.availableGeometry()
        print('Available: %d x %d' % (rect.width(), rect.height()))

        info = Info('Valter Ferlete', 'ferlete@gmail.com')
        print(SOFTWARE_NAME)
        print("Author %s" % info.author)

        window = MainWindow(SOFTWARE_NAME, rect.width(), rect.height())
        window.show()
        sys.exit(app.exec_())

    except Exception as ex:
        print(ex)
