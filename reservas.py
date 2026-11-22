from excepciones import (
    ErrorDatoInvalido,
    ErrorOperacionInvalida,
    ErrorDisponibilidadServicio,
    ErrorSoftwareFJ,
    logger_fj,
)
from entidades import Cliente
from servicios import Servicio


class Reserva:
    # Gestiona el ciclo de vida de una reserva sin persistencia en base de datos.
    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        horas: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        recargo_fijo: float = 0.0,
    ):
        if not id_reserva or not str(id_reserva).strip():
            raise ErrorDatoInvalido("El identificador de la reserva es obligatorio.")
        if not isinstance(cliente, Cliente):
            raise ErrorDatoInvalido("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ErrorDatoInvalido("Se requiere una instancia válida de Servicio.")
        if not cliente.activo:
            raise ErrorOperacionInvalida(f"El cliente {cliente.id_entidad} no está activo.")
        if not servicio.disponible:
            raise ErrorDisponibilidadServicio(
                f"El servicio {servicio.codigo} no está disponible para reservar."
            )

        # Encadena la excepción original si el cálculo o las reglas de duración fallan.
        try:
            self.total = servicio.calcular_costo(
                horas,
                descuento_pct=descuento_pct,
                impuesto_pct=impuesto_pct,
                recargo_fijo=recargo_fijo,
            )
        except ErrorSoftwareFJ as exc:
            raise ErrorOperacionInvalida(
                f"Falló la creación de la reserva '{id_reserva}' al validar costos/parámetros."
            ) from exc

        self.id_reserva = str(id_reserva).strip().upper()
        self.cliente = cliente
        self.servicio = servicio
        self.horas = float(horas)
        self.estado = "PENDIENTE"

    def confirmar(self) -> None:
        if self.estado == "CANCELADA":
            raise ErrorOperacionInvalida(f"La reserva {self.id_reserva} está cancelada y no puede confirmarse.")
        if self.estado in {"CONFIRMADA", "PROCESADA"}:
            raise ErrorOperacionInvalida(
                f"La reserva {self.id_reserva} ya fue {self.estado.lower()}."
            )
        if not self.servicio.disponible:
            raise ErrorDisponibilidadServicio(
                f"No se puede confirmar {self.id_reserva}: el servicio {self.servicio.codigo} no está disponible."
            )
        self.estado = "CONFIRMADA"
        logger_fj.info(f"Reserva {self.id_reserva} confirmada para {self.cliente.id_entidad}.")

    def procesar(self) -> float:
        if self.estado != "CONFIRMADA":
            raise ErrorOperacionInvalida(
                f"Solo reservas confirmadas pueden procesarse. Estado de {self.id_reserva}: {self.estado}."
            )
        self.estado = "PROCESADA"
        logger_fj.info(f"Reserva {self.id_reserva} procesada por valor de ${self.total:,.2f}.")
        return self.total

    def cancelar(self, motivo: str = "Cancelada por solicitud") -> None:
        if self.estado == "PROCESADA":
            raise ErrorOperacionInvalida(
                f"No es posible cancelar {self.id_reserva} porque ya fue procesada."
            )
        if self.estado == "CANCELADA":
            raise ErrorOperacionInvalida(f"La reserva {self.id_reserva} ya estaba cancelada.")
        self.estado = "CANCELADA"
        logger_fj.warning(f"Reserva {self.id_reserva} cancelada. Motivo: {motivo}")

    def detalle(self) -> str:
        return (
            f"Reserva [{self.id_reserva}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.codigo} | Horas: {self.horas} | "
            f"Total: ${self.total:,.2f} | Estado: {self.estado}"
        )


class GestorReservasFJ:
    # Mantiene colecciones en memoria durante la ejecución del programa.
    def __init__(self):
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def agregar_cliente(self, cliente: Cliente) -> None:
        if any(c.id_entidad == cliente.id_entidad for c in self.clientes):
            raise ErrorOperacionInvalida(f"Cliente duplicado con ID {cliente.id_entidad}.")
        self.clientes.append(cliente)
        logger_fj.info(f"Cliente agregado: {cliente.id_entidad} - {cliente.nombre}")

    def agregar_servicio(self, servicio: Servicio) -> None:
        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise ErrorOperacionInvalida(f"Servicio duplicado con código {servicio.codigo}.")
        self.servicios.append(servicio)
        logger_fj.info(f"Servicio agregado: {servicio.codigo} - {servicio.nombre}")

    def agregar_reserva(self, reserva: Reserva) -> None:
        if any(r.id_reserva == reserva.id_reserva for r in self.reservas):
            raise ErrorOperacionInvalida(f"Reserva duplicada con ID {reserva.id_reserva}.")
        self.reservas.append(reserva)
        logger_fj.info(f"Reserva registrada: {reserva.id_reserva}")