# == Class: vnc::config
#
# Configures the VNC Server
#
# This class should not be called directly and is called from the vnc, class.
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
class vnc::config {
  include vnc

  $notify_class = $vnc::refresh ? {
    false   => undef,
    default => Class['vnc::service'],
  }

  case $::osfamily {
    'RedHat': {
      $vncservers_template = $vnc::vncservers_template
      file { '/etc/sysconfig/vncservers':
        ensure  => present,
        owner   => root,
        group   => root,
        mode    => '0440',
        content => template($vncservers_template),
        notify  => $notify_class,
      }

      file { '/etc/skel/.vnc':
        ensure => directory,
        owner  => 'root',
        group  => 'root',
        mode   => '0755',
      }

      # drop a file in /etc/skel to setup some sane defaults for users
      $xstartup_template = $vnc::xstartup_template
      file { '/etc/skel/.vnc/xstartup':
        ensure  => present,
        owner   => 'root',
        group   => 'root',
        mode    => '0750',
        require => File['/etc/skel/.vnc'],
        content => template($xstartup_template),
      }
    }

    default: { }
  }
}
