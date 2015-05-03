# vnc Server Module #

This is a module for managing a VNC server on Red Hat based hosts.  It currently
is geared towards rhel6. Pull requests supporting other distros are welcome.

## Further Development ##

Further development of this module will consist of bugfixes and pull requests
only.

## Examples ##

The simplest method for configuring two VNC servers on `:1` and `:2`

    $vnc_arusso = {
      'user' => 'arusso',
      'args' => '-SecurityTypes=VeNCrypt,TLSPlain -PlainUsers=arusso pam_service=login',
    }
    $vnc_brusso = {
      'user' => 'brusso',
      'args' => '-SecurityTypes=VeNCrypt,TLSVNC',
    }

    class { 'vnc': servers => [ $vnc_arusso, $vnc_brusso ] }

You should now be able to connect to `5901` as arusso and `5902` as brusso.


Binary Requirements
-------------------

See module documentation (init.pp) for more information.

License
-------

See LICENSE file

Copyright
---------

Copyright &copy; 2013 The Regents of the University of California

Contact
-------

Aaron Russo <arusso@berkeley.edu>

Support
-------

Please log tickets and issues at the
[Projects site](https://github.com/arusso/puppet-vnc/issues/)
