module Puppet::Parser::Functions
  newfunction(:validate_vnc_servers, :doc => <<-EOS

Given an array of hashes, validates the following:
  - The passed parameter is an array
  - Array member objects are hashes
  - Each hash has a 'user' and 'args' key

If an empty array is passed, then this function validates successfully.

Passing Examples:

  $vnc_arusso = { 'user' => 'arusso',
                  'args' => '' }
  $vnc_brusso = { 'user' => 'brusso',
                  'args' => '' }
  validate_vnc_servers([ $vnc_arusso ])
  validate_vnc_servers([ $vnc_arusso, $vnc_brusso ])
  validate_vnc_servers([ ])

Failing Examples:

   $vnc_arusso = { 'user' => 'arusso',
                   'arg' => '' }
   validate_vnc_servers([ $vnc_arusso ]) # args key not specified
   validate_vnc_servers([ '' ]) # array member not a hash
   validate_vnc_servers($vnc_arusso) # array not passed

EOS
) do |args|
    server_array = args[0]
    if server_array.is_a?(Array)
      server_array.each do |sh|
        if sh.is_a?(Hash)
          raise Puppet::ParseError, \
            "Hash object must have 'user' and 'args' keys" \
            unless sh.has_key?('user') and sh.has_key?('args')
        else
          raise Puppet::ParseError, "Array member not a Hash"
        end
      end
    else
      raise Puppet::ParseError, "Parameter must be an Array"
    end
  end
end
