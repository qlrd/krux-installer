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
import math
import re
from threading import Thread
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.uix.label import Label
from src.app.screens.base_screen import BaseScreen
from src.utils.downloader.beta_downloader import BetaDownloader


class DownloadBetaScreen(BaseScreen):
    """DownloadBetaScreen manage the download process of beta releases"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="download_beta_screen", name="DownloadBetaScreen", **kwargs
        )
        self.make_grid(wid="download_beta_screen_grid", rows=2)
        self.downloader = None
        self.downloader_thread = None

        # progress label
        progress = Label(
            text="", markup=True, font_size="80sp", valign="center", halign="center"
        )
        progress.id = "download_progress"
        self.ids["download_beta_screen_grid"].add_widget(progress)
        self.ids[progress.id] = WeakProxy(progress)

        # build label
        asset_label = Label(markup=True, valign="center", halign="center")
        asset_label.id = "asset_label"
        self.ids["download_beta_screen_grid"].add_widget(asset_label)
        self.ids[asset_label.id] = WeakProxy(asset_label)

    def update(self, *args, **kwargs):
        """Update screen with device key"""
        if kwargs.get("key") == "device":
            self.downloader = BetaDownloader(
                device=kwargs.get("value"),
                binary_type="kboot.kfpkg",
                destdir=App.get_running_app().config.get("destdir", "assets"),
            )

            def on_progress(data: bytes):
                l1 = self.downloader.downloaded_len
                l2 = self.downloader.content_len
                p = l1 / l2
                self.ids["download_progress"].text = "\n".join(
                    [
                        f"[size=100sp][b]{p * 100.00:.2f}%[/b][/size]",
                        f"[size=16sp]{l1} of {l2} B[/size]",
                    ]
                )

            self.downloader.on_write_to_buffer = on_progress

            self.ids["asset_label"].text = "\n".join(
                [
                    "Downloading",
                    f"[color=#00AABB][ref={self.downloader.url}]{self.downloader.url}[/ref][/color]",
                    "" f"to {self.downloader.destdir}",
                ]
            )

    def on_enter(self):
        """Event fired when the screen is displayed: the entering animation is complete"""
        Thread(target=self.downloader.download).start()
