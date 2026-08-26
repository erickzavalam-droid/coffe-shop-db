# CAFFEE — Base de Datos Relacional para Cadena de Cafeterías

Diseño e implementación de una base de datos relacional para **CAFFEE**, una cadena de cafeterías con sede en Nueva York en proceso de expansión nacional. El proyecto consolida datos que originalmente viven dispersos en distintos sistemas — software de contabilidad, bases de datos de proveedores, sistemas de punto de venta (POS) y hojas de cálculo — en una única base de datos central que facilita la toma de decisiones basada en datos.

Basado en el proyecto final del curso **IBM: Introducción a Bases de Datos Relacionales**, extendido con un pipeline propio de ETL en Python y visualización en Power BI.

## Escenario

Como Ingeniero de Datos recién contratado por CAFFEE, el objetivo es diseñar el sistema de base de datos relacional que soporte la expansión de la cadena, integrando datos de:

- Información de personal (hoja de cálculo, sede)
- Puntos de venta (hoja de cálculo, sede)
- Ventas (CSV exportado del sistema POS)
- Clientes (CSV exportado del CRM)
- Productos (hoja de cálculo exportada de la base de datos del proveedor)

## Estado del proyecto

### ✅ Completado
- Identificación de entidades y atributos a partir de las fuentes de datos originales
- Diagrama de relación de entidades (ERD) construido con la herramienta ERD de pgAdmin
- Normalización de tablas (2NF)
- Definición de llaves primarias/foráneas y relaciones
- Generación y ejecución del script SQL de creación de objetos de base de datos (PostgreSQL)
- Creación de vistas y vista materializada
- Exportación de datos e importación a MySQL vía phpMyAdmin

### 🚧 En progreso
- Pipeline ETL en Python para extraer, transformar y cargar los datos hacia un schema `staging`
- Conexión del schema `staging` a Power BI para construir dashboards de análisis operativo

## Tecnologías

- **PostgreSQL** — diseño y modelado de la base de datos central
- **pgAdmin** — herramienta ERD para modelado visual
- **MySQL / phpMyAdmin** — replicación de datos hacia un segundo RDBMS
- **Python** — pipeline ETL (en construcción)
- **Power BI** — capa de visualización y análisis (en construcción)

## Estructura

```
/sql
  01_schema.sql              → creación de tablas, llaves primarias y foráneas
  02_views.sql                → vistas
  03_materialized_view.sql    → vista materializada
/erd
  ERD_COFFEE.png               → diagrama de relación de entidades
/etl                          → pipeline de Python (en desarrollo)
```

> **Nota:** el dataset de prueba (~180,000 registros, generado como parte del curso IBM) se omite de este repositorio por tamaño. La base de datos se puede reconstruir ejecutando `sql/01_schema.sql` y cargando los datos de origen del curso.

## Próximos pasos

1. Construir el pipeline de extracción y transformación en Python desde las fuentes originales hacia el schema `staging`.
2. Conectar Power BI al schema `staging` para construir reportes de ventas, desempeño por ubicación y análisis de clientes.
3. Documentar el flujo completo de datos (arquitectura end-to-end) una vez conectado el pipeline.
