class python {
    package {
        [
         "python",
         "python-devel",
         "python-pip",
         "python3",
         "python3-devel",
        ]: ensure => installed,
    }
    exec { "pip upgrade":
        command => "pip install --upgrade pip virtualenv virtualenvwrapper",
        require => [Package["python"],
                    Package["python-pip"],
                    Package["python-devel"]],
    }
}
