import rumps
from subprocess import Popen


DEFAULT_VOLUME = 50
CHECK_INTERVAL_SECONDS = 2


class SoundFixer(rumps.App):
    def __init__(self):
        super(SoundFixer, self).__init__("SoundFixer", title="", icon="icon.png")
        self.enabled = True
        self.volume = DEFAULT_VOLUME
        self._build_menu()

    def _build_menu(self):
        enabled_menu_item = rumps.MenuItem("Enabled", callback=self.toggle)
        enabled_menu_item.state = self.enabled
        self.menu.add(enabled_menu_item)

        self.menu.add(
            rumps.SliderMenuItem(
                value=DEFAULT_VOLUME,
                min_value=0,
                max_value=100,
                callback=self.set_volume,
                dimensions=(200, 40),
            )
        )

        self.menu.add(rumps.separator)

    def toggle(self, sender):
        self.enabled = not self.enabled
        sender.state = not sender.state

    def set_volume(self, sender):
        self.volume = sender.value

    @rumps.timer(CHECK_INTERVAL_SECONDS)
    def _event_loop(self, _):
        if not self.enabled:
            return

        Popen(["osascript", "-e", f"set volume input volume {self.volume}"])


if __name__ == "__main__":
    SoundFixer().run()
