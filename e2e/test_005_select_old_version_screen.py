from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.select_old_version_screen import SelectOldVersionScreen

MOCKED_FOUND_API = [
    {"author": "test", "tag_name": "v23.08.1"},
    {"author": "test", "tag_name": "v23.08.0"},
    {"author": "test", "tag_name": "v22.08.1"},
    {"author": "test", "tag_name": "v22.08.0"},
    {"author": "test", "tag_name": "v22.02.0"},
]

OLD_VERSIONS = [d["tag_name"] for d in MOCKED_FOUND_API]


class TestSelectOldVersionScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectOldVersionScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SelectOldVersionScreen")
        self.assertEqual(screen.id, "select_old_version_screen")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_grid_layout(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "select_old_version_screen_grid")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("kivy.uix.gridlayout.GridLayout.clear_widgets")
    def test_clear_grid(self, mock_clear_widgets, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_clear_widgets.assert_called_once()
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_background"
    )
    def test_on_press(self, mock_set_background, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        calls = []
        for button in grid.children:
            on_press = getattr(screen, f"on_press_{button.id}")
            on_press(button)
            calls.append(call(wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_old_version_screen.SelectOldVersionScreen.manager")
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_background"
    )
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_screen"
    )
    def test_on_release(
        self, mock_set_screen, mock_set_background, mock_manager, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        mock_manager.get_screen = MagicMock()

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        set_background_calls = []
        set_screen_calls = []

        for button in grid.children:
            on_release = getattr(screen, f"on_release_{button.id}")
            on_release(button)
            set_background_calls.append(call(wid=button.id, rgba=(0, 0, 0, 0)))

            if button.id == "select_old_version_back":
                set_screen_calls.append(
                    call(name="SelectVersionScreen", direction="right")
                )
            else:
                set_screen_calls.append(call(name="MainScreen", direction="right"))

        mock_set_background.assert_has_calls(set_background_calls)
        mock_set_screen.assert_has_calls(set_screen_calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_locale(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        screen.update(name="ConfigKruxInstaller", key="locale", value="pt_BR.UTF-8")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button_back = grid.children[0]

        self.assertEqual(button_back.text, "Voltar")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_locale(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="Mock", key="locale", value="pt_BR.UTF-8")

        self.assertEqual(str(exc_info.exception), "Invalid screen name: Mock")
        mock_get_running_app.assert_called_once()
