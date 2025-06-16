import json
import os
import base64
from typing import Dict, Any, Optional
from src.client import DocDigitalesClient
from src.exceptions import DocDigitalesAPIError, AuthenticationError, ValidationError, APIError
from src.models import Factura

def get_error_response(error: Exception, status_code: int = 500) -> Dict[str, Any]:
    """Genera una respuesta de error estandarizada"""
    return {
        'statusCode': status_code,
        'body': json.dumps({
            'error': str(error),
            'tipo': error.__class__.__name__
        })
    }

def get_success_response(data: Any, status_code: int = 200) -> Dict[str, Any]:
    """Genera una respuesta exitosa estandarizada"""
    return {
        'statusCode': status_code,
        'body': json.dumps(data)
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Manejador principal de la función Lambda
    
    Args:
        event (Dict[str, Any]): Evento de Lambda
        context (Any): Contexto de Lambda
        
    Returns:
        Dict[str, Any]: Respuesta de la función
    """
    try:
        # Obtener credenciales desde variables de entorno
        api_key = os.environ.get('DOCDIGITALES_API_KEY')
        if not api_key:
            raise AuthenticationError("API key no configurada en las variables de entorno")

        # Inicializar cliente
        client = DocDigitalesClient(api_key)
        
        # Obtener el cuerpo de la petición
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if not action:
            return get_error_response(ValueError("Se requiere especificar una acción"), 400)
            
        # Procesar la acción solicitada
        if action == 'facturar':
            if 'factura' not in body:
                return get_error_response(ValueError("Se requieren los datos de la factura"), 400)
                
            factura = Factura(**body['factura'])
            resultado = client.facturar(factura)
            return get_success_response(resultado.model_dump())
            
        elif action == 'consultar':
            factura_id = body.get('factura_id')
            if not factura_id:
                return get_error_response(ValueError("Se requiere el ID de la factura"), 400)
                
            resultado = client.consultar_estado(factura_id)
            return get_success_response(resultado.model_dump())
            
        elif action == 'cancelar':
            factura_id = body.get('factura_id')
            motivo = body.get('motivo')
            
            if not factura_id or not motivo:
                return get_error_response(
                    ValueError("Se requieren el ID de la factura y el motivo de cancelación"), 
                    400
                )
                
            resultado = client.cancelar_factura(factura_id, motivo)
            return get_success_response(resultado)
            
        elif action == 'descargar_pdf':
            factura_id = body.get('factura_id')
            if not factura_id:
                return get_error_response(ValueError("Se requiere el ID de la factura"), 400)
                
            pdf_content = client.descargar_pdf(factura_id)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/pdf',
                    'Content-Disposition': f'attachment; filename="factura_{factura_id}.pdf"'
                },
                'body': base64.b64encode(pdf_content).decode('utf-8'),
                'isBase64Encoded': True
            }
            
        elif action == 'descargar_xml':
            factura_id = body.get('factura_id')
            if not factura_id:
                return get_error_response(ValueError("Se requiere el ID de la factura"), 400)
                
            xml_content = client.descargar_xml(factura_id)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/xml',
                    'Content-Disposition': f'attachment; filename="factura_{factura_id}.xml"'
                },
                'body': base64.b64encode(xml_content).decode('utf-8'),
                'isBase64Encoded': True
            }
            
        else:
            return get_error_response(
                ValueError(f"Acción no válida: {action}"), 
                400
            )
            
    except AuthenticationError as e:
        return get_error_response(e, 401)
    except ValidationError as e:
        return get_error_response(e, 422)
    except APIError as e:
        return get_error_response(e, 500)
    except Exception as e:
        return get_error_response(e, 500) 