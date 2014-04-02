define python($user, $home) {
    Class['development_tools'] -> Python[$user]
    User_environment[$user] -> Python[$user]

    exec { "git clone pyenv $user":
        command => "git clone git://github.com/yyuu/pyenv.git .pyenv",
        cwd => $home,
        user => $user,
        creates => "$home/.pyenv/.git",
    }
    file { "$home/.pyenv/plugins":
        ensure => "directory",
        require => Exec["git clone pyenv $user"],
    }
    exec { "git clone pyenv virtualenvwrapper $user":
        command => "git clone git://github.com/yyuu/pyenv-virtualenvwrapper.git",
        cwd => "$home/.pyenv/plugins",
        user => $user,
        creates => "$home/.pyenv/plugins/pyenv-virtualenvwrapper/.git",
        require => File["$home/.pyenv/plugins"],
    }
    exec { "pyenv install 2.7.6 $user":
        command => "su - $user -c 'pyenv install 2.7.6'",
        cwd => $home,
        require => [Exec["git clone pyenv virtualenvwrapper $user"],
                    Class['python_source']],
        unless => "su - $user  -c 'pyenv versions | grep 2.7.6'",
    }
    exec { "pyenv rehash 2.7.6 $user":
        command => "su - $user -c 'pyenv rehash'",
        cwd => $home,
        require => Exec["pyenv install 2.7.6 $user"],
    }
    exec { "pyenv install 3.4.0 $user":
        command => "su - $user -c 'pyenv install 3.4.0'",
        cwd => $home,
        require => [Exec["git clone pyenv virtualenvwrapper $user"],
                    Class['python_source']],
        unless => "su - $user  -c 'pyenv versions | grep 3.4.0'",
    }
    exec { "pyenv rehash 3.4.0 $user":
        command => "su - $user -c 'pyenv rehash'",
        cwd => $home,
        require => Exec["pyenv install 3.4.0 $user"],
    }
    exec { "pyenv global 2.7.6 $user":
        command => "su - $user -c 'pyenv global 2.7.6'",
        cwd => $home,
        require => Exec["pyenv rehash 2.7.6 $user"],
    }
    exec { "pip install 2.7.6 $user":
        command => "su - $user -c 'pyenv shell 2.7.6; pip install virtualenv virtualenvwrapper'",
        cwd => $home,
        require => Exec["pyenv rehash 2.7.6 $user"],
    }
    exec { "pip install 3.4.0 $user":
        command => "su - $user -c 'pyenv shell 3.4.0; pip install virtualenv virtualenvwrapper'",
        cwd => $home,
        require => Exec["pyenv rehash 3.4.0 $user"],
    }
}
