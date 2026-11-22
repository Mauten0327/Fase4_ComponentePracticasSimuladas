from excepciones import ErrorSoftwareFJ, logger_fj
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva, GestorReservasFJ


def correr_operacion(num: int, titulo: str, tarea) -> None:
    # Ejecuta cada caso de prueba manteniendo la aplicación viva ante fallos.
    print(f"\n[{num:02d}] {titulo}")
    try:
        salida = tarea()
    except ErrorSoftwareFJ as exc:
        logger_fj.error(f"Op {num:02d} ({titulo}) -> {exc} | Causa previa: {exc.__cause__}")
        print(f"   Error controlado: {exc}")
        if exc.__cause__ is not None:
            print(f"   Origen encadenado (__cause__): {exc.__cause__}")
    except Exception as exc:
        logger_fj.critical(f"Op {num:02d} ({titulo}) -> Fallo inesperado: {exc}")
        print(f"   Fallo inesperado: {exc}")
    else:
        print(f"   OK: {salida if salida is not None else 'Completada'}")
    finally:
        print(f"   Cierre de bloque 'finally' en operación {num:02d}.")


def ejecutar_simulacion() -> None:
    print("=== SOFTWARE FJ - SIMULACIÓN DE OPERACIONES (SIN BASE DE DATOS) ===")
    logger_fj.info("=== Inicio de simulación de operaciones Software FJ ===")

    gestor = GestorReservasFJ()

    # 1. Registro de cliente válido
    correr_operacion(
        1,
        "Registrar cliente válido",
        lambda: (
            c1 := Cliente("CLI-101", "Laura Gómez", "laura.gomez@empresa.com", "3105551234"),
            gestor.agregar_cliente(c1),
            c1.resumen(),
        )[-1],
    )

    # 2. Registro de cliente inválido (correo sin formato válido)
    correr_operacion(
        2,
        "Intentar registrar cliente con correo inválido",
        lambda: Cliente("CLI-102", "Carlos Ruiz", "correo_invalido", "3001112233"),
    )

    # 3. Registro de segundo cliente válido
    correr_operacion(
        3,
        "Registrar segundo cliente válido",
        lambda: (
            c2 := Cliente("CLI-103", "Andrés Pérez", "andres.perez@correo.co", "3209876543"),
            gestor.agregar_cliente(c2),
            c2.resumen(),
        )[-1],
    )

    # 4. Creación de servicio ReservaSala válido
    correr_operacion(
        4,
        "Crear servicio ReservaSala válido",
        lambda: (
            s_sala := ReservaSala("SAL-01", "Sala Reuniones Principal", 60000, 16),
            gestor.agregar_servicio(s_sala),
            s_sala.describir(),
        )[-1],
    )

    # 5. Creación de servicio AlquilerEquipo inválido (tarifa en cero/negativa)
    correr_operacion(
        5,
        "Intentar crear AlquilerEquipo con tarifa inválida",
        lambda: AlquilerEquipo("EQ-ERR", "Estación Trabajo", -20000, "Dell Latitude"),
    )

    # 6. Creación de servicios AlquilerEquipo y AsesoriaEspecializada válidos
    correr_operacion(
        6,
        "Crear servicios AlquilerEquipo y AsesoriaEspecializada",
        lambda: (
            s_eq := AlquilerEquipo("EQ-01", "Portátil Ingeniería", 25000, "ThinkPad T14"),
            s_ase := AsesoriaEspecializada("ASE-01", "Asesoría Arquitectura", 110000, "Software"),
            gestor.agregar_servicio(s_eq),
            gestor.agregar_servicio(s_ase),
            f"{s_eq.describir()} || {s_ase.describir()}",
        )[-1],
    )

    # 7. Reserva exitosa con descuento e impuesto, confirmada y procesada
    correr_operacion(
        7,
        "Crear, confirmar y procesar reserva válida con descuento e IVA",
        lambda: (
            r1 := Reserva(
                "RES-01",
                gestor.clientes[0],
                gestor.servicios[0],
                horas=4,
                descuento_pct=10,
                impuesto_pct=19,
            ),
            gestor.agregar_reserva(r1),
            r1.confirmar(),
            r1.procesar(),
            r1.detalle(),
        )[-1],
    )

    # 8. Reserva fallida con encadenamiento de excepciones (excede máximo de 12h en sala)
    correr_operacion(
        8,
        "Reserva fallida por duración inválida (encadenamiento de excepción)",
        lambda: Reserva("RES-02", gestor.clientes[0], gestor.servicios[0], horas=16),
    )

    # 9. Reserva confirmada y luego cancelada válidamente
    correr_operacion(
        9,
        "Crear, confirmar y cancelar reserva válidamente",
        lambda: (
            r2 := Reserva("RES-03", gestor.clientes[1], gestor.servicios[2], horas=3),
            gestor.agregar_reserva(r2),
            r2.confirmar(),
            r2.cancelar("Cambio de agenda del cliente"),
            r2.detalle(),
        )[-1],
    )

    # 10. Operación no permitida: cancelar una reserva ya procesada
    correr_operacion(
        10,
        "Intentar cancelar una reserva ya procesada",
        lambda: gestor.reservas[0].cancelar("Solicitud tardía"),
    )

    # 11. Servicio marcado como no disponible e intento de reserva
    correr_operacion(
        11,
        "Marcar equipo no disponible e intentar reservarlo",
        lambda: (
            setattr(gestor.servicios[1], "disponible", False),
            Reserva("RES-04", gestor.clientes[1], gestor.servicios[1], horas=5),
        )[-1],
    )

    # 12. Consulta de estado final de las listas en memoria
    correr_operacion(
        12,
        "Verificar integridad final de listas en memoria",
        lambda: (
            f"Clientes={len(gestor.clientes)}, "
            f"Servicios={len(gestor.servicios)}, "
            f"Reservas={len(gestor.reservas)}"
        ),
    )

    print("\n=== RESUMEN FINAL EN MEMORIA ===")
    for cli in gestor.clientes:
        print(" -", cli.resumen())
    for srv in gestor.servicios:
        print(" -", srv.describir(), f"| Disponible={srv.disponible}")
    for res in gestor.reservas:
        print(" -", res.detalle())


if __name__ == "__main__":
    ejecutar_simulacion()