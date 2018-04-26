# Bartiméus Sensoren

## Requirements
- Python 3.6.*
- Pip 9.* / 10.*

## Installing dependencies
If you want to use a virtual environment, you can follow the following tutorial:
[http://docs.python-guide.org/en/latest/dev/virtualenvs/]()

If you want to use the virtual environment, you can activate it by running the following command from the base folder:
```bash
source environment/sensor_env/bin/activate
```

You have to install the dependencies by running the following command from the project folder:
```bash 
pip install -r requirements.txt
```

Or, you can install the following packages by hand:
- imutils
- numpy
- opencv-python


## Running the script
After installing the dependencies, you can start the app by running the following command from the src folder:
```bash
python start.py
```

You can also run the motion detector by itself, by running the following command from the src folder:
```bash
python motiondetector.py
```