import os
import sys
from unittest.mock import patch, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.download_selfcustody_pem_screen import (
    DownloadSelfcustodyPemScreen,
)


class TestDownloadSelfcustodyPemScreen(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        noto_sans_path = os.path.join(assets_path, "NotoSansCJK_Cy_SC_KR_Krux.ttf")
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(screen.downloader, None)
        self.assertEqual(screen.thread, None)
        self.assertEqual(screen.trigger, None)
        self.assertEqual(screen.to_screen, "VerifyStableZipScreen")
        self.assertEqual(grid.id, "download_selfcustody_pem_screen_grid")
        self.assertEqual(
            grid.children[1].id, "download_selfcustody_pem_screen_progress"
        )
        self.assertEqual(grid.children[0].id, "download_selfcustody_pem_screen_info")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_invalid_name(self, mock_redirect_exception, mock_get_locale):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="MockScreen")

        # patch assertions
        mock_redirect_exception.assert_called_once()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_fail_update_key(self, mock_get_locale):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="mock")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        # default assertions
        self.assertEqual(screen.locale, "en_US.UTF-8")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets",
        return_value="mockdir",
    )
    @patch("src.app.screens.download_selfcustody_pem_screen.PemDownloader")
    def test_update_public_key_certificate(
        self, mock_downloader, mock_destdir_assets, mock_get_locale
    ):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="public-key-certificate")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_destdir_assets.assert_any_call()
        mock_downloader.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_progress(self, mock_get_locale):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        fontsize_g = 0
        fontsize_mp = 0

        if sys.platform in ("linux", "win32"):
            fontsize_g = window.size[0] // 16
            fontsize_mp = window.size[0] // 48

        if sys.platform == "darwin":
            fontsize_g = window.size[0] // 32
            fontsize_mp = window.size[0] // 128

        # do tests
        screen.update(
            name="ConfigKruxInstaller",
            key="progress",
            value={"downloaded_len": 210000, "content_len": 21000000},
        )

        # do tests
        text = "".join(
            [
                f"[size={fontsize_g}sp][b]1.00 %[/b][/size]",
                "\n",
                f"[size={fontsize_mp}sp]",
                "210000",
                " of ",
                "21000000",
                " B",
                "[/size]",
            ]
        )

        self.assertEqual(
            screen.ids["download_selfcustody_pem_screen_progress"].text, text
        )

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.download_selfcustody_pem_screen.PemDownloader")
    @patch("src.app.screens.download_selfcustody_pem_screen.partial")
    @patch("src.app.screens.download_selfcustody_pem_screen.Clock.schedule_once")
    def test_on_progress(
        self,
        mock_schedule_once,
        mock_partial,
        mock_downloader,
        mock_get_locale,
    ):
        mock_downloader.downloaded_len = 8
        mock_downloader.content_len = 21000000

        # screen
        screen = DownloadSelfcustodyPemScreen()
        screen.downloader = mock_downloader
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        # pylint: disable=no-member
        DownloadSelfcustodyPemScreen.on_progress(data=b"")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    screen.update,
                    name=screen.name,
                    key="progress",
                    value={"downloaded_len": 8, "content_len": 21000000},
                ),
            ]
        )

        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 0)], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_progress_100_percent(self, mock_get_locale):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        fontsize_g = 0
        fontsize_mp = 0

        if sys.platform in ("linux", "win32"):
            fontsize_g = window.size[0] // 16
            fontsize_mp = window.size[0] // 48

        if sys.platform == "darwin":
            fontsize_g = window.size[0] // 32
            fontsize_mp = window.size[0] // 128

        # do tests
        with patch.object(screen, "trigger") as mock_trigger, patch.object(
            screen, "downloader"
        ) as mock_downloader:

            mock_downloader.destdir = "mockdir"
            screen.update(
                name="ConfigKruxInstaller",
                key="progress",
                value={"downloaded_len": 210, "content_len": 21},
            )

            # do tests
            text_progress = "".join(
                [
                    f"[size={fontsize_g}sp][b]100.00 %[/b][/size]",
                    "\n",
                    f"[size={fontsize_mp}sp]",
                    "21",
                    " of ",
                    "21",
                    " B",
                    "[/size]",
                ]
            )

            filepath = os.path.join("mockdir", "selfcustody.pem")
            text_info = "".join(
                [
                    f"[size={fontsize_mp}sp]",
                    filepath,
                    "\n",
                    "downloaded",
                    "[/size]",
                ]
            )

            self.assertEqual(
                screen.ids["download_selfcustody_pem_screen_progress"].text,
                text_progress,
            )
            self.assertEqual(
                screen.ids["download_selfcustody_pem_screen_info"].text, text_info
            )

            # patch assertions
            mock_get_locale.assert_any_call()
            assert len(mock_trigger.mock_calls) >= 1

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.download_selfcustody_pem_screen.time.sleep")
    @patch(
        "src.app.screens.download_selfcustody_pem_screen.DownloadSelfcustodyPemScreen.set_screen"
    )
    def test_on_trigger(self, mock_set_screen, mock_sleep, mock_get_locale):
        # screen
        screen = DownloadSelfcustodyPemScreen()

        # pylint: disable=no-member
        screen.trigger = screen.on_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        # pylint: disable=no-member
        DownloadSelfcustodyPemScreen.on_trigger(0)

        # default assertions
        self.assertFalse(screen.on_trigger is None)
        self.assertFalse(screen.trigger is None)

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_sleep.assert_called_once_with(2.1)
        mock_set_screen.assert_called_once_with(
            name="VerifyStableZipScreen", direction="left"
        )
