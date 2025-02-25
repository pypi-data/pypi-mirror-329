"""GLFW Library"""
from __future__ import annotations
import imgui.glfw
import typing

__all__ = [
    "ACCUM_ALPHA_BITS",
    "ACCUM_BLUE_BITS",
    "ACCUM_GREEN_BITS",
    "ACCUM_RED_BITS",
    "ALPHA_BITS",
    "ANY_RELEASE_BEHAVIOR",
    "API_UNAVAILABLE",
    "ARROW_CURSOR",
    "AUTO_ICONIFY",
    "AUX_BUFFERS",
    "BLUE_BITS",
    "CENTER_CURSOR",
    "CLIENT_API",
    "COCOA_CHDIR_RESOURCES",
    "COCOA_FRAME_NAME",
    "COCOA_GRAPHICS_SWITCHING",
    "COCOA_MENUBAR",
    "COCOA_RETINA_FRAMEBUFFER",
    "CONNECTED",
    "CONTEXT_CREATION_API",
    "CONTEXT_NO_ERROR",
    "CONTEXT_RELEASE_BEHAVIOR",
    "CONTEXT_REVISION",
    "CONTEXT_ROBUSTNESS",
    "CONTEXT_VERSION_MAJOR",
    "CONTEXT_VERSION_MINOR",
    "CROSSHAIR_CURSOR",
    "CURSOR",
    "CURSOR_DISABLED",
    "CURSOR_HIDDEN",
    "CURSOR_NORMAL",
    "CreateCursor",
    "CreateStandardCursor",
    "CreateWindow",
    "Cursor",
    "DECORATED",
    "DEPTH_BITS",
    "DISCONNECTED",
    "DONT_CARE",
    "DOUBLEBUFFER",
    "DefaultWindowHints",
    "DestroyCursor",
    "DestroyWindow",
    "EGL_CONTEXT_API",
    "ExtensionSupported",
    "FLOATING",
    "FOCUSED",
    "FOCUS_ON_SHOW",
    "FORMAT_UNAVAILABLE",
    "FocusWindow",
    "GAMEPAD_AXIS_LEFT_TRIGGER",
    "GAMEPAD_AXIS_LEFT_X",
    "GAMEPAD_AXIS_LEFT_Y",
    "GAMEPAD_AXIS_RIGHT_TRIGGER",
    "GAMEPAD_AXIS_RIGHT_X",
    "GAMEPAD_AXIS_RIGHT_Y",
    "GAMEPAD_BUTTON_A",
    "GAMEPAD_BUTTON_B",
    "GAMEPAD_BUTTON_BACK",
    "GAMEPAD_BUTTON_CIRCLE",
    "GAMEPAD_BUTTON_CROSS",
    "GAMEPAD_BUTTON_DPAD_DOWN",
    "GAMEPAD_BUTTON_DPAD_LEFT",
    "GAMEPAD_BUTTON_DPAD_RIGHT",
    "GAMEPAD_BUTTON_DPAD_UP",
    "GAMEPAD_BUTTON_GUIDE",
    "GAMEPAD_BUTTON_LEFT_BUMPER",
    "GAMEPAD_BUTTON_LEFT_THUMB",
    "GAMEPAD_BUTTON_RIGHT_BUMPER",
    "GAMEPAD_BUTTON_RIGHT_THUMB",
    "GAMEPAD_BUTTON_SQUARE",
    "GAMEPAD_BUTTON_START",
    "GAMEPAD_BUTTON_TRIANGLE",
    "GAMEPAD_BUTTON_X",
    "GAMEPAD_BUTTON_Y",
    "GREEN_BITS",
    "Gamepadstate",
    "Gammaramp",
    "GetClipboardString",
    "GetCurrentContext",
    "GetCursorPos",
    "GetError",
    "GetFramebufferSize",
    "GetGamepadName",
    "GetGamepadState",
    "GetGammaRamp",
    "GetInputMode",
    "GetJoyStickGUID",
    "GetJoystickAxes",
    "GetJoystickButtons",
    "GetJoystickHats",
    "GetJoystickname",
    "GetKey",
    "GetKeyName",
    "GetKeyScancode",
    "GetMonitorContentScale",
    "GetMonitorName",
    "GetMonitorPhysicalSize",
    "GetMonitorPos",
    "GetMonitorWorkarea",
    "GetMonitors",
    "GetMouseButton",
    "GetPrimaryMonitor",
    "GetTime",
    "GetTimerFrequency",
    "GetTimerValue",
    "GetVersion",
    "GetVersionString",
    "GetVideoMode",
    "GetVideoModes",
    "GetWindowAttrib",
    "GetWindowContentScale",
    "GetWindowFrameSize",
    "GetWindowMonitor",
    "GetWindowOpacity",
    "GetWindowPos",
    "GetWindowSize",
    "HAND_CURSOR",
    "HAT_CENTERED",
    "HAT_DOWN",
    "HAT_LEFT",
    "HAT_LEFT_DOWN",
    "HAT_LEFT_UP",
    "HAT_RIGHT",
    "HAT_RIGHT_DOWN",
    "HAT_RIGHT_UP",
    "HAT_UP",
    "HOVERED",
    "HRESIZE_CURSOR",
    "HideWindow",
    "IBEAM_CURSOR",
    "ICONIFIED",
    "INVALID_ENUM",
    "INVALID_VALUE",
    "IconifyWindow",
    "Image",
    "Init",
    "InitHint",
    "JOYSTICK_1",
    "JOYSTICK_10",
    "JOYSTICK_11",
    "JOYSTICK_12",
    "JOYSTICK_13",
    "JOYSTICK_14",
    "JOYSTICK_15",
    "JOYSTICK_16",
    "JOYSTICK_2",
    "JOYSTICK_3",
    "JOYSTICK_4",
    "JOYSTICK_5",
    "JOYSTICK_6",
    "JOYSTICK_7",
    "JOYSTICK_8",
    "JOYSTICK_9",
    "JOYSTICK_HAT_BUTTONS",
    "JoystickIsGamepad",
    "JoystickPresent",
    "KEY_0",
    "KEY_1",
    "KEY_2",
    "KEY_3",
    "KEY_4",
    "KEY_5",
    "KEY_6",
    "KEY_7",
    "KEY_8",
    "KEY_9",
    "KEY_A",
    "KEY_APOSTROPHE",
    "KEY_B",
    "KEY_BACKSLASH",
    "KEY_BACKSPACE",
    "KEY_C",
    "KEY_CAPS_LOCK",
    "KEY_COMMA",
    "KEY_D",
    "KEY_DELETE",
    "KEY_DOWN",
    "KEY_E",
    "KEY_END",
    "KEY_ENTER",
    "KEY_EQUAL",
    "KEY_ESCAPE",
    "KEY_F",
    "KEY_F1",
    "KEY_F10",
    "KEY_F11",
    "KEY_F12",
    "KEY_F13",
    "KEY_F14",
    "KEY_F15",
    "KEY_F16",
    "KEY_F17",
    "KEY_F18",
    "KEY_F19",
    "KEY_F2",
    "KEY_F20",
    "KEY_F21",
    "KEY_F22",
    "KEY_F23",
    "KEY_F24",
    "KEY_F25",
    "KEY_F3",
    "KEY_F4",
    "KEY_F5",
    "KEY_F6",
    "KEY_F7",
    "KEY_F8",
    "KEY_F9",
    "KEY_G",
    "KEY_GRAVE_ACCENT",
    "KEY_H",
    "KEY_HOME",
    "KEY_I",
    "KEY_INSERT",
    "KEY_J",
    "KEY_K",
    "KEY_KP_0",
    "KEY_KP_1",
    "KEY_KP_2",
    "KEY_KP_3",
    "KEY_KP_4",
    "KEY_KP_5",
    "KEY_KP_6",
    "KEY_KP_7",
    "KEY_KP_8",
    "KEY_KP_9",
    "KEY_KP_ADD",
    "KEY_KP_DECIMAL",
    "KEY_KP_DIVIDE",
    "KEY_KP_ENTER",
    "KEY_KP_EQUAL",
    "KEY_KP_MULTIPLY",
    "KEY_KP_SUBTRACT",
    "KEY_L",
    "KEY_LEFT",
    "KEY_LEFT_ALT",
    "KEY_LEFT_BRACKET",
    "KEY_LEFT_CONTROL",
    "KEY_LEFT_SHIFT",
    "KEY_LEFT_SUPER",
    "KEY_M",
    "KEY_MENU",
    "KEY_MINUS",
    "KEY_N",
    "KEY_NUM_LOCK",
    "KEY_O",
    "KEY_P",
    "KEY_PAGE_DOWN",
    "KEY_PAGE_UP",
    "KEY_PAUSE",
    "KEY_PERIOD",
    "KEY_PRINT_SCREEN",
    "KEY_Q",
    "KEY_R",
    "KEY_RIGHT",
    "KEY_RIGHT_ALT",
    "KEY_RIGHT_BRACKET",
    "KEY_RIGHT_CONTROL",
    "KEY_RIGHT_SHIFT",
    "KEY_RIGHT_SUPER",
    "KEY_S",
    "KEY_SCROLL_LOCK",
    "KEY_SEMICOLON",
    "KEY_SLASH",
    "KEY_SPACE",
    "KEY_T",
    "KEY_TAB",
    "KEY_U",
    "KEY_UNKNOWN",
    "KEY_UP",
    "KEY_V",
    "KEY_W",
    "KEY_WORLD_1",
    "KEY_WORLD_2",
    "KEY_X",
    "KEY_Y",
    "KEY_Z",
    "LOCK_KEY_MODS",
    "LOSE_CONTEXT_ON_RESET",
    "ListWrapperF",
    "ListWrapperMonitor",
    "ListWrapperStr",
    "ListWrapperUC",
    "ListWrapperUS",
    "ListWrapperVidmode",
    "MAXIMIZED",
    "MOD_ALT",
    "MOD_CAPS_LOCK",
    "MOD_CONTROL",
    "MOD_NUM_LOCK",
    "MOD_SHIFT",
    "MOD_SUPER",
    "MOUSE_BUTTON_1",
    "MOUSE_BUTTON_2",
    "MOUSE_BUTTON_3",
    "MOUSE_BUTTON_4",
    "MOUSE_BUTTON_5",
    "MOUSE_BUTTON_6",
    "MOUSE_BUTTON_7",
    "MOUSE_BUTTON_8",
    "MOUSE_BUTTON_LEFT",
    "MOUSE_BUTTON_MIDDLE",
    "MOUSE_BUTTON_RIGHT",
    "MakeContextCurrent",
    "MaximizeWindow",
    "Monitor",
    "NATIVE_CONTEXT_API",
    "NOT_INITIALIZED",
    "NO_API",
    "NO_CURRENT_CONTEXT",
    "NO_ERROR",
    "NO_RESET_NOTIFICATION",
    "NO_ROBUSTNESS",
    "NO_WINDOW_CONTEXT",
    "OPENGL_ANY_PROFILE",
    "OPENGL_API",
    "OPENGL_COMPAT_PROFILE",
    "OPENGL_CORE_PROFILE",
    "OPENGL_DEBUG_CONTEXT",
    "OPENGL_ES_API",
    "OPENGL_FORWARD_COMPAT",
    "OPENGL_PROFILE",
    "OSMESA_CONTEXT_API",
    "OUT_OF_MEMORY",
    "PLATFORM_ERROR",
    "PRESS",
    "PollEvents",
    "PostEmptyEvent",
    "RAW_MOUSE_MOTION",
    "RED_BITS",
    "REFRESH_RATE",
    "RELEASE",
    "RELEASE_BEHAVIOR_FLUSH",
    "RELEASE_BEHAVIOR_NONE",
    "REPEAT",
    "RESIZABLE",
    "RawMouseMotionSupported",
    "RequestWindowAttention",
    "RestoreWindow",
    "SAMPLES",
    "SCALE_TO_MONITOR",
    "SRGB_CAPABLE",
    "STENCIL_BITS",
    "STEREO",
    "STICKY_KEYS",
    "STICKY_MOUSE_BUTTONS",
    "SetCharCallback",
    "SetCharModsCallback",
    "SetClipboardString",
    "SetCursor",
    "SetCursorEnterCallback",
    "SetCursorPos",
    "SetCursorPosCallback",
    "SetDropCallback",
    "SetErrorCallback",
    "SetFramebufferSizeCallback",
    "SetGamma",
    "SetGammaRamp",
    "SetInputMode",
    "SetJoystickCallback",
    "SetKeyCallback",
    "SetMonitorCallback",
    "SetMouseButtonCallback",
    "SetScrollCallback",
    "SetTime",
    "SetWindowAspectRatio",
    "SetWindowAttrib",
    "SetWindowCloseCallback",
    "SetWindowContentScaleCallback",
    "SetWindowFocusCallback",
    "SetWindowIcon",
    "SetWindowIconifyCallback",
    "SetWindowMaximizeCallback",
    "SetWindowMonitor",
    "SetWindowPos",
    "SetWindowPosCallback",
    "SetWindowRefreshCallback",
    "SetWindowShouldClose",
    "SetWindowSize",
    "SetWindowSizeCallback",
    "SetWindowSizeLimits",
    "SetWindowTitle",
    "ShowWindow",
    "SwapBuffers",
    "SwapInterval",
    "TRANSPARENT_FRAMEBUFFER",
    "Terminate",
    "UpdateGamepadMappings",
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_REVISION",
    "VERSION_UNAVAILABLE",
    "VISIBLE",
    "VRESIZE_CURSOR",
    "Vidmode",
    "VulkanSupported",
    "WaitEvents",
    "WaitEventsTimeout",
    "Window",
    "WindowHint",
    "WindowHintString",
    "WindowShouldClose",
    "X11_CLASS_NAME",
    "X11_INSTANCE_NAME",
    "setWindowOpacity"
]


class Cursor():
    pass
class Gamepadstate():
    @property
    def axes(self) -> ListWrapperF:
        """
        :type: ListWrapperF
        """
    @property
    def buttons(self) -> ListWrapperUC:
        """
        :type: ListWrapperUC
        """
    pass
class Gammaramp():
    @property
    def blue(self) -> ListWrapperUS:
        """
        :type: ListWrapperUS
        """
    @property
    def greeen(self) -> ListWrapperUS:
        """
        :type: ListWrapperUS
        """
    @property
    def red(self) -> ListWrapperUS:
        """
        :type: ListWrapperUS
        """
    pass
class Image():
    @property
    def height(self) -> int:
        """
        :type: int
        """
    @property
    def pixels(self) -> ListWrapperUC:
        """
        :type: ListWrapperUC
        """
    @property
    def width(self) -> int:
        """
        :type: int
        """
    pass
class ListWrapperF():
    def __getitem__(self, arg0: int) -> float: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperMonitor():
    def __getitem__(self, arg0: int) -> Monitor: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperStr():
    def __getitem__(self, arg0: int) -> str: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperUC():
    def __getitem__(self, arg0: int) -> int: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperUS():
    def __getitem__(self, arg0: int) -> int: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperVidmode():
    def __getitem__(self, arg0: int) -> Vidmode: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class Monitor():
    pass
class Vidmode():
    @property
    def blueBits(self) -> int:
        """
        :type: int
        """
    @property
    def greenBits(self) -> int:
        """
        :type: int
        """
    @property
    def height(self) -> int:
        """
        :type: int
        """
    @property
    def redBits(self) -> int:
        """
        :type: int
        """
    @property
    def refreshRate(self) -> int:
        """
        :type: int
        """
    @property
    def width(self) -> int:
        """
        :type: int
        """
    pass
class Window():
    pass
def CreateCursor(image: Image, xhot: int, yhot: int) -> Cursor:
    pass
def CreateStandardCursor(shape: int) -> Cursor:
    pass
def CreateWindow(width: int, height: int, title: str, monitor: typing.Optional[Monitor] = None, share: typing.Optional[Window] = None) -> Window:
    pass
def DefaultWindowHints() -> None:
    pass
def DestroyCursor(cursor: Cursor) -> None:
    pass
def DestroyWindow(window: Window) -> None:
    pass
def ExtensionSupported(extension: str) -> int:
    pass
def FocusWindow(window: Window) -> None:
    pass
def GetClipboardString(window: Window) -> str:
    pass
def GetCurrentContext() -> Window:
    pass
def GetCursorPos(window: Window) -> tuple:
    pass
def GetError() -> tuple:
    pass
def GetFramebufferSize(window: Window) -> tuple:
    pass
def GetGamepadName(jid: int) -> str:
    pass
def GetGamepadState(state: int) -> str:
    """
    jid_a
    """
def GetGammaRamp(monitor: Monitor) -> Gammaramp:
    pass
def GetInputMode(window: Window, mode: int) -> int:
    pass
def GetJoyStickGUID(jid: int) -> str:
    pass
def GetJoystickAxes(jid: int) -> ListWrapperF:
    pass
def GetJoystickButtons(jid: int) -> ListWrapperUC:
    pass
def GetJoystickHats(jid: int) -> ListWrapperUC:
    pass
def GetJoystickname(jid: int) -> str:
    pass
def GetKey(window: Window, key: int) -> int:
    pass
def GetKeyName(key: int, scancode: int) -> str:
    pass
def GetKeyScancode(key: int) -> int:
    pass
def GetMonitorContentScale(monitor: Monitor) -> tuple:
    pass
def GetMonitorName(monitor: Monitor) -> str:
    pass
def GetMonitorPhysicalSize(monitor: Monitor) -> tuple:
    pass
def GetMonitorPos(monitor: Monitor) -> tuple:
    pass
def GetMonitorWorkarea(monitor: Monitor) -> tuple:
    pass
def GetMonitors() -> ListWrapperMonitor:
    pass
def GetMouseButton(window: Window, button: int) -> int:
    pass
def GetPrimaryMonitor() -> Monitor:
    pass
def GetTime() -> float:
    pass
def GetTimerFrequency() -> int:
    pass
def GetTimerValue() -> int:
    pass
def GetVersion() -> None:
    pass
def GetVersionString() -> str:
    pass
def GetVideoMode(monitor: Monitor) -> Vidmode:
    pass
def GetVideoModes(monitor: Monitor) -> ListWrapperVidmode:
    pass
def GetWindowAttrib(window: Window, attrib: int) -> int:
    pass
def GetWindowContentScale(window: Window) -> tuple:
    pass
def GetWindowFrameSize(window: Window) -> tuple:
    pass
def GetWindowMonitor(window: Window) -> Monitor:
    pass
def GetWindowOpacity(window: Window) -> float:
    pass
def GetWindowPos(window: Window) -> tuple:
    pass
def GetWindowSize(window: Window) -> tuple:
    pass
def HideWindow(window: Window) -> None:
    pass
def IconifyWindow(window: Window) -> None:
    pass
def Init() -> int:
    pass
def InitHint(hint: int, value: int) -> None:
    pass
def JoystickIsGamepad(jid: int) -> bool:
    pass
def JoystickPresent(jid: int) -> bool:
    pass
def MakeContextCurrent(window: Window) -> None:
    pass
def MaximizeWindow(window: Window) -> None:
    pass
def PollEvents() -> None:
    pass
def PostEmptyEvent() -> None:
    pass
def RawMouseMotionSupported() -> bool:
    pass
def RequestWindowAttention(window: Window) -> None:
    pass
def RestoreWindow(window: Window) -> None:
    pass
def SetCharCallback(window: Window, callback: typing.Callable[[Window, int], None]) -> typing.Callable[[Window, int], None]:
    pass
def SetCharModsCallback(window: Window, callback: typing.Callable[[Window, int, int], None]) -> typing.Callable[[Window, int, int], None]:
    pass
def SetClipboardString(window: Window, string: str) -> None:
    pass
def SetCursor(window: Window, cursor: Cursor) -> None:
    pass
def SetCursorEnterCallback(window: Window, callback: typing.Callable[[Window, int], None]) -> typing.Callable[[Window, int], None]:
    pass
def SetCursorPos(window: Window, xpos: float, ypos: float) -> None:
    pass
def SetCursorPosCallback(window: Window, callback: typing.Callable[[Window, float, float], None]) -> typing.Callable[[Window, float, float], None]:
    pass
def SetDropCallback(window: Window, callback: typing.Callable[[Window, ListWrapperStr], None]) -> typing.Callable[[Window, ListWrapperStr], None]:
    pass
def SetErrorCallback(callback: typing.Callable[[int, str], None]) -> typing.Callable[[int, str], None]:
    pass
def SetFramebufferSizeCallback(window: Window, callback: typing.Callable[[Window, int, int], None]) -> typing.Callable[[Window, int, int], None]:
    pass
def SetGamma(monitor: Monitor, gamma: float) -> None:
    pass
def SetGammaRamp(monitor: Monitor, ramp: Gammaramp) -> None:
    pass
def SetInputMode(window: Window, mode: int, value: int) -> None:
    pass
def SetJoystickCallback(callback: typing.Callable[[int, int], None]) -> typing.Callable[[int, int], None]:
    pass
def SetKeyCallback(window: Window, callback: typing.Callable[[Window, int, int, int, int], None]) -> typing.Callable[[Window, int, int, int, int], None]:
    pass
def SetMonitorCallback(arg0: typing.Callable[[Monitor, int], None]) -> typing.Callable[[Monitor, int], None]:
    pass
def SetMouseButtonCallback(window: Window, callback: typing.Callable[[Window, int, int, int], None]) -> typing.Callable[[Window, int, int, int], None]:
    pass
def SetScrollCallback(window: Window, callback: typing.Callable[[Window, float, float], None]) -> typing.Callable[[Window, float, float], None]:
    pass
def SetTime(time: float) -> None:
    pass
def SetWindowAspectRatio(window: Window, numer: int, denom: int) -> None:
    pass
def SetWindowAttrib(window: Window, attrib: int, value: int) -> None:
    pass
def SetWindowCloseCallback(window: Window, callback: typing.Callable[[Window], None]) -> typing.Callable[[Window], None]:
    pass
def SetWindowContentScaleCallback(window: Window, callback: typing.Callable[[Window, float, float], None]) -> typing.Callable[[Window, float, float], None]:
    pass
def SetWindowFocusCallback(window: Window, callback: typing.Callable[[Window, int], None]) -> typing.Callable[[Window, int], None]:
    pass
def SetWindowIcon(window: Window, image: Image) -> None:
    pass
def SetWindowIconifyCallback(window: Window, callback: typing.Callable[[Window, int], None]) -> typing.Callable[[Window, int], None]:
    pass
def SetWindowMaximizeCallback(window: Window, callback: typing.Callable[[Window, int], None]) -> typing.Callable[[Window, int], None]:
    pass
def SetWindowMonitor(window: Window, monitor: Monitor, xpos: int, ypos: int, width: int, height: int, refreshRate: int) -> None:
    pass
def SetWindowPos(window: Window, xpos: int, ypos: int) -> None:
    pass
def SetWindowPosCallback(window: Window, callback: typing.Callable[[Window, int, int], None]) -> typing.Callable[[Window, int, int], None]:
    pass
def SetWindowRefreshCallback(window: Window, callback: typing.Callable[[Window], None]) -> typing.Callable[[Window], None]:
    pass
def SetWindowShouldClose(window: Window, value: int) -> None:
    pass
def SetWindowSize(window: Window, width: int, height: int) -> None:
    pass
def SetWindowSizeCallback(window: Window, callback: typing.Callable[[Window, int, int], None]) -> typing.Callable[[Window, int, int], None]:
    pass
def SetWindowSizeLimits(window: Window, minWidth: int, minHeight: int, maxWidth: int, maxHeight: int) -> None:
    pass
def SetWindowTitle(window: Window, title: str) -> None:
    pass
def ShowWindow(window: Window) -> None:
    pass
def SwapBuffers(window: Window) -> None:
    pass
def SwapInterval(interval: int) -> None:
    pass
def Terminate() -> None:
    pass
def UpdateGamepadMappings(string: str) -> int:
    pass
def VulkanSupported() -> int:
    pass
def WaitEvents() -> None:
    pass
def WaitEventsTimeout(timeout: float) -> None:
    pass
def WindowHint(hint: int, value: int) -> None:
    pass
def WindowHintString(hint: int, value: str) -> None:
    pass
def WindowShouldClose(window: Window) -> bool:
    pass
def setWindowOpacity(window: Window, opacity: float) -> None:
    pass
ACCUM_ALPHA_BITS = 135178
ACCUM_BLUE_BITS = 135177
ACCUM_GREEN_BITS = 135176
ACCUM_RED_BITS = 135175
ALPHA_BITS = 135172
ANY_RELEASE_BEHAVIOR = 0
API_UNAVAILABLE = 65542
ARROW_CURSOR = 221185
AUTO_ICONIFY = 131078
AUX_BUFFERS = 135179
BLUE_BITS = 135171
CENTER_CURSOR = 131081
CLIENT_API = 139265
COCOA_CHDIR_RESOURCES = 331777
COCOA_FRAME_NAME = 143362
COCOA_GRAPHICS_SWITCHING = 143363
COCOA_MENUBAR = 331778
COCOA_RETINA_FRAMEBUFFER = 143361
CONNECTED = 262145
CONTEXT_CREATION_API = 139275
CONTEXT_NO_ERROR = 139274
CONTEXT_RELEASE_BEHAVIOR = 139273
CONTEXT_REVISION = 139268
CONTEXT_ROBUSTNESS = 139269
CONTEXT_VERSION_MAJOR = 139266
CONTEXT_VERSION_MINOR = 139267
CROSSHAIR_CURSOR = 221187
CURSOR = 208897
CURSOR_DISABLED = 212995
CURSOR_HIDDEN = 212994
CURSOR_NORMAL = 212993
DECORATED = 131077
DEPTH_BITS = 135173
DISCONNECTED = 262146
DONT_CARE = -1
DOUBLEBUFFER = 135184
EGL_CONTEXT_API = 221186
FLOATING = 131079
FOCUSED = 131073
FOCUS_ON_SHOW = 131084
FORMAT_UNAVAILABLE = 65545
GAMEPAD_AXIS_LEFT_TRIGGER = 4
GAMEPAD_AXIS_LEFT_X = 0
GAMEPAD_AXIS_LEFT_Y = 1
GAMEPAD_AXIS_RIGHT_TRIGGER = 5
GAMEPAD_AXIS_RIGHT_X = 2
GAMEPAD_AXIS_RIGHT_Y = 3
GAMEPAD_BUTTON_A = 0
GAMEPAD_BUTTON_B = 1
GAMEPAD_BUTTON_BACK = 6
GAMEPAD_BUTTON_CIRCLE = 1
GAMEPAD_BUTTON_CROSS = 0
GAMEPAD_BUTTON_DPAD_DOWN = 13
GAMEPAD_BUTTON_DPAD_LEFT = 14
GAMEPAD_BUTTON_DPAD_RIGHT = 12
GAMEPAD_BUTTON_DPAD_UP = 11
GAMEPAD_BUTTON_GUIDE = 8
GAMEPAD_BUTTON_LEFT_BUMPER = 4
GAMEPAD_BUTTON_LEFT_THUMB = 9
GAMEPAD_BUTTON_RIGHT_BUMPER = 5
GAMEPAD_BUTTON_RIGHT_THUMB = 10
GAMEPAD_BUTTON_SQUARE = 2
GAMEPAD_BUTTON_START = 7
GAMEPAD_BUTTON_TRIANGLE = 3
GAMEPAD_BUTTON_X = 2
GAMEPAD_BUTTON_Y = 3
GREEN_BITS = 135170
HAND_CURSOR = 221188
HAT_CENTERED = 0
HAT_DOWN = 4
HAT_LEFT = 8
HAT_LEFT_DOWN = 12
HAT_LEFT_UP = 9
HAT_RIGHT = 2
HAT_RIGHT_DOWN = 6
HAT_RIGHT_UP = 3
HAT_UP = 1
HOVERED = 131083
HRESIZE_CURSOR = 221189
IBEAM_CURSOR = 221186
ICONIFIED = 131074
INVALID_ENUM = 65539
INVALID_VALUE = 65540
JOYSTICK_1 = 0
JOYSTICK_10 = 9
JOYSTICK_11 = 10
JOYSTICK_12 = 11
JOYSTICK_13 = 12
JOYSTICK_14 = 13
JOYSTICK_15 = 14
JOYSTICK_16 = 15
JOYSTICK_2 = 1
JOYSTICK_3 = 2
JOYSTICK_4 = 3
JOYSTICK_5 = 4
JOYSTICK_6 = 5
JOYSTICK_7 = 6
JOYSTICK_8 = 7
JOYSTICK_9 = 8
JOYSTICK_HAT_BUTTONS = 327681
KEY_0 = 48
KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_4 = 52
KEY_5 = 53
KEY_6 = 54
KEY_7 = 55
KEY_8 = 56
KEY_9 = 57
KEY_A = 65
KEY_APOSTROPHE = 39
KEY_B = 66
KEY_BACKSLASH = 92
KEY_BACKSPACE = 259
KEY_C = 67
KEY_CAPS_LOCK = 280
KEY_COMMA = 44
KEY_D = 68
KEY_DELETE = 261
KEY_DOWN = 264
KEY_E = 69
KEY_END = 269
KEY_ENTER = 257
KEY_EQUAL = 61
KEY_ESCAPE = 256
KEY_F = 70
KEY_F1 = 290
KEY_F10 = 299
KEY_F11 = 300
KEY_F12 = 301
KEY_F13 = 302
KEY_F14 = 303
KEY_F15 = 304
KEY_F16 = 305
KEY_F17 = 306
KEY_F18 = 307
KEY_F19 = 308
KEY_F2 = 291
KEY_F20 = 309
KEY_F21 = 310
KEY_F22 = 311
KEY_F23 = 312
KEY_F24 = 313
KEY_F25 = 314
KEY_F3 = 292
KEY_F4 = 293
KEY_F5 = 294
KEY_F6 = 295
KEY_F7 = 296
KEY_F8 = 297
KEY_F9 = 298
KEY_G = 71
KEY_GRAVE_ACCENT = 96
KEY_H = 72
KEY_HOME = 268
KEY_I = 73
KEY_INSERT = 260
KEY_J = 74
KEY_K = 75
KEY_KP_0 = 320
KEY_KP_1 = 321
KEY_KP_2 = 322
KEY_KP_3 = 323
KEY_KP_4 = 324
KEY_KP_5 = 325
KEY_KP_6 = 326
KEY_KP_7 = 327
KEY_KP_8 = 328
KEY_KP_9 = 329
KEY_KP_ADD = 334
KEY_KP_DECIMAL = 330
KEY_KP_DIVIDE = 331
KEY_KP_ENTER = 335
KEY_KP_EQUAL = 336
KEY_KP_MULTIPLY = 332
KEY_KP_SUBTRACT = 333
KEY_L = 76
KEY_LEFT = 263
KEY_LEFT_ALT = 342
KEY_LEFT_BRACKET = 91
KEY_LEFT_CONTROL = 341
KEY_LEFT_SHIFT = 340
KEY_LEFT_SUPER = 343
KEY_M = 77
KEY_MENU = 348
KEY_MINUS = 45
KEY_N = 78
KEY_NUM_LOCK = 282
KEY_O = 79
KEY_P = 80
KEY_PAGE_DOWN = 267
KEY_PAGE_UP = 266
KEY_PAUSE = 284
KEY_PERIOD = 46
KEY_PRINT_SCREEN = 283
KEY_Q = 81
KEY_R = 82
KEY_RIGHT = 262
KEY_RIGHT_ALT = 346
KEY_RIGHT_BRACKET = 93
KEY_RIGHT_CONTROL = 345
KEY_RIGHT_SHIFT = 344
KEY_RIGHT_SUPER = 347
KEY_S = 83
KEY_SCROLL_LOCK = 281
KEY_SEMICOLON = 59
KEY_SLASH = 47
KEY_SPACE = 32
KEY_T = 84
KEY_TAB = 258
KEY_U = 85
KEY_UNKNOWN = -1
KEY_UP = 265
KEY_V = 86
KEY_W = 87
KEY_WORLD_1 = 161
KEY_WORLD_2 = 162
KEY_X = 88
KEY_Y = 89
KEY_Z = 90
LOCK_KEY_MODS = 208900
LOSE_CONTEXT_ON_RESET = 200706
MAXIMIZED = 131080
MOD_ALT = 4
MOD_CAPS_LOCK = 16
MOD_CONTROL = 2
MOD_NUM_LOCK = 32
MOD_SHIFT = 1
MOD_SUPER = 8
MOUSE_BUTTON_1 = 0
MOUSE_BUTTON_2 = 1
MOUSE_BUTTON_3 = 2
MOUSE_BUTTON_4 = 3
MOUSE_BUTTON_5 = 4
MOUSE_BUTTON_6 = 5
MOUSE_BUTTON_7 = 6
MOUSE_BUTTON_8 = 7
MOUSE_BUTTON_LEFT = 0
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 1
NATIVE_CONTEXT_API = 221185
NOT_INITIALIZED = 65537
NO_API = 0
NO_CURRENT_CONTEXT = 65538
NO_ERROR = 0
NO_RESET_NOTIFICATION = 200705
NO_ROBUSTNESS = 0
NO_WINDOW_CONTEXT = 65546
OPENGL_ANY_PROFILE = 0
OPENGL_API = 196609
OPENGL_COMPAT_PROFILE = 204802
OPENGL_CORE_PROFILE = 204801
OPENGL_DEBUG_CONTEXT = 139271
OPENGL_ES_API = 196610
OPENGL_FORWARD_COMPAT = 139270
OPENGL_PROFILE = 139272
OSMESA_CONTEXT_API = 221187
OUT_OF_MEMORY = 65541
PLATFORM_ERROR = 65544
PRESS = 1
RAW_MOUSE_MOTION = 208901
RED_BITS = 135169
REFRESH_RATE = 135183
RELEASE = 0
RELEASE_BEHAVIOR_FLUSH = 217089
RELEASE_BEHAVIOR_NONE = 217090
REPEAT = 2
RESIZABLE = 131075
SAMPLES = 135181
SCALE_TO_MONITOR = 139276
SRGB_CAPABLE = 135182
STENCIL_BITS = 135174
STEREO = 135180
STICKY_KEYS = 208898
STICKY_MOUSE_BUTTONS = 208899
TRANSPARENT_FRAMEBUFFER = 131082
VERSION_MAJOR = 3
VERSION_MINOR = 4
VERSION_REVISION = 0
VERSION_UNAVAILABLE = 65543
VISIBLE = 131076
VRESIZE_CURSOR = 221190
X11_CLASS_NAME = 147457
X11_INSTANCE_NAME = 147458
