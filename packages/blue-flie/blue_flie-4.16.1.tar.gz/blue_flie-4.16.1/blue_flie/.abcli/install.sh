#! /usr/bin/env bash

# https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-brushless/
function abcli_install_blue_flie() {
    abcli_git_clone https://github.com/bitcraze/crazyflie-lib-python.git \
        cd
    pip install -e .

    # https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/installation/install/#macos
    python3 -m pip install cfclient
}

abcli_install_module blue_flie 1.1.1
