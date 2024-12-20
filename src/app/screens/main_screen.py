# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
main_screen.py
"""
import os
import re
import typing
from functools import partial
from kivy.clock import Clock
from src.utils.selector import VALID_DEVICES
from src.app.screens.base_screen import BaseScreen


class MainScreen(BaseScreen):
    """
    Main screen is the 'Home' page

    .. versionadded:: 0.0.2-alpha-1
    """

    def __init__(self, **kwargs):
        super().__init__(wid="main_screen", name="MainScreen", **kwargs)

        # Prepare some variables
        self.device = "select a new one"
        self.version = "select a new one"
        self.will_flash = False
        self.will_wipe = False

        # Build grid where buttons will be placed
        self.make_grid(wid="main_screen_grid", rows=6)
        self.build_select_version_button()
        self.build_select_device_button()
        self.build_flash_button()
        self.build_wipe_button()
        self.build_settings_button()
        self.build_about_button()

    @property
    def device(self) -> str:
        """Getter for device property"""
        return self._device

    @device.setter
    def device(self, value: str):
        self.debug(f"device = {value}")
        self._device = value

    @property
    def version(self) -> str:
        """Getter for version property"""
        return self._version

    @version.setter
    def version(self, value: str):
        """Setter for version property"""
        self.debug(f"version = {value}")
        self._version = value

    @property
    def will_flash(self) -> bool:
        """Getter for will_flash property"""
        return self._will_flash

    @will_flash.setter
    def will_flash(self, value: bool):
        """Setter for will_flash property"""
        self.debug(f"will_flash = {value}")
        self._will_flash = value

    @property
    def will_wipe(self) -> bool:
        """Getter for will_wipe property"""
        return self._will_wipe

    @will_wipe.setter
    def will_wipe(self, value: bool):
        """Setter for will_wipe property"""
        self.debug(f"will_wipe = {value}")
        self._will_wipe = value

    def build_select_version_button(self):
        """Create a staticmethod using instance variables to control the select_version button"""
        url = "https://api.github.com/repos/selfcustody/krux/releases"
        wid = "main_select_version"
        msg = self.translate("Version")

        def on_press(instance):
            self.debug(f"Calling {instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))
            fetch_msg = self.translate("Fetching data from")
            self.ids[instance.id].text = "".join(
                [
                    "[color=#efcc00]",
                    f"[b]{fetch_msg}[/b]",
                    "\n",
                    url,
                    "[/color]",
                ]
            )

        def on_release(instance):
            self.debug(f"Calling {instance.id}::on_release")
            select_version = self.manager.get_screen("SelectVersionScreen")
            select_version.clear()
            select_version.fetch_releases()
            self.set_background(wid="main_select_version", rgba=(0, 0, 0, 1))
            self.set_screen(name="SelectVersionScreen", direction="left")
            self.update(name=self.name, key="version", value=self.version)

        self.make_button(
            row=0,
            wid=wid,
            root_widget="main_screen_grid",
            text="".join(
                [
                    f"{msg}: ",
                    "[color=#00AABB]",
                    self.translate(self.version),
                    "[/color]",
                ]
            ),
            halign=None,
            font_factor=28,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def build_select_device_button(self):
        """Create staticmethods using instance variables to control the select_device button"""
        wid = "main_select_device"
        msg = self.translate("Device")

        def on_press_select_device(instance):
            self.debug(f"Calling {instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release_select_device(instance):
            self.debug(f"Calling {instance.id}::on_release")
            select_device = self.manager.get_screen("SelectDeviceScreen")
            fn = partial(
                select_device.update,
                name=self.name,
                key="version",
                value=self.version,
            )
            Clock.schedule_once(fn, 0)
            self.set_background(wid="main_select_device", rgba=(0, 0, 0, 1))
            self.set_screen(name="SelectDeviceScreen", direction="left")

        setattr(MainScreen, "on_press_select_device", on_press_select_device)
        setattr(MainScreen, "on_release_select_device", on_release_select_device)

        self.make_button(
            row=1,
            wid=wid,
            root_widget="main_screen_grid",
            text="".join(
                [
                    f"{msg}: ",
                    "[color=#00AABB]",
                    self.translate(self.device),
                    "[/color]",
                ]
            ),
            font_factor=28,
            halign=None,
            on_press=getattr(MainScreen, "on_press_select_device"),
            on_release=getattr(MainScreen, "on_release_select_device"),
            on_ref_press=None,
        )
        self.ids[wid].size_hint = (1, 1)

    def on_check_any_official_release(
        self, partial_list: typing.List[typing.Callable]
    ) -> str:
        """Check if any official release file exists"""
        resources = MainScreen.get_destdir_assets()
        zipfile = os.path.join(resources, f"krux-{self.version}.zip")
        to_screen = None

        if os.path.isfile(zipfile):
            to_screen = "WarningAlreadyDownloadedScreen"
        else:
            to_screen = "DownloadStableZipScreen"

        screen = self.manager.get_screen(to_screen)
        partial_list.append(
            partial(
                screen.update,
                name=self.name,
                key="canvas",
            )
        )
        partial_list.append(
            partial(
                screen.update,
                name=self.name,
                key="version",
                value=self.version,
            )
        )

        return to_screen

    def on_check_any_beta_release(
        self, partial_list: typing.List[typing.Callable]
    ) -> str:
        """Check if release is beta"""
        to_screen = "DownloadBetaScreen"
        screen = self.manager.get_screen(to_screen)
        partial_list.append(
            partial(
                screen.update,
                name=self.name,
                key="canvas",
            )
        )
        partial_list.append(
            partial(
                screen.update,
                name=self.name,
                key="firmware",
                value="kboot.kfpkg",
            )
        )
        partial_list.append(
            partial(
                screen.update,
                name=self.name,
                key="device",
                value=self.device,
            )
        )

        partial_list.append(partial(screen.update, name=self.name, key="downloader"))
        return to_screen

    def build_flash_button(self):
        """Create staticmethods using instance variables to control the flash button"""
        wid = "main_flash"

        def on_press_flash(instance):
            self.debug(f"Calling {instance.id}::on_press")
            if self.will_flash:
                self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))
            else:
                self.warning(f"Button::{instance.id} disabled")

        def on_release_flash(instance):
            self.debug(f"Calling {instance.id}::on_release")
            if not self.will_flash:
                self.warning(f"Button::{instance.id} disabled")
            else:
                # do a click effect
                self.set_background(wid="main_flash", rgba=(0, 0, 0, 1))

                # partials are functions that call `update`
                # method in screen before go to them
                partial_list = []
                err = None

                if re.match(r"^v\d+\.\d+\.\d$", self.version):
                    to_screen = self.on_check_any_official_release(
                        partial_list=partial_list
                    )

                elif re.match("^odudex/krux_binaries", self.version):
                    to_screen = self.on_check_any_beta_release(
                        partial_list=partial_list
                    )

                else:
                    err = RuntimeError(f"version '{self.version}' not supported")
                    self.redirect_exception(exception=err)
                    return

                # Execute the partials
                for fn in partial_list:
                    Clock.schedule_once(fn, 0)

                # Goto the selected screen
                self.set_screen(name=to_screen, direction="left")

        setattr(MainScreen, f"on_press_{wid}", on_press_flash)
        setattr(MainScreen, f"on_release_{wid}", on_release_flash)

        flash_msg = self.translate("Flash")
        self.make_button(
            row=2,
            wid=wid,
            root_widget="main_screen_grid",
            text=f"[color=#333333]{flash_msg}[/color]",
            font_factor=28,
            halign=None,
            on_press=getattr(MainScreen, f"on_press_{wid}"),
            on_release=getattr(MainScreen, f"on_release_{wid}"),
            on_ref_press=None,
        )

    def build_wipe_button(self):
        """Create staticmethods using instance variables to control the wipe button"""
        wid = "main_wipe"

        def on_press_wipe(instance):
            self.debug(f"Calling {instance.id}::on_press")
            if self.will_wipe:
                self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))
            else:
                self.warning(f"Button::{instance.id} disabled")

        def on_release_wipe(instance):
            self.debug(f"Calling {instance.id}::on_release")
            if self.will_wipe:
                self.set_background(wid="main_wipe", rgba=(0, 0, 0, 1))
                self.set_screen(name="WarningWipeScreen", direction="left")
            else:
                self.debug(f"Button::{instance.id} disabled")

        setattr(MainScreen, "on_press_wipe", on_press_wipe)
        setattr(MainScreen, "on_release_wipe", on_release_wipe)

        wipe_msg = self.translate("Wipe")
        self.make_button(
            row=3,
            wid=wid,
            root_widget="main_screen_grid",
            text=f"[color=#333333]{wipe_msg}[/color]",
            font_factor=28,
            halign=None,
            on_press=getattr(MainScreen, "on_press_wipe"),
            on_release=getattr(MainScreen, "on_release_wipe"),
            on_ref_press=None,
        )

    def build_settings_button(self):
        """Create staticmethods using instance variables to control the settings button"""
        wid = "main_settings"

        def on_press_settings(instance):
            self.debug(f"Calling {instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release_settings(instance):
            self.debug(f"Calling {instance.id}::on_release")
            self.set_background(wid="main_settings", rgba=(0, 0, 0, 1))
            MainScreen.open_settings()

        setattr(MainScreen, "on_press_settings", on_press_settings)
        setattr(MainScreen, "on_release_settings", on_release_settings)

        self.make_button(
            row=4,
            wid=wid,
            root_widget="main_screen_grid",
            text=self.translate("Settings"),
            font_factor=28,
            halign=None,
            on_press=getattr(MainScreen, "on_press_settings"),
            on_release=getattr(MainScreen, "on_release_settings"),
            on_ref_press=None,
        )

    def build_about_button(self):
        """Create staticmethods using instance variables to control the about button"""
        wid = "main_about"

        def on_press_about(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release_about(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid="main_about", rgba=(0, 0, 0, 1))
            self.set_screen(name="AboutScreen", direction="left")

        setattr(MainScreen, "on_press_about", on_press_about)
        setattr(MainScreen, "on_release_about", on_release_about)

        self.make_button(
            row=5,
            wid=wid,
            root_widget="main_screen_grid",
            text=self.translate("About"),
            font_factor=28,
            halign=None,
            on_press=getattr(MainScreen, "on_press_about"),
            on_release=getattr(MainScreen, "on_release_about"),
            on_ref_press=None,
        )

    def update_version(self, value: str):
        """Update the version shown in button. To be used on update method"""
        version_msg = self.translate("Version")
        self.version = MainScreen.sanitize_markup(value)
        self.ids["main_select_version"].text = "".join(
            [
                f"{version_msg}: ",
                "[color=#00AABB]",
                self.version,
                "[/color]",
            ]
        )

    def update_device(self, value: str):
        """Update the device shown in button. To be used on update method"""
        self.device = MainScreen.sanitize_markup(value)

        # check if update to given values
        if value in VALID_DEVICES:
            self.device = value
            self.will_flash = True
            self.will_wipe = True
            self.ids["main_flash"].text = self.translate("Flash")
            self.ids["main_wipe"].text = self.translate("Wipe")

        else:
            self.will_flash = False
            self.will_wipe = False
            self.ids["main_flash"].markup = True
            self.ids["main_wipe"].markup = True
            self.ids["main_flash"].text = "".join(
                ["[color=#333333]", self.translate("Flash"), "[/color]"]
            )
            self.ids["main_wipe"].text = "".join(
                ["[color=#333333]", self.translate("Wipe"), "[/color]"]
            )

        # translate device type value even if it is a vXX.YY.Z
        # the translator will try to translate and if a proper
        # value isnt found, use the raw one
        device_type = self.translate(value)
        device_msg = self.translate("Device")
        self.ids["main_select_device"].text = "".join(
            [
                f"{device_msg}: ",
                "[color=#00AABB]",
                device_type,
                "[/color]",
            ]
        )

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons from selected device/versions on related screens"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            # Check if update to given key
            if key == "version":
                if value is not None:
                    self.update_version(value)
                else:
                    error = RuntimeError(f"Invalid value for key '{key}': {value}")
                    self.redirect_exception(exception=error)

            if key == "device":
                if value is not None:
                    self.update_device(value)
                else:
                    error = RuntimeError(f"Invalid value for key '{key}': {value}")
                    self.redirect_exception(exception=error)

            if key == "flash":
                if not self.will_flash:
                    self.ids["main_flash"].text = "".join(
                        ["[color=#333333]", self.translate("Flash"), "[/color]"]
                    )
                else:
                    self.ids["main_flash"].text = self.translate("Flash")

            if key == "wipe":
                if not self.will_wipe:
                    self.ids["main_wipe"].text = "".join(
                        ["[color=#333333]", self.translate("Wipe"), "[/color]"]
                    )
                else:
                    self.ids["main_wipe"].text = self.translate("Wipe")

            if key == "settings":
                self.ids["main_settings"].text = self.translate("Settings")

            if key == "about":
                self.ids["main_about"].text = self.translate("About")

        setattr(MainScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "KruxInstallerApp",
                "ConfigKruxInstaller",
                "GreetingsScreen",
                "MainScreen",
                "SelectDeviceScreen",
                "SelectVersionScreen",
                "SelectOldVersionScreen",
            ),
            on_update=getattr(MainScreen, "on_update"),
        )
