<!--

Pisos

matrices:
cada fila es un piso

 -->

[[planta baja],[piso 1],[piso 2], [piso 3]]

cada piso es a su vez una matriz

A futuro: transformar el arreglo de

representacion de slot

enum1: auto, camioneta, moto, bici

[
id: int incremental + 1
patente: string
tipo_vehiculo: enum1
espacio_ocupado: booleano
espacio_reservado_mensualmente: booleano
]

funcionalidad

ver espacios disponbiles en la matriz entera
ver espacios disponibles por piso

buscar el lugar de un auto estacionado

    •	Definir edificio: cantidad de pisos, filas y columnas por piso.
    •	Tipos de slot por celda: moto / auto / 4x4 / multi; posibilidad de marcar “reservado mensual”.
    •	Salidas por piso: una posición por nivel para medir “cercanía”.
    •	Tarifas: por tipo de vehículo (base + fracción o por hora), regla de redondeo (a 30/60 min).
    •	Reloj: fuente de tiempo (simulado o del sistema).

Criterios de aceptación
• Queda un estado inicial coherente (total de slots, por tipo, por piso).
• Se puede listar la configuración actual.

    Operación diaria (MVP)

Ingreso de vehículo
• Datos: patente, tipo.
• Sugerencia de slot: debe aceptar el tipo y no estar reservado (o validar permiso).
• Heurística: “más cercano” a la salida del piso elegido (o primer libre que cumpla).
• Registrar: piso, celda, hora de entrada.

Aceptación
• Rechaza duplicados (misma patente adentro).
• Rechaza tipo incompatible / slot reservado indebidamente.

Egreso de vehículo
• Ubicar por patente.
• (Si usan modelo con bloqueos): informar cuántos/qué autos hay que mover.
• Calcular tiempo y costo según la tarifa configurada.
• Liberar slot.
• Comprobante: patente, tipo, piso/celda, horas, tarifa aplicada y total.

Aceptación
• No permite egresar patentes inexistentes.
• Aplica redondeos de tiempo definidos.

Reubicación (Opcional útil)
• Mover un vehículo a otro slot válido (misma regla de asignación).
• Mantener la hora de ingreso original.
• Loguear el evento.

Consultas de disponibilidad (MVP)
• Global: total de libres/ocupados en todo el edificio.
• Por piso: libres/ocupados por nivel.
• Por tipo: libres para moto / auto / 4x4 (global y por piso).
• Mapa del piso (texto): matriz con marcadores (., M, A, 4, R).

Aceptación
• Las cuentas coinciden con el mapa.
• Filtros por tipo funcionan.

Búsquedas (MVP)
• Por patente: devolver piso, fila, columna y hora de entrada.
• Por slot: dado piso/fila/columna, mostrar estado (libre/ocupado, quién).
• Permanencias largas (Opcional): listar vehículos con estadía > N horas.

Reportes (MVP)
• Estado instantáneo por piso: totales, libres, ocupados, por tipo.
• Historial de eventos: ingresos, egresos, reubicaciones (timestamp, piso, celda, patente).
• Recaudación acumulada: total y por tipo de vehículo.
• Tiempo promedio de estadía (Opcional).
• Distribución por tipo (porcentaje de uso y aporte a caja) (Opcional).
• Cierre del día: resumen compacto de ocupación y recaudación (MVP u Opcional según tiempo).

Aceptación
• Los totales de recaudación coinciden con la suma de comprobantes.
• El historial está ordenado cronológicamente.

Validaciones y reglas (MVP)
• Patentes únicas dentro del edificio.
• No asignar slot incompatible con el tipo.
• Respeto de “reservado mensual” (bloquea o pide confirmación).
• No permitir salida si no hay ingreso registrado.
• Manejo básico de errores de entrada (patente vacía, tipo inválido).

Reservas mensuales
• Marcar/desmarcar un slot como reservado.
• Política: solo ingresar si la patente está en la lista de ese slot o bloquear con mensaje.
• Reporte: uso de reservados vs. reales.

Parametrización en ejecución (Opcional)
• Cambiar tarifas y/o fracción de tiempo durante la sesión.
• Cambiar heurística de asignación (probar “primer libre” vs. “más cercano”).
• Generar ocupación aleatoria de prueba (semilla).

No funcionales (MVP)
• Salidas de texto claras y compactas.
• Operaciones en tiempo razonable sobre matrices (recorridos lineales).
• Estados siempre consistentes (no hay doble ocupación; liberar/ocupar sincronizado).

División sugerida de trabajo (4 personas)
• A) Modelo & Layout: configuración inicial, mapa, tipos de slot, salidas por piso, validaciones base.
• B) Ingreso & Asignación: heurística, compatibilidad por tipo, registro de entradas, reservas (si va).
• C) Egreso & Facturación: búsqueda por patente, bloqueos (si aplica), cálculo de tiempo/costo, comprobante.
• D) Reportes & Menú / QA: consultas de disponibilidad, reportes de uso/recaudación, historial, pruebas y casos borde.

!!A FUTURO
Bloqueos / movimientos (si el modelo lo contempla)
• Definir claramente el layout:
• Modelo “fila apilada”: una fila necesita liberar “los de adelante” para que salga el de atrás.
→ Dado un slot, contar cuántos ocupan posiciones previas hacia el pasillo y listarlos.
• Modelo “no bloqueante”: cada slot colinda con pasillo → nunca requiere mover otros.
• Reportar en egreso: cantidad de movimientos y patentes a mover.

Aceptación
• Para un mismo layout, el conteo de bloqueos es determinista y coherente con el mapa.
