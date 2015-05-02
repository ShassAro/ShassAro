# == Class: vnc
#
# Installs and manages a VNC Server
#
# === Parameters
#
# [*refresh*]
#   when set to true, restarts the vnc server service after each configuration
#   update.  when set to false, does nothing to the service after configuration
#   changes.
#
# [*servers*]
#   Specify an array of hashes with keys:
#     * user - username to associate with a vncserver session
#     * args - arguments to pass to this users vncserver session
#
#   order matters, objects are assigned to a vnc server in the order they appear
#   in the array based on the 'name' value.
#
# [*service_enable*]
#   specify whether service should be started at boot time. valid values are
#   true/false/nochange.  Default is true.
#
# [*service_ensure*]
#   specify whether service should be running, stopped or noaction (left alone).
#   default is running
#
# [*xstartup_template*]
#   specify an alternative xstartup script that will be installed to /etc/skel
#   for all NEW users
#
# [*vncservers_template*]
#   specify an alternative vncservers configuration template that will be
#   installed to /etc/sysconfig/vncservers.
#
# === Binary Requirements
#
# This class assumes that the desktop environment(s) is installed and configure
# appropriately.  The provided xstartup script assumes that gnome is the desktop
# environment.
#
# On RHEL6/CentOS6 hosts, the following package/groups are recommended:
#  $ yum groupinstall Desktop
#  $ yum install xrdb xterm
#
# === Examples
#
#  $vnc_arusso = {
#    'user' => 'arusso',
#    'args' => '-SecurityTypes=VeNCrypt,TLSPlain pam_service=login'
#  }
#  $vnc_brusso = {
#    'user' => 'brusso',
#    'args' => '-SecurityTypes=VeNCrypt,TLSVnc'
#  }
#  class { 'vnc':
#    refresh           => false,
#    servers           => [ $vnc_arusso, $vnc_brusso ],
#    service_ensure    => undef,
#    xstartup_template => 'myclass/xstartup.erb',
#  }
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
class vnc (
  $refresh = true,
  $servers = [ ],
  $service_enable = true,
  $service_ensure = running,
  $xstartup_template = 'vnc/xstartup.erb',
  $vncservers_template = 'vnc/vncservers.erb'
) {
  include vnc::install, vnc::config, vnc::service

  validate_vnc_servers( $servers )

  $service_ensure_real = $service_ensure ? {
    /no(action|change)/ => undef,
    default             => $service_ensure,
  }

  $service_enable_real = $service_enable ? {
    /no(action|change)/ => undef,
    default             => $service_enable,
  }

  Class['vnc'] ->
    Class['vnc::install'] ->
    Class['vnc::config'] ->
    Class['vnc::service']
}
