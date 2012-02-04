#!/bin/bash

python manage.py sqldiff vps | psql pysk
