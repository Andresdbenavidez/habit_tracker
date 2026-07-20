# Habit Tracker (Rastreador de Hábitos) - Python & Docker

Este es un proyecto en Python diseñado para gestionar y trackear hábitos diarios, utilizando una base de datos relacional MySQL aislada dentro de un contenedor de Docker.

## Características del proyecto (Fase 1)
- **Conexión Robusta:** Control de excepciones (`try/except`) para evitar caídas si la base de datos no responde.
- **Persistencia Segura:** Creación automática de la base de datos y la tabla de hábitos si no existen.
- **Rachas Automatizadas:** Los nuevos hábitos se registran automáticamente con una racha inicial de 0.

## Estructura de la Base de Datos (`habit_tracker`)
### Tabla: `habitos`
- `id`: INT (AUTO_INCREMENT, PRIMARY KEY)
- `nombre`: VARCHAR(100)
- `racha`: INT

## Requisitos e Infraestructura
Asegúrate de tener Docker encendido y ejecuta el siguiente comando en tu terminal para levantar el contenedor de MySQL:

```bash
docker run --name mi_mysql -e MYSQL_ROOT_PASSWORD=qwerty -p 3306:3306 -d mysql:latest
