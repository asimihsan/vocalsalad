define user_environment ($user, $group, $home) {
    user { $user:
        home => $home,
        managehome => true,
        shell => "/bin/bash",
        ensure => "present",
        groups => [$group],
        require => Group[$group],
    }
    group { $group:
        ensure => "present",
    }
    File {
        owner => $user,
        group => $group,
        require => [User[$user], Group[$group]],
    }
    file { "$home/.bashrc":
        source => "/vagrant/vagrant/puppet/modules/user_environment/files/bashrc",
        mode => 644,
    }
}
