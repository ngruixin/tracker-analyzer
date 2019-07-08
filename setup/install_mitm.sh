#!/bin/bash

# install pyenv 
# from http://www.knight-of-pi.org/pyenv-for-python-version-management-on-raspbian-stretch/
sudo apt-get install bzip2 libbz2-dev libreadline6 libreadline6-dev libffi-dev libssl1.0-dev sqlite3 libsqlite3-dev -y
git clone git://github.com/yyuu/pyenv.git .pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
. ~/.bashrc

# install virtualenv 
# from https://github.com/pyenv/pyenv-virtualenv
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
exec "$SHELL" 

# install mitmproxy (requires python>=3.6 but raspbian only has python 3.5.3)
pyenv install 3.7.1
pyenv virtualenv 3.7.1 mitm
pyenv activate mitm
pip install mitmproxy

# install tshark for packet capture 
sudo apt-get install tshark
echo "export SSLKEYLOGFILE=\"$PWD/.mitmproxy/sslkeylogfile.txt\"" >> ~/.bashrc
source ~/.bashrc
