#!/bin/sh
coverage run --branch --include="*elephantblog/elephantblog*" ./manage.py test testapp -v 2
coverage html
