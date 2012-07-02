#!/usr/bin/env python

import sys
import shutil
import os

if __name__ == "__main__":
    args_length = len(sys.argv)
    if args_length < 1:
        print "Usage : run this script in project's base folder"
        sys.exit()
    else:
        template_name = 'build_slave_svn_template'
        current_location = os.getcwd()
        if 'bin' in current_location:
            current_location = current_location.rstrip('bin')
        template_location = '%s/utilities/%s' % (current_location, template_name)
        target_location = 'buildbot_config/slave_svn/build_svn_slave.py'
        shutil.copy(src=template_location, dst=target_location)




