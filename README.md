# Windows Setup
1. download python 3.8 Windows installer (64-bit) https://www.python.org/downloads/release/python-3810/
2. navigate to muzero-general directory on command line
3. `py -3.8 -m ensurepip`
4. Create a virtual environment
   1. `py -3.8 -m pip install virtualenv`
   2. `py -3.8 -m virtualenv venv`
5. Activate virtual environment (you will need to do this every time before you run the application)
   1. `.\venv\Scripts\activate`
7. `pip install -r requirements.txt` 
8. `python muzero.py`


# Mac
1. download python https://www.python.org/downloads/macos/
2. navigate to muzero-general directory on command line
3. `python3 -m ensurepip --upgrade`
4. Create Virtual Environment
   1. `python3 -m venv venv`
5. Activate Virtual Environment 
   1. `source ./venv/bin/activate`
6. `pip3 install -r requirements.txt`
7. `python3 muzero.py`

# GPU Setup (to be added)