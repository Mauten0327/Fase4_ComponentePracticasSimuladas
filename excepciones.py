import logging
from pathlib import Path


def configurar_logger(ruta_log: str = "logs/sistema_fj.log") -> logging.Logger:
    # Crea la carpeta de logs si todavía no existe para evitar fallos de ruta.
    archivo_log = Path(ruta_log)
    archivo_log.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evita duplicar handlers si el módulo se importa más de una vez.
    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler = logging.FileHandler(archivo_log, mode="a", encoding="utf-8")
        handler.setFormatter(formato)
        logger.addHandler(handler)

    return logger


logger_fj = configurar_logger()


class ErrorSoftwareFJ(Exception):
    # Base común para diferenciar errores del negocio frente a fallos del sistema.
    def __init__(self, mensaje: str, codigo: str = "FJ_ERR"):
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


class ErrorDatoInvalido(ErrorSoftwareFJ):
    # Datos con formato incorrecto o valores fuera de rango.
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ_DATO_INVALIDO")


class ErrorParametroFaltante(ErrorSoftwareFJ):
    # Campos o argumentos obligatorios ausentes o vacíos.
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ_PARAM_FALTANTE")


class ErrorOperacionInvalida(ErrorSoftwareFJ):
    # Acciones que rompen reglas de estado o duplicidad.
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ_OP_INVALIDA")


class ErrorDisponibilidadServicio(ErrorSoftwareFJ):
    # Servicio inactivo o no disponible para reserva.
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ_NO_DISPONIBLE")


class ErrorCalculoCosto(ErrorSoftwareFJ):
    # Inconsistencias al calcular tarifas, descuentos, recargos o impuestos.
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ_CALCULO_ERR")
        