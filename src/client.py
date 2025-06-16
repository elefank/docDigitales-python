import os
import json
import requests
from typing import Dict, Any, Optional, Union
from datetime import datetime
from .exceptions import DocDigitalesAPIError, AuthenticationError, ValidationError, APIError
from .models import Factura, RespuestaFactura

class DocDigitalesClient:
    """Cliente para interactuar con la API de DocDigitales"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.docdigitales.com"):
        """
        Inicializa el cliente de DocDigitales
        
        Args:
            api_key (str): Clave de API para autenticación
            base_url (str): URL base de la API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token token={self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza una petición a la API
        
        Args:
            method (str): Método HTTP (GET, POST, etc.)
            endpoint (str): Endpoint de la API
            data (Dict[str, Any], optional): Datos a enviar en el cuerpo
            params (Dict[str, Any], optional): Parámetros de URL
            
        Returns:
            Dict[str, Any]: Respuesta de la API
            
        Raises:
            AuthenticationError: Si hay un error de autenticación
            ValidationError: Si hay un error de validación
            APIError: Si hay un error general de la API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, json=data, params=params)
            
            if response.status_code == 401:
                raise AuthenticationError("Error de autenticación: API key inválida")
            elif response.status_code == 422:
                raise ValidationError(f"Error de validación: {response.json().get('error', 'Datos inválidos')}")
            elif response.status_code >= 400:
                raise APIError(f"Error en la API: {response.text}")
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error en la comunicación con la API: {str(e)}")

    def facturar(self, factura: Union[Factura, Dict[str, Any]]) -> RespuestaFactura:
        """
        Envía una factura a la API para su procesamiento
        
        Args:
            factura (Union[Factura, Dict[str, Any]]): Datos de la factura
            
        Returns:
            RespuestaFactura: Respuesta con los datos de la factura procesada
        """
        if isinstance(factura, dict):
            factura = Factura(**factura)
            
        datos = factura.model_dump(exclude_none=True)
        respuesta = self._make_request("POST", "/api/v1/facturas", data=datos)
        return RespuestaFactura(**respuesta)

    def consultar_estado(self, factura_id: str) -> RespuestaFactura:
        """
        Consulta el estado de una factura
        
        Args:
            factura_id (str): ID de la factura a consultar
            
        Returns:
            RespuestaFactura: Estado actual de la factura
        """
        respuesta = self._make_request("GET", f"/api/v1/facturas/{factura_id}")
        return RespuestaFactura(**respuesta)

    def cancelar_factura(self, factura_id: str, motivo: str) -> Dict[str, Any]:
        """
        Cancela una factura
        
        Args:
            factura_id (str): ID de la factura a cancelar
            motivo (str): Motivo de la cancelación
            
        Returns:
            Dict[str, Any]: Respuesta de la cancelación
        """
        data = {"motivo": motivo}
        return self._make_request("POST", f"/api/v1/facturas/{factura_id}/cancelar", data=data)

    def descargar_pdf(self, factura_id: str) -> bytes:
        """
        Descarga el PDF de una factura
        
        Args:
            factura_id (str): ID de la factura
            
        Returns:
            bytes: Contenido del PDF
        """
        url = f"{self.base_url}/api/v1/facturas/{factura_id}/pdf"
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

    def descargar_xml(self, factura_id: str) -> bytes:
        """
        Descarga el XML de una factura
        
        Args:
            factura_id (str): ID de la factura
            
        Returns:
            bytes: Contenido del XML
        """
        url = f"{self.base_url}/api/v1/facturas/{factura_id}/xml"
        response = self.session.get(url)
        response.raise_for_status()
        return response.content 