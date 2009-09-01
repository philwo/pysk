#!/bin/bash

/usr/bin/mysqlcheck -Acgs --auto-repair
/usr/bin/mysqlcheck -Aas
/usr/bin/mysqlcheck -Aos

