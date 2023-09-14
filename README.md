# Sound Fixer

## Description
This simple Mac OS app resets the microphone input volume to 50% every 2 seconds. This is useful for when the microphone volume is automatically set by applications like Slack or Zoom.

## Build
1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Build the app: `python setup.py py2app`

## Run
1. Open the app: `open dist/Sound\ Fixer.app`
2. (Optional) Add the app to the login items: `System Settings > Login Items`


