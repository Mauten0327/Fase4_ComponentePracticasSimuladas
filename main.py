from excepciones import ErrorSoftwareFJ, logger_fj
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva, GestorReservasFJ


def correr_operacion(num: int, titulo: str, tarea) -> None:
    # Mantiene la app estable ante errores y registra todo en log.
    print(f"\n[{num:02d}] {titulo}")
    try:
        salida = tarea()
    except ErrorSoftwareFJ as exc:
        logger_fj.error(f"Op {num:02d} ({titulo}) -> {exc} | Causa: {exc.__cause__}")
        print(f"   Error controlado: {exc}")
        if exc.__cause__ is not None:
            print(f"   Causa encadenada: {exc.__cause__}")
    except Exception as exc:
        logger_fj.critical(f"Op {num:02d} ({titulo}) -> Inesperado: {exc}")
        print(f"   Error inesperado: {exc}")
    else:
        print(f"   OK: {salida if salida is not None else 'Completada'}")
    finally:
        print(f"   Fin de bloque finally en op {num:02d}.")


def main() -> None:
    print("=== SOFTWARE FJ - SIMULACIÓN DE 12 OPERACIONES ===")
    logger_fj.info("=== Inicio de simulación Software FJ ===")

    gestor = GestorReservasFJ()

    # 1. Cliente válido
    correr_operacion(
        1,
        "Registrar cliente válido",
        lambda: (
            c1 := Cliente("CLI-01", "Laura Gómez", "laura@empresa.com", "3105551234"),
            gestor.agregar_cliente(c1),
            c1.resumen(),
        )[-1],
    )

    # 2. Cliente inválido
    correr_operacion(
        2,
        "Registrar cliente con correo inválido",
        lambda: Cliente("CLI-02", "Carlos Ruiz", "correo_malo", "3001112233"),
    )

    # 3. Segundo cliente válido
    correr_operacion(
        3,
        "Registrar segundo cliente válido",
        lambda: (
            c2 := Cliente("CLI-03", "Andrés Pérez", "andres@correo.co", "3209876543"),
            gestor.agregar_cliente(c2),
            c2.resumen(),
        )[-1],
    )

    # 4. Servicio ReservaSala válido
    correr_operacion(
        4,
        "Crear servicio ReservaSala válido",
        lambda: (
            sala := ReservaSala("SAL-01", "Sala Principal", 60000, 15),
            gestor.agregar_servicio(sala),
            sala.describir(),
        )[-1],
    )

    # 5. Servicio AlquilerEquipo inválido
    correr_operacion(
        5,
        "Intentar crear AlquilerEquipo con tarifa negativa",
        lambda: AlquilerEquipo("EQ-ERR", "Portátil Error", -10000, "HP EliteBook"),
    )

    # 6. Servicios AlquilerEquipo y AsesoriaEspecializada válidos
    correr_operacion(
        6,
        "Crear servicios AlquilerEquipo y AsesoriaEspecializada",
        lambda: (
            eq := AlquilerEquipo("EQ-01", "Portátil Dev", 25000, "ThinkPad T14"),
            ase := AsesoriaEspecializada("ASE-01", "Asesoría TI", 110000, "Software"),
            gestor.agregar_servicio(eq),
            gestor.agregar_servicio(ase),
            f"{eq.describir()} | {ase.describir()}",
        )[-1],
    )

    # 7. Reserva exitosa, confirmada y procesada
    correr_operacion(
        7,
        "Crear, confirmar y procesar reserva válida",
        lambda: (
            r1 := Reserva("RES-01", gestor.clientes[0], gestor.servicios[0], horas=4, descuento_pct=10, impuesto_pct=19),
            gestor.agregar_reserva(r1),
            r1.confirmar(),
            r1.procesar(),
            r1.detalle(),
        )[-1],
    )

    # 8. Reserva fallida con encadenamiento de excepciones
    correr_operacion(
        8,
        "Reserva fallida por duración inválida (encadenada)",
        lambda: Reserva("RES-02", gestor.clientes[0], gestor.servicios[0], horas=16),
    )

    # 9. Reserva confirmada y luego cancelada
    correr_operacion(
        9,
        "Crear, confirmar y cancelar reserva válida",
        lambda: (
            r2 := Reserva("RES-03", gestor.clientes[1], gestor.servicios[2], horas=3),
            gestor.agregar_reserva(r2),
            r2.confirmar(),
            r2.cancelar("Cambio de agenda"),
            r2.detalle(),
        )[-1],
    )

    # 10. Cancelar reserva ya procesada (operación no permitida)
    correr_operacion(
        10,
        "Intentar cancelar reserva ya procesada",
        lambda: gestor.reservas[0].cancelar("Tarde"),
    )

    # 11. Servicio no disponible al intentar reservar
    correr_operacion(
        11,
        "Marcar equipo no disponible e intentar reservar",
        lambda: (
            setattr(gestor.servicios[1], "disponible", False),
            Reserva("RES-04", gestor.clientes[1], gestor.servicios[1], horas=5),
        )[-1],
    )

    # 12. Resumen final en memoria
    correr_operacion(
        12,
        "Verificar estado final de listas en memoria",
        lambda: f"Clientes={len(gestor.clientes)}, Servicios={len(gestor.servicios)}, Reservas={len(gestor.reservas)}",
    )


if __name__ == "__main__":
    main()