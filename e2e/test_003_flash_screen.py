from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.flash_screen import FlashScreen


class TestFlashScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_main_screen(self):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "FlashScreen")
        self.assertEqual(screen.id, "flash_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.flash_screen.FlashScreen.on_press")
    def test_before_goto_screen_select_device(self, mock_on_press):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.before_goto_screen(name="SelectDeviceScreen")
        mock_on_press.assert_called_once_with(wid="flash_select_device")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.flash_screen.FlashScreen.set_screen")
    @patch("src.app.screens.flash_screen.FlashScreen.on_release")
    def test_goto_screen_select_device(self, mock_on_release, mock_set_screen):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.goto_screen(name="SelectDeviceScreen", direction="left")
        mock_on_release.assert_called_once_with(wid="flash_select_device")
        mock_set_screen.assert_called_once_with(
            name="SelectDeviceScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.flash_screen.FlashScreen.on_press")
    def test_before_goto_screen_select_version(self, mock_on_press):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.before_goto_screen(name="SelectVersionScreen")
        mock_on_press.assert_called_once_with(wid="flash_select_version")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.flash_screen.FlashScreen.set_screen")
    @patch("src.app.screens.flash_screen.FlashScreen.on_release")
    def test_goto_screen_select_version(self, mock_on_release, mock_set_screen):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.goto_screen(name="SelectVersionScreen", direction="left")
        mock_on_release.assert_called_once_with(wid="flash_select_version")
        mock_set_screen.assert_called_once_with(
            name="SelectVersionScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_fail_before_goto_screen(self):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.before_goto_screen(name="MockScreen")

        self.assertEqual(str(exc_info.exception), "Invalid 'MockScreen' widget")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_fail_goto_screen(self):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.goto_screen(name="MockScreen", direction="left")

        self.assertEqual(str(exc_info.exception), "Invalid 'MockScreen' widget")
