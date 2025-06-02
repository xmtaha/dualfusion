from PyQt5.QtGui import QPalette, QColor

def apply_nordic_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(46, 52, 64))
    palette.setColor(QPalette.WindowText, QColor(236, 239, 244))
    palette.setColor(QPalette.Base, QColor(59, 66, 82))
    palette.setColor(QPalette.AlternateBase, QColor(67, 76, 94))
    palette.setColor(QPalette.ToolTipBase, QColor(236, 239, 244))
    palette.setColor(QPalette.ToolTipText, QColor(46, 52, 64))
    palette.setColor(QPalette.Text, QColor(236, 239, 244))
    palette.setColor(QPalette.Button, QColor(76, 86, 106))
    palette.setColor(QPalette.ButtonText, QColor(236, 239, 244))
    palette.setColor(QPalette.BrightText, QColor(191, 97, 106))
    palette.setColor(QPalette.Highlight, QColor(94, 129, 172))
    palette.setColor(QPalette.HighlightedText, QColor(236, 239, 244))
    app.setPalette(palette)
    app.setStyle("Fusion")
