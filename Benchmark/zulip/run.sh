# freeze requirements from zuilp-py3-venv and remove it
pip freeze > requirements.txt
deactivate
sudo rm -r zulip-py3-venv

# requirements for cinder
sudo apt install libsqlite3-dev
export CFLAGS="-I /srv/zulip/cinder/Include"
export PATH=$PATH:/home/vagrant/.local/bin

# download and build cinder
git clone https://github.com/facebookincubator/cinder && cd cinder
./configure --enable-loadable-sqlite-extensions && make -j

# reinstall requirements in static-python
./python -m ensurepip # install pip
./python -m pip install -r ../requirements.txt --no-cache-dir

## create venv with static-python
cd ../
./cinder/python -m venv zulip-py3-venv --system-site-packages
source ./zulip-py3-venv/bin/activate
# pip install -r requirements.txt

# add __call__ to all method calls (our hack for the 'nargsf' issue)
find /home/vagrant/.local/lib/python3.10/site-packages/aiohttp/ -type f -exec sed -i -E "s/self\.([a-zA-Z_\.]*)\(/self\.\1\.__call__\(/g" {} \;
find /home/vagrant/.local/lib/python3.10/site-packages/aiosignal/ -type f -exec sed -i -E "s/self\.([a-zA-Z_\.]*)\(/self\.\1\.__call__\(/g" {} \;
find /home/vagrant/.local/lib/python3.10/site-packages/lxml/ -type f -exec sed -i -E "s/self\.([a-zA-Z_\.]*)\(/self\.\1\.__call__\(/g" {} \;

# run
./tools/run-dev
