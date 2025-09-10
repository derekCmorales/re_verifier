# 🔍 Regex Studio- Herramienta de Expresiones Regulares

![regex logo](https://github.com/derekCmorales/re_verifier/blob/main/regex_logo.png)

Una herramienta profesional que combina teoría y práctica para verificar la validez de expresiones regulares y probarlas en texto, con una interfaz moderna y características avanzadas.

## Características Principales

### Interfaz

- **Diseño Moderno**: Interfaz gráfica elegante con PyQt6
- **Resaltado Visual**: Coincidencias marcadas con colores vibrantes y subrayado
- **Resaltado de Sintaxis**: Colores diferenciados para operadores, paréntesis y meta caracteres
- **Procesamiento Asíncrono**: No bloquea la interfaz durante el análisis

### Funcionalidades Avanzadas

- ✅ Validación de sintaxis en tiempo real
- ✅ Resaltado visual de coincidencias con colores
- ✅ Lista numerada de coincidencias encontradas
- ✅ Documentación integrada con ejemplos

## 🚀 Instalación Rápida

### Requisitos

- Python 3.7 o superior
- PyQt6

### Instalación

```bash
# Clonar o descargar el proyecto
git clone git@github.com:derekCmorales/re_verifier.git

# Instalar dependencias
pip install PyQt6

```

```bash
python regex_gui.py
```

## 📚 Alfabeto Soportado

### Caracteres Básicos

- **Letras:** [A-Z], [a-z]
- **Dígitos:** [0-9]
- **Caracteres especiales:** . ^ $ \* + ? { } [ ] \ | ( )

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

## Características de la Interfaz

### Editor Principal

- **Campo de Regex**: Con resaltado de sintaxis en tiempo real
- **Área de Texto**: Para análisis de contenido (mínimo 5 líneas)
- **Panel de Resultados**: Lista de coincidencias con contador dinámico
- **Texto Resaltado**: Coincidencias marcadas con colores vibrantes

![ss interface](https://github.com/derekCmorales/re_verifier/blob/main/ss-interface.png)

### Pestañas de Ayuda

- **📚 Ayuda y Referencia**: Documentación completa con ejemplos

![ss help](https://github.com/derekCmorales/re_verifier/blob/main/ss-help.png)

### Diseño Profesional

- **Colores Vibrantes**: Esquema de colores moderno y atractivo
- **Gradientes**: Efectos visuales profesionales
- **Iconos**: Interfaz intuitiva con emojis y símbolos
- **Responsive**: Adaptable a diferentes tamaños de ventana

## Conexión con Teoría de Autómatas

Esta herramienta demuestra la conexión práctica entre:

1. **Expresiones Regulares** - Representación textual de patrones
2. **Autómatas Finitos** - Implementación interna de `re.compile()`
3. **Gramáticas Regulares** - Sintaxis y validación de patrones
4. **Aplicaciones Reales** - Procesamiento de texto, validación de datos

## Arquitectura del Sistema

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

## Ejemplos de Uso

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

## Características Técnicas

- **PyQt6**: Framework moderno para interfaces gráficas
- **Procesamiento Asíncrono**: Threads para no bloquear la UI
- **Resaltado Avanzado**: Colores y formatos personalizados
- **Validación Robusta**: Manejo completo de errores
- **Diseño Responsive**: Adaptable y profesional

## Rendimiento

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

## Autor

Desarrollado como parte del curso de Lenguajes Formales y Autómatas por:
Derek Adolfo Calderón Morales 1567624
Adrián Fabricio Matul Racancoj 1509224
Diego Alejandro Ovalle Pedroza 1500324
