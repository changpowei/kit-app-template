# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
import omni
import omni.usd
from pxr import Sdf
import omni.kit.commands
import omni.ext
import omni.ui as ui
import omni.kit.ui

# Any class derived from 'omni.ext.IExt' in top level module (defined in 'python.modules' of 'extension.toml') will be instantiated when Extension gets enabled and 'on_startup(ext_id)' will be called. Later when Extension gets disabled 'on_shutdown()' is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current Extension id. It can be used with Extension manager to query additional information, like where this Extension is located on filesystem.
    def on_startup(self, ext_id):
        # Initialize some properties
        self._count = 0
        self._window = None
        self._menu = None
        # Create a menu item inside the already existing "Window" menu.
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item("Window/My Company Window", self.show_window, toggle=True, value=False)
    def on_shutdown(self):
        self._window = None
        self._menu = None
    def show_window(self, menu_path: str, visible: bool):
        if visible:
            # Create window
            self._window = ui.Window("My Company Window", width=300, height=300)
            with self._window.frame:
                with ui.VStack():
                    def on_click(asset_name = "Cardbox_B2", asset_path = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Containers/Cardboard/Cardbox_B2.usd"):
                        omni.kit.commands.execute('CreatePayloadCommand',
                            usd_context=omni.usd.get_context(),
                            path_to=Sdf.Path('/World/' + asset_name),
                            asset_path=asset_path,
                            instanceable=False)

                    with ui.HStack():
                        ui.Button("Add Cardbox", clicked_fn=on_click)
                        ui.Button("Add Pallets", clicked_fn=lambda name="Pallets", path="http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Piles/Pallets_A1.usd": on_click(name, path))
            self._window.set_visibility_changed_fn(self._visiblity_changed_fn)
        elif self._window:
            # Remove window
            self._window = None
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value("Window/My Company Window", visible)

    def _visiblity_changed_fn(self, visible):
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            # Toggle the checked state of the menu item
            editor_menu.set_value("Window/My Company Window", visible)
