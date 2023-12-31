from setuptools import setup

APP = ["src/SoundFixer/app.py"]
DATA_FILES = ["icon-on.png", "icon-off.png"]
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "icon.icns",
    "plist": {
        "CFBundleShortVersionString": "1.0.0",
        "LSUIElement": True,
    },
    "packages": ["rumps", "requests"],
}

setup(
    app=APP,
    name="SoundFixer",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    install_requires=["rumps", "requests"],
)
