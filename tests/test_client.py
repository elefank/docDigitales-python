import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.client import DocDigitalesClient
from src.models import Cliente, Concepto, Factura
from src.exceptions import AuthenticationError, ValidationError, APIError

@pytest.fixture
def api_key():
    return "test_api_key"

@pytest.fixture
def client(api_key):
    return DocDigitalesClient(api_key)

@pytest.fixture
def factura_data():
    return {
        "cliente": {
            "rfc": "XAXX010101000",
            "nombre": "Cliente Prueba",
            "email": "cliente@prueba.com"
        },
        "conceptos": [
            {
                "clave_producto": "001",
                "descripcion": "Producto Prueba",
                "cantidad": 1,
                "precio_unitario": 100.00,
                "unidad": "PIEZA"
            }
        ]
    }

def test_client_initialization(api_key):
    client = DocDigitalesClient(api_key)
    assert client.api_key == api_key
    assert client.base_url == "https://api.docdigitales.com"
    assert client.session.headers["Authorization"] == f"Token token={api_key}"

def test_facturar_success(client, factura_data):
    # Mock de la respuesta exitosa
    mock_response = {
        "id": "12345",
        "uuid": "abc-123",
        "estado": "TIMBRADO",
        "fecha_creacion": datetime.now().isoformat(),
        "pdf_url": "https://api.docdigitales.com/facturas/12345/pdf",
        "xml_url": "https://api.docdigitales.com/facturas/12345/xml"
    }
    
    with patch.object(client.session, 'request') as mock_request:
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.status_code = 200
        
        factura = Factura(**factura_data)
        resultado = client.facturar(factura)
        
        assert resultado.id == "12345"
        assert resultado.uuid == "abc-123"
        assert resultado.estado == "TIMBRADO"
        assert resultado.pdf_url is not None
        assert resultado.xml_url is not None

def test_facturar_authentication_error(client, factura_data):
    with patch.object(client.session, 'request') as mock_request:
        mock_request.return_value.status_code = 401
        
        factura = Factura(**factura_data)
        with pytest.raises(AuthenticationError):
            client.facturar(factura)

def test_facturar_validation_error(client, factura_data):
    # Datos inválidos
    factura_data["cliente"]["rfc"] = "invalid"
    
    with pytest.raises(ValidationError):
        Factura(**factura_data)

def test_consultar_estado_success(client):
    mock_response = {
        "id": "12345",
        "uuid": "abc-123",
        "estado": "TIMBRADO",
        "fecha_creacion": datetime.now().isoformat()
    }
    
    with patch.object(client.session, 'request') as mock_request:
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.status_code = 200
        
        resultado = client.consultar_estado("12345")
        assert resultado.id == "12345"
        assert resultado.estado == "TIMBRADO"

def test_cancelar_factura_success(client):
    mock_response = {
        "id": "12345",
        "estado": "CANCELADO",
        "mensaje": "Factura cancelada exitosamente"
    }
    
    with patch.object(client.session, 'request') as mock_request:
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.status_code = 200
        
        resultado = client.cancelar_factura("12345", "Motivo de prueba")
        assert resultado["estado"] == "CANCELADO"
        assert resultado["mensaje"] == "Factura cancelada exitosamente" 