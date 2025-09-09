# 🔍 Regex Master Pro - Herramienta Profesional de Expresiones Regulares

Una herramienta profesional que combina teoría y práctica para verificar la validez de expresiones regulares y probarlas en texto, con una interfaz moderna y características avanzadas.

## ✨ Características Principales

### 🎨 Interfaz Profesional
- **Diseño Moderno**: Interfaz gráfica elegante con PyQt6
- **Resaltado Visual**: Coincidencias marcadas con colores vibrantes y subrayado
- **Resaltado de Sintaxis**: Colores diferenciados para operadores, paréntesis y meta caracteres
- **Procesamiento Asíncrono**: No bloquea la interfaz durante el análisis

### 🔧 Funcionalidades Avanzadas
- ✅ Validación de sintaxis en tiempo real
- ✅ Resaltado visual de coincidencias con colores
- ✅ Lista numerada de coincidencias encontradas
- ✅ Contador dinámico de resultados
- ✅ Casos de prueba automatizados
- ✅ Documentación integrada con ejemplos

## 🚀 Instalación Rápida

### Requisitos
- Python 3.7 o superior
- PyQt6

### Instalación
```bash
# Clonar o descargar el proyecto
git clone <url-del-repositorio>
cd PROYECTO3

# Instalar dependencias
pip install PyQt6

# O usar el archivo de requisitos
pip install -r requirements.txt
```

## 🎯 Uso

### Lanzador Principal (Recomendado)
```bash
python launcher.py
```

### Ejecución Directa
```bash
python regex_gui.py
```

## 📚 Alfabeto Soportado

### Caracteres Básicos
- **Letras:** [A-Z], [a-z]
- **Dígitos:** [0-9]
- **Caracteres especiales:** . ^ $ * + ? { } [ ] \ | ( )

### Meta Caracteres
- `\d` - cualquier dígito [0-9]
- `\D` - cualquier no dígito [^0-9]
- `\s` - cualquier espacio en blanco
- `\S` - cualquier no espacio en blanco
- `\w` - cualquier alfanumérico [a-zA-Z0-9_]
- `\W` - cualquier no alfanumérico [^a-zA-Z0-9_]
- `.` - cualquier carácter excepto nueva línea
- `^` - inicio de línea
- `$` - final de línea
- `*` - cero o más repeticiones
- `+` - una o más repeticiones
- `?` - cero o una repetición
- `|` - alternancia (OR)
- `()` - agrupación
- `[]` - clases de caracteres
- `\` - escape

## 🧪 Casos de Prueba Incluidos

La herramienta incluye casos de prueba automatizados:

1. **Regex válida:** `\d+` - Encuentra secuencias de dígitos
2. **Regex inválida:** `(ab` - Detecta errores de sintaxis
3. **Regex con alternancia:** `(perro|gato)` - Encuentra palabras alternativas
4. **Regex con clases:** `[A-Z][a-z]+` - Encuentra palabras con mayúscula inicial
5. **Regex con espacios:** `\s+` - Encuentra espacios en blanco
6. **Regex con palabras:** `\w+` - Encuentra palabras alfanuméricas

## 🎨 Características de la Interfaz

### Editor Principal
- **Campo de Regex**: Con resaltado de sintaxis en tiempo real
- **Área de Texto**: Para análisis de contenido (mínimo 5 líneas)
- **Panel de Resultados**: Lista de coincidencias con contador dinámico
- **Texto Resaltado**: Coincidencias marcadas con colores vibrantes

### Pestañas de Ayuda
- **📚 Ayuda y Referencia**: Documentación completa con ejemplos
- **🧪 Casos de Prueba**: Ejecución automática de pruebas

### Diseño Profesional
- **Colores Vibrantes**: Esquema de colores moderno y atractivo
- **Gradientes**: Efectos visuales profesionales
- **Iconos**: Interfaz intuitiva con emojis y símbolos
- **Responsive**: Adaptable a diferentes tamaños de ventana

## 🔗 Conexión con Teoría de Autómatas

Esta herramienta demuestra la conexión práctica entre:

1. **Expresiones Regulares** - Representación textual de patrones
2. **Autómatas Finitos** - Implementación interna de `re.compile()`
3. **Gramáticas Regulares** - Sintaxis y validación de patrones
4. **Aplicaciones Reales** - Procesamiento de texto, validación de datos

## 🏗️ Arquitectura del Sistema

### Clases Principales

#### `RegexValidator`
- Valida sintaxis de expresiones regulares
- Encuentra coincidencias en texto
- Obtiene posiciones de coincidencias

#### `RegexMainWindow`
- Interfaz gráfica principal
- Gestión de pestañas y paneles
- Coordinación de funcionalidades

#### `RegexHighlighter`
- Resaltado de sintaxis para expresiones regulares
- Colores diferenciados para diferentes elementos

#### `TextHighlighter`
- Resaltado visual de coincidencias en texto
- Colores vibrantes y subrayado

#### `ModernButton`
- Botones con estilo profesional
- Gradientes y efectos visuales

#### `RegexWorker`
- Procesamiento asíncrono
- Manejo de errores robusto

## 📝 Ejemplos de Uso

### Ejemplo 1: Encontrar Números
```
Regex: \d+
Texto: El precio es $299.99 y la fecha es 15/03/2024
Resultado: ["299", "99", "15", "03", "2024"]
```

### Ejemplo 2: Encontrar Palabras con Mayúscula
```
Regex: [A-Z][a-z]+
Texto: Pedro y maria son amigos de Juan
Resultado: ["Pedro", "Juan"]
```

### Ejemplo 3: Encontrar Emails
```
Regex: \w+@\w+\.\w+
Texto: Contacto: usuario@ejemplo.com o admin@test.org
Resultado: ["usuario@ejemplo.com", "admin@test.org"]
```

## 🚀 Características Técnicas

- **PyQt6**: Framework moderno para interfaces gráficas
- **Procesamiento Asíncrono**: Threads para no bloquear la UI
- **Resaltado Avanzado**: Colores y formatos personalizados
- **Validación Robusta**: Manejo completo de errores
- **Diseño Responsive**: Adaptable y profesional

## 📊 Rendimiento

- **Validación Instantánea**: Verificación en tiempo real
- **Procesamiento Rápido**: Optimizado para textos grandes
- **Interfaz Fluida**: Sin bloqueos durante el análisis
- **Memoria Eficiente**: Gestión optimizada de recursos

## 🎯 Casos de Uso

### Para Desarrolladores
- Validar patrones de regex antes de implementar
- Probar expresiones regulares con datos reales
- Aprender sintaxis de regex con ejemplos visuales

### Para Estudiantes
- Entender conceptos de lenguajes formales
- Practicar con expresiones regulares
- Ver conexión entre teoría y práctica

### Para Profesionales
- Herramienta de productividad para análisis de texto
- Validación de patrones de datos
- Prototipado rápido de filtros de texto

## 🔧 Requisitos del Sistema

- **Python**: 3.7 o superior
- **PyQt6**: Para la interfaz gráfica
- **Sistema Operativo**: Windows, macOS, Linux
- **Memoria**: Mínimo 512MB RAM
- **Espacio**: 50MB de espacio en disco

## 📈 Versiones

### Versión 2.0 (Actual)
- Interfaz completamente rediseñada
- Resaltado visual mejorado
- Diseño profesional
- Características avanzadas

### Características Futuras
- Exportación de resultados
- Múltiples patrones simultáneos
- Historial de expresiones
- Temas personalizables

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la herramienta:

1. Fork del proyecto
2. Crea una rama para tu feature
3. Implementa tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 👨‍💻 Autor

Desarrollado como parte del curso de Lenguajes Formales y Autómatas.

## 🎉 Conclusión

Regex Master Pro es más que una herramienta de expresiones regulares; es un puente entre la teoría académica y la aplicación práctica. Con su interfaz moderna, características avanzadas y diseño profesional, hace que el aprendizaje y uso de expresiones regulares sea una experiencia visual y educativa.

La herramienta demuestra cómo los conceptos abstractos de lenguajes formales se pueden materializar en aplicaciones reales y útiles, creando valor tanto educativo como práctico.