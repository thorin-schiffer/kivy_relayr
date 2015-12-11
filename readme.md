## Relayr Kivy Workshop Project

This repository contains code for a workshop about creating IoT dashboards with Kivy.
The sensor data used here comes from a WunderBar, an IoT development kit by relayr.io,
but it should be fairly easy to use data from anywhere.
Since Kivy is a mobile-first, cross-platform GUI framework, the same code should run
on platforms like Linux, Android, iOS and MacOS. But since making this really happen
can be challenging, this workshop will focus on an implemention on Linux (including
the Raspberry Pi).

### Before you start

* Ensure you are under Ubuntu (or in virtualbox). Best case 15.10, because i have it.
* Install kivy (we will need daily build, it looks better)

     sudo add-apt-repository ppa:kivy-team/kivy-daily
     sudo apt-get update
     sudo apt-get install python-kivy

It's the easiest way to install. See for more options here http://kivy.org/docs/installation/installation-linux.html
You can install it also under OSX (http://kivy.org/docs/installation/installation-osx.html), it's your way then padawan,
I won't be able to help you.

Current version in the ppa is 1.9.0 (november 2015). It's possible to install kivy in a virtualenv also, but we'll keep
simple (for curious ones, don't forget to set  mkvirtualenv --system-site-packages)

* Install relayr library

    pip install git+https://github.com/relayr/python-sdk

* Install pip reqs
    pip install -r requirements.txt

* Install garden deps

    garden install graph
