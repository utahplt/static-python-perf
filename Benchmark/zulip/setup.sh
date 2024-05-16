# pre-requisites
# TODO: install git and docker
sudo apt install vagrant
sudo adduser $USER docker
# TODO: reboot the system

# Get Zulip Code
git clone https://github.com/mrigankpawagi/zulip
cd zulip
git remote add -f upstream https://github.com/zulip/zulip.git

# Start the development environment
sudo vagrant up --provider=docker
vagrant ssh
./tools/run-dev
