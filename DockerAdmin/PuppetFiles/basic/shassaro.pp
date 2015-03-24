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

# Add the shassaro group
group {"shassaro":

	ensure => present,
}

# Gets the users json and parse it to hash
$hashUsers = parsejson($myusers)

# Create the default elements
$defaults = {

	managehome => true,
	groups	   => ["shassaro"],
	require	   => Group["shassaro"],
}

# Create the users
create_resources(user, $hashUsers, $defaults)

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

