# vocalsalad

Run long-running tasks on remote machines, and gather file-based
artifacts

## Running tests

-   Install pyenv (https://github.com/yyuu/pyenv)
-   Set up pyenv on your machine, then install all Python versions
    via pyenv:

```
pyenv install 2.7.5
pyenv install 2.6.8
pyenv install 3.2.5
pyenv install 3.3.2
pyenv install 3.4.0
pyenv rehash
pyenv global 2.7.5 2.6.8 3.3.2 3.2.5 3.4.0
```

-   Run the tests via tox:

```
tox
```

## How to build an RPM (TODO script this)

For a Python 2.7 RPM:

```
cd ~
deactivate
sudo chown vagrant:vagrant /opt
ROOT=/opt/vocalsalad
rm -rf $ROOT
virtualenv $ROOT --python=python2.7 --always-copy --system-site-packages
source "$ROOT/bin/activate"
cd /vagrant
python setup.py install
virtualenv $ROOT --relocatable
cd $ROOT

echo #!/usr/bin/env bash              > post-install.sh
echo ln -s /opt/vocalsalad/bin/vocalsalad /usr/local/bin/vocalsalad >> post-install.sh
echo #!/usr/bin/env bash              > post-uninstall.sh
echo unlink /usr/local/bin/vocalsalad >> post-uninstall.sh
fpm -s dir -t rpm -n 'vocalsalad' -v 0.0.1 -C $ROOT \
    --python-bin python2.7 --directories=$ROOT \
    --post-install post-install.sh --post-uninstall post-uninstall.sh \
    $ROOT
mv vocalsalad-0.0.1-1.x86_64.rpm /vagrant/package-dist/

```
