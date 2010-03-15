#!/bin/bash

set -e
set -u

python /opt/pysk/pysk/manage.py shell_plus <<'EOF'
from pysk.vps.models import PHPConfig

vps_phpconfig_1 = PHPConfig()
vps_phpconfig_1.name = u'development'
vps_phpconfig_1.short_open_tag = False
vps_phpconfig_1.max_execution_time = 30
vps_phpconfig_1.max_input_time = 60
vps_phpconfig_1.memory_limit = u'128M'
vps_phpconfig_1.post_max_size = u'32M'
vps_phpconfig_1.upload_max_filesize = u'16M'
vps_phpconfig_1.allow_call_time_pass_reference = False
vps_phpconfig_1.error_reporting = u'E_ALL | E_STRICT'
vps_phpconfig_1.display_errors = True
vps_phpconfig_1.display_startup_errors = True
vps_phpconfig_1.log_errors = False
vps_phpconfig_1.track_errors = True
vps_phpconfig_1.html_errors = True
vps_phpconfig_1.session_bug_compat_42 = True
vps_phpconfig_1.session_bug_compat_warn = True
vps_phpconfig_1.save()

vps_phpconfig_2 = PHPConfig()
vps_phpconfig_2.name = u'legacy'
vps_phpconfig_2.short_open_tag = False
vps_phpconfig_2.max_execution_time = 30
vps_phpconfig_2.max_input_time = 60
vps_phpconfig_2.memory_limit = u'128M'
vps_phpconfig_2.post_max_size = u'32M'
vps_phpconfig_2.upload_max_filesize = u'16M'
vps_phpconfig_2.allow_call_time_pass_reference = True
vps_phpconfig_2.error_reporting = u'E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_USER_DEPRECATED'
vps_phpconfig_2.display_errors = True
vps_phpconfig_2.display_startup_errors = True
vps_phpconfig_2.log_errors = False
vps_phpconfig_2.track_errors = False
vps_phpconfig_2.html_errors = True
vps_phpconfig_2.session_bug_compat_42 = True
vps_phpconfig_2.session_bug_compat_warn = True
vps_phpconfig_2.save()

vps_phpconfig_3 = PHPConfig()
vps_phpconfig_3.name = u'production'
vps_phpconfig_3.short_open_tag = False
vps_phpconfig_3.max_execution_time = 30
vps_phpconfig_3.max_input_time = 60
vps_phpconfig_3.memory_limit = u'128M'
vps_phpconfig_3.post_max_size = u'32M'
vps_phpconfig_3.upload_max_filesize = u'16M'
vps_phpconfig_3.allow_call_time_pass_reference = False
vps_phpconfig_3.error_reporting = u'E_ALL & ~E_DEPRECATED'
vps_phpconfig_3.display_errors = False
vps_phpconfig_3.display_startup_errors = False
vps_phpconfig_3.log_errors = True
vps_phpconfig_3.track_errors = False
vps_phpconfig_3.html_errors = False
vps_phpconfig_3.session_bug_compat_42 = False
vps_phpconfig_3.session_bug_compat_warn = False
vps_phpconfig_3.save()

from pysk.vps.models import ServerConfig

vps_serverconfig_1 = ServerConfig()
vps_serverconfig_1.active = True
vps_serverconfig_1.default_php_config = vps_phpconfig_2
vps_serverconfig_1.save()

exit()
EOF

