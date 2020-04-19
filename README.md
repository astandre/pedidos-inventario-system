# Instalacion
[![Build Status](https://travis-ci.org/astandre/pedidos-inventario-system.svg?branch=master)](https://travis-ci.org/astandre/pedidos-inventario-system)
## Construccion de contenedores

```
docker-compose  -d --build
```
## Migracion de tablas

```
docker-compose exec web python manage.py migrate --noinput
```
## Carga de datos
```
exec web python manage.py dumpdata inventarioHandler.categoria inventarioHandler.producto
```


## Collect static

```
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```
