"""Entidades de dominio para el sistema académico de subastas en memoria."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum


class ErrorSubasta(ValueError):
    """Incumplimiento de una regla de negocio."""


def a_dinero(valor: object) -> Decimal:
    """Normaliza importes sin introducir errores de precisión binaria."""
    try:
        importe = Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise ErrorSubasta("El importe debe ser numérico.") from exc
    if not importe.is_finite() or importe.as_tuple().exponent < -2:
        raise ErrorSubasta("El importe debe ser finito y tener como máximo dos decimales.")
    return importe.quantize(Decimal("0.01"))


class Usuario(ABC):
    """Clase abstracta con los datos compartidos de los participantes."""

    def __init__(self, identificador: int, nombre: str, correo: str) -> None:
        if identificador <= 0 or not nombre.strip() or "@" not in correo:
            raise ErrorSubasta("Identificador, nombre o correo inválido.")
        self._id = identificador
        self._nombre = nombre.strip()
        self._correo = correo.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    @abstractmethod
    def descripcion_rol(self) -> str:
        """Permite demostrar polimorfismo entre tipos de usuario."""


class Vendedor(Usuario):
    def descripcion_rol(self) -> str:
        return "Vendedor"

    def crear_producto(self, identificador: int, nombre: str, descripcion: str) -> Producto:
        return Producto(identificador, nombre, descripcion, self)


class Comprador(Usuario):
    def descripcion_rol(self) -> str:
        return "Comprador"

    def ofertar(self, subasta: Subasta, importe: object) -> Puja:
        return subasta.registrar_puja(self, importe)


class Producto:
    def __init__(self, identificador: int, nombre: str, descripcion: str, vendedor: Vendedor) -> None:
        if identificador <= 0 or not nombre.strip() or not descripcion.strip():
            raise ErrorSubasta("Producto inválido.")
        self._id = identificador
        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()
        self._vendedor = vendedor

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def vendedor(self) -> Vendedor:
        return self._vendedor


class EstadoSubasta(Enum):
    ACTIVA = "ACTIVA"
    CERRADA = "CERRADA"


class Puja:
    """Una puja pertenece a una única subasta (composición UML)."""

    def __init__(self, comprador: Comprador, importe: Decimal, fecha: datetime) -> None:
        self._comprador = comprador
        self._importe = importe
        self._fecha = fecha

    @property
    def comprador(self) -> Comprador:
        return self._comprador

    @property
    def importe(self) -> Decimal:
        return self._importe

    @property
    def fecha(self) -> datetime:
        return self._fecha


class Subasta:
    def __init__(self, identificador: int, producto: Producto, precio_inicial: object) -> None:
        precio = a_dinero(precio_inicial)
        if identificador <= 0 or precio <= 0:
            raise ErrorSubasta("Identificador o precio inicial inválido.")
        self._id = identificador
        self._producto = producto
        self._precio_inicial = precio
        self._estado = EstadoSubasta.ACTIVA
        self._pujas: list[Puja] = []
        self._ganador: Comprador | None = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def precio_inicial(self) -> Decimal:
        return self._precio_inicial

    @property
    def estado(self) -> EstadoSubasta:
        return self._estado

    @property
    def pujas(self) -> tuple[Puja, ...]:
        return tuple(self._pujas)

    @property
    def precio_actual(self) -> Decimal:
        return self._pujas[-1].importe if self._pujas else self._precio_inicial

    @property
    def ganador(self) -> Comprador | None:
        return self._ganador

    def registrar_puja(self, comprador: Comprador, importe: object) -> Puja:
        if self._estado is not EstadoSubasta.ACTIVA:
            raise ErrorSubasta("No se puede pujar por una subasta cerrada.")
        if comprador.id == self._producto.vendedor.id:
            raise ErrorSubasta("El vendedor no puede ofertar por su propia subasta.")
        valor = a_dinero(importe)
        if valor <= self.precio_actual:
            raise ErrorSubasta("La oferta debe superar el precio actual.")
        puja = Puja(comprador, valor, datetime.now().astimezone())
        self._pujas.append(puja)
        return puja

    def cerrar(self) -> Comprador | None:
        if self._estado is EstadoSubasta.CERRADA:
            raise ErrorSubasta("La subasta ya está cerrada.")
        self._estado = EstadoSubasta.CERRADA
        self._ganador = self._pujas[-1].comprador if self._pujas else None
        return self._ganador
