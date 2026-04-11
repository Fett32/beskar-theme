from PySide6.QtGui import QColor

# Surfaces
SURFACE_BASE    = QColor(22, 22, 22)       # #161616 — deepest background
SURFACE_RAISED  = QColor(30, 30, 30)       # #1e1e1e — window bg
SURFACE_OVERLAY = QColor(26, 34, 48)       # #1a2230 — dialogs, panels
SURFACE_INPUT   = QColor(37, 45, 58)       # #252d3a — fields, inputs
SURFACE_DOCK_HEADER = QColor(22, 28, 40)   # #161c28 — dock header band
SURFACE_ALT     = QColor(35, 35, 35)       # alternateBase

# Borders
BORDER             = QColor(58, 68, 85)       # #3a4455 — general purpose
BORDER_OUTER_FRAME = QColor(50, 62, 82)        # #323e52 — window-level border
BORDER_INNER_FRAME = QColor(42, 52, 69)       # #2a3445 — dock/canvas panels
BORDER_MENU_FRAME  = QColor(58, 68, 85)       # #3a4455 — tab bar, section dividers
BORDER_HOVER       = QColor(52, 64, 80)       # #344050

# Text
TEXT            = QColor(208, 208, 208)    # #d0d0d0
TEXT_BRIGHT     = QColor(255, 255, 255)    # #ffffff
TEXT_SLOT       = QColor(180, 175, 160)
TEXT_LABEL      = QColor(140, 148, 160)
TEXT_DIM        = QColor(80, 88, 100)

# Accents
ACCENT_YELLOW   = QColor(255, 209, 0)      # #ffd100 — focus / OSHA yellow
ACCENT_BLUE     = QColor(107, 180, 230)    # #6bb4e6 — headers
ACCENT_LINK     = QColor(90, 160, 230)

# Menus (top menu bar, context menus, flyout pickers)
MENU_BG          = QColor(26, 34, 48)        # #1a2230 — menu background
MENU_BG_HOVER    = QColor(37, 45, 58)        # #252d3a — hovered item
MENU_BORDER      = QColor(58, 68, 85)        # #3a4455 — menu outline
MENU_SEPARATOR   = QColor(58, 68, 85)        # #3a4455 — divider lines
MENU_TEXT        = QColor(208, 208, 208)     # #d0d0d0 — normal item text
MENU_TEXT_DIM    = QColor(80, 88, 100)       # #505864 — disabled items

# Semantic
HIGHLIGHT       = QColor(60, 120, 200)
SELECTION_GREEN = QColor(60, 120, 0)       # #3c7800
TERMINAL_GREEN  = QColor(140, 200, 124)    # #8cc87c
BUTTON          = QColor(45, 45, 45)
BUTTON_TEXT     = QColor(208, 208, 208)
