from PySide6.QtWidgets import QLineEdit
from constants import BIG_FONT_SIZE, TEXT_MARGINS, MINIMUM_WIDTH
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from utils import is_empty, is_num_or_dot

class Display(QLineEdit):
    eq_pressed = Signal()
    del_pressed = Signal()
    clear_pressed = Signal()  # esc key for clear
    input_pressed = Signal(str)
    operator_pressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.configstyle()

    def configstyle(self):
        margins = [TEXT_MARGINS for _ in range(4)] # list comprehension for set margins(left, right, top, bottom)
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 4)    # minimum height of the input box
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight) # changing where the words start to the right
        self.setTextMargins(*margins)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        is_enter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        is_delete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        is_esc = key in [KEYS.Key_Escape, KEYS.Key_C]
        is_operator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]

        # emiting signal when you press enter on keyboard
        if is_enter:
            self.eq_pressed.emit()
            return event.ignore
        
        # emiting signal when you press backspace on keyboard
        if is_delete:
            self.del_pressed.emit()
            return event.ignore
        
        # emiting signal when you press esc on keyboard
        if is_esc:
            self.clear_pressed.emit()
            return event.ignore
        
        if is_operator:
            if text.lower() == 'p':
                text = '^'
            self.operator_pressed.emit(text)
            return event.ignore
        
        # if it doesn't have text it wont pass from here
        if is_empty(text):
            return event.ignore()
        
        # emiting signal when you press numbers on keyboard (it prevents the user from pressing words)
        if is_num_or_dot(text):    
            self.input_pressed.emit(text)
            return event.ignore()
