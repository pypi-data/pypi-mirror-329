# Changelog

## [0.2.11] - 2024-01-06

### Added
- Soporte para múltiples conexiones de bases de datos simultáneas
  - Configuración mediante `connections` en groovindb.json
  - Acceso a diferentes bases de datos vía `db.client.[database]`
  - Documentación actualizada con ejemplos de uso
- Queries raw específicas por tipo de base de datos
  - Métodos `query()`, `query_one()` y `execute()`
  - Soporte para placeholders específicos por driver ($1, %s, ?)
  - Validación de parámetros según el tipo de base de datos
- Mejoras en el sistema de logging
  - Soporte para rotación de archivos de log
  - Configuración de tamaño máximo y número de backups
  - Mejor formato de mensajes de log
- Soporte para driver SQLite
  - Implementación de driver base con aiosqlite
  - Introspección de schemas para SQLite
  - Documentación de uso con SQLite

### Changed
- Refactorización del sistema de drivers
  - Abstracción mejorada con BaseDriver
  - Soporte para context managers en drivers
  - Mejor manejo de transacciones
- Mejoras en la gestión de conexiones
  - Conexiones lazy-loaded por base de datos
  - Mejor manejo de desconexiones
- Actualización de la documentación
  - Nuevos ejemplos de uso con múltiples bases de datos
  - Clarificación de la configuración inicial vs avanzada
  - Documentación específica por tipo de driver

## [0.2.10] - 2024-12-27

### Added
- Nueva funcionalidad createMany para inserciones masivas
  - Soporte para inserción de múltiples registros en una sola operación
  - Opción skipDuplicates para ignorar registros duplicados
  - Validación de consistencia en las columnas

## [0.2.9] - 2024-12-27

### Fixed
- Corrección en la validación de operadores de agregación
- Unificación de operadores de agregación en validator.py
- Soporte mejorado para COUNT en agregaciones

## [0.2.8] - 2024-12-27

### Added
- Soporte para operadores de comparación en consultas WHERE
  - Nuevos operadores: gt, gte, lt, lte, in, notIn, contains, notContains, startsWith, endsWith, between, notBetween
  - Ejemplo: `where={"id": {"gt": 1}}`
  - Validación unificada de operadores

### Changed
- Refactorización de la validación de operadores
- Unificación de operadores SQL en un solo lugar (validator.py)

### Fixed
- Corrección en la validación de tipos para operadores de comparación
- Simplificación de la clase Table removiendo requerimiento de model_type 