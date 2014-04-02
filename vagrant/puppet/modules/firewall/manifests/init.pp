class firewall {
    service { "firewalld":
        ensure => "stopped",
        enable => false,
    }
}