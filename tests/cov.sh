#!/bin/sh
venv/bin/coverage run --branch --include="*elephantblog/elephantblog*" ./manage.py test testapp -v 2
venv/bin/coverage html
