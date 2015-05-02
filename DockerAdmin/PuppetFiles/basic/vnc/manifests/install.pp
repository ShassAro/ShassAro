# == Class: vnc::install
#
# Installs our vnc server packages
#
# This class should not be called directly, and is called from the vnc class
#
# === Authors
#
# Aaron Russo <arusso@berkeley.edu>
#
# === Copyright
#
# Copyright 2013 The Regents of the University of California
# All Rights Reserved
#
# === Note
#
# This class is intended to be called from the vnc class, and should not be
# called directly
#
class vnc::install {
  case $::osfamily {
    'RedHat': {
      case $::operatingsystemrelease {
        /^6\./: { $package = 'tigervnc-server' }
        /^5\./: { $package = 'vnc-server' }
        default: { fail('Unsupported OS version') }
      }
    }
    default: {
      fail('Unsupported OS')
    }
  }

  package { $package: ensure => installed }
}
