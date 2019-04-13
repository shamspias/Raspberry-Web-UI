# Raspberry Web UI
Simple Python3 Flask Application for controlling the GPIO pins on a Raspberry Pi

# Install
1. First Create a Virtual Environment
-->Windows
    First, make sure you have python installed on your pcopen cmd or PowerShell
        python -m venv  yourvenv
-->Linux and others
    Open terminal
        sudo apt-get install python3-pip
        pip3 install virtualenv
After installing virtualenv just type
        virtualenv yourvenv

2. Activate Virtual Environment.
    -->Windows
        yourvenv/Scripts/activate
If show any error then open Powershell in admin
then type
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
and press "A" then Enter.

    -->Linux
        . yourvenv/bin/activate
3. Install the requirement .txt
    -->Windows
        pip install -r requirement .txt
    -->Linux
        pip3 install -r requirement .txt

-------------------------------
Now if you are not in raspberry pi then you need to install Fack-GPIO.
    pip install git+https://github.com/sn4k3/FakeRPi
Then go to lib/GPIOSetup.py and edit 
    "import RPi.GPIO as GPIO" to "import FakeRPi.GPIO as GPIO"

# Run Application

    Windows
        cd ..
        set FLASK_APP=project (Name of your project folder)
    Linux
        cd ..
        export FLASK_APP=project (Name of your project folder)

Then 
        flask run --host 0.0.0.0 --port 8000

Access the UI at http://ip_address:8000
