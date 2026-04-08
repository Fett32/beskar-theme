def button() -> str:
    return """
        QPushButton {
            background-color: #252d3a;
            color: #d0d0d0;
            border: 1px solid #3a4455;
            border-radius: 4px;
            padding: 4px 10px;
        }
        QPushButton:hover { background-color: #344050; }
        QPushButton:pressed { background-color: #1a2230; }
        QPushButton:disabled { color: #555; background-color: #1e1e1e; }
    """


def input_field() -> str:
    return """
        QLineEdit {
            background-color: #252d3a;
            color: #d0d0d0;
            border: 1px solid #3a4455;
            border-radius: 4px;
            padding: 4px 8px;
            selection-background-color: #3c4a6a;
        }
        QLineEdit:focus { border-color: #ffd100; }
    """


def dialog() -> str:
    return """
        background-color: #1a2230;
        color: #d0d0d0;
    """


def scrollbar() -> str:
    return """
        QScrollBar:vertical {
            background: #1a2230;
            width: 6px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #3a4455;
            border-radius: 3px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover { background: #ffd100; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    """
