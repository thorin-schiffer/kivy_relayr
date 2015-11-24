## Relayr Kivy Workshop Project

### Before you start

* Ensure you are under Ubuntu (or in virtualbox). Best case 15.10, because i have it.
* Install kivy

     sudo add-apt-repository ppa:kivy-team/kivy
     sudo apt-get install python-kivy

It's the easiest way to install. See for more options here http://kivy.org/docs/installation/installation-linux.html
You can install it also under OSX (http://kivy.org/docs/installation/installation-osx.html), it's your way then padawan,
I won't be able to help you.

Current version in the ppa is 1.9.0 (november 2015). It's possible to install kivy in a virtualenv also, but we'll keep
simple (for curious ones, don't forget to set  mkvirtualenv --system-site-packages)

* Install relayr library

    pip install git+https://github.com/relayr/python-sdk

### Todo

* History widget, matplotlib
* Multiple devices
* Device id in storage
* Sensor widget interaction
* Buildozer, android sdk, entry in readme (in before you start)
* Android packaging