# WLM Image Converter 🖼️

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)

Una aplicación de escritorio desarrollada en Python que convierte imágenes a formato base64 y genera un archivo CSV compatible con WLM (Warehouse Labor Managment).

## 🚀 Características

- Interfaz gráfica intuitiva y fácil de usar
- Selección de carpetas mediante explorador de archivos
- Soporte para múltiples formatos de imagen (PNG, JPG, JPEG, GIF, BMP)
- Conversión automática a base64
- Generación de CSV con formato específico para WML
- Barra de progreso en tiempo real
- Validación de tamaño de archivos
- Interfaz centrada en la pantalla
- Soporte para íconos personalizados

## 📋 Requisitos Previos

- Python 3.6 o superior
- Biblioteca PIL (Pillow)
- Tkinter (incluido en la instalación estándar de Python)

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Alex-Appleby/Image_to_Base_64.git
```

2. Navega al directorio del proyecto:
```bash
cd Image_to_Base_64-main
```

3. Instala las dependencias requeridas:
```bash
pip install Pillow
```

## 💻 Uso

1. Ejecuta el programa:
```bash
python Image_to_Base_64.py
```

2. Selecciona la carpeta que contiene las imágenes a convertir
3. Elige la carpeta de destino para el archivo CSV
4. Ingresa el Warehouse ID
5. Haz clic en "Convertir Imágenes"

## 📁 Estructura del CSV Generado

El programa genera un archivo CSV con el siguiente formato:

| Columna    | Descripción                           |
|------------|---------------------------------------|
| file_name  | Nombre del archivo sin extensión      |
| user       | Nombre del archivo                    |
| title      | Nombre del archivo                    |
| seq        | Secuencia (valor por defecto: 1)      |
| tag        | Nombre del archivo                    |
| media      | Imagen en formato base64              |
| wh_id      | ID del almacén ingresado             |
| file_type  | Extensión del archivo                 |

## ⚠️ Limitaciones

- Tamaño máximo de archivo recomendado: 5MB
- Los archivos JPEG se convertirán automáticamente a extensión JPG

## 👨‍💻 Autor

Creado por Alejandro Enriquez Rivera

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.

1. Haz Fork del proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Realiza tus cambios y haz commit (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún bug o tienes alguna sugerencia, por favor abre un issue en el repositorio.