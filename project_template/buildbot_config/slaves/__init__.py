# we need to append python path to simulate what the buildbot command (i.e. 
# buildbot checkconfig) would see when running on the server.
#
# I know this is nasty but I cannot find a better way yet.
# -- juacompe 9 April 2012

import sys
sys.path.append('project_template')

