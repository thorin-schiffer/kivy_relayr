# Install kivy_relayr on OS X

If you want you can try running Kivy on Mac OS X by first following the 
instructions on this page: https://kivy.org/docs/installation/installation-osx.html. 
Below there is a summary for Kivy2 using Python 2, plus dependencies:

Install Kivy:

1. `wget https://kivy.org/downloads/1.9.1/Kivy-1.9.1-osx-python2.7z`
2. `open Kivy-1.9.1-osx-python2.7z` (or use some tool directly to unpack it into Kivy2.app)
3. `sudo mv Kivy2.app /Applications/Kivy.app`
4. `sudo ln -s /Applications/Kivy.app/Contents/Resources/script /usr/local/bin/kivy`

Install dependencies:

5. `kivy -m pip install git+git://github.com/relayr/python-sdk.git`
 Note: If you see a setup error like this when configuring pexpect (a dependency of the python-sdk package)
 ```
Running setup.py install for pexpect
      File "/Applications/Kivy.app/Contents/Resources/venv/lib/python2.7/site-packages/pexpect/async.py", line 16
        transport, pw = yield from asyncio.get_event_loop()\
                                 ^
    SyntaxError: invalid syntax
 ```
 
 it is a [known issue](https://github.com/pexpect/pexpect/issues/220) on Python 2.7 and it is safe to ignore this error.
6. `kivy -m pip install kivy-garden`
7. `source /Applications/Kivy.app/Contents/Resources/venv/bin/activate`
8. `garden install graph`
9. `deactivate`

Fetch/config/hack/run workshop code:

10. `git clone https://github.com/eviltnan/kivy_relayr.git`
11. `cd kivy_relayr`
12. `cp relayr_credentials_sample.json relayr_credentials.json`
13. `cp -R ~/.kivy/garden/garden.graph graph`
14. `kivy my_main.py`
