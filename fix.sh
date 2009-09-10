#!/bin/bash

chmod 0711 /opt/pysk
chmod 0755 /opt/pysk/*

chown -R root:http /opt/pysk/secret
chmod 0750 /opt/pysk/secret
chmod 0640 /opt/pysk/secret/*

