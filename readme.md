## Relayr Kivy Workshop

This repository contains code for a workshop about creating IoT dashboards with Kivy.
The sensor data used here comes from a WunderBar, an IoT development kit by relayr.io,
but it should be fairly easy to use data from anywhere.
Since Kivy is a mobile-first, cross-platform GUI framework, the same code should run
on platforms like Linux, Android, iOS and MacOS.
But since making this really happen can be challenging (mostly to setup and configure
the respective environments), this workshop will focus on an implemention on Linux
(including the Raspberry Pi).

### Target Platform

For this workshop the target platform is defined as following:

- Ubuntu 15.10
- native or inside a virtual machine (VirtualBox recommended)
- the code here (as well as Ubuntu 15.10) also works on the Raspberry Pi 2
- previous Ubuntu versions might work, too, but have not been tested

### Installing Kivy

This project uses the most recent version (daily build) of Kivy.
This is the easiest type of installation.
See http://kivy.org/docs/installation/installation-linux.html for more options.

```
sudo apt-get update
sudo apt-get python-pip
sudo pip install -U pip
sudo pip install cython

sudo add-apt-repository ppa:kivy-team/kivy-daily
sudo apt-get update
sudo apt-get install python-kivy
````

The current version in the ppa is 1.9.1-dev (December 2015).
It is possible to install Kivy in a virtualenv also, but we want to keep it simple 
(for the curious, don't forget to set `mkvirtualenv --system-site-packages`).

While you can install Kivy also under Mac OS X, the focus in this workshop will be
on Linux and not OS X, but you can find more details here:
http://kivy.org/docs/installation/installation-osx.html.

### Installing Other Dependencies

* relayr API client

  The relayr library is an API client that provides access to the open sensor data 
  cloud by relayr.io. The recommended installation is directly from GitHub:

  `pip install git+https://github.com/relayr/python-sdk`

* Install pip reqs
    pip install -r requirements.txt

* Install garden deps

    garden install graph
