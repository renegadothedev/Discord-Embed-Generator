import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QTextEdit, QLabel, QScrollArea, QColorDialog, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles import STYLE_SHEET
from logic.exporter import EmbedExporter

class FieldWidget(QWidget):
    changed = pyqtSignal()
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        self.name = QLineEdit(placeholderText="Field Name")
        self.value = QLineEdit(placeholderText="Field Value")
        self.inline = QCheckBox("Inline")
        
        for w in [self.name, self.value, self.inline]:
            layout.addWidget(w)
            if hasattr(w, 'textChanged'): w.textChanged.connect(self.changed.emit)
            else: w.stateChanged.connect(self.changed.emit)

class EmbedGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord Embed Generator")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(STYLE_SHEET)
        
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # PAINEL ESQUERDO: FORMULÁRIO
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_content = QWidget()
        self.form_layout = QVBoxLayout(form_content)
        
        self.title_input = QLineEdit(placeholderText="Título do Embed")
        self.desc_input = QTextEdit(placeholderText="Descrição...")
        self.color_btn = QPushButton("Selecionar Cor")
        self.color_hex = "#5865f2"
        
        self.form_layout.addWidget(QLabel("CONTEÚDO PRINCIPAL"))
        self.form_layout.addWidget(self.title_input)
        self.form_layout.addWidget(self.desc_input)
        self.form_layout.addWidget(self.color_btn)
        
        # Sistema de Fields dinâmicos
        self.fields = []
        self.add_field_btn = QPushButton("+ Adicionar Field")
        self.add_field_btn.clicked.connect(self.add_field)
        self.form_layout.addWidget(self.add_field_btn)

        form_scroll.setWidget(form_content)
        layout.addWidget(form_scroll, 1)

        # PAINEL DIREITO: PREVIEW
        self.preview_panel = QWidget()
        self.preview_panel.setObjectName("preview_container")
        self.preview_layout = QVBoxLayout(self.preview_panel)
        
        self.p_title = QLabel("Título Exemplo")
        self.p_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        self.p_desc = QLabel("Descrição do seu embed aparecerá aqui...")
        self.p_desc.setWordWrap(True)
        
        self.preview_layout.addWidget(self.p_title)
        self.preview_layout.addWidget(self.p_desc)
        self.preview_layout.addStretch()
        
        layout.addWidget(self.preview_panel, 1)

        # Conectar sinais para Live Preview
        self.title_input.textChanged.connect(self.update_preview)
        self.desc_input.textChanged.connect(self.update_preview)

    def add_field(self):
        fw = FieldWidget()
        fw.changed.connect(self.update_preview)
        self.fields.append(fw)
        self.form_layout.insertWidget(self.form_layout.count() - 1, fw)

    def update_preview(self):
        self.p_title.setText(self.title_input.text() or "Título Exemplo")
        self.p_desc.setText(self.desc_input.toPlainText() or "Descrição...")
        # Atualizar cor da borda lateral via QSS dinâmico
        self.preview_panel.setStyleSheet(f"border-left: 4px solid {self.color_hex};")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmbedGeneratorApp()
    window.show()
    sys.exit(app.exec())