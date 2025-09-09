import sys
import re
from typing import List, Tuple, Optional
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, 
                             QListWidget, QSplitter, QGroupBox, QMessageBox, QTabWidget,
                             QScrollArea, QFrame, QGridLayout, QSpacerItem, QSizePolicy,
                             QStatusBar, QMenuBar, QMenu, QToolBar, QProgressBar,
                             QDockWidget, QTextBrowser, QComboBox, QSpinBox, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import (QFont, QColor, QTextCharFormat, QSyntaxHighlighter, 
                        QTextDocument, QPalette, QLinearGradient, QBrush, QPainter,
                        QAction, QIcon, QTextCursor, QTextBlockFormat)

class RegexValidator:
    """Clase para validar y procesar expresiones regulares"""
    
    def __init__(self):
        self.supported_metacharacters = {
            '\\d': 'cualquier dígito [0-9]',
            '\\D': 'cualquier no dígito [^0-9]',
            '\\s': 'cualquier espacio en blanco',
            '\\S': 'cualquier no espacio en blanco',
            '\\w': 'cualquier alfanumérico [a-zA-Z0-9_]',
            '\\W': 'cualquier no alfanumérico [^a-zA-Z0-9_]',
            '.': 'cualquier carácter excepto nueva línea',
            '^': 'inicio de línea',
            '$': 'final de línea',
            '*': 'cero o más repeticiones',
            '+': 'una o más repeticiones',
            '?': 'cero o una repetición',
            '|': 'alternancia (OR)',
            '()': 'agrupación',
            '[]': 'clases de caracteres',
            '\\': 'escape'
        }
    
    def verify_regex(self, pattern: str) -> Tuple[bool, Optional[str]]:
        """Verifica si una expresión regular está bien formada"""
        if not pattern.strip():
            return False, "La expresión regular no puede estar vacía"
            
        try:
            re.compile(pattern)
            return True, None
        except re.error as e:
            return False, str(e)
    
    def find_matches(self, pattern: str, text: str) -> Tuple[Optional[List[str]], Optional[str]]:
        """Encuentra todas las coincidencias de la regex en el texto"""
        try:
            compiled_pattern = re.compile(pattern)
            matches = compiled_pattern.findall(text)
            return matches, None
        except re.error as e:
            return None, str(e)
    
    def get_match_positions(self, pattern: str, text: str) -> Tuple[Optional[List[Tuple[int, int, str]]], Optional[str]]:
        """Obtiene las posiciones de las coincidencias en el texto"""
        try:
            compiled_pattern = re.compile(pattern)
            matches = []
            for match in compiled_pattern.finditer(text):
                matches.append((match.start(), match.end(), match.group()))
            return matches, None
        except re.error as e:
            return None, str(e)

class RegexHighlighter(QSyntaxHighlighter):
    """Resaltador de sintaxis para expresiones regulares"""
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        
        # Operadores básicos - Azul
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(99, 102, 241))  # Indigo
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        operators = ['\\*', '\\+', '\\?', '\\|', '\\.', '\\^', '\\$']
        for pattern in operators:
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Paréntesis y corchetes - Rojo
        paren_format = QTextCharFormat()
        paren_format.setForeground(QColor(239, 68, 68))  # Red
        paren_format.setFontWeight(QFont.Weight.Bold)
        
        self.highlighting_rules.append(('[\\(\\)\\[\\]]', paren_format))
        
        # Meta caracteres - Verde
        meta_format = QTextCharFormat()
        meta_format.setForeground(QColor(34, 197, 94))  # Green
        meta_format.setFontWeight(QFont.Weight.Bold)
        
        meta_patterns = ['\\\\[dDsSwW]', '\\\\[\\^\\$\\*\\+\\?\\|]']
        for pattern in meta_patterns:
            self.highlighting_rules.append((pattern, meta_format))
        
        # Clases de caracteres - Púrpura
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(168, 85, 247))  # Purple
        class_format.setFontWeight(QFont.Weight.Bold)
        
        self.highlighting_rules.append(('\\[.*?\\]', class_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = re.compile(pattern)
            for match in expression.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)

class TextHighlighter(QTextEdit):
    """Editor de texto con resaltado de coincidencias"""
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.matches = []
        
    def highlight_matches(self, text, matches):
        """Resalta las coincidencias en el texto"""
        self.matches = matches
        self.clear()
        
        if not matches:
            self.setPlainText(text)
            return
            
        # Crear documento con formato
        doc = QTextDocument()
        self.setDocument(doc)
        cursor = self.textCursor()
        
        # Procesar texto línea por línea
        lines = text.split('\n')
        current_pos = 0
        
        for line_num, line in enumerate(lines):
            line_start = current_pos
            
            # Crear formato para texto normal
            normal_format = QTextCharFormat()
            normal_format.setForeground(QColor(31, 41, 55))  # Gray-800
            
            # Crear formato para coincidencias
            match_format = QTextCharFormat()
            match_format.setBackground(QColor(254, 240, 138))  # Yellow-200
            match_format.setForeground(QColor(17, 24, 39))     # Gray-900
            match_format.setFontWeight(QFont.Weight.Bold)
            match_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
            
            # Procesar cada coincidencia en esta línea
            line_matches = []
            for match_start, match_end, match_text in matches:
                if match_start >= current_pos and match_start < current_pos + len(line):
                    line_matches.append((match_start - current_pos, match_end - current_pos, match_text))
            
            # Ordenar coincidencias por posición
            line_matches.sort(key=lambda x: x[0])
            
            # Construir texto con formato
            last_pos = 0
            for match_start, match_end, match_text in line_matches:
                # Agregar texto antes de la coincidencia
                if match_start > last_pos:
                    before_text = line[last_pos:match_start]
                    cursor.insertText(before_text, normal_format)
                
                # Agregar coincidencia con formato especial
                cursor.insertText(match_text, match_format)
                last_pos = match_end
            
            # Agregar el resto de la línea
            if last_pos < len(line):
                remaining_text = line[last_pos:]
                cursor.insertText(remaining_text, normal_format)
            
            # Agregar salto de línea (excepto en la última línea)
            if line_num < len(lines) - 1:
                cursor.insertText('\n', normal_format)
            
            current_pos += len(line) + 1

class RegexWorker(QThread):
    """Worker thread para procesar regex sin bloquear la UI"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, pattern, text):
        super().__init__()
        self.pattern = pattern
        self.text = text
        self.validator = RegexValidator()
    
    def run(self):
        try:
            # Verificar si la regex es válida
            is_valid, error_msg = self.validator.verify_regex(self.pattern)
            
            if not is_valid:
                self.error.emit(f"Error en la expresión regular: {error_msg}")
                return
            
            # Encontrar coincidencias
            matches, error = self.validator.find_matches(self.pattern, self.text)
            if error:
                self.error.emit(f"Error al procesar: {error}")
                return
            
            # Obtener posiciones de coincidencias
            positions, error = self.validator.get_match_positions(self.pattern, self.text)
            if error:
                self.error.emit(f"Error al obtener posiciones: {error}")
                return
            
            result = {
                'is_valid': is_valid,
                'matches': matches,
                'positions': positions,
                'match_count': len(matches) if matches else 0
            }
            
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(f"Error inesperado: {str(e)}")

class ModernButton(QPushButton):
    """Botón con estilo moderno"""
    def __init__(self, text, color_scheme="primary", icon=None):
        super().__init__(text)
        self.color_scheme = color_scheme
        self.setMinimumHeight(44)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.setStyleSheet(self.get_style())
        
    def get_style(self):
        if self.color_scheme == "primary":
            return """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3B82F6, stop:1 #2563EB);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #60A5FA, stop:1 #3B82F6);
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2563EB, stop:1 #1D4ED8);
                }
                QPushButton:disabled {
                    background: #E5E7EB;
                    color: #9CA3AF;
                }
            """
        elif self.color_scheme == "success":
            return """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #10B981, stop:1 #059669);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #34D399, stop:1 #10B981);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #059669, stop:1 #047857);
                }
            """
        elif self.color_scheme == "danger":
            return """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #EF4444, stop:1 #DC2626);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F87171, stop:1 #EF4444);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #DC2626, stop:1 #B91C1C);
                }
            """
        else:  # secondary
            return """
                QPushButton {
                    background: #F3F4F6;
                    border: 2px solid #E5E7EB;
                    border-radius: 8px;
                    color: #374151;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #E5E7EB;
                    border-color: #D1D5DB;
                }
                QPushButton:pressed {
                    background: #D1D5DB;
                }
            """

class RegexMainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    def __init__(self):
        super().__init__()
        self.validator = RegexValidator()
        self.init_ui()
        self.apply_modern_style()
        
    def init_ui(self):
        self.setWindowTitle("Regex Studio - Analizador de Expresiones Regulares")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)
        
        # Header moderno
        self.create_header(main_layout)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #E5E7EB;
                width: 2px;
                border-radius: 1px;
            }
            QSplitter::handle:hover {
                background: #3B82F6;
            }
        """)
        main_layout.addWidget(main_splitter)
        
        # Panel izquierdo - Entrada
        self.create_input_panel(main_splitter)
        
        # Panel derecho - Resultados
        self.create_output_panel(main_splitter)
        
        # Configurar proporciones del splitter
        main_splitter.setSizes([700, 700])
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self, parent_layout):
        """Crear encabezado con logo a la izquierda y botones"""
        header_frame = QFrame()
        header_frame.setFixedHeight(120)  # Altura aumentada para evitar cortes
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E2E8F0, stop:1 #CBD5E1);
                border-radius: 16px;
                border: 1px solid #94A3B8;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(20)
        
        # Contenedor del logo con fondo circular
        logo_container = QFrame()
        logo_container.setFixedSize(90, 90)  # Tamaño optimizado
        logo_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #1D4ED8);
                border-radius: 45px;
                border: 3px solid white;
            }
        """)
        logo_container_layout = QHBoxLayout(logo_container)
        logo_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_container_layout.setContentsMargins(8, 8, 8, 8)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        
        # Cargar y escalar el logo con mejor calidad
        try:
            from PyQt6.QtGui import QPixmap
            pixmap = QPixmap("egex.png")
            if not pixmap.isNull():
                # Usar alta calidad y tamaño optimizado
                scaled_pixmap = pixmap.scaled(74, 74, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                logo_label.setText("REGEX")
                logo_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        background: transparent;
                    }
                """)
        except:
            logo_label.setText("REGEX")
            logo_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    background: transparent;
                }
            """)
        
        logo_container_layout.addWidget(logo_label)
        header_layout.addWidget(logo_container)
        
        # Espaciador para empujar botones a la derecha
        header_layout.addStretch()
        
        # Contenedor para botones con más espacio
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(15)  # Más espacio entre botones
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Botones de navegación
        self.inicio_btn = ModernButton("Inicio", "primary")
        self.inicio_btn.setFixedSize(120, 45)  # Más ancho para el texto
        self.inicio_btn.clicked.connect(self.show_inicio)
        
        self.ayuda_btn = ModernButton("Ayuda", "primary")
        self.ayuda_btn.setFixedSize(120, 45)  # Más ancho para el texto
        self.ayuda_btn.clicked.connect(self.show_ayuda)
        
        buttons_layout.addWidget(self.inicio_btn)
        buttons_layout.addWidget(self.ayuda_btn)
        
        header_layout.addWidget(buttons_container)
        
        parent_layout.addWidget(header_frame)
        
    def create_input_panel(self, parent):
        """Crear panel de entrada"""
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setSpacing(20)
        
        # Grupo de regex
        regex_group = self.create_group_box("Expresión Regular", input_layout)
        regex_layout = QVBoxLayout(regex_group)
        regex_layout.setSpacing(16)
        
        # Campo de entrada de regex
        self.regex_input = QTextEdit()
        self.regex_input.setMaximumHeight(100)
        self.regex_input.setPlaceholderText("Ingrese su expresión regular aquí...\nEjemplo: \\d{3}-\\d{3}-\\d{4}")
        self.regex_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 16px;
                font-family: 'JetBrains Mono', 'Consolas', monospace;
                font-size: 14px;
                background: #FAFAFA;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border-color: #3B82F6;
                background: white;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
        """)
        
        # Aplicar resaltador de sintaxis
        self.highlighter = RegexHighlighter(self.regex_input.document())
        
        regex_layout.addWidget(self.regex_input)
        
        # Botones de control
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.validate_btn = ModernButton("Validar", "primary")
        self.validate_btn.clicked.connect(self.validate_regex)
        
        self.process_btn = ModernButton("Analizar", "success")
        self.process_btn.clicked.connect(self.process_text)
        self.process_btn.setEnabled(False)
        
        self.clear_btn = ModernButton("Limpiar", "danger")
        self.clear_btn.clicked.connect(self.clear_all)
        
        button_layout.addWidget(self.validate_btn)
        button_layout.addWidget(self.process_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        regex_layout.addLayout(button_layout)
        
        # Grupo de texto
        text_group = self.create_group_box("Texto a Analizar", input_layout)
        text_layout = QVBoxLayout(text_group)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Ingrese el texto a analizar aquí...\n\nEjemplo:\nMi teléfono es 555-123-4567\nEmail: usuario@ejemplo.com\nFecha: 2024-01-15")
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 16px;
                font-family: 'Inter', sans-serif;
                font-size: 13px;
                background: #FAFAFA;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border-color: #3B82F6;
                background: white;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
        """)
        text_layout.addWidget(self.text_input)
        
        parent.addWidget(input_widget)
        
    def create_output_panel(self, parent):
        """Crear panel de resultados"""
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.setSpacing(20)
        
        # Estadísticas
        stats_group = self.create_group_box("Estadísticas", output_layout)
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_label = QLabel("Coincidencias encontradas: 0")
        self.stats_label.setStyleSheet("""
            font-weight: 700; 
            font-size: 16px;
            color: #6B7280;
            background: #F9FAFB;
            border: 2px solid #E5E7EB;
            border-radius: 12px;
            padding: 20px;
        """)
        stats_layout.addWidget(self.stats_label)
        
        # Contador de palabras
        self.word_count_label = QLabel("Palabras en el texto: 0")
        self.word_count_label.setStyleSheet("""
            font-weight: 600; 
            font-size: 14px;
            color: #6B7280;
            background: #F9FAFB;
            border: 2px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            margin-top: 8px;
        """)
        stats_layout.addWidget(self.word_count_label)
        
        # Lista de coincidencias
        matches_group = self.create_group_box("Coincidencias Encontradas", output_layout)
        matches_layout = QVBoxLayout(matches_group)
        
        self.matches_list = QListWidget()
        self.matches_list.setMaximumHeight(220)  # Aumentado para mejor visibilidad
        self.matches_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                background: #FAFAFA;
                font-family: 'JetBrains Mono', 'Consolas', monospace;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid #F3F4F6;
                background: white;
                margin: 2px;
                border-radius: 8px;
            }
            QListWidget::item:selected {
                background: #DBEAFE;
                color: #1D4ED8;
                border: 2px solid #3B82F6;
            }
            QListWidget::item:hover {
                background: #F3F4F6;
            }
        """)
        matches_layout.addWidget(self.matches_list)
        
        # Texto resaltado
        highlight_group = self.create_group_box("Texto con Coincidencias Resaltadas", output_layout)
        highlight_layout = QVBoxLayout(highlight_group)
        
        self.highlighted_text = TextHighlighter()
        self.highlighted_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                background: white;
                font-family: 'Inter', sans-serif;
                font-size: 13px;
                line-height: 1.6;
                padding: 16px;
            }
        """)
        highlight_layout.addWidget(self.highlighted_text)
        
        parent.addWidget(output_widget)
        
    def create_group_box(self, title, parent_layout):
        """Crear un grupo con estilo moderno"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: 700;
                font-size: 16px;
                color: #374151;
                border: 2px solid #E5E7EB;
                border-radius: 16px;
                margin-top: 16px;
                padding-top: 20px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 12px 0 12px;
                background: white;
            }
        """)
        parent_layout.addWidget(group)
        return group
        
    def create_status_bar(self):
        """Crear barra de estado"""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #F9FAFB;
                border-top: 2px solid #E5E7EB;
                color: #6B7280;
                font-weight: 500;
                padding: 8px 16px;
            }
        """)
        
        self.status_label = QLabel("Listo para analizar")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                background: #F3F4F6;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #1D4ED8);
                border-radius: 6px;
            }
        """)
        
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.setStatusBar(self.status_bar)
        
    def apply_modern_style(self):
        """Aplicar estilo moderno a toda la aplicación"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8FAFC, stop:1 #F1F5F9);
            }
            QWidget {
                background: transparent;
            }
        """)
        
    def validate_regex(self):
        """Validar la expresión regular ingresada"""
        pattern = self.regex_input.toPlainText().strip()
        
        if not pattern:
            self.show_message("Advertencia", "Por favor ingrese una expresión regular.", "warning")
            return
        
        is_valid, error_msg = self.validator.verify_regex(pattern)
        
        if is_valid:
            self.show_message("Éxito", "La expresión regular es válida y está lista para usar.", "success")
            self.process_btn.setEnabled(True)
            self.status_label.setText("Regex válida - Lista para analizar")
        else:
            self.show_message("Error", f"Error en la expresión regular:\n\n{error_msg}", "error")
            self.process_btn.setEnabled(False)
            self.status_label.setText("Regex inválida")
    
    def process_text(self):
        """Procesar el texto con la expresión regular"""
        pattern = self.regex_input.toPlainText().strip()
        text = self.text_input.toPlainText().strip()
        
        if not pattern:
            self.show_message("Advertencia", "Por favor ingrese una expresión regular.", "warning")
            return
            
        if not text:
            self.show_message("Advertencia", "Por favor ingrese texto a analizar.", "warning")
            return
        
        # Contar palabras
        word_count = len(text.split())
        self.word_count_label.setText(f"Palabras en el texto: {word_count}")
        
        # Mostrar progreso
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminado
        self.status_label.setText("Analizando texto...")
        
        # Crear y ejecutar worker thread
        self.worker = RegexWorker(pattern, text)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        self.worker.start()
        
        # Deshabilitar botones durante el procesamiento
        self.process_btn.setEnabled(False)
        self.process_btn.setText("Analizando...")
    
    def on_processing_finished(self, result):
        """Manejar el resultado del procesamiento"""
        # Ocultar progreso
        self.progress_bar.setVisible(False)
        
        # Actualizar estadísticas
        count = result['match_count']
        if count == 0:
            self.stats_label.setText("Coincidencias encontradas: 0")
            self.stats_label.setStyleSheet("""
                font-weight: 700; 
                font-size: 16px;
                color: #EF4444;
                background: #FEF2F2;
                border: 2px solid #FECACA;
                border-radius: 12px;
                padding: 20px;
            """)
            self.status_label.setText("No se encontraron coincidencias")
        else:
            self.stats_label.setText(f"Coincidencias encontradas: {count}")
            self.stats_label.setStyleSheet("""
                font-weight: 700; 
                font-size: 16px;
                color: #059669;
                background: #ECFDF5;
                border: 2px solid #A7F3D0;
                border-radius: 12px;
                padding: 20px;
            """)
            self.status_label.setText(f"Análisis completado - {count} coincidencias encontradas")
        
        # Limpiar y llenar lista de coincidencias
        self.matches_list.clear()
        if result['matches']:
            for i, match in enumerate(result['matches'], 1):
                self.matches_list.addItem(f"{i}. '{match}'")
        else:
            self.matches_list.addItem("No se encontraron coincidencias.")
        
        # Mostrar texto resaltado
        self.highlighted_text.highlight_matches(self.text_input.toPlainText(), result['positions'])
        
        # Restaurar botón
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Analizar")
    
    def on_processing_error(self, error_msg):
        """Manejar errores del procesamiento"""
        self.progress_bar.setVisible(False)
        self.show_message("Error", f"Error al procesar:\n\n{error_msg}", "error")
        self.status_label.setText("Error en el análisis")
        
        # Restaurar botón
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Analizar")
    
    def show_message(self, title, message, msg_type):
        """Mostrar mensaje con estilo moderno"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background: white;
                    border-radius: 12px;
                }
                QMessageBox QLabel {
                    color: #374151;
                    font-size: 14px;
                }
                QPushButton {
                    background: #3B82F6;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: #2563EB;
                }
            """)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background: white;
                    border-radius: 12px;
                }
                QMessageBox QLabel {
                    color: #374151;
                    font-size: 14px;
                }
                QPushButton {
                    background: #F59E0B;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: #D97706;
                }
            """)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background: white;
                    border-radius: 12px;
                }
                QMessageBox QLabel {
                    color: #374151;
                    font-size: 14px;
                }
                QPushButton {
                    background: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: #DC2626;
                }
            """)
        
        msg_box.exec()
    
    def clear_all(self):
        """Limpiar todos los campos"""
        self.regex_input.clear()
        self.text_input.clear()
        self.matches_list.clear()
        self.highlighted_text.clear()
        self.stats_label.setText("Coincidencias encontradas: 0")
        self.stats_label.setStyleSheet("""
            font-weight: 700; 
            font-size: 16px;
            color: #6B7280;
            background: #F9FAFB;
            border: 2px solid #E5E7EB;
            border-radius: 12px;
            padding: 20px;
        """)
        self.word_count_label.setText("Palabras en el texto: 0")
        self.process_btn.setEnabled(False)
        self.status_label.setText("Listo para analizar")
    
    def show_inicio(self):
        """Mostrar ventana de inicio"""
        self.show_message("Inicio", "Bienvenido a Regex Studio\n\nEsta es la pantalla principal donde puedes:\n• Ingresar expresiones regulares\n• Validar su sintaxis\n• Analizar texto\n• Ver coincidencias resaltadas", "success")
    
    def show_ayuda(self):
        """Mostrar ventana de ayuda completa"""
        ayuda_window = QMainWindow(self)
        ayuda_window.setWindowTitle("Ayuda - Regex Studio")
        ayuda_window.setGeometry(200, 200, 1000, 700)
        ayuda_window.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8FAFC, stop:1 #F1F5F9);
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        ayuda_window.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Título
        title_label = QLabel("📚 Guía Completa de Expresiones Regulares")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1E293B;
            margin-bottom: 20px;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3B82F6, stop:1 #1D4ED8);
            color: white;
            border-radius: 12px;
        """)
        main_layout.addWidget(title_label)
        
        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 2px solid #E2E8F0;
                border-radius: 12px;
                background: white;
            }
            QScrollBar:vertical {
                background: #F1F5F9;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94A3B8;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(25)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        
        # Contenido de ayuda
        help_content = QTextBrowser()
        help_text = """
        <div style="font-family: 'Segoe UI', sans-serif; line-height: 1.8; color: #374151;">
        
        <h1 style="color: #1E293B; border-bottom: 3px solid #3B82F6; padding-bottom: 10px;">¿Qué son las Expresiones Regulares?</h1>
        
        <p style="background: #F0F9FF; padding: 20px; border-radius: 8px; border-left: 4px solid #0EA5E9;">
        Las <strong>expresiones regulares (regex)</strong> son patrones de texto que permiten buscar, validar y manipular cadenas de caracteres de manera eficiente. Son una herramienta fundamental en programación para el procesamiento de texto.
        </p>
        
        <h2 style="color: #1E293B; border-bottom: 2px solid #10B981; padding-bottom: 8px;">Caracteres Básicos</h2>
        
        <div style="background: #F0FDF4; padding: 20px; border-radius: 8px; border-left: 4px solid #10B981;">
        <h3 style="color: #166534; margin-top: 0;">Literales</h3>
        <ul>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">abc</code> - Coincide exactamente con "abc"</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">123</code> - Coincide exactamente con "123"</li>
        </ul>
        
        <h3 style="color: #166534;">Caracteres Especiales</h3>
        <ul>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">.</code> - Cualquier carácter excepto nueva línea</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">^</code> - Inicio de línea</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">$</code> - Final de línea</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">|</code> - Operador OR (alternancia)</li>
        </ul>
        </div>
        
        <h2 style="color: #1E293B; border-bottom: 2px solid #F59E0B; padding-bottom: 8px;">Cuantificadores</h2>
        
        <div style="background: #FFFBEB; padding: 20px; border-radius: 8px; border-left: 4px solid #F59E0B;">
        <table style="width: 100%; border-collapse: collapse; margin: 10px 0;">
        <tr style="background: #FEF3C7;">
            <th style="padding: 12px; border: 1px solid #FCD34D; text-align: left;">Cuantificador</th>
            <th style="padding: 12px; border: 1px solid #FCD34D; text-align: left;">Significado</th>
            <th style="padding: 12px; border: 1px solid #FCD34D; text-align: left;">Ejemplo</th>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace; background: #FEFBF3;"><strong>*</strong></td>
            <td style="padding: 12px; border: 1px solid #FCD34D;">Cero o más repeticiones</td>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace;">ab* → "a", "ab", "abb", "abbb"</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace; background: #FEFBF3;"><strong>+</strong></td>
            <td style="padding: 12px; border: 1px solid #FCD34D;">Una o más repeticiones</td>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace;">ab+ → "ab", "abb", "abbb"</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace; background: #FEFBF3;"><strong>?</strong></td>
            <td style="padding: 12px; border: 1px solid #FCD34D;">Cero o una repetición</td>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace;">ab? → "a", "ab"</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace; background: #FEFBF3;"><strong>{n}</strong></td>
            <td style="padding: 12px; border: 1px solid #FCD34D;">Exactamente n repeticiones</td>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace;">ab{2} → "abb"</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace; background: #FEFBF3;"><strong>{n,m}</strong></td>
            <td style="padding: 12px; border: 1px solid #FCD34D;">Entre n y m repeticiones</td>
            <td style="padding: 12px; border: 1px solid #FCD34D; font-family: monospace;">ab{2,4} → "abb", "abbb", "abbbb"</td>
        </tr>
        </table>
        </div>
        
        <h2 style="color: #1E293B; border-bottom: 2px solid #8B5CF6; padding-bottom: 8px;">Clases de Caracteres</h2>
        
        <div style="background: #FAF5FF; padding: 20px; border-radius: 8px; border-left: 4px solid #8B5CF6;">
        <h3 style="color: #7C3AED; margin-top: 0;">Clases Predefinidas</h3>
        <ul>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">\\d</code> - Cualquier dígito [0-9]</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">\\D</code> - Cualquier no dígito [^0-9]</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">\\w</code> - Carácter alfanumérico [a-zA-Z0-9_]</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">\\W</code> - No alfanumérico [^a-zA-Z0-9_]</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">\\s</code> - Espacio en blanco</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">\\S</code> - No espacio en blanco</li>
        </ul>
        
        <h3 style="color: #7C3AED;">Clases Personalizadas</h3>
        <ul>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">[abc]</code> - Cualquiera de a, b, o c</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">[a-z]</code> - Cualquier letra minúscula</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">[0-9]</code> - Cualquier dígito</li>
        <li><code style="background: #E5E7EB; padding: 2px 6px; border-radius: 4px;">[^abc]</code> - Cualquier carácter excepto a, b, o c</li>
        </ul>
        </div>
        
        <h2 style="color: #1E293B; border-bottom: 2px solid #EF4444; padding-bottom: 8px;">Ejemplos Prácticos</h2>
        
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border-left: 4px solid #EF4444;">
        <h3 style="color: #DC2626; margin-top: 0;">Validación de Email</h3>
        <p><code style="background: #E5E7EB; padding: 4px 8px; border-radius: 4px; font-size: 14px;">^[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}$</code></p>
        <p>Coincide con: usuario@ejemplo.com, test.email@dominio.org</p>
        
        <h3 style="color: #DC2626;">Número de Teléfono</h3>
        <p><code style="background: #E5E7EB; padding: 4px 8px; border-radius: 4px; font-size: 14px;">\\d{3}-\\d{3}-\\d{4}</code></p>
        <p>Coincide con: 555-123-4567, 123-456-7890</p>
        
        <h3 style="color: #DC2626;">Palabras que Empiezan con Mayúscula</h3>
        <p><code style="background: #E5E7EB; padding: 4px 8px; border-radius: 4px; font-size: 14px;">[A-Z][a-z]+</code></p>
        <p>Coincide con: Hola, Mundo, Python</p>
        
        <h3 style="color: #DC2626;">Fechas en Formato DD/MM/YYYY</h3>
        <p><code style="background: #E5E7EB; padding: 4px 8px; border-radius: 4px; font-size: 14px;">\\d{2}/\\d{2}/\\d{4}</code></p>
        <p>Coincide con: 15/03/2024, 01/12/2023</p>
        </div>
        
        <h2 style="color: #1E293B; border-bottom: 2px solid #06B6D4; padding-bottom: 8px;">Cómo Usar Regex Studio</h2>
        
        <div style="background: #F0FDFA; padding: 20px; border-radius: 8px; border-left: 4px solid #06B6D4;">
        <ol style="margin: 0; padding-left: 20px;">
        <li><strong>Ingresa tu expresión regular</strong> en el campo superior</li>
        <li><strong>Haz clic en "Validar"</strong> para verificar la sintaxis</li>
        <li><strong>Escribe el texto</strong> que quieres analizar en el panel izquierdo</li>
        <li><strong>Haz clic en "Analizar"</strong> para encontrar coincidencias</li>
        <li><strong>Revisa los resultados</strong> en el panel derecho con resaltado visual</li>
        </ol>
        </div>
        
        <h2 style="color: #1E293B; border-bottom: 2px solid #84CC16; padding-bottom: 8px;">Consejos y Trucos</h2>
        
        <div style="background: #F7FEE7; padding: 20px; border-radius: 8px; border-left: 4px solid #84CC16;">
        <ul style="margin: 0;">
        <li><strong>Usa herramientas online</strong> para probar regex antes de implementarlas</li>
        <li><strong>Comienza simple</strong> y añade complejidad gradualmente</li>
        <li><strong>Usa paréntesis</strong> para agrupar y capturar partes del patrón</li>
        <li><strong>Escapa caracteres especiales</strong> con \\ cuando necesites el carácter literal</li>
        <li><strong>Prueba con diferentes casos</strong> para asegurar que tu regex funciona correctamente</li>
        </ul>
        </div>
        
        </div>
        """
        
        help_content.setHtml(help_text)
        scroll_layout.addWidget(help_content)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Botón de cerrar
        close_btn = ModernButton("Cerrar", "danger")
        close_btn.setFixedSize(100, 40)
        close_btn.clicked.connect(ayuda_window.close)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        main_layout.addLayout(btn_layout)
        
        ayuda_window.show()

def main():
    """Función principal para ejecutar la aplicación"""
    app = QApplication(sys.argv)
    
    # Configurar estilo de la aplicación
    app.setStyle('Fusion')
    
    # Configurar paleta de colores moderna
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(248, 250, 252))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(31, 41, 55))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(249, 250, 251))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(31, 41, 55))
    palette.setColor(QPalette.ColorRole.Text, QColor(31, 41, 55))
    palette.setColor(QPalette.ColorRole.Button, QColor(243, 244, 246))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(31, 41, 55))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(239, 68, 68))
    palette.setColor(QPalette.ColorRole.Link, QColor(59, 130, 246))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(59, 130, 246))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Crear y mostrar ventana principal
    window = RegexMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
