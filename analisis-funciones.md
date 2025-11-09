# Análisis de Funciones - SlotMaster

## ✅ CAMBIOS APLICADOS

### 1. `calcular_costo_de_estadia()` - CONSOLIDADA ✅

**Archivo:** `garage/precios.py`

La función ahora acepta **ambos sistemas de tarifas**:

- **Sistema CSV:** Usa parámetro `tarifa` (lista de listas desde tarifas.csv)
- **Sistema antiguo:** Usa `configurar_precios()` si no se pasa `tarifa`

**Firma unificada:**

```python
def calcular_costo_de_estadia(patente, hora_salida=None, garage=None, tarifa=None):
```

**Funciones auxiliares agregadas:**

- `_obtener_precio_tarifa()` - Busca precio en CSV
- `_convertir_tipo_a_nombre()` - Convierte número a nombre (1→moto, 2→auto, 3→camion)

**Mejora de formato de fecha:**

- ✅ Soporta formato con segundos: `YYYY-MM-DD HH:MM:SS`
- ✅ Soporta formato sin segundos: `YYYY-MM-DD HH:MM`

**Eliminado de `main.py`:**

- ❌ `calcular_costo_de_estadia()` (versión antigua)
- ❌ `_obtener_precio_tarifa()` (duplicada)
- ❌ `_calcular_horas()` (reemplazada por datetime)

---

### 2. `buscar_espacio_libre()` - CONSOLIDADA ✅

**Archivo:** `garage/garage_util.py`

Unificación de `busqueda_espacio_libre()` (main.py) y `buscar_espacio_libre()` (garage_util.py)

**Firma unificada:**

```python
def buscar_espacio_libre(garage, tipo_vehiculo=None):
```

**Mejoras:**

- ✅ Parámetro `tipo_vehiculo` ahora es **opcional** (None = cualquier tipo)
- ✅ Soporta tipo_vehiculo como `int` o `str`
- ✅ Retorna `(piso, slot_id)` usando valores del slot cuando están disponibles
- ✅ Documentación completa con docstring

**Eliminado de `main.py`:**

- ❌ `busqueda_espacio_libre()` (duplicada)

**Actualizado en `main.py`:**

- ✅ Import actualizado: `from garage.garage_util import buscar_espacio_libre`
- ✅ Llamada actualizada en `registrar_entrada_auto()`

---

### 3. `contar_espacios_libres()` - CONSOLIDADA ✅

**Archivo:** `garage/garage_util.py`

**Firma única:**

```python
def contar_espacios_libres(garage):
```

**Implementación mantenida:**

```python
def contar_espacios_libres(garage):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot["ocupado"] == False:
                cont += 1
    return cont
```

**Ventajas:**

- ✅ Implementación clara y directa
- ✅ Itera correctamente sobre estructura 2D (pisos/slots)
- ✅ Compara `ocupado` como booleano (más robusto que string)

**Eliminado de `main.py`:**

- ❌ `contar_espacios_libres()` (versión que usaba `leer_garage_normalizado()`)

**Uso actual:**

- ✅ Importada correctamente en `menu_principal_handlers.py`
- ✅ Usada en `mostrar_estadisticas_rapidas()` dentro de `garage_util.py`

---

### 4. `contar_por_tipo_vehiculo()` - CONSOLIDADA ✅

**Archivo:** `garage/garage_util.py`

**Firma única:**

```python
def contar_por_tipo_vehiculo(garage, tipo_buscado):
```

**Implementación mantenida:**

```python
def contar_por_tipo_vehiculo(garage, tipo_buscado):
    return sum(slot["tipo_vehiculo"] == tipo_buscado and slot["ocupado"] for piso in garage for slot in piso)
```

**Ventajas:**

- ✅ **Una sola línea**: Implementación compacta y pythonic
- ✅ **Eficiente**: Usa generator expression con sum()
- ✅ **Itera correctamente**: Doble for sobre estructura 2D
- ✅ **Comparación booleana directa**: `slot["ocupado"]` en vez de `== True`

**Eliminado de `main.py`:**

- ❌ `contar_por_tipo_vehiculo()` (versión que usaba `leer_garage_normalizado()` con múltiples loops)

**Uso actual:**

- ✅ Importada en `menu_principal_handlers.py`
- ✅ Usada internamente en `mostrar_estadisticas_rapidas()` de `garage_util.py`
- ✅ Llamada desde `handle_estadisticas_rapidas()` en menu handlers

---

### 5. `chequear_existencia_patente()` - CONSOLIDADA ✅

**Archivo:** `garage/garage_util.py`

**Firma única:**

```python
def chequear_existencia_patente(patente, garage):
```

**Implementación mantenida:**

```python
def chequear_existencia_patente(patente, garage):
    """
    Verifica si una patente existe en el garage y está ocupada.

    Parámetros:
    - patente: string con la patente a buscar
    - garage: lista de pisos con slots (estructura 2D)

    Retorna:
    - True: si la patente existe y el slot está ocupado
    - False: si no se encuentra o el slot está libre
    """
    for piso in garage:
        for slot in piso:
            if slot["patente"] == patente and slot["ocupado"] == True:
                return True
    return False
```

**Ventajas:**

- ✅ **Implementación clara**: Itera sobre estructura 2D (pisos/slots)
- ✅ **Comparación directa**: Verifica patente y estado ocupado en una sola condición
- ✅ **Firma consistente**: Requiere garage como parámetro (coherente con otras funciones del módulo)
- ✅ **Documentación completa**: Docstring detallado con parámetros y retornos

**Eliminado:**

- ❌ `chequear_existencia_patente(patente, garage)` de `main.py` (versión casi idéntica pero sin docstring)
- ❌ `chequear_existencia_patente(patente)` de `users/interaccion_usuario.py` (versión con lógica diferente que usaba `acceder_a_info_de_patentes()`)

**Actualizado en `main.py`:**

- ✅ Import actualizado: `from garage.garage_util import ... chequear_existencia_patente`
- ✅ Llamada en `ingresar_patente()` actualizada para pasar garage: `chequear_existencia_patente(patente, garage)`
- ✅ Agregado `garage = leer_garage_normalizado()` en `ingresar_patente()` para obtener el garage antes de la validación

**Uso actual:**

- ✅ Usada en `main.py` función `ingresar_patente()` para validar que la patente no exista antes de registrar entrada

---

### 6. `ingresar_patente()` - SIMPLIFICADA ✅

**Archivo:** `main.py`

**Problema original:** Duplicaba la validación de formato que ya hace `pedir_patente()`

**Firma:**

```python
def ingresar_patente():
```

**Implementación simplificada:**

```python
def ingresar_patente():
    """
    Solicita y valida una patente nueva que no exista en el sistema.
    Usa pedir_patente() para validar formato y solo verifica existencia.
    """
    garage = leer_garage_normalizado()
    while True:
        try:
            patente = pedir_patente()  # Ya valida formato completo (6 o 7 dígitos)
            if chequear_existencia_patente(patente, garage):
                print(Fore.RED + "Error: La patente ya existe en el sistema." + Style.RESET_ALL)
                continue
            print(Fore.GREEN + "Patente válida ingresada." + Style.RESET_ALL)
            return patente
        except Exception as e:
            print(Fore.RED + f"Error procesando la patente: {e}. Intente nuevamente." + Style.RESET_ALL)
```

**Ventajas:**

- ✅ **Eliminada validación redundante**: Ya no valida formato (6 dígitos) que `pedir_patente()` ya validó
- ✅ **Responsabilidad única**: Solo verifica que la patente no exista en el sistema
- ✅ **Confía en `pedir_patente()`**: Delega toda la validación de formato a la función especializada
- ✅ **Soporta ambos formatos**: Ahora acepta patentes de 6 y 7 dígitos (antes solo validaba 6)
- ✅ **Código más limpio**: Menos líneas, más fácil de mantener

**Cambios aplicados:**

- ❌ Eliminado bloque de validación redundante:
  ```python
  if len(patente) == 6 and patente[:3].isalpha() and patente[3:].isdigit():
      # ...
  else:
      print(Fore.YELLOW + "Error: Formato de patente inválido...")
  ```
- ✅ Simplificado flujo: `pedir_patente()` → verificar existencia → retornar

**Uso actual:**

- ✅ Usada en `main.py` para registrar nuevas patentes que ingresan al garage

---

### 7. `actualizar_csv_garage()` - ELIMINADA ✅

**Problema original:** Duplicación con `actualizar_garage()` en `users/users_garage.py`

**Implementación eliminada de `main.py`:**

```python
def actualizar_csv_garage(garage_id, garage):
    """Actualiza el CSV del garage con la estructura modificada."""
    # Reescribía TODO el archivo CSV con la estructura completa del garage
```

**Solución:** Usar `actualizar_garage()` de `users/users_garage.py`

**Ventajas de `actualizar_garage()`:**

- ✅ **Más eficiente**: Actualiza solo los slots necesarios, no reescribe todo el archivo
- ✅ **API flexible**: Soporta actualización de un slot (`bulk=False`) o múltiples slots (`bulk=True`)
- ✅ **Ya existente y probada**: Función consolidada en el módulo correcto (`users/users_garage.py`)
- ✅ **Mejor organización**: Toda la lógica de persistencia CSV está en un solo módulo

**Cambios aplicados en `main.py`:**

- ❌ Eliminada función `actualizar_csv_garage(garage_id, garage)` completa
- ✅ Reemplazada llamada en `registrar_salida_vehiculo()`:

  ```python
  # Antes:
  actualizar_csv_garage(garage_id, garage)

  # Ahora:
  slot_data = {
      "slot_id": found_slot.get("id"),
      "piso": found_piso_idx,
      "tipo_slot": found_slot.get("tipo_slot"),
      "reservado_mensual": found_slot.get("reservado_mensual", False),
      "ocupado": False,
      "patente": "",
      "hora_entrada": "",
      "tipo_vehiculo": 0
  }
  actualizar_garage(garage_id=garage_id, data=slot_data, bulk=False)
  ```

**Resultado:**

- ✅ Eliminada duplicación completamente
- ✅ `registrar_salida_vehiculo()` ahora actualiza solo el slot liberado (más eficiente)
- ✅ Import de `actualizar_garage` ya existía en `main.py`

---

## 📋 Resumen Ejecutivo

Este documento analiza todas las funciones del proyecto SlotMaster para identificar:

1. **Funciones REPETIDAS** (duplicadas en múltiples archivos)
2. **Funciones SIN USO** (vacías o que no hacen nada útil)

---

## 🔴 FUNCIONES REPETIDAS

### 1. `es_subscripcion_mensual(patente, garage)`

**Encontrada en 3 archivos:**

#### 📁 `main.py` (línea 102)

```python
def es_subscripcion_mensual(patente, garage):
    """Chequea si la subscripcion es mensual usando la vista de diccionarios."""
    datos = garage
    for slot in datos:
        if slot["patente"] == patente and slot["ocupado"] == True:
            val = slot["reservado_mensual"]
            if type(val) is str:
                return val == "True"
            return bool(val)
    return False
```

#### 📁 `garage/precios.py` (línea 36)

```python
def es_subscripcion_mensual(patente, garage):
    """Chequea si la suscripción es mensual usando la vista de diccionarios."""
    for slot in garage:
        if slot["patente"].lower() == patente.lower() and slot["ocupado"] == "True":
            val = slot.get("reservado_mensual", False)
            if isinstance(val, str):
                return val.lower() == "true"
            return bool(val)
    return False
```

#### 📁 `users/interaccion_usuario.py` (línea 40)

```python
def es_subscripcion_mensual(patente):
    """Chequea si la subscripcion es mensual o diaria"""
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info[3]
```

**⚠️ PROBLEMA:** Tres implementaciones diferentes de la misma función con lógica inconsistente.

**💡 RECOMENDACIÓN:** Mantener solo la versión de `garage/precios.py` (más robusta) y eliminar las otras dos.

---

### 2. `calcular_costo_de_estadia()`

**Encontrada en 2 archivos:**

#### 📁 `main.py` (línea 137)

```python
def calcular_costo_de_estadia(patente, hora_salida, tarifa):
    """
    Calcula el costo de estadía de un vehículo.
    Lee el garage desde cache, busca la patente y calcula según tarifa (diaria o mensual).
    """
    # Implementación completa con lectura de cache, búsqueda de patente, etc.
```

#### 📁 `garage/precios.py` (línea 60)

```python
def calcular_costo_de_estadia(patente, hora_salida=None, garage=None):
    """
    Calcula el costo de estadía de un vehículo según su patente y hora de salida.
    - Si tiene suscripción mensual → cobra tarifa mensual.
    - Si no → cobra tarifa por hora.
    """
    # Implementación diferente con configurar_precios()
```

**⚠️ PROBLEMA:** Dos implementaciones con firmas distintas y lógica diferente.

**💡 RECOMENDACIÓN:** Consolidar en una sola función en `garage/precios.py` o `main.py`.

---

### 3. `busqueda_espacio_libre()` / `buscar_espacio_libre()`

**Encontrada en 2 archivos:**

#### 📁 `main.py` (línea 117)

```python
def busqueda_espacio_libre(garage, tipo_vehiculo=None):
    for piso in garage:
        for slot in piso:
            if slot["ocupado"] == False:
                if tipo_vehiculo is None or slot["tipo_slot"] == str(tipo_vehiculo) or slot["tipo_slot"] == tipo_vehiculo:
                    piso_val = int(slot["piso"]) if "piso" in slot else 0
                    id_val = int(slot["id"]) if "id" in slot else 0
                    return (piso_val, id_val)
    return (-1, -1)
```

#### 📁 `garage/garage_util.py` (línea 26)

```python
def buscar_espacio_libre(garage, tipo_vehiculo):
    for i in range(len(garage)):
        piso = garage[i]
        for slot in piso:
            if slot["ocupado"] == False and (tipo_vehiculo == slot["tipo_slot"] or slot["tipo_slot"] == tipo_vehiculo):
                return (i, slot["id"])
    return (-1, -1)
```

**⚠️ PROBLEMA:** Nombre casi idéntico con lógica similar pero no igual.

**💡 RECOMENDACIÓN:** Unificar en `garage/garage_util.py` y eliminar de `main.py`.

---

### 4. `contar_espacios_libres(garage)`

**Encontrada en 2 archivos:**

#### 📁 `main.py` (línea 129)

```python
def contar_espacios_libres(garage=None):
    """Cuenta la cantidad de espacios libres en el garage."""
    datos = leer_garage_normalizado()
    return sum(1 for slot in datos if slot["ocupado"] == "False")
```

#### 📁 `garage/garage_util.py` (línea 35)

```python
def contar_espacios_libres(garage):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot["ocupado"] == False:
                cont += 1
    return cont
```

**⚠️ PROBLEMA:** Duplicación exacta con diferente implementación.

**💡 RECOMENDACIÓN:** Mantener solo la versión de `garage/garage_util.py` (más clara).

---

### 5. `contar_por_tipo_vehiculo(garage, tipo_buscado)`

**Encontrada en 2 archivos:**

#### 📁 `main.py` (línea 444)

```python
def contar_por_tipo_vehiculo(garage=None, tipo_buscado=None):
    """Cuenta vehículos estacionados de un tipo (tipo_vehiculo_estacionado)."""
    datos = leer_garage_normalizado()
    count = 0
    for pisos in datos:
        count += sum(1 for slot in pisos if slot.get("ocupado") == True and slot.get("tipo_vehiculo") == tipo_buscado)
    return count
```

#### 📁 `garage/garage_util.py` (línea 52)

```python
def contar_por_tipo_vehiculo(garage, tipo_buscado):
    return sum(slot["tipo_vehiculo"] == tipo_buscado and slot["ocupado"] for piso in garage for slot in piso)
```

**⚠️ PROBLEMA:** Duplicación con implementaciones distintas.

**💡 RECOMENDACIÓN:** Mantener solo la versión de `garage/garage_util.py` (más eficiente).

---

### 6. `acceder_a_info_de_patentes(garage)`

**Encontrada en 2 archivos:**

#### 📁 `main.py` (línea 89)

```python
def acceder_a_info_de_patentes(garage):
    """Devuelve lista de dicts con slots ocupados."""
    datos = garage
    return [slot for slot in datos if slot.get("ocupado") == True]
```

#### 📁 `users/interaccion_usuario.py` (línea 16)

```python
def acceder_a_info_de_patentes(GARAGE):
    """Accede a los datos guardados de las patentes."""
    datos = []
    for d in GARAGE:
        for pisos in d:
            datos.append(pisos)
    return datos
```

**⚠️ PROBLEMA:** Lógica completamente diferente.

## **💡 RECOMENDACIÓN:** Clarificar cuál es la correcta y eliminar la otra.

## ❌ FUNCIONES SIN USO O VACÍAS

### 7. `generar_fecha_aleatoria()` - `main.py` (línea 49)

```python
def generar_fecha_aleatoria():
    """Genera una fecha y hora aleatoria en formato 'YYYY-MM-DD HH:MM'"""
    year = "2025"
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}"
```

**⚠️ PROBLEMA:** Nunca se usa en el código. Parece ser de pruebas/debugging.

**💡 RECOMENDACIÓN:** Eliminar si no tiene uso productivo.

---

### 10. `eliminar_fila_por_valor(valor, garage)` - `main.py` (línea 59)

```python
def eliminar_fila_por_valor(valor, garage):
    """Elimina la primera fila que contiene el valor dado."""
    try:
        for i in range(len(garage)):
            if valor in garage[i]:
                del garage[i]
                print(Fore.GREEN + f"Fila eliminada correctamente (valor: {valor})." + Style.RESET_ALL)
                return True
    except Exception as e:
        print(Fore.RED + f"Error eliminando fila: {e}" + Style.RESET_ALL)
        return False
    # ...
```

**⚠️ PROBLEMA:** No se encuentra ningún llamado a esta función.

**💡 RECOMENDACIÓN:** Eliminar si no se usa.

---

### 11. `modificar_vehiculo()` - `main.py` (línea 27)

```python
def modificar_vehiculo(garage, patente, nuevo_tipo=None, nueva_patente=None, nueva_estadia=None):
    """Modifica los datos de un vehículo en el garage según la patente."""
    try:
        for piso in garage:
            for slot in piso:
                if slot["ocupado"] == True and slot["patente"] == patente:
                    if nuevo_tipo:
                        slot["tipo_vehiculo"] = nuevo_tipo
                    if nueva_patente:
                        slot["patente"] = nueva_patente
                    if nueva_estadia:
                        slot["reservado_mensual"] = nueva_estadia
                    return True
    except Exception as e:
        print(Fore.RED + f"Error modificando vehículo: {e}" + Style.RESET_ALL)
    return False
```

**⚠️ PROBLEMA:** No se encuentra uso en el proyecto (pero podría ser útil en el futuro).

**💡 RECOMENDACIÓN:** Si no se usa actualmente, eliminar o documentar como "TODO".

---

### 12. `salida_tipo_vehiculo(tipo_slot)` - `main.py` (línea 389)

```python
def salida_tipo_vehiculo(tipo_slot):
    """Convierte un valor numérico que representa el tipo de vehículo en una cadena de texto descriptiva."""
    if tipo_slot == 1:
        return "Moto"
    elif tipo_slot == 2:
        return "Auto"
    elif tipo_slot == 3:
        return "Camioneta"
    return "Desconocido"
```

**⚠️ PROBLEMA:** Esta función ya existe en `constantes/tipos_vehiculos.py` como `obtener_nombre_vehiculo()`.

**💡 RECOMENDACIÓN:** Eliminar esta versión y usar la de `constantes/tipos_vehiculos.py`.

---

### 13. `buscar_patente(patente)` - `users/interaccion_usuario.py` (línea 34)

```python
def buscar_patente(patente):
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info
```

**⚠️ PROBLEMA:** Función incompleta sin uso aparente. Ya existe `buscar_por_patente()` en `garage/garage_util.py`.

**💡 RECOMENDACIÓN:** Eliminar.

---

### 14. `pedir_piso(garage)` - `users/interaccion_usuario.py` ✅

```python
def pedir_piso(garage):
    """Solicita al usuario un número de piso válido."""
    while True:
        try:
            piso = int(input(f"Ingrese el piso que desea consultar entre 0 y {len(garage)-1}: "))
            if piso < 0 or piso >= len(garage):
                print("El piso ingresado no es válido. Intente nuevamente.")
            else:
                return piso
        except ValueError:
            print("Por favor, ingrese un número válido.")
        except Exception as e:
            print(f"Error: {e}")
```

**✅ CORRECCIÓN:** La función SÍ se usa en `visual/menu_principal_handlers.py` (línea 41).

**Uso actual:**

- ✅ Importada en `menu_principal_handlers.py`
- ✅ Usada en función `handle_mostrar_estado_garage()` para solicitar el piso a visualizar

**Mejora aplicada:** Agregado manejo de `ValueError` para mejor validación de entrada.

---

### 15. `pedir_tipo_vehiculo()` - `users/interaccion_usuario.py` (línea 87)

```python
def pedir_tipo_vehiculo():
    return pedir_num_natural(min=1, max=4)
```

**⚠️ PROBLEMA:** Función que solo delega. Ya existe `tipo_slot()` en `garage/slot_utils.py` con mejor implementación.

**💡 RECOMENDACIÓN:** Usar `tipo_slot()` y eliminar esta.

---

### 16. `mostrar_estado_garage(garage)` - `users/interaccion_usuario.py` (línea 47)

```python
def mostrar_estado_garage(garage):
    print(Fore.GREEN + "\n--- ESTADO DEL GARAGE ---" + Style.RESET_ALL)
    # Implementación con lambda
```

**⚠️ PROBLEMA:** Existe pero no se usa en menu handlers. Podría consolidarse con `handle_mostrar_estado_garage()`.

**💡 RECOMENDACIÓN:** Verificar si se usa y consolidar.

---

### 17. `leer_garage_normalizado()` - `main.py` (línea 18)

```python
def leer_garage_normalizado():
    """Lee el garage y retorna una lista de diccionarios normalizados."""
    garage_id = leer_estado_garage()['garage_id']
    return users_garage.get_garage_data(garage_id)
```

**⚠️ PROBLEMA:** Función wrapper que solo llama a `get_garage_data()`. Uso limitado.

**💡 RECOMENDACIÓN:** Considerar eliminar y llamar directamente a `get_garage_data()`.

---

### 18. `buscar_slots_por_tipo(garage, tipo_slot)` - `garage/garage_util.py` (línea 75)

```python
def buscar_slots_por_tipo(garage, tipo_slot):
    """Busca todos los ids de slots en el garage que coinciden con el tipo de slot."""
    slots_por_tipo = []
    pisos = {}
    for num_piso, piso_data in enumerate(garage):
        for slot in piso_data:
            if slot.get('tipo_slot') == tipo_slot and not slot.get('ocupado'):
                slots_por_tipo.append(slot.get('id'))
        pisos.update({num_piso: slots_por_tipo})
    return pisos
```

**⚠️ PROBLEMA:** Función compleja que no parece tener uso.

**💡 RECOMENDACIÓN:** Verificar uso y documentar o eliminar.

---

### 20. `obtener_slot_por_id(garage, slot_id)` - `garage/slot_utils.py` (línea 29)

```python
def obtener_slot_por_id(garage, slot_id):
    # No implementada completamente
```

**⚠️ PROBLEMA:** Función vacía o incompleta.

**💡 RECOMENDACIÓN:** Implementar o eliminar.

---

## 📊 ESTADÍSTICAS

- **Total de funciones analizadas:** ~118
- **Funciones repetidas consolidadas:** 5/7 ✅ (71% completado)
- **Funciones sin uso eliminadas:** 1/12 ✅
- **Funciones simplificadas/mejoradas:** 1 función ✅

### ✅ Consolidaciones completadas:

1. ✅ `calcular_costo_de_estadia()` → `garage/precios.py`
2. ✅ `buscar_espacio_libre()` → `garage/garage_util.py`
3. ✅ `contar_espacios_libres()` → `garage/garage_util.py`
4. ✅ `contar_por_tipo_vehiculo()` → `garage/garage_util.py`
5. ✅ `chequear_existencia_patente()` → `garage/garage_util.py`

### ✅ Funciones sin uso eliminadas:

1. ✅ `actualizar_csv_garage()` → Reemplazada por `actualizar_garage()` de `users/users_garage.py`

### ✅ Simplificaciones completadas:

1. ✅ `ingresar_patente()` → Eliminada validación redundante de formato
2. ✅ `registrar_salida_vehiculo()` → Usa `actualizar_garage()` en vez de reescribir todo el CSV

---

## 🎯 PLAN DE ACCIÓN RECOMENDADO

### Prioridad ALTA

1. ✅ **COMPLETADO: Eliminar funciones duplicadas de cálculo de costo:**

   - ✅ Mantener solo una versión de `calcular_costo_de_estadia()`
   - ⚠️ PENDIENTE: Eliminar duplicados de `es_subscripcion_mensual()`

2. ✅ **COMPLETADO: Consolidar funciones de búsqueda y validación:**

   - ✅ Unificar `busqueda_espacio_libre()` / `buscar_espacio_libre()`
   - ✅ Mantener solo `buscar_por_patente()` en `garage/garage_util.py`
   - ✅ Consolidar `chequear_existencia_patente()` en `garage/garage_util.py`

3. 🔄 **EN PROGRESO: Eliminar funciones sin uso:**
   - ✅ `actualizar_csv_garage()` - Reemplazada por `actualizar_garage()`
   - ⚠️ PENDIENTE: `generar_fecha_aleatoria()`
   - ⚠️ PENDIENTE: `eliminar_fila_por_valor()`
   - ⚠️ PENDIENTE: `buscar_patente()` en `interaccion_usuario.py`

### Prioridad MEDIA

4. ✅ **COMPLETADO: Consolidar funciones de conteo:**

   - ✅ `contar_espacios_libres()` → Solo en `garage/garage_util.py`
   - ✅ `contar_por_tipo_vehiculo()` → Solo en `garage/garage_util.py`
   - Eliminar duplicados en `main.py`

5. ✅ **COMPLETADO: Simplificar validación de patentes:**
   - ✅ `ingresar_patente()` ahora confía en `pedir_patente()` para validación de formato
   - ✅ `ingresar_patente()` solo verifica existencia (responsabilidad única)
   - ✅ Eliminada validación redundante de formato

### Prioridad BAJA

6. 📝 **Documentar funciones útiles sin uso actual:**
   - `modificar_vehiculo()` - marcar como TODO
   - `buscar_slots_por_tipo()` - documentar propósito

---

## 🔍 NOTAS FINALES

Este análisis identifica problemas de duplicación y organización en el código. La consolidación de estas funciones:

- ✅ **Mejorará el mantenimiento** (cambios en un solo lugar)
- ✅ **Reducirá bugs** (lógica inconsistente entre duplicados)
- ✅ **Simplificará testing** (menos funciones que probar)
- ✅ **Mejorará legibilidad** (menos confusión sobre qué función usar)

**Fecha de análisis:** $(date)  
**Archivos analizados:** 38 archivos `.py`  
**Total de funciones:** 118 funciones
