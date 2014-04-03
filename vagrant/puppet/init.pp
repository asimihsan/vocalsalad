Exec {
    path => "/home/vagrant/.pyenv/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin",
    logoutput => "on_failure",
    timeout => 0,
}

File {
    owner => "vagrant",
    group => "vagrant",
    mode => 600,
}

include development_tools
include firewall
include openssl
include python
user_environment { 'vagrant':
    user => 'vagrant',
    group => 'vagrant',
    home => '/home/vagrant',
}
