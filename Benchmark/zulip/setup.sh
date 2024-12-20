# pre-requisites
# TODO: install docker
sudo apt install vagrant git
sudo adduser $USER docker
# TODO: reboot the system

# Get Zulip Code
git clone https://github.com/zulip/zulip
cd zulip
git remote add -f upstream https://github.com/zulip/zulip.git

# Start the development environment
vagrant up --provider=docker # `vagrant provision` if this fails
cat run.sh | vagrant ssh
