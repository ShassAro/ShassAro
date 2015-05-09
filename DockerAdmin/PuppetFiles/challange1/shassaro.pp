####### SHASSARO MANDATORY #######
include "stdlib"

# Define type so we can use the same json as the users get
define shassaro::vnc($user = $title, $password) {

        $my_file_arg = "/home/${user}/.vnc/passwd"

	# Enforce the file
        file { $my_file_arg:
        	ensure => file,
		mode => 600,
		owner => $user,
		group => $user,
        }

	# And its content
        exec {"Use $my_file_arg":
          require => File[$my_file_arg],
          command => "/bin/echo ${password} | /usr/bin/vncpasswd -f > $my_file_arg",
        }
}

define shassaro::user($user = $title, $password) {

	user { $user:
		managehome => true,
		groups => ["shassaro"],
		require => Group["shassaro"],
		password => generate('/bin/sh', '-c', "openssl passwd -1 ${password} | tr -d '\n'"),
	}
}

# Add the shassaro group
group {"shassaro":

	ensure => present,
}

# Gets the users json and parse it to hash
$hashUsers = parsejson($myusers)

# Create the users
create_resources(shassaro::user, $hashUsers)

# Create the vnc password
create_resources(shassaro::vnc, $hashUsers)

# Declare the vnc arguments
$vnc_user = {

	'user' => keys($hashUsers), # Only one user!!!
	'args' => '',
}

# Declare the vnc class
class { "vnc": 
       servers => [ $vnc_user ]}

# Resource ordering
User<| |> -> Shassaro::Vnc<| |>
###################################

# Goal1 = user hackme password
# Goal2 = .secret file content

file {"/tmp/password":

	ensure => file,
	content => "User: hackme \nPassword: Password1\n",
}

user {"hackme":

	password => generate('/bin/sh', '-c', "openssl passwd -1 Password1 | tr -d '\n'"),
	managehome => true,
}

file {"/home/hackme/.secret":

	ensure => file,
	content => $goal1,
	mode => 644,
	require => User['hackme'],
}

service {"sshd":
    ensure => running,
}