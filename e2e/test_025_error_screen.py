import os
from unittest.mock import patch, MagicMock
from kivy.base import EventLoop
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.error_screen import ErrorScreen


class TestErrorScreen(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        font_name = "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
        noto_sans_path = os.path.join(assets_path, font_name)
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = ErrorScreen()

        # default assertions
        self.assertTrue("error_screen_grid" in screen.ids)
        self.assertTrue("error_screen_label" in screen.ids)

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_make_label_text(self, mock_get_locale):
        screen = ErrorScreen()
        screen.manager = MagicMock()
        screen.manager.screen_names = ["KruxInstallerApp", screen.name]

        # get your Window instance safely
        label = screen.ids[f"{screen.id}_label"]

        error = RuntimeError("Error: mocked error: at test")
        screen.update(name=screen.name, key="error", value=error)

        text = "".join(
            [
                "[color=#ff0000]Error[/color]",
                "\n",
                " mocked error",
                "\n",
                " at test",
                "\n",
                "Report issue at ",
                "[color=#00aabb]",
                "[ref=ReportIssue]",
                f"{screen.src_code}/issues",
                "[/ref]",
                "[/color]",
                "\n",
                "[color=#00FF00]",
                "[ref=Back]",
                "[u]Back[/u]",
                "[/ref]",
                "[/color]",
                "        ",
                "[color=#FF0000]",
                "[ref=Quit]",
                "[u]Quit[/u]",
                "[/ref]",
            ]
        )

        self.assertEqual(label.text, text)

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.error_screen.ErrorScreen.set_screen")
    def test_on_ref_press_back(self, mock_set_screen, mock_get_locale):
        screen = ErrorScreen()
        button = screen.ids[f"{screen.id}_label"]

        action = getattr(ErrorScreen, f"on_ref_press_{button.id}")
        action(button, "Back")

        mock_get_locale.assert_any_call()
        mock_set_screen.assert_called_once_with(
            name="GreetingsScreen", direction="right"
        )

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.error_screen.BaseScreen.quit_app")
    def test_on_ref_press_quit(self, mock_quit_app, mock_get_locale):
        screen = ErrorScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        button = screen.ids[f"{screen.id}_label"]

        action = getattr(ErrorScreen, f"on_ref_press_{button.id}")
        action(button, "Quit")

        mock_get_locale.assert_any_call()
        mock_quit_app.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.error_screen.webbrowser.open")
    def test_on_ref_press_report(self, mock_web_open, mock_get_locale):
        screen = ErrorScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        button = screen.ids[f"{screen.id}_label"]

        action = getattr(ErrorScreen, f"on_ref_press_{button.id}")
        action(button, "ReportIssue")

        mock_get_locale.assert_any_call()
        mock_web_open.assert_called_once_with(
            "https://github.com/selfcustody/krux-installer/issues"
        )
