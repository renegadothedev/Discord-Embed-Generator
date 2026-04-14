import sys
import json
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QTextEdit, QLabel, QScrollArea, QColorDialog, 
    QCheckBox, QPushButton, QFrame, QGridLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QTimer, QSize
from PyQt6.QtGui import QColor, QFont, QPixmap, QImage
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

# --- DESIGN SYSTEM ---
COLORS = {
    "bg": "#1E1F22",
    "card": "#2B2D31",
    "sidebar": "#111214",
    "accent": "#5865F2",
    "accent_hover": "#4752C4",
    "success": "#23A559",
    "danger": "#F23F42",
    "text": "#F2F3F5",
    "muted": "#949BA4"
}

STYLE_SHEET = f"""
QMainWindow {{ background-color: {COLORS['bg']}; }}
QWidget {{ color: {COLORS['text']}; font-family: 'Segoe UI Semibold', sans-serif; }}

/* Stylized Scrollbar */
QScrollBar:vertical {{ border: none; background: transparent; width: 5px; }}
QScrollBar::handle:vertical {{ background: {COLORS['accent']}; border-radius: 2px; }}

/* Elite Inputs */
QLineEdit, QTextEdit {{ 
    background-color: {COLORS['sidebar']}; 
    border: 2px solid {COLORS['sidebar']}; 
    border-radius: 6px; 
    padding: 12px; 
    color: white; 
    font-size: 13px;
}}
QLineEdit:focus {{ border: 2px solid {COLORS['accent']}; }}

/* Modern Buttons */
QPushButton {{ 
    background-color: {COLORS['accent']}; 
    color: white; 
    border-radius: 6px; 
    padding: 15px; 
    font-weight: bold; 
    font-size: 14px;
    border: none;
}}
QPushButton:hover {{ background-color: {COLORS['accent_hover']}; }}
QPushButton#Secondary {{ background-color: #35373C; }}
QPushButton#Secondary:hover {{ background-color: #4E5058; }}

.LabelHeading {{ 
    font-size: 11px; 
    font-weight: 800; 
    color: {COLORS['muted']}; 
    text-transform: uppercase; 
    letter-spacing: 1.5px;
    margin-top: 15px;
}}
"""

class AsyncImage(QLabel):
    def __init__(self, size=(40, 40)):
        super().__init__()
        self.setFixedSize(size[0], size[1])
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self._render)

    def load(self, url):
        if url and url.startswith("http"):
            self.manager.get(QNetworkRequest(QUrl(url)))
        else: self.clear()

    def _render(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            img = QImage()
            img.loadFromData(reply.readAll())
            self.setPixmap(QPixmap.fromImage(img).scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        reply.deleteLater()

class FieldWidget(QFrame):
    changed = pyqtSignal()
    delete = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {COLORS['sidebar']}; border-radius: 10px;")
        layout = QHBoxLayout(self)
        self.n = QLineEdit(placeholderText="Field Name")
        self.v = QLineEdit(placeholderText="Field Value")
        self.i = QCheckBox("Inline")
        self.btn = QPushButton("✕")
        self.btn.setFixedSize(30, 30)
        self.btn.setObjectName("Secondary")
        self.btn.clicked.connect(lambda: self.delete.emit(self))
        
        for w in [self.n, self.v, self.i, self.btn]:
            layout.addWidget(w)
            if hasattr(w, 'textChanged'): w.textChanged.connect(self.changed.emit)
            elif isinstance(w, QCheckBox): w.stateChanged.connect(self.changed.emit)

class EliteEmbedStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord Messiah Studio Elite | v3.0")
        self.setMinimumSize(1400, 900)
        self.setStyleSheet(STYLE_SHEET)
        self.color_hex = COLORS['accent']
        self.fields = []
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0,0,0,0)

        # --- CONTROL PANEL (LEFT) ---
        sidebar = QFrame()
        sidebar.setFixedWidth(480)
        sidebar.setStyleSheet(f"background: {COLORS['bg']}; border-right: 1px solid #2B2D31;")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(30, 30, 30, 30)

        side_layout.addWidget(QLabel("🚀 WEBHOOK CONFIG"))
        self.webhook_url = QLineEdit(placeholderText="https://discord.com/api/webhooks/...")
        side_layout.addWidget(self.webhook_url)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        self.form = QVBoxLayout(container)

        self.add_sec("IDENTITY")
        self.auth_n = QLineEdit(placeholderText="Author Name")
        self.auth_i = QLineEdit(placeholderText="Author Icon URL")
        self.form.addWidget(self.auth_n)
        self.form.addWidget(self.auth_i)

        self.add_sec("MESSAGE CONTENT")
        self.title_in = QLineEdit(placeholderText="Embed Title")
        self.desc_in = QTextEdit(placeholderText="Main description (Markdown supported)... \nExample: **Bold**, *Italic*")
        self.form.addWidget(self.title_in)
        self.form.addWidget(self.desc_in)

        self.add_sec("VISUAL DESIGN")
        col_btn = QPushButton("PICK BORDER COLOR")
        col_btn.setObjectName("Secondary")
        col_btn.clicked.connect(self.pick_color)
        self.thumb_in = QLineEdit(placeholderText="Thumbnail URL (Top Right)")
        self.img_in = QLineEdit(placeholderText="Main Banner URL (Large Image)")
        self.form.addWidget(col_btn)
        self.form.addWidget(self.thumb_in)
        self.form.addWidget(self.img_in)

        self.add_sec("DYNAMIC FIELDS")
        self.f_box = QVBoxLayout()
        self.form.addLayout(self.f_box)
        add_f = QPushButton("+ ADD NEW FIELD")
        add_f.setObjectName("Secondary")
        add_f.clicked.connect(self.new_f)
        self.form.addWidget(add_f)

        self.add_sec("NOTIFICATION")
        self.footer_in = QLineEdit(placeholderText="Footer Text")
        self.form.addWidget(self.footer_in)

        scroll.setWidget(container)
        side_layout.addWidget(scroll)

        # Master Send Button
        self.send_btn = QPushButton("⚡ SEND TO DISCORD")
        self.send_btn.setMinimumHeight(65)
        self.send_btn.clicked.connect(self.send_to_webhook)
        side_layout.addWidget(self.send_btn)

        main_layout.addWidget(sidebar)

        # --- PREVIEW AREA (RIGHT) ---
        prev_area = QFrame()
        prev_area.setStyleSheet(f"background: {COLORS['sidebar']};")
        p_layout = QVBoxLayout(prev_area)
        p_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Professional Shadow Card
        self.card = QFrame()
        self.card.setFixedWidth(540)
        self.card.setObjectName("Card")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0,0,0,180))
        self.card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        # Author Layout
        a_row = QHBoxLayout()
        self.p_auth_i = AsyncImage((24,24))
        self.p_auth_n = QLabel("")
        self.p_auth_n.setStyleSheet("font-weight: bold; font-size: 14px;")
        a_row.addWidget(self.p_auth_i)
        a_row.addWidget(self.p_auth_n)
        a_row.addStretch()

        # Content (Title + Description + Thumbnail)
        m_row = QHBoxLayout()
        m_vbox = QVBoxLayout()
        self.p_title = QLabel("Example Title")
        self.p_title.setStyleSheet("color: #00A8FC; font-size: 17px; font-weight: bold;")
        self.p_desc = QLabel("Start configuring on the left panel...")
        self.p_desc.setWordWrap(True)
        m_vbox.addWidget(self.p_title)
        m_vbox.addWidget(self.p_desc)
        self.p_thumb = AsyncImage((80, 80))
        m_row.addLayout(m_vbox)
        m_row.addWidget(self.p_thumb)

        # Fields Grid
        self.p_f_grid = QGridLayout()
        self.p_f_grid.setSpacing(15)

        # Large Image and Footer
        self.p_main_i = AsyncImage((500, 280))
        self.p_main_i.setFixedSize(500, 0)
        self.p_footer = QLabel("")
        self.p_footer.setStyleSheet(f"color: {COLORS['muted']}; font-size: 12px; margin-top: 10px;")

        card_layout.addLayout(a_row)
        card_layout.addLayout(m_row)
        card_layout.addLayout(self.p_f_grid)
        card_layout.addWidget(self.p_main_i)
        card_layout.addWidget(self.p_footer)

        p_layout.addWidget(self.card)
        main_layout.addWidget(prev_area, 1)

        # Live Preview Signals
        for i in [self.auth_n, self.auth_i, self.title_in, self.desc_in, self.thumb_in, self.img_in, self.footer_in]:
            if hasattr(i, 'textChanged'): i.textChanged.connect(self.sync)

        self.sync()

    def add_sec(self, text):
        label = QLabel(text)
        label.setProperty("class", "LabelHeading")
        self.form.addWidget(label)

    def new_f(self):
        f = FieldWidget()
        f.changed.connect(self.sync)
        f.delete.connect(self.del_f)
        self.fields.append(f)
        self.f_box.addWidget(f)
        self.sync()

    def del_f(self, f):
        f.deleteLater()
        self.fields.remove(f)
        self.sync()

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_hex = color.name()
            self.sync()

    def sync(self):
        self.p_auth_n.setText(self.auth_n.text())
        self.p_auth_i.load(self.auth_i.text())
        self.p_title.setText(self.title_in.text() or "Embed Title")
        self.p_desc.setText(self.desc_in.toPlainText() or "Description will appear here...")
        self.p_thumb.load(self.thumb_in.text())
        self.p_footer.setText(self.footer_in.text())
        
        if self.img_in.text():
            self.p_main_i.setFixedHeight(280)
            self.p_main_i.load(self.img_in.text())
        else:
            self.p_main_i.setFixedHeight(0)

        self.card.setStyleSheet(f"#Card {{ background: {COLORS['card']}; border-left: 5px solid {self.color_hex}; border-radius: 5px; }}")

        for i in reversed(range(self.p_f_grid.count())):
            self.p_f_grid.itemAt(i).widget().setParent(None)
        
        row, col = 0, 0
        for f in self.fields:
            if f.n.text():
                w = QWidget()
                v = QVBoxLayout(w)
                v.setContentsMargins(0,0,0,0)
                name_lbl = QLabel(f.n.text())
                name_lbl.setStyleSheet("font-weight: bold; color: white;")
                val_lbl = QLabel(f.v.text())
                val_lbl.setStyleSheet("color: #DBDEE1;")
                v.addWidget(name_lbl)
                v.addWidget(val_lbl)
                self.p_f_grid.addWidget(w, row, col)
                if f.i.isChecked():
                    col += 1
                    if col > 2:
                        col = 0
                        row += 1
                else:
                    row += 1
                    col = 0

    def send_to_webhook(self):
        url = self.webhook_url.text()
        if not url.startswith("https://discord.com"):
            self.send_btn.setText("❌ INVALID URL")
            QTimer.singleShot(2000, lambda: self.send_btn.setText("⚡ SEND TO DISCORD"))
            return

        data = {
            "embeds": [{
                "title": self.title_in.text(),
                "description": self.desc_in.toPlainText(),
                "color": int(self.color_hex.lstrip('#'), 16),
                "author": {"name": self.auth_n.text(), "icon_url": self.auth_i.text()},
                "footer": {"text": self.footer_in.text()},
                "thumbnail": {"url": self.thumb_in.text()},
                "image": {"url": self.img_in.text()},
                "fields": [{"name": f.n.text(), "value": f.v.text(), "inline": f.i.isChecked()} for f in self.fields if f.n.text()]
            }]
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 204:
                self.send_btn.setText("✅ SENT SUCCESSFULLY!")
                self.send_btn.setStyleSheet(f"background: {COLORS['success']};")
                QTimer.singleShot(2000, lambda: (self.send_btn.setText("⚡ SEND TO DISCORD"), self.send_btn.setStyleSheet("")))
            else:
                raise Exception
        except:
            self.send_btn.setText("❌ ERROR SENDING")
            self.send_btn.setStyleSheet(f"background: {COLORS['danger']};")
            QTimer.singleShot(2000, lambda: (self.send_btn.setText("⚡ SEND TO DISCORD"), self.send_btn.setStyleSheet("")))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = EliteEmbedStudio()
    window.show()
    sys.exit(app.exec())