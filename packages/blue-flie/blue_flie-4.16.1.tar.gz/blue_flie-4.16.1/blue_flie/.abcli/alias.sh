#! /usr/bin/env bash

alias @flie=blue_flie

alias toolbelt=blue_flie_toolbelt

# https://www.bitcraze.io/documentation/repository/toolbelt/master/installation/#installation
# docker run --rm -it bitcraze/toolbelt
alias tb='docker run --rm -it -e "HOST_CW_DIR=${PWD}" -e "CALLING_HOST_NAME=$(hostname)" -e "CALLING_UID"=$UID -e "CALLING_OS"=$(uname) -v ${PWD}:/tb-module -v ${HOME}/.ssh:/root/.ssh -v /var/run/docker.sock:/var/run/docker.sock bitcraze/toolbelt'
