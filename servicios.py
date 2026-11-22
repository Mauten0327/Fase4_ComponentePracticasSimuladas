from abc import ABC, abstractmethod
from excepciones import (
    ErrorDatoInvalido,
    ErrorParametroFaltante,
    ErrorCalculoCosto,
)


class Servicio(ABC):
    # Clase base abstracta para los servicios que ofrece Software FJ.
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        if not codigo or not str(codigo).strip():
            raise ErrorParametroFaltante("El código del servicio es obligatorio.")
        if not nombre or not str(nombre).strip():
            raise ErrorParametroFaltante("El nombre del servicio es obligatorio.")
        if tarifa_hora is None or float(tarifa_hora) <= 0:
            raise ErrorDatoInvalido("La tarifa por hora debe ser mayor que cero.")

        self._codigo = str(codigo).strip().upper()
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, horas: float) -> None:
        # Cada tipo de servicio valida sus propios límites de tiempo o uso.
        pass

    @abstractmethod
    def describir(self) -> str:
        # Cada servicio detalla sus atributos específicos.
        pass

    # Variantes de cálculo de costo mediante parámetros opcionales (sobrecarga en Python).
    def calcular_costo(
        self,
        horas: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        recargo_fijo: float = 0.0,
    ) -> float:
        if horas is None or float(horas) <= 0:
            raise ErrorDatoInvalido("La duración en horas debe ser mayor que cero.")
        if descuento_pct < 0 or descuento_pct >= 100:
            raise ErrorCalculoCosto("El porcentaje de descuento debe estar entre 0 y 99.")
        if impuesto_pct < 0 or recargo_fijo < 0:
            raise ErrorCalculoCosto("El impuesto y el recargo fijo no pueden ser negativos.")

        self.validar_parametros(horas)

        subtotal = self._tarifa_hora * float(horas)
        con_descuento = subtotal * (1 - (float(descuento_pct) / 100.0))
        con_recargo = con_descuento + float(recargo_fijo)
        total = con_recargo * (1 + (float(impuesto_pct) / 100.0))

        if total <= 0:
            raise ErrorCalculoCosto("El cálculo produjo un total menor o igual a cero.")

        return round(total, 2)


class ReservaSala(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if capacidad is None or int(capacidad) < 1:
            raise ErrorDatoInvalido("La capacidad de la sala debe ser al menos de 1 persona.")
        self.capacidad = int(capacidad)

    def validar_parametros(self, horas: float) -> None:
        # Evita bloqueos prolongados de salas en una sola reserva.
        if float(horas) < 1 or float(horas) > 12:
            raise ErrorDatoInvalido("Una reserva de sala debe durar entre 1 y 12 horas.")

    def describir(self) -> str:
        return (
            f"Sala [{self._codigo}] {self._nombre} | "
            f"Capacidad: {self.capacidad} | Tarifa/h: ${self._tarifa_hora:,.2f}"
        )


class AlquilerEquipo(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, referencia: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not referencia or not str(referencia).strip():
            raise ErrorParametroFaltante("La referencia del equipo es obligatoria.")
        self.referencia = str(referencia).strip()

    def validar_parametros(self, horas: float) -> None:
        if float(horas) > 72:
            raise ErrorDatoInvalido("El alquiler continuo de equipo no puede superar 72 horas.")

    def describir(self) -> str:
        return (
            f"Equipo [{self._codigo}] {self._nombre} ({self.referencia}) | "
            f"Tarifa/h: ${self._tarifa_hora:,.2f}"
        )


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, area: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not area or not str(area).strip():
            raise ErrorParametroFaltante("El área de especialidad es obligatoria.")
        self.area = str(area).strip()

    def validar_parametros(self, horas: float) -> None:
        if float(horas) < 0.5 or float(horas) > 20:
            raise ErrorDatoInvalido("La asesoría debe durar entre 0.5 y 20 horas.")

    def describir(self) -> str:
        return (
            f"Asesoría [{self._codigo}] {self._nombre} | "
            f"Área: {self.area} | Tarifa/h: ${self._tarifa_hora:,.2f}"
        )