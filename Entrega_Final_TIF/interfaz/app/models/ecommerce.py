from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ItemCarrito(BaseModel):
    id_variante: int = Field(..., gt=0, description="ID de la variante elegida")
    cantidad: int = Field(..., gt=0, description="Cantidad a comprar")


class PreciosWeb(BaseModel):
    precio_base: Decimal = Field(..., description="Precio base cargado en el sistema")
    precio_lista_web: Decimal = Field(..., description="Precio lista web (+25% financiero y +5% logístico)")
    precio_transferencia: Decimal = Field(..., description="Precio con 20% OFF por transferencia")
    ahorro_transferencia: Decimal = Field(..., description="Monto ahorrado pagando con transferencia")


class ProductoWebResponse(BaseModel):
    id_producto: int
    nombre_producto: str
    sku: Optional[str] = None
    descripcion: Optional[str] = None
    nombre_categoria: str
    nombre_material: str
    precios: PreciosWeb
    imagenes: List[str] = []
    stock_total: int
    variantes: List[dict] = []


class CheckoutTransferenciaCreate(BaseModel):
    nombre_cliente: str = Field(..., min_length=2, max_length=100)
    email_cliente: str = Field(..., min_length=5, max_length=120)
    telefono_cliente: str = Field(..., min_length=6, max_length=30)
    direccion_envio: str = Field(..., min_length=5, max_length=200)
    zona_envio: str = Field(..., pattern="^(Centro|Norte|Sur)$", description="Zona de entrega en Paraná")
    items: List[ItemCarrito] = Field(..., min_length=1)
    observaciones: Optional[str] = None


class CheckoutMercadoPagoCreate(BaseModel):
    nombre_cliente: str = Field(..., min_length=2, max_length=100)
    email_cliente: str = Field(..., min_length=5, max_length=120)
    telefono_cliente: str = Field(..., min_length=6, max_length=30)
    direccion_envio: str = Field(..., min_length=5, max_length=200)
    zona_envio: str = Field(..., pattern="^(Centro|Norte|Sur)$", description="Zona de entrega en Paraná")
    items: List[ItemCarrito] = Field(..., min_length=1)


class DetallePedidoResponse(BaseModel):
    renglon: int
    id_variante: int
    nombre_producto: str
    nombre_color: str
    nombre_tamano: str
    cantidad: int
    precio_unitario_cobrado: Decimal
    subtotal: Decimal


class PedidoWebResponse(BaseModel):
    id_pedido: int
    codigo_seguimiento: str
    fecha_creacion: datetime
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: str
    direccion_envio: str
    zona_envio: str
    costo_envio: Decimal
    metodo_pago: str
    estado: str
    subtotal: Decimal
    total: Decimal
    comprobante_url: Optional[str] = None
    mp_preference_id: Optional[str] = None
    mp_payment_id: Optional[str] = None
    fecha_expiracion: Optional[datetime] = None
    detalles: Optional[List[DetallePedidoResponse]] = None

    class Config:
        from_attributes = True
