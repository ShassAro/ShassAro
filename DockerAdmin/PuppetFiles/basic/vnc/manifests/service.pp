# == Class: vnc::service
#
# Manages the VNC service
#
class vnc::service {
  include vnc

  service { 'vncserver':
    ensure    => $vnc::service_ensure_real,
    enable    => $vnc::service_enable_real,
    hasstatus => true,
    status    => '/sbin/service vncserver status; /usr/bin/test $? -eq 0',
  }
}
