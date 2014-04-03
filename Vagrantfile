# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
      vb.customize ["modifyvm", :id, "--cpus", "2"]
    end

    config.vm.define "fedora20" do |fedora20|
        fedora20.vm.box = "fedora20"
        fedora20.vm.box_url = "https://db.tt/38SDhilg"
        fedora20.vm.network "private_network", ip: "192.168.50.8"
        fedora20.vm.provision :shell, :path => "vagrant/shell/main.sh"
        fedora20.vm.provision :puppet do |puppet|
            puppet.module_path = "vagrant/puppet/modules"
            puppet.manifests_path = "vagrant/puppet"
            puppet.manifest_file  = "init.pp"
            puppet.options = "--verbose --debug"
        end
    end

    config.vm.define "fedora19" do |fedora19|
        fedora19.vm.box = "fedora19"
        fedora19.vm.box_url = "https://db.tt/6NjYJoCi"
        fedora19.vm.network "private_network", ip: "192.168.50.9"
        fedora19.vm.provision :shell, :path => "vagrant/shell/main.sh"
        fedora19.vm.provision :puppet do |puppet|
            puppet.module_path = "vagrant/puppet/modules"
            puppet.manifests_path = "vagrant/puppet"
            puppet.manifest_file  = "init.pp"
            puppet.options = "--verbose --debug"
        end
    end

    config.vm.define "fedora18" do |fedora18|
        fedora18.vm.box = "fedora18"
        fedora18.vm.box_url = "https://db.tt/CGhtLXRW"
        fedora18.vm.network "private_network", ip: "192.168.50.10"
        fedora18.vm.provision :shell, :path => "vagrant/shell/main.sh"
        fedora18.vm.provision :puppet do |puppet|
            puppet.module_path = "vagrant/puppet/modules"
            puppet.manifests_path = "vagrant/puppet"
            puppet.manifest_file  = "init.pp"
            puppet.options = "--verbose --debug"
        end
    end

    config.vm.define "fedora17" do |fedora17|
        fedora17.vm.box = "fedora17"
        fedora17.vm.box_url = "https://db.tt/DnHSqDlZ"
        fedora17.vm.network "private_network", ip: "192.168.50.11"
        fedora17.vm.provision :shell, :path => "vagrant/shell/main.sh"
        fedora17.vm.provision :puppet do |puppet|
            puppet.module_path = "vagrant/puppet/modules"
            puppet.manifests_path = "vagrant/puppet"
            puppet.manifest_file  = "init.pp"
            puppet.options = "--verbose --debug"
        end
    end

end

