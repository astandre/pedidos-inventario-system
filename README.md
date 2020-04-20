# Instalacion
[![Build Status](https://travis-ci.org/astandre/pedidos-inventario-system.svg?branch=master)](https://travis-ci.org/astandre/pedidos-inventario-system)
## Construccion de contenedores

```
docker-compose  up
```
## Hacer migraciones

```
docker exec -it pedidos_backend python manage.py makemigrations
```
## Migrar
```
docker exec -it pedidos_backend python manage.py migrate 
```
## Carga de datos
```
docker exec -it pedidos_backend python manage.py dumpdata inventarioHandler.categoria inventarioHandler.producto
```
## Crear super usuario
```
docker exec -it pedidos_backend python manage.py createsuperuser
```

## Collect static

```
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```
