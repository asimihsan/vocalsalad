VERSION = 0.0.1
ITERATION = 2

MAINTAINER = asim.ihsan@gmail.com
URL = https://github.com/asimihsan/vocalsalad

PYTHON_BIN = python2.7
PROJECT = vocalsalad
ROOT = /opt/$(PROJECT)

define POST_INSTALL_SH
#!/usr/bin/env bash
ln -s $(ROOT)/bin/$(PROJECT) /usr/local/bin/$(PROJECT)
endef
export POST_INSTALL_SH

define POST_UNINSTALL_SH
#!/usr/bin/env bash
unlink /usr/local/bin/$(PROJECT)
endef
export POST_UNINSTALL_SH

rpm:
	sudo chown vagrant:vagrant /opt
	rm -rf $(ROOT)
	virtualenv --python=$(PYTHON_BIN) --clear \
		--system-site-packages $(ROOT)
	source "$(ROOT)/bin/activate"; python setup.py install
	virtualenv --relocatable $(ROOT)
	echo "$$POST_INSTALL_SH" > /tmp/post-install.sh
	echo "$$POST_UNINSTALL_SH" > /tmp/post-uninstall.sh
	rm -f *.rpm
	source /etc/os-release; fpm -s dir -t rpm -n '$(PROJECT)' \
		--package-name-suffix "$$ID$$VERSION_ID" \
		--version $(VERSION) --iteration $(ITERATION) --epoch 0 \
		-C $(ROOT) --python-bin $(PYTHON_BIN) \
		--directories=$(ROOT) --post-install /tmp/post-install.sh \
	    --post-uninstall /tmp/post-uninstall.sh --architecture native \
	    --depends python --maintainer $(MAINTAINER) --url $(URL) \
	    $(ROOT)
	mv *.rpm /vagrant/package-dist/
	rm -rf $(ROOT)
	rm -f /tmp/post-install.sh /tmp/post-uninstall.sh
