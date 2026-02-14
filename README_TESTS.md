# Pruebas Unitarias - SGSC

## Casos de Uso Cubiertos
Este repositorio incluye pruebas unitarias para los siguientes casos de uso:

1. Crear Solicitud
2. Cambiar Estado de Solicitud

## Propósito de las Pruebas

### Crear Solicitud
Estas pruebas validan:
- Creación exitosa de una solicitud.
- Verificación de campos obligatorios.
- Manejo de prioridades inválidas.
- Requisitos de autenticación del usuario.

### Cambiar Estado de Solicitud
Estas pruebas validan:
- Transiciones válidas de estado.
- Intentos de transición inválidos.
- Manejo de solicitudes inexistentes.
- Control de permisos del usuario.

## Cómo Ejecutar las Pruebas
Instalar dependencias:
pip install -r requirements.txt

Ejecutar pruebas:
pytest
