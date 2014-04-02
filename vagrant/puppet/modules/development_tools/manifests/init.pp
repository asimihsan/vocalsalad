class development_tools {
    case $operatingsystem {
        /(centos|redhat|oel|Fedora)/: {
            exec { 'yum --assumeyes groupinstall "Development Tools"':
                unless => 'yum grouplist "Development Tools" | grep "^Installed Groups"',
            }
        }
    }
    $base_packages = ["wget",
                      "git",
                      "tree",
                      "htop",
                      "dtach",
                      "expect",
                      "pigz"]
    case $operatingsystem {
        ubuntu: {
            $packages = ["build-essential"]
        }
        Fedora: {
            $packages = ["automake",
                         "gcc",
                         "gcc-c++",
                         "make",
                         "rpm-build"]
        }
    }
    package { $base_packages: ensure => installed }
    package { $packages: ensure => installed }

    class { '::ntp':
        servers => ['0.uk.pool.ntp.org',
                    '1.uk.pool.ntp.org',
                    '2.uk.pool.ntp.org',
                    '3.uk.pool.ntp.org'],
    }
}
