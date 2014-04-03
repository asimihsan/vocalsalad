# vocalsalad

[![Build Status](https://travis-ci.org/asimihsan/vocalsalad.svg?branch=master)](https://travis-ci.org/asimihsan/vocalsalad)
[![Code Health](https://landscape.io/github/asimihsan/vocalsalad/master/landscape.png)](https://landscape.io/github/asimihsan/vocalsalad/master)
[![Requirements Status](https://requires.io/github/asimihsan/vocalsalad/requirements.png?branch=master)](https://requires.io/github/asimihsan/vocalsalad/requirements/?branch=master)

Run long-running tasks on remote machines, and gather file-based
artifacts.

Supports CPython 2.6, 2.7, 3.2, 3.3, and 3.4, and PyPy 2.2.

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

## How to build an RPM

On your host machine, after installing VirtualBox and Vagrant:

```
vagrant up fedora19  # fedora17, fedora18, fedora19, fedora20
vagrant ssh fedora19  # after this command you're in a shell in the VM
cd /vagrant
make rpm
```

You'll find the RPM in `package-dist`.

### Notes on building RPMs manually

If you want to run the build manually on the VM for a Python 2.7 RPM:

```
ROOT=/opt/vocalsalad
PYTHON_BIN=python2.7

cd ~
sudo chown vagrant:vagrant /opt
rm -rf $ROOT
virtualenv --python=$PYTHON_BIN --clear --system-site-packages $ROOT
source "$ROOT/bin/activate"
cd /vagrant
python setup.py install
virtualenv --relocatable $ROOT
deactivate

cd $ROOT
rm -f *.rpm
cat << EOF > post-install.sh
#!/usr/bin/env bash
ln -s /opt/vocalsalad/bin/vocalsalad /usr/local/bin/vocalsalad
EOF
cat << EOF > post-uninstall.sh
#!/usr/bin/env bash
unlink /usr/local/bin/vocalsalad
EOF
fpm -s dir -t rpm -n 'vocalsalad' -v 0.0.1 -C $ROOT \
    --python-bin $PYTHON_BIN --directories=$ROOT \
    --post-install post-install.sh --post-uninstall post-uninstall.sh
    --architecture all $ROOT
mv *.rpm /vagrant/package-dist/
rm -rf $ROOT

```
