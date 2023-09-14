import rumps
from subprocess import Popen


DEFAULT_VOLUME = 50


class SoundFixer(rumps.App):
    def __init__(self):
        super(SoundFixer, self).__init__("SoundFixer", title="", icon="icon.png")
        self.enabled = True

    @rumps.timer(2)
    def _set_volume(self, _):
        if not self.enabled:
            return

        Popen(["osascript", "-e", f"set volume input volume {DEFAULT_VOLUME}"])


if __name__ == "__main__":
    SoundFixer().run()
