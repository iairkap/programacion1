## Funcionalidades

**Pasos:**
1. Pedir al usuario el piso a consultar.
2. Validar que el piso ingresado exista.
   - Si no es válido, mostrar mensaje de error.
3. Mostrar la cantidad de slots libres en ese piso.

---

### 2. Conteo de Vehículos Estacionados

- Contar cuántos autos, motos y camionetas hay estacionados en el garage.
- Mostrar los resultados al usuario.

---

### 3. Salida Amigable de la Lectura del Garage

- Crear una función que muestre el estado del garage de forma clara y ordenada para el usuario.

---

### 4. Reubicar un Vehículo

- Permitir al usuario reubicar un vehículo dentro del garage.

**Pasos:**
1. Pedir al usuario la patente del vehículo a reubicar.
2. Buscar la patente en el garage.
   - Si no se encuentra, mostrar mensaje de error.
3. Si se encuentra:
   - Buscar un nuevo espacio libre del mismo tipo de vehículo.
   - Si no hay espacio libre, mostrar mensaje de error.
   - Si hay espacio libre:
     - Actualizar el slot antiguo (liberarlo) y ocupar el nuevo.
     - Mostrar mensaje de éxito con la nueva ubicación.

---

## Constantes

- Definir todas las constantes necesarias para el funcionamiento del programa (por ejemplo, cantidad de pisos, tipos de vehículos, etc).
