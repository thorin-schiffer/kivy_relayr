## Relayr Kivy Workshop

This repository contains code for a 
[workshop](http://www.meetup.com/IoT-Innovation-Lab/events/227863351/ "workshop") 
about creating IoT dashboards with 
[Kivy](http://kivy.org/ "Kivy").
The sensor data used here comes from a 
[WunderBar](https://www.relayr.io/wunderbar/ "WunderBar"), an IoT development kit by 
[relayr.io](http://relayr.io/ "relayr.io"),
but it should be fairly easy to use data from anywhere.
Since Kivy is a mobile-first, cross-platform GUI framework, the same code should run
on platforms like Linux, Android, iOS and Mac OS X.
But turning this into native applications can be challenging (mostly to setup and configure
the respective environments), so this workshop will focus on an implemention on Linux.
Nevertheless, you can find some notes in the file `install_osx.md` that should be useful
to run this code on Mac OS X (while is will not be supported by Sergey who is leading the
workshop).

### Target Platform

For this workshop the target platform is defined as following:

- Ubuntu 15.10
- native or inside a virtual machine (VirtualBox recommended)
- the code here (as well as Ubuntu 15.10) also works on the Raspberry Pi 2
- previous Ubuntu versions might work, too, but have not been tested

For the Raspberry Pi there is even an image of a complete distribution named
[KivyPie](http://kivypie.mitako.eu/ "KivyPie") that you can try out (this was
not tested though with the code in this repository).

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

### Installing the relayr API client

The relayr library is an API client that provides access to the open sensor data 
cloud by [relayr.io](http://relayr.io/ "relayr.io").
The recommended installation is directly from GitHub:

`pip install git+https://github.com/relayr/python-sdk`

In order to use this API client and receive data from a WunderBar, one must have
a WunderBar and an account on the [relayr.io](http://relayr.io/ "relayr.io")
cloud. 
To make things as fast and easy as possible both will be provided during the
workshop.
  
### Installing This Project

Since the focus of this workshop is on developing with Kivy and relayr there will
be no dashboard package to really "install" from this project and we can simply
work in the cloned repository.

```
git clone https://github.com/eviltnan/kivy_relayr.git
cd kivy_relayr
pip install -r requirements.txt
garden install graph
```

### Running the Code

Before you can run the code you must create a file named `relayr_credentials.json`
which contains an API access token as well as a list of device IDs for devices 
on the WunderBar that you will want to display in a dashboard.
You can pick up these IDs from the 
[relayr developer dashboard](https://developer.relayr.io/ "relayr developer dashboard").
For conveniance reasons a temporary token (valid for 14 days) and three device IDs
were added to the file `relayr_credentials_sample.json` in this repo, so pleople
can play with before the workshop.
Once this file is created and populated with the correct information you can start 
the dashboard with this command and watch how your device sensors are doing:

```
python main.py
```
