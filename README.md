# Fase4_ComponentePracticasSimuladas
# Fase4_ComponentePracticasSimuladas — Software FJ

Aplicación orientada a objetos en Python para gestionar clientes, servicios y reservas de **Software FJ** (salas, alquiler de equipos y asesorías especializadas), trabajando únicamente con objetos y listas en memoria, sin base de datos, y registrando eventos y errores en archivo de log[cite: 1, 2, 3].

## Módulos del proyecto
- `excepciones.py`: excepciones del dominio y configuración del registro en `logs/sistema_fj.log`[cite: 2, 3].
- `entidades.py`: clase abstracta `EntidadSistema` y clase `Cliente` con encapsulación y validaciones[cite: 2].
- `servicios.py`: clase abstracta `Servicio`, clases derivadas (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) con polimorfismo y cálculo de costo con parámetros opcionales[cite: 2].
- `reservas.py`: clase `Reserva` (estados, confirmación, procesamiento, cancelación y encadenamiento de excepciones) y `GestorReservasFJ` en memoria[cite: 1, 2, 3].
- `main.py`: ejecución de 12 operaciones (casos válidos e inválidos, disponibilidad y manejo continuo con `try/except/else/finally`)[cite: 2, 3, 4].

## Ejecución
```bash
python3 excepciones.py
python3 entidades.py
python3 servicios.py
python3 reservas.py
python3 main.py