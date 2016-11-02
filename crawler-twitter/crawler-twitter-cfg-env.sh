#!/bin/bash -e

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

if [ ! -d "$SCRIPTPATH/.virtual" ]; then
    echo "+++ Create virtualenv +++"
    python -m virtualenv $SCRIPTPATH/.virtual
    echo "+++ Virtualenv created +++"
fi

if [ ! -f "$SCRIPTPATH/.virtual" -o $SCRIPTPATH/requirements.pip -nt $SCRIPTPATH/.virtual ]; then
    source $SCRIPTPATH/.virtual/bin/activate
    echo "+++ Virtualenv activate +++"

    echo "+++ Upgrade pip and setuptools +++"
    pip install --upgrade pip
    pip install --upgrade setuptools
    echo "+++ Pip and setuptools upgraded +++"

    echo "+++ Install requirements +++"
    pip install -r $SCRIPTPATH/requirements.txt
    echo "+++ Requirements installed +++"

    deactivate
    echo "+++ Virtualenv deactivate +++"
fi
