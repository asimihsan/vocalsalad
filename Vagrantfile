# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
      vb.customize ["modifyvm", :id, "--cpus", "2"]
    end

    config.vm.define "fedora20" do |fedora20|
        fedora20.vm.box = "fedora20"
        fedora20.vm.box_url = "http://goo.gl/svGCgY"
        fedora20.vm.network "private_network", ip: "192.168.50.8"
        fedora20.vm.provision :shell, :path => "vagrant/shell/main.sh"
        fedora20.vm.provision :puppet do |puppet|
            puppet.module_path = "vagrant/puppet/modules"
            puppet.manifests_path = "vagrant/puppet"
            puppet.manifest_file  = "init.pp"
            puppet.options = "--verbose --debug"
        end
    end

end

