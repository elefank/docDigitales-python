from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class Cliente(BaseModel):
    """Modelo para los datos del cliente"""
    rfc: str = Field(..., min_length=12, max_length=13)
    nombre: str = Field(..., min_length=1)
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    direccion: Optional[str] = None

class Concepto(BaseModel):
    """Modelo para los conceptos de la factura"""
    clave_producto: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    cantidad: float = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)
    unidad: str = Field(..., min_length=1)

class Factura(BaseModel):
    """Modelo para la factura"""
    serie: Optional[str] = None
    folio: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.now)
    cliente: Cliente
    conceptos: List[Concepto] = Field(..., min_items=1)
    moneda: str = Field(default="MXN")
    metodo_pago: str = Field(default="PPD")
    forma_pago: str = Field(default="01")
    tipo_comprobante: str = Field(default="I")
    uso_cfdi: str = Field(default="G01")
    observaciones: Optional[str] = None

class RespuestaFactura(BaseModel):
    """Modelo para la respuesta de la API al crear una factura"""
    id: str
    uuid: str
    estado: str
    fecha_creacion: datetime
    fecha_timbrado: Optional[datetime] = None
    pdf_url: Optional[str] = None
    xml_url: Optional[str] = None
    mensaje: Optional[str] = None 