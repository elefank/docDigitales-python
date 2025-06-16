# DocDigitales Python Client

Cliente Python para la API de DocDigitales, diseñado para ejecutarse como una función Lambda de AWS.

## Requisitos

- Python 3.10 o superior
- AWS Lambda
- Credenciales de API de DocDigitales

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd docdigitales-python
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
docdigitales-python/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── client.py      # Cliente principal de la API
│   ├── exceptions.py  # Excepciones personalizadas
│   └── models.py      # Modelos de datos
├── tests/
│   ├── __init__.py
│   └── test_client.py
└── lambda_function.py # Función Lambda
```

## Configuración

1. Configurar la variable de entorno `DOCDIGITALES_API_KEY` en AWS Lambda con tu clave de API.

2. Configurar los siguientes parámetros en AWS Lambda:
   - Runtime: Python 3.10
   - Handler: lambda_function.lambda_handler
   - Memory: 256 MB (mínimo recomendado)
   - Timeout: 30 segundos (ajustar según necesidades)

## Uso

La función Lambda acepta las siguientes acciones:

### Facturar
```json
{
    "action": "facturar",
    "factura": {
        "cliente": {
            "rfc": "XAXX010101000",
            "nombre": "Cliente Ejemplo",
            "email": "cliente@ejemplo.com"
        },
        "conceptos": [
            {
                "clave_producto": "001",
                "descripcion": "Producto 1",
                "cantidad": 1,
                "precio_unitario": 100.00,
                "unidad": "PIEZA"
            }
        ]
    }
}
```

### Consultar Estado
```json
{
    "action": "consultar",
    "factura_id": "12345"
}
```

### Cancelar Factura
```json
{
    "action": "cancelar",
    "factura_id": "12345",
    "motivo": "Motivo de cancelación"
}
```

### Descargar PDF
```json
{
    "action": "descargar_pdf",
    "factura_id": "12345"
}
```

### Descargar XML
```json
{
    "action": "descargar_xml",
    "factura_id": "12345"
}
```

## Despliegue

1. Crear un archivo ZIP con el contenido del proyecto:
```bash
zip -r function.zip . -x "venv/*" "*.pyc" "__pycache__/*"
```

2. Subir el archivo ZIP a AWS Lambda a través de la consola de AWS o usando AWS CLI.

## Desarrollo Local

Para probar localmente:

1. Crear un archivo `.env` con tus credenciales:
```
DOCDIGITALES_API_KEY=tu_api_key
```

2. Ejecutar pruebas:
```bash
pytest tests/
```

## Seguridad

- Las credenciales de API se manejan a través de variables de entorno
- Se recomienda usar AWS Secrets Manager para almacenar el API_KEY
- Implementar rate limiting según las necesidades
- Usar IAM roles apropiados para la Lambda

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 