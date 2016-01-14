# Install kivy_relayr on OS X

If you want you can try running Kivy on Mac OS X by first following the 
instructions on this page: https://kivy.org/docs/installation/installation-osx.html. 
Below there is a summary for Kivy2 using Python 2, plus dependancies:

Install Kivy:

1. wget https://kivy.org/downloads/1.9.1/Kivy-1.9.1-osx-python2.7z
2. open Kivy-1.9.1-osx-python2.7z (or use some tool directly to unpack it into Kivy2.app)
3. sudo mv Kivy2.app /Applications/Kivy.app
4. sudo ln -s /Applications/Kivy.app/Contents/Resources/script /usr/local/bin/kivy

Install dependancies:

5. kivy -m pip install git+git://github.com/relayr/python-sdk.git
6. kivy -m pip install kivy-garden
7. source /Applications/Kivy.app/Contents/Resources/venv/bin/activate
8. garden install graph
9. deactivate

Fetch/config/hack/run workshop code:

10. git clone https://github.com/eviltnan/kivy_relayr.git
11. cd kivy_relayr
12. cp relayr_credentials_sample.json relayr_credentials.json
13. emacs relayr_credentials.json (replace IDs)
14. cp -R ~/.kivy/garden/garden.graph graph
15. kivy my_main.py
