# SlotMaster 🚗🅿️

**Proyecto Final – Programación 1**

---

## 📌 Descripción del Proyecto

**SlotMaster** es una simulación de un estacionamiento de varios pisos, diseñada para resolver los principales problemas de los usuarios y administradores de parkings:

- Identificación rápida de espacios disponibles.
- Registro ordenado de ingresos y egresos.
- Cálculo automático y transparente de la estadía.
- Diferenciación de espacios y tarifas según el tipo de vehículo (motos, autos y 4x4).

El sistema se desarrolla con un enfoque académico, trabajando con **matrices y listas** para modelar pisos, slots y movimientos.

---

## 🎯 Objetivos

- **Visualización de ocupación por piso:** Representar y mostrar claramente el estado de cada slot.
- **Asignación y liberación de espacios:** Validar el tipo de vehículo y sugerir el lugar más adecuado.
- **Cálculo automático de costos:** Registrar la hora de entrada/salida y liquidar la estadía según reglas configurables.
- **Gestión por tipo de vehículo:** Soporte para motos, autos y 4x4 con reglas y tarifas diferenciadas.
- **Egresos por piso:** Modelar salidas en cada nivel para mejorar circulación.

---

## 📊 Reportes y Resultados

El programa genera información útil para usuarios y administradores:

- **Estado instantáneo:** Slots libres/ocupados y mapa textual por piso.
- **Métricas diarias:** Cantidad de ingresos/egresos y ocupación promedio.
- **Distribución de uso:** Espacios libres vs espacios ocupados

A futuro ->

- **Historial de movimientos:** Registro cronológico de ingresos y salidas.
- **Reportes relacionados con recaudacion y dinero:**

## 🚀 Futuras Mejoras

- Persistencia en archivos.
- Exportación de reportes.
- Algoritmos avanzados de asignación y circulación. (PILAS)

---

## 👩‍💻 Integrantes

- Iair Kaplun
- Juan Pablo Etchart
- Emma Aprile
- Klear Madera

**Profesor/a:** Ing. Verónica Galat

---

## 🏁 Conclusión

**SlotMaster** busca brindar una experiencia más eficiente y transparente en la gestión de estacionamientos, a la vez que constituye un ejercicio académico sólido en el manejo de estructuras de datos, interacción por menús y simulaciones realistas.

---

## PARAMETROS POR OMISION

Dentro del archivo interaccion_usuario -> pedir_tipo_de_vehciculo
def pedir_tipo_vehiculo():
return pedir_num_natural(min = 1, max = 4)

Dentro del archivo main.py la funcion modificar_vehiculo el nuevo_tipo y nueva_patente tiene como omision valores None

def modificar_vehiculo(garage, patente, nuevo_tipo=None, nueva_patente=None):
"""
devuelve True si se modificó, False si no se encontró la patente.
""" # Busca el vehículo por patente
for piso in garage:
for slot in piso:
if slot[3] == True and slot[1] == patente: # Modifica solo los campos que no son None
if nuevo_tipo is not None:
slot[6] = nuevo_tipo # Cambia tipo de vehículo
if nueva_patente is not None:
slot[1] = nueva_patente # Cambia patente
return True
return False

## Listas y listas de listas. (en lo posible ambas estructuras)

En estos momentos estamos trabajando con un mockdata de una matriz (que representaria el garage)
El array matricial vendria hacer el garage, y cada array que se encuentra dentro del principal representaria cada uno de los pisos.

Representación del garage: lista de pisos (matrices)

Cada elemento es: [id, patente, tipo_slot, ocupado, reservado_mensual, hora_entrada, tipo_vehiculo_estacionado]

tipo_slot: 1=moto, 2=auto, 3=camioneta, 4=multi (acepta cualquiera)

ocupado: True/False

reservado_mensual: True/False

hora_entrada: timestamp (por el momento simulamos a traves de random y funciones propias el manejo de fechas) o None si está vacío

tipo_vehiculo_estacionado: 1=moto, 2=auto, 3=camioneta, 4=bici, 0=vacío

# Comprension de listas

No trabajamos por compresion de listas pero si resolvimos los ejercicios con sumatorias y generadores resolviendo varias funciones en un solo renglon.

# Slices / Rebanadas

Para validar la patente usamos slices en la funcion modificar_vehiculo dentro del archivo main.py
Por ejemplo si la patente es ABC123, usamos slices para validar que las primeras 3 posiciones sean letras y las ultimas 3 numeros

if len(patente) == 6 and patente[:3].isalpha() and patente[3:].isdigit():

if patente[:2].isalpha() and patente[2:5].isdigit() and patente[5:].isalpha():

# Funciones lambda

Dentro del archivo interaccion_usuario -> mostrar_estado_garage implmementamos una funcion lambda para imprimir el estado de cada piso del garage

def mostrar_estado_garage(garage):
print("\n--- ESTADO DEL GARAGE ---")
imprimir_piso = lambda idx, piso: (
print(f"\nPiso {idx}:"),
[print(
f" Slot {slot[0]}: {'Ocupado' if slot[3] else 'Libre'} | Patente: {slot[1] if slot[3] else '-'} | Tipo: {slot[6] if slot[3] else '-'}"
) for slot in piso]
)
for idx in range(len(garage)):
imprimir_piso(idx, garage[idx])

# Manejo de cadenas

Normalizacion de la patente (quita espacios y pasa a mayusculas)
patente = input("ingrese la patente:").strip().upper()

Validacion de la patente (verifica que los primeros 3 caracteres sean letras y los ultimos 3 numeros)
if patente[:3].isalpha() and patente[3:].isdigit():

Formateo de cadenas (f-strings)
f"Slot {slot[0]}: {'Ocupado' if slot[3] else 'Libre'} | Patente: {slot[1] if slot[3] else '-'}"

# Excepciones

en pedir_patente() Implementamos excepeciones
def pedir_patente():
while True:
try:
patente = input("ingrese la patente:").strip().upper() # ... validaciones ...
except Exception as e:
print(e)

del mismo modo en pedir_num_natural

def pedir_num_natural(max, min=0):
while True:
try:
num = int(input("ingresa el numero: "))
if num < min or num > max: # validación de rango
else:
return num
except ValueError:
print("por favor ingresa un numero")
except Exception as e:
print(e)
