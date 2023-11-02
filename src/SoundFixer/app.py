import os
import rumps
from subprocess import check_output, Popen
import signal


DEFAULT_VOLUME = 50.0
CHECK_INTERVAL_SECONDS = 4


class SoundFixer(rumps.App):
    def __init__(self):
        super(SoundFixer, self).__init__("SoundFixer", title="", quit_button=None)
        self.app_data_file = os.path.expanduser(
            "~/Library/Application Support/SoundFixer/data.txt"
        )
        self.device_name = None
        self.volume = DEFAULT_VOLUME
        self.load_data()
        self.build_menu()

    def build_menu(self):
        self.icon = "icon-on.png" if self.device_name is not None else "icon-off.png"
        self.menu.clear()

        if self.device_name is None:
            self.menu.add(rumps.MenuItem("Devices", callback=None))
            for device in self.list_devices():
                self.menu.add(rumps.MenuItem(device, callback=self.set_device))
        else:
            menu_item = rumps.MenuItem(self.device_name, callback=self.disable)
            menu_item.state = True
            self.menu.add(menu_item)

            self.menu.add(rumps.separator)

            self.menu.add(rumps.MenuItem("Volume", callback=None))
            self.menu.add(
                rumps.SliderMenuItem(
                    value=self.volume,
                    min_value=0,
                    max_value=100,
                    callback=self.set_volume,
                    dimensions=(200, 30),
                )
            )

        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Quit", callback=self.save_and_quit))

    def set_volume(self, sender):
        self.volume = round(sender.value)
        self.save_data()

    def set_device(self, sender):
        self.device_name = sender.title
        self.build_menu()
        self.save_data()

    def list_devices(self):
        devices = check_output(
            ["/usr/local/bin/SwitchAudioSource", "-a", "-t", "input"]
        ).splitlines()
        for device in devices:
            yield device.decode("utf-8")

    def disable(self, _):
        self.device_name = None
        self.build_menu()

    def save_data(self):
        try:
            if self.device_name is not None:
                with open(self.app_data_file, "w") as f:
                    f.write(f"{self.device_name}\n{round(self.volume)}")
            else:
                os.remove(self.app_data_file)
        except FileNotFoundError:
            pass

    def load_data(self):
        try:
            with open(self.app_data_file, "r") as f:
                device = f.readline().strip()
                self.device_name = (
                    device if device in list(self.list_devices()) else None
                )
                self.volume = float(f.readline().strip())
        except Exception:
            self.device_name = None
            self.volume = DEFAULT_VOLUME

    def save_and_quit(self, sender):
        self.save_data()
        rumps.quit_application(sender)

    @rumps.timer(CHECK_INTERVAL_SECONDS)
    def _event_loop(self, _):
        if self.device_name is None:
            return

        Popen(["osascript", "-e", f"set volume input volume {self.volume}"])
        Popen(
            [
                "/usr/local/bin/SwitchAudioSource",
                "-s",
                self.device_name,
                "-t",
                "input",
            ]
        )


if __name__ == "__main__":
    app = SoundFixer()
    signal.signal(signal.SIGINT, app.save_and_quit)
    app.run()
