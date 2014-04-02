class python_source {
    Class['openssl'] -> Class['python_source']
    case $operatingsystem {
        Fedora: {
            $packages = ["bzip2-devel",
                         "expat-devel",
                         "gdbm-devel",
                         "patch",
                         "readline-devel",
                         "sqlite-devel"]
        }
        ubuntu: {
            $packages = ["libncursesw5-dev",
                         "libreadline-dev",
                         "libgdbm-dev",
                         "libc6-dev",
                         "libbz2-dev",
                         "libicu-dev",
                         "libsqlite3-dev"]
        }
    }        
    package { $packages: ensure => installed }
}
