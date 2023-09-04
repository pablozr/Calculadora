from PySide6.QtWidgets import QApplication
import sys
from main_window import MainWindow
from constants import WINDOW_ICON_PATH
from PySide6.QtGui import QIcon
from display import Display
from info import Info
from styles import setup_theme
from buttons import Button, ButtonsGrid


if __name__ == '__main__':

    # Basic Application start
    app = QApplication(sys.argv) 
    setup_theme()
    window =  MainWindow()

    # Defines the icon
    icon = QIcon(str(WINDOW_ICON_PATH))  
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info('a')
    window.add_widget_to_vlayout(info)

    # Display
    display = Display()
    window.add_widget_to_vlayout(display)

    #Grid
    buttons_grid = ButtonsGrid(display, info, window)  # ButtonsGrid it's another layout
    window.v_layout.addLayout(buttons_grid)   # adding a layout inside other layout

    # loop
    window.adjust_fixed()
    window.show()
    app.exec()  