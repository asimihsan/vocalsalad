class openssl {
    $base_packages = ["openssl"]
    case $operatingsystem {
        ubuntu: {
            $packages = ["libssl-dev"]
        }
        Fedora: {
            $packages = ["openssl-devel"]
        }
    }
    package { $base_packages: ensure => latest }
    package { $packages: ensure => latest }
}
