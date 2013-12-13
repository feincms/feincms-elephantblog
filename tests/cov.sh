#!/bin/sh
coverage run --branch --include="*elephantblog/elephantblog*" ./manage.py test testapp
coverage html
