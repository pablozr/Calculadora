
from PySide6.QtWidgets import QPushButton, QGridLayout
from constants import MEDIUM_FONT_SIZE
from utils import is_empty, is_num_or_dot, is_valid_number, conver_to_number
from display import Display
from PySide6.QtCore import Slot
from info import Info
import math
from main_window import MainWindow

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configstyle()

    def configstyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: MainWindow, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self._grid_mask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]

        self.display = display   # getting acess to display
        self.info = info
        self.window = window
        self._equation = ''
        self._equation_initial = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equation_initial  
        self._make_grid()
    
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _make_grid(self):
        # giving funcionality to the pressed keys
        self.display.eq_pressed.connect(self._eq) # enter or equal
        self.display.del_pressed.connect(self._backspace)
        self.display.clear_pressed.connect(self._clear) # esc
        self.display.input_pressed.connect(self._insert_to_display) # numbers
        self.display.operator_pressed.connect(self._config_left_op)

        for row_number, row in enumerate(self._grid_mask):
            for column_number, button_text in enumerate(row):  # each row is a new list so we can do a for to get the button text
                button = Button(button_text) # and by using enumerate, we can locate them to put on the right order

                if not is_num_or_dot(button_text) and not is_empty(button_text):
                    button.setProperty('cssClass', 'specialButton') # linking the buttons I want to the style
                    self._config_special_button(button) # configurating special buttons

                self.addWidget(button, row_number, column_number)
                slot = self._make_slot(self._insert_to_display, button_text,)
                self._connect_button_clicked(button, slot)


    def _connect_button_clicked(self, button, slot):
        button.clicked.connect(slot)

    def _config_special_button(self, button):
        text = button.text()

        if text == 'C':
            self._connect_button_clicked(button, self._clear)

        if text in '+-/*^':
            self._connect_button_clicked(button, self._make_slot(self._config_left_op, text))

        if text == '=':
            self._connect_button_clicked(button, self._eq)

        if text == 'N':
            self._connect_button_clicked(button, self._invert_number)
        
        if text == 'D':
            self._connect_button_clicked(button, self.display.backspace)

    def _make_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def realslot():
            func(*args, **kwargs)
        return realslot
    
    @Slot()
    def _insert_to_display(self, text): 
        new_display_value = self.display.text() + text

        if not is_valid_number(new_display_value):
            return
        self.display.insert(text)
        self.display.setFocus()

   # adding the Negative numbers funcionality by pressing the N
    @Slot()
    def _invert_number(self):
        display_text = self.display.text()

        
        if not is_valid_number(display_text):
            return
        
        new_number = conver_to_number(display_text) * -1 # inverting number
        self.display.setText(str(new_number))
        self.display.setFocus()


    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equation_initial
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _config_left_op(self, text):
        display_text = self.display.text() # left number  '_left'
        self.display.clear()  # when you click on any operators it will clear display bc i want to get the number and put on memory
        self.display.setFocus()

        # if the person clicked on operator without configurating any number before
        if not is_valid_number(display_text) and self._left is None:
            self._show_error('Você não digitou nada')
            return
        
        # if there is something on left number, we do nothing, we wait for right number
        if self._left is None:
            self._left = conver_to_number(display_text)

        self._op = text
        self.equation = f'{self._left} {self._op}'

    # configurating '=' button with the right number
    @Slot()
    def _eq(self):
        display_text = self.display.text()

        if not is_valid_number(display_text) or self._left is None:
            self._show_error("Você não digitou o outro número")
            return
        
        self._right = conver_to_number(display_text)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'   # default value
        
        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = conver_to_number(str(result))
            
            else:
              result = eval(self.equation)
        except ZeroDivisionError:
            self._show_error("Divisão por zero")
        except OverflowError:
            self._show_error("Conta muito extensa")

        self.display.clear()  # clear after calculating
        self.info.setText(f'{self.equation} = {result}')
        self._left = result     # sets left number as the previous result to continue calculating
        self._right = None      # sets right number as none to continue calculating
        self.display.setFocus()

        if result == 'error':  # if it cant calculate result will take the default value names as error
            self._left = None
    
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()
    
    def _make_dialog(self, text):
        msg_box = self.window.make_msg_box()
        msg_box.setText(text)
        return msg_box
    
    def _show_error(self, text):
        msg_box = self._make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Critical)
        msg_box.exec()
        self.display.setFocus()

    def _show_info(self, text):
        msg_box = self._make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Information)
        msg_box.exec()