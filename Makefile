VERSION = 0.0.1
ITERATION = 6

MAINTAINER = asim.ihsan@gmail.com
URL = https://github.com/asimihsan/vocalsalad

PYTHON_BIN = python2.7
PROJECT = vocalsalad
ROOT = /opt/$(PROJECT)

define BEFORE_INSTALL_SH
#!/usr/bin/env bash
set -e
if [ "$$1" = "2" ]; then
	# Perform whatever maintenance must occur before the upgrade begins
	echo "BEFORE_INSTALL: This is an upgrade. Stop the service."
	systemctl stop $(PROJECT).service
fi
endef
export BEFORE_INSTALL_SH

define AFTER_INSTALL_SH
#!/usr/bin/env bash
set -e

if [ "$$1" = "1" ]; then
	# Perform tasks to prepare for the initial installation (no previous
	# installation is present)
	echo "AFTER_INSTALL: This is an initial installation. Create/copy "
	echo "files, enable/start the service."
	ln -s $(ROOT)/bin/$(PROJECT) /usr/local/bin/$(PROJECT)
	if [ ! -f /etc/systemd/system/$(PROJECT).service ]; then
		cp $(ROOT)/infrastructure/fedora/$(PROJECT).service \
			/etc/systemd/system/$(PROJECT).service
	fi
	systemctl daemon-reload
	systemctl enable $(PROJECT).service
	systemctl start $(PROJECT).service
elif [ "$$1" = "2" ]; then
	# Perform whatever maintenance must occur before the upgrade begins
	echo "AFTER_INSTALL: This is an upgrade. Just restart the service."
	systemctl restart $(PROJECT).service
fi
endef
export AFTER_INSTALL_SH

define BEFORE_REMOVE_SH
#!/usr/bin/env bash
set -e

if [ "$$1" = "0" ]; then
	# Perform tasks to prepare for the uninstallation (we are not
	# upgrading so brutally clean everything up).
	echo "BEFORE_REMOVE: This is a final uninstallation. Stop/disable "
	echo "service, remove service file."
	if [ -f /etc/systemd/system/$(PROJECT).service ]; then
		systemctl stop $(PROJECT).service
		systemctl disable $(PROJECT).service
		rm -f /etc/systemd/system/$(PROJECT).service
		systemctl daemon-reload
	fi;
elif [ "$$1" = "1" ]; then
	# Perform whatever maintenance must occur before the upgrade ends
	echo "BEFORE_REMOVE: This is an upgrade. Do nothing."
fi
endef
export BEFORE_REMOVE_SH

define AFTER_REMOVE_SH
#!/usr/bin/env bash
set -e

if [ "$$1" = "0" ]; then
	# Perform tasks to prepare for the uninstallation (we are not
	# upgrading so brutally clean everything up).
	echo "AFTER_REMOVE: This is a final uninstallation. Remove files."
	unlink /usr/local/bin/$(PROJECT)
elif [ "$$1" = "1" ]; then
	# Perform whatever maintenance must occur before the upgrade ends
	echo "AFTER_REMOVE: This is an upgrade. Do nothing."
fi
endef
export AFTER_REMOVE_SH

rpm:
	sudo chown vagrant:vagrant /opt
	rm -rf $(ROOT)
	virtualenv --python=$(PYTHON_BIN) --clear \
		--system-site-packages $(ROOT)
	source "$(ROOT)/bin/activate"; python setup.py install
	virtualenv --relocatable $(ROOT)
	cp -r /vagrant/$(PROJECT)/infrastructure $(ROOT)

	echo "$$BEFORE_INSTALL_SH" > /tmp/before-install.sh
	echo "$$AFTER_INSTALL_SH" > /tmp/after-install.sh
	echo "$$BEFORE_REMOVE_SH" > /tmp/before-remove.sh
	echo "$$AFTER_REMOVE_SH" > /tmp/after-remove.sh
	rm -f *.rpm
	source /etc/os-release; fpm -s dir -t rpm -n '$(PROJECT)' \
		--version $(VERSION) --iteration $(ITERATION) --epoch 0 \
		-C $(ROOT) --python-bin $(PYTHON_BIN) \
		--directories=$(ROOT) \
		--before-install /tmp/before-install.sh \
		--after-install /tmp/after-install.sh \
		--before-remove /tmp/before-remove.sh \
	    --after-remove /tmp/after-remove.sh \
	    --architecture native --depends python \
	    --maintainer $(MAINTAINER) --url $(URL) \
	    --package "$(PROJECT)-$(VERSION)-$(ITERATION).$$ID$$VERSION_ID.$(shell uname -i).rpm" \
	    $(ROOT)
	mv *.rpm /vagrant/package-dist/
	rm -rf $(ROOT)
	rm -f /tmp/before-install.sh /tmp/after-install.sh \
		/tmp/before-remove.sh /tmp/after-remove.sh
