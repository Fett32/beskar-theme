from PySide6.QtGui import QPalette, QColor


def make_palette() -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,          QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText,      QColor(208, 208, 208))
    palette.setColor(QPalette.ColorRole.Base,            QColor(22, 22, 22))
    palette.setColor(QPalette.ColorRole.AlternateBase,   QColor(35, 35, 35))
    palette.setColor(QPalette.ColorRole.ToolTipBase,     QColor(40, 40, 40))
    palette.setColor(QPalette.ColorRole.ToolTipText,     QColor(208, 208, 208))
    palette.setColor(QPalette.ColorRole.Text,            QColor(208, 208, 208))
    palette.setColor(QPalette.ColorRole.Button,          QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ButtonText,      QColor(208, 208, 208))
    palette.setColor(QPalette.ColorRole.BrightText,      QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link,            QColor(90, 160, 230))
    palette.setColor(QPalette.ColorRole.Highlight,       QColor(60, 120, 200))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    return palette
