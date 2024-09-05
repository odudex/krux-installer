import os
import sys
from unittest.mock import patch, MagicMock
from pytest import mark
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.ask_permission_dialout_screen import AskPermissionDialoutScreen


# WARNING: Do not run these tests on windows
# they will break because it do not have the builtin 'grp' module
@mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestAskPermissionDialoutScreen(GraphicUnitTest):

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
    def test_render_label(self, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="AskPermissionDialoutScreen", key="user", value="mockeduser")
        screen.update(name="AskPermissionDialoutScreen", key="group", value="dialout")
        screen.update(name="AskPermissionDialoutScreen", key="distro", value="mockos")
        screen.update(name="AskPermissionDialoutScreen", key="screen")
        self.assertTrue("ask_permission_dialout_screen_label" in screen.ids)

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.ask_permission_dialout_screen.SudoerLinux.exec")
    def test_press_allow(self, mock_exec, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.bin = "mock"
        screen.bin_args = ["-a", "-G"]
        screen.group = "mockedgroup"
        screen.user = "mockeduser"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        action = getattr(screen, f"on_ref_press_{screen.id}_label")
        action("Allow")

        # patch assertions
        on_permission_created = getattr(
            AskPermissionDialoutScreen, "on_permission_created"
        )
        mock_get_locale.assert_called_once()
        mock_exec.assert_called_once_with(
            cmd=["/usr/bin/usermod", "-a", "-G", "mockedgroup", "mockeduser"],
            env={},
            callback=on_permission_created,
        )
