# Installation

These instructions are for a Unix-based environment (specifically Ubuntu in parts).

## Basic Game

To run the game and see output using the text interface:

    # Set this to whatever you want.
    PARENT_DIR=/var/www
    cd $PARENT_DIR
    git clone git@github.com:maxbogue/planetwars.git
    cd planetwars
    python play.py Random Random

Works with Python 2 or Python 3.

## Web Server

To get the web server running on port 4200 (Python 2 only):

    # virtualenv is highly recommended.
    virtualenv env
    # Add the parent directory to the PYTHONPATH.
    echo $PARENT_DIR > env/lib/python2.7/site-packages/www.pth
    # Activate our virtualenv.
    . env/bin/activate
    # libevent is required by gevent.
    sudo apt-get install libevent-dev
    # Python libraries.
    pip install flask gevent gevent-socketio
    # Run the server!
    python web/server.py
