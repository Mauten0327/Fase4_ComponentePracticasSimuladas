from abc import ABC, abstractmethod
import re
from excepciones import ErrorDatoInvalido, ErrorParametroFaltante
class EntidadSistema(ABC):
    # Clase abstracta base para entidades generales del sistema (sin BD).
    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise ErrorParametroFaltante("El identificador de la entidad es obligatorio.")
        self._id_entidad = str(id_entidad).strip().upper()

        @property
        def id_entidad(self) -> str:
        # Expone el ID en modo lectura para evitar alteraciones accidentales.
            return self._id_entidad

    @abstractmethod
    def resumen(self) -> str:
        # Cada subclase define cómo resumir su estado actual.
        pass

class Cliente(EntidadSistema):
    # Encapsula datos del cliente y valida reglas básicas al asignar o modificar.
    
    def __init__(
        self,
        id_cliente: str,
        nombre: str,
        correo: str,
        telefono: str,
        activo: bool = True,
    ):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self._activo = bool(activo)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorDatoInvalido("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ErrorDatoInvalido("El correo electrónico es obligatorio.")
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron_correo, valor.strip()):
            raise ErrorDatoInvalido(f"Formato de correo inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        # Conserva solo dígitos para normalizar números con espacios o guiones.
        solo_digitos = re.sub(r"\D", "", str(valor or ""))
        if len(solo_digitos) < 7 or len(solo_digitos) > 15:
            raise ErrorDatoInvalido(f"Teléfono fuera de rango (7 a 15 dígitos): '{valor}'.")
        self._telefono = solo_digitos

    @property
    def activo(self) -> bool:
        return self._activo

    def cambiar_estado(self, activo: bool) -> None:
        self._activo = bool(activo)

    def resumen(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente [{self._id_entidad}] {self._nombre} | "
            f"Correo: {self._correo} | Tel: {self._telefono} | Estado: {estado}"
        )