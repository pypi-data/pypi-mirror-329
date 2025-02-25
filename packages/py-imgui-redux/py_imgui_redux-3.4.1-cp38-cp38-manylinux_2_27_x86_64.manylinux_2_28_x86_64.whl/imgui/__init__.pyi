"""DearImGui Framework"""
from __future__ import annotations
import imgui
import typing

__all__ = [
    "AcceptDragDropPayload",
    "AlignTextToFramePadding",
    "ArrowButton",
    "BackendFlags",
    "Begin",
    "BeginChild",
    "BeginCombo",
    "BeginDisabled",
    "BeginDragDropSource",
    "BeginDragDropTarget",
    "BeginGroup",
    "BeginItemTooltip",
    "BeginListBox",
    "BeginMainMenuBar",
    "BeginMenu",
    "BeginMenuBar",
    "BeginPopup",
    "BeginPopupContextItem",
    "BeginPopupContextVoid",
    "BeginPopupContextWindow",
    "BeginPopupModal",
    "BeginTabBar",
    "BeginTabItem",
    "BeginTable",
    "BeginTooltip",
    "BoolRef",
    "Bullet",
    "BulletText",
    "Button",
    "ButtonFlags",
    "CalcItemWidth",
    "CalcTextSize",
    "CheckBox",
    "CheckBoxFlags",
    "ChildFlags",
    "CloseCurrentPopup",
    "Col",
    "CollapsingHeader",
    "Color",
    "ColorButton",
    "ColorConvertFloat4ToU32",
    "ColorConvertHSVtoRGB",
    "ColorConvertRGBtoHSV",
    "ColorConvertU32ToFloat4",
    "ColorEdit3",
    "ColorEdit4",
    "ColorEditFlags",
    "ColorPicker3",
    "ColorPicker4",
    "ComboFlags",
    "Cond",
    "ConfigFlags",
    "Context",
    "CreateContext",
    "DebugFlashStyleColor",
    "DebugStartItemPicker",
    "DebugTextEncoding",
    "DestroyContext",
    "Dir",
    "DoubleList",
    "DoubleRef",
    "DragDropFlags",
    "DragFloat",
    "DragFloat2",
    "DragFloat3",
    "DragFloat4",
    "DragFloatRange2",
    "DragInt",
    "DragInt2",
    "DragInt3",
    "DragInt4",
    "DragIntRange2",
    "DrawFlags",
    "DrawListFlags",
    "Dummy",
    "End",
    "EndChild",
    "EndCombo",
    "EndDisabled",
    "EndDragDropSource",
    "EndDragDropTarget",
    "EndFrame",
    "EndGroup",
    "EndListBox",
    "EndMainMenuBar",
    "EndMenu",
    "EndMenuBar",
    "EndPopup",
    "EndTabBar",
    "EndTabItem",
    "EndTable",
    "EndTooltip",
    "FLT_MAX",
    "FloatList",
    "FloatRef",
    "FocusedFlags",
    "GetBackgroundDrawList",
    "GetClipboardText",
    "GetColorU32",
    "GetContentRegionAvail",
    "GetCurrentContext",
    "GetCursorPos",
    "GetCursorPosX",
    "GetCursorPosY",
    "GetCursorScreenPos",
    "GetCursorStartPos",
    "GetDragDropPayload",
    "GetDrawData",
    "GetDrawListSharedData",
    "GetFont",
    "GetFontSize",
    "GetFontTexUvWhitePixel",
    "GetForegroundDrawList",
    "GetFrameCount",
    "GetFrameHeight",
    "GetFrameHeightWithSpacing",
    "GetID",
    "GetIO",
    "GetItemID",
    "GetItemRectMax",
    "GetItemRectMin",
    "GetItemRectSize",
    "GetKeyName",
    "GetKeyPressedAmount",
    "GetMainViewport",
    "GetMouseCursor",
    "GetMouseDragDelta",
    "GetMousePos",
    "GetMousePosOnOpeningCurrentPopup",
    "GetScrollMaxX",
    "GetScrollMaxY",
    "GetScrollX",
    "GetScrollY",
    "GetStateStorage",
    "GetStyle",
    "GetStyleColorName",
    "GetStyleColorVec4",
    "GetTextLineHeight",
    "GetTextLineHeightWithSpacing",
    "GetTime",
    "GetTreeNodeToLabelSpacing",
    "GetVersion",
    "GetWindowDrawList",
    "GetWindowHeight",
    "GetWindowPos",
    "GetWindowSize",
    "GetWindowWidth",
    "HoveredFlags",
    "IO",
    "ImDrawList",
    "ImFont",
    "ImFontAtlas",
    "ImFontConfig",
    "ImFontGlyph",
    "ImKey",
    "Image",
    "ImageButton",
    "Indent",
    "InitContextForGLFW",
    "InputFlags",
    "InputFloat",
    "InputFloat2",
    "InputFloat3",
    "InputFloat4",
    "InputInt",
    "InputInt2",
    "InputInt3",
    "InputInt4",
    "InputText",
    "InputTextFlags",
    "InputTextMultiline",
    "InputTextWithHint",
    "IntList",
    "IntRef",
    "InvisibleButton",
    "IsAnyItemActive",
    "IsAnyItemFocused",
    "IsAnyItemHovered",
    "IsItemActivated",
    "IsItemActive",
    "IsItemClicked",
    "IsItemDeactivated",
    "IsItemDeactivatedAfterEdit",
    "IsItemEdited",
    "IsItemFocused",
    "IsItemHovered",
    "IsItemToggledOpen",
    "IsItemVisible",
    "IsKeyChordPressed",
    "IsKeyDown",
    "IsKeyPressed",
    "IsKeyReleased",
    "IsMouseClicked",
    "IsMouseDoubleClicked",
    "IsMouseDown",
    "IsMouseDragging",
    "IsMouseHoveringRect",
    "IsMousePosValid",
    "IsMouseReleased",
    "IsMouseReleasedWithDelay",
    "IsPopupOpen",
    "IsRectVisible",
    "IsWindowAppearing",
    "IsWindowCollapsed",
    "IsWindowFocused",
    "IsWindowHovered",
    "ItemFlags",
    "KeyData",
    "LabelText",
    "ListClipper",
    "ListWrapperBool",
    "ListWrapperDouble",
    "ListWrapperImVec2",
    "ListWrapperTCSS",
    "LoadIniSettingsFromDisk",
    "LoadIniSettingsFromMemory",
    "LoadTexture",
    "LoadTextureFile",
    "LogButtons",
    "LogFinish",
    "LogText",
    "LogToClipboard",
    "LogToFile",
    "LogToTTY",
    "MenuItem",
    "MouseButton",
    "MouseCursor",
    "MouseSource",
    "MultiSelectFlags",
    "MultiSelectIO",
    "NewFrame",
    "NewLine",
    "OpenPopup",
    "OpenPopupOnItemClick",
    "PopClipRect",
    "PopFont",
    "PopID",
    "PopItemFlag",
    "PopItemWidth",
    "PopStyleColor",
    "PopStyleVar",
    "PopTextWrapPos",
    "PopupFlags",
    "ProgressBar",
    "PushClipRect",
    "PushFont",
    "PushID",
    "PushItemFlag",
    "PushItemWidth",
    "PushStyleColor",
    "PushStyleVar",
    "PushStyleVarX",
    "PushStyleVarY",
    "PushTextWrapPos",
    "RadioButton",
    "Render",
    "ResetMouseDragDelta",
    "SameLine",
    "SaveIniSettingsToDisk",
    "SaveIniSettingsToMemory",
    "Selectable",
    "SelectableFlags",
    "SelectionRequest",
    "SelectionRequestType",
    "Separator",
    "SeparatorText",
    "SetClipboardText",
    "SetColorEditOptions",
    "SetCurrentContext",
    "SetCursorPos",
    "SetCursorPosX",
    "SetCursorPosY",
    "SetCursorScreenPos",
    "SetDragDropPayload",
    "SetItemDefaultFocus",
    "SetItemKeyOwner",
    "SetItemTooltip",
    "SetKeyboardFocusHere",
    "SetMouseCursor",
    "SetNextFrameWantCaptureKeyboard",
    "SetNextFrameWantCaptureMouse",
    "SetNextItemAllowOverlap",
    "SetNextItemOpen",
    "SetNextItemShortcut",
    "SetNextItemStorageID",
    "SetNextItemWidth",
    "SetNextWindowBgAlpha",
    "SetNextWindowCollapsed",
    "SetNextWindowContentSize",
    "SetNextWindowFocus",
    "SetNextWindowPos",
    "SetNextWindowScroll",
    "SetNextWindowSize",
    "SetScrollFromPosX",
    "SetScrollFromPosY",
    "SetScrollHereX",
    "SetScrollHereY",
    "SetScrollX",
    "SetScrollY",
    "SetStateStorage",
    "SetTabItemClosed",
    "SetTooltip",
    "SetWindowCollapsed",
    "SetWindowFocus",
    "SetWindowPos",
    "SetWindowSize",
    "Shortcut",
    "ShowAboutWindow",
    "ShowDebugLogWindow",
    "ShowDemoWindow",
    "ShowFontSelector",
    "ShowMetricsWindow",
    "ShowStackToolWindow",
    "ShowStyleEditor",
    "ShowStyleSelector",
    "ShowUserGuide",
    "Shutdown",
    "SliderAngle",
    "SliderFlags",
    "SliderFloat",
    "SliderFloat2",
    "SliderFloat3",
    "SliderFloat4",
    "SliderInt",
    "SliderInt2",
    "SliderInt3",
    "SliderInt4",
    "SmallButton",
    "SortDirection",
    "Spacing",
    "StrList",
    "StrRef",
    "Style",
    "StyleColorsClassic",
    "StyleColorsDark",
    "StyleColorsLight",
    "StyleVar",
    "TabBarFlags",
    "TabItemButton",
    "TabItemFlags",
    "TableBgTarget",
    "TableColumnFlags",
    "TableColumnSortSpecs",
    "TableFlags",
    "TableGetColumnCount",
    "TableGetColumnFlags",
    "TableGetColumnIndex",
    "TableGetColumnName",
    "TableGetHoveredColumn",
    "TableGetRowIndex",
    "TableGetSortSpecs",
    "TableHeader",
    "TableHeadersRow",
    "TableNextColumn",
    "TableNextRow",
    "TableRowFlags",
    "TableSetBgColor",
    "TableSetColumnEnabled",
    "TableSetColumnIndex",
    "TableSetupColumn",
    "TableSetupScrollFreeze",
    "TableSortSpecs",
    "Text",
    "TextColored",
    "TextDisabled",
    "TextLink",
    "TextLinkOpenURL",
    "TextWrapped",
    "Texture",
    "TreeNode",
    "TreeNodeEx",
    "TreeNodeFlags",
    "TreePop",
    "TreePush",
    "Unindent",
    "UnloadTexture",
    "VSliderFloat",
    "VSliderInt",
    "Vec2",
    "Vec2List",
    "Vec4",
    "Viewport",
    "ViewportFlags",
    "WCharList",
    "WindowFlags",
    "glfw",
    "imnodes",
    "implot"
]


class BackendFlags():
    HasGamepad = 1
    HasMouseCursors = 2
    HasSetMousePos = 4
    None_ = 0
    RendererHasVtxOffset = 8
    pass
class BoolRef():
    """
    A pass-by-ref wrapper for a bool
    """
    def __init__(self, val: bool = False) -> None: ...
    def __str__(self) -> str: ...
    @property
    def val(self) -> bool:
        """
        The wrapped value

        :type: bool
        """
    @val.setter
    def val(self, arg0: bool) -> None:
        """
        The wrapped value
        """
    pass
class ButtonFlags():
    EnableNav = 8
    MouseButtonLeft = 1
    MouseButtonMask_ = 7
    MouseButtonMiddle = 4
    MouseButtonRight = 2
    None_ = 0
    pass
class ChildFlags():
    AlwaysAutoResize = 64
    AlwaysUseWindowPadding = 2
    AutoResizeX = 16
    AutoResizeY = 32
    Borders = 1
    FrameStyle = 128
    NavFlattened = 256
    None_ = 0
    ResizeX = 4
    ResizeY = 8
    pass
class Col():
    Border = 5
    BorderShadow = 6
    Button = 21
    ButtonActive = 23
    ButtonHovered = 22
    CheckMark = 18
    ChildBg = 3
    DragDropTarget = 51
    FrameBg = 7
    FrameBgActive = 9
    FrameBgHovered = 8
    Header = 24
    HeaderActive = 26
    HeaderHovered = 25
    MenuBarBg = 13
    ModalWindowDimBg = 55
    NavCursor = 52
    NavWindowingDimBg = 54
    NavWindowingHighlight = 53
    PlotHistogram = 42
    PlotHistogramHovered = 43
    PlotLines = 40
    PlotLinesHovered = 41
    PopupBg = 4
    ResizeGrip = 30
    ResizeGripActive = 32
    ResizeGripHovered = 31
    ScrollbarBg = 14
    ScrollbarGrab = 15
    ScrollbarGrabActive = 17
    ScrollbarGrabHovered = 16
    Separator = 27
    SeparatorActive = 29
    SeparatorHovered = 28
    SliderGrab = 19
    SliderGrabActive = 20
    Tab = 34
    TabDimmed = 37
    TabDimmedSelected = 38
    TabDimmedSelectedOverline = 39
    TabHovered = 33
    TabSelected = 35
    TabSelectedOverline = 36
    TableBorderLight = 46
    TableBorderStrong = 45
    TableHeaderBg = 44
    TableRowBg = 47
    TableRowBgAlt = 48
    Text = 0
    TextDisabled = 1
    TextLink = 49
    TextSelectedBg = 50
    TitleBg = 10
    TitleBgActive = 11
    TitleBgCollapsed = 12
    WindowBg = 2
    pass
class Color():
    @staticmethod
    def HSV(h: float, s: float, v: float, a: float = 1.0) -> Color: ...
    def SetHSV(self, h: float, s: float, v: float, a: float = 1.0) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, r: float, g: float, b: float, a: float = 1.0) -> None: ...
    @typing.overload
    def __init__(self, r: int, g: int, b: int, a: int = 255) -> None: ...
    @property
    def Value(self) -> Vec4:
        """
        :type: Vec4
        """
    @Value.setter
    def Value(self, arg0: Vec4) -> None:
        pass
    pass
class ColorEditFlags():
    AlphaBar = 65536
    AlphaNoBg = 4096
    AlphaOpaque = 2048
    AlphaPreviewHalf = 8192
    DefaultOptions_ = 177209344
    DisplayHSV = 2097152
    DisplayHex = 4194304
    DisplayRGB = 1048576
    Float = 16777216
    HDR = 524288
    InputHSV = 268435456
    InputRGB = 134217728
    NoAlpha = 2
    NoBorder = 1024
    NoDragDrop = 512
    NoInputs = 32
    NoLabel = 128
    NoOptions = 8
    NoPicker = 4
    NoSidePreview = 256
    NoSmallPreview = 16
    NoTooltip = 64
    None_ = 0
    PickerHueBar = 33554432
    PickerHueWheel = 67108864
    Uint8 = 8388608
    pass
class ComboFlags():
    HeightLarge = 8
    HeightLargest = 16
    HeightMask_ = 30
    HeightRegular = 4
    HeightSmall = 2
    NoArrowButton = 32
    NoPreview = 64
    None_ = 0
    PopupAlignLeft = 1
    WidthFitPreview = 128
    pass
class Cond():
    Always = 1
    Appearing = 8
    FirstUseEver = 4
    None_ = 0
    Once = 2
    pass
class ConfigFlags():
    IsSRGB = 1048576
    IsTouchScreen = 2097152
    NavEnableGamepad = 2
    NavEnableKeyboard = 1
    NoMouse = 16
    NoMouseCursorChange = 32
    None_ = 0
    pass
class Context():
    pass
class Dir():
    Down = 3
    Left = 0
    None_ = -1
    Right = 1
    Up = 2
    pass
class DoubleList():
    """
    Thin wrapper over a std::vector<double>
    """
    def __getitem__(self, index: int) -> float: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, vals: list[float] = []) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, index: int, val: float) -> None: ...
    def append(self, val: float) -> None: 
        """
        Append a value to the end
        """
    def clear(self) -> None: ...
    def pop(self) -> float: 
        """
        Pop a value from the end
        """
    def resize(self, size: int) -> None: 
        """
        Resize the vector, dropping any lost values
        """
    pass
class DoubleRef():
    """
    A pass-by-ref wrapper for a double
    """
    def __init__(self, val: float = 0.0) -> None: ...
    def __str__(self) -> str: ...
    @property
    def val(self) -> float:
        """
        The wrapped value

        :type: float
        """
    @val.setter
    def val(self, arg0: float) -> None:
        """
        The wrapped value
        """
    pass
class DragDropFlags():
    AcceptBeforeDelivery = 1024
    AcceptNoDrawDefaultRect = 2048
    AcceptNoPreviewTooltip = 4096
    AcceptPeekOnly = 3072
    None_ = 0
    PayloadAutoExpire = 32
    PayloadNoCrossContext = 64
    PayloadNoCrossProcess = 128
    SourceAllowNullID = 8
    SourceExtern = 16
    SourceNoDisableHover = 2
    SourceNoHoldToOpenOthers = 4
    SourceNoPreviewTooltip = 1
    pass
class DrawFlags():
    Closed = 1
    None_ = 0
    RoundCornersAll = 240
    RoundCornersBottom = 192
    RoundCornersBottomLeft = 64
    RoundCornersBottomRight = 128
    RoundCornersDefault_ = 240
    RoundCornersLeft = 80
    RoundCornersMask_ = 496
    RoundCornersNone = 256
    RoundCornersRight = 160
    RoundCornersTop = 48
    RoundCornersTopLeft = 16
    RoundCornersTopRight = 32
    pass
class DrawListFlags():
    AllowVtxOffset = 8
    AntiAliasedFill = 4
    AntiAliasedLines = 1
    AntiAliasedLinesUseTex = 2
    None_ = 0
    pass
class FloatList():
    """
    Thin wrapper over a std::vector<float>
    """
    def __getitem__(self, index: int) -> float: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, vals: list[float] = []) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, index: int, val: float) -> None: ...
    def append(self, val: float) -> None: 
        """
        Append a value to the end
        """
    def clear(self) -> None: ...
    def pop(self) -> float: 
        """
        Pop a value from the end
        """
    def resize(self, size: int) -> None: 
        """
        Resize the vector, dropping any lost values
        """
    pass
class FloatRef():
    """
    A pass-by-ref wrapper for a float
    """
    def __init__(self, val: float = 0.0) -> None: ...
    def __str__(self) -> str: ...
    @property
    def val(self) -> float:
        """
        The wrapped value

        :type: float
        """
    @val.setter
    def val(self, arg0: float) -> None:
        """
        The wrapped value
        """
    pass
class FocusedFlags():
    AnyWindow = 4
    ChildWindows = 1
    NoPopupHierarchy = 8
    None_ = 0
    RootAndChildWindows = 3
    RootWindow = 2
    pass
class HoveredFlags():
    AllowWhenBlockedByActiveItem = 128
    AllowWhenBlockedByPopup = 32
    AllowWhenDisabled = 1024
    AllowWhenOverlapped = 768
    AllowWhenOverlappedByItem = 256
    AllowWhenOverlappedByWindow = 512
    AnyWindow = 4
    ChildWindows = 1
    DelayNone = 16384
    DelayNormal = 65536
    DelayShort = 32768
    ForTooltip = 4096
    NoNavOverride = 2048
    NoPopupHierarchy = 8
    NoSharedDelay = 131072
    None_ = 0
    RectOnly = 928
    RootAndChildWindows = 3
    RootWindow = 2
    Stationary = 8192
    pass
class IO():
    def AddFocusEvent(self, focused: bool) -> None: ...
    def AddInputCharacter(self, c: int) -> None: ...
    def AddInputCharacterUTF16(self, c: int) -> None: ...
    def AddInputCharactersUTF8(self, str: str) -> None: ...
    def AddKeyAnalogEvent(self, key: ImGuiKey, down: bool, v: float) -> None: ...
    def AddKeyEvent(self, key: ImGuiKey, down: bool) -> None: ...
    def AddMouseButtonEvent(self, button: int, down: bool) -> None: ...
    def AddMousePosEvent(self, x: float, y: float) -> None: ...
    def AddMouseSourceEvent(self, source: ImGuiMouseSource) -> None: ...
    def AddMouseWheelEvent(self, wh_x: float, wh_y: float) -> None: ...
    def ClearEventsQueue(self) -> None: ...
    def ClearInputKeys(self) -> None: ...
    def ClearInputMouse(self) -> None: ...
    def SetAppAcceptingEvents(self, accepting_events: bool) -> None: ...
    def SetKeyEventNativeData(self, key: ImGuiKey, native_keycode: int, native_scancode: int, native_legacy_index: int = -1) -> None: ...
    def __init__(self) -> None: ...
    @property
    def AppAcceptingEvents(self) -> bool:
        """
        :type: bool
        """
    @AppAcceptingEvents.setter
    def AppAcceptingEvents(self, arg0: bool) -> None:
        pass
    @property
    def AppFocusLost(self) -> bool:
        """
        :type: bool
        """
    @AppFocusLost.setter
    def AppFocusLost(self, arg0: bool) -> None:
        pass
    @property
    def BackendFlags(self) -> int:
        """
        :type: int
        """
    @BackendFlags.setter
    def BackendFlags(self, arg0: int) -> None:
        pass
    @property
    def BackendLanguageUserData(self) -> capsule:
        """
        :type: capsule
        """
    @BackendLanguageUserData.setter
    def BackendLanguageUserData(self, arg0: capsule) -> None:
        pass
    @property
    def BackendPlatformName(self) -> str:
        """
        :type: str
        """
    @BackendPlatformName.setter
    def BackendPlatformName(self, arg0: str) -> None:
        pass
    @property
    def BackendPlatformUserData(self) -> capsule:
        """
        :type: capsule
        """
    @BackendPlatformUserData.setter
    def BackendPlatformUserData(self, arg0: capsule) -> None:
        pass
    @property
    def BackendRendererName(self) -> str:
        """
        :type: str
        """
    @BackendRendererName.setter
    def BackendRendererName(self, arg0: str) -> None:
        pass
    @property
    def BackendRendererUserData(self) -> capsule:
        """
        :type: capsule
        """
    @BackendRendererUserData.setter
    def BackendRendererUserData(self, arg0: capsule) -> None:
        pass
    @property
    def ConfigDebugBeginReturnValueLoop(self) -> bool:
        """
        :type: bool
        """
    @ConfigDebugBeginReturnValueLoop.setter
    def ConfigDebugBeginReturnValueLoop(self, arg0: bool) -> None:
        pass
    @property
    def ConfigDebugBeginReturnValueOnce(self) -> bool:
        """
        :type: bool
        """
    @ConfigDebugBeginReturnValueOnce.setter
    def ConfigDebugBeginReturnValueOnce(self, arg0: bool) -> None:
        pass
    @property
    def ConfigDebugHighlightIdConflicts(self) -> bool:
        """
        :type: bool
        """
    @ConfigDebugHighlightIdConflicts.setter
    def ConfigDebugHighlightIdConflicts(self, arg0: bool) -> None:
        pass
    @property
    def ConfigDebugIgnoreFocusLoss(self) -> bool:
        """
        :type: bool
        """
    @ConfigDebugIgnoreFocusLoss.setter
    def ConfigDebugIgnoreFocusLoss(self, arg0: bool) -> None:
        pass
    @property
    def ConfigDebugIniSettings(self) -> bool:
        """
        :type: bool
        """
    @ConfigDebugIniSettings.setter
    def ConfigDebugIniSettings(self, arg0: bool) -> None:
        pass
    @property
    def ConfigDebugIsDebuggerPresent(self) -> bool:
        """
        :type: bool
        """
    @ConfigDebugIsDebuggerPresent.setter
    def ConfigDebugIsDebuggerPresent(self, arg0: bool) -> None:
        pass
    @property
    def ConfigDragClickToInputText(self) -> bool:
        """
        :type: bool
        """
    @ConfigDragClickToInputText.setter
    def ConfigDragClickToInputText(self, arg0: bool) -> None:
        pass
    @property
    def ConfigErrorRecovery(self) -> bool:
        """
        :type: bool
        """
    @ConfigErrorRecovery.setter
    def ConfigErrorRecovery(self, arg0: bool) -> None:
        pass
    @property
    def ConfigErrorRecoveryEnableAssert(self) -> bool:
        """
        :type: bool
        """
    @ConfigErrorRecoveryEnableAssert.setter
    def ConfigErrorRecoveryEnableAssert(self, arg0: bool) -> None:
        pass
    @property
    def ConfigErrorRecoveryEnableDebugLog(self) -> bool:
        """
        :type: bool
        """
    @ConfigErrorRecoveryEnableDebugLog.setter
    def ConfigErrorRecoveryEnableDebugLog(self, arg0: bool) -> None:
        pass
    @property
    def ConfigErrorRecoveryEnableTooltip(self) -> bool:
        """
        :type: bool
        """
    @ConfigErrorRecoveryEnableTooltip.setter
    def ConfigErrorRecoveryEnableTooltip(self, arg0: bool) -> None:
        pass
    @property
    def ConfigFlags(self) -> int:
        """
        :type: int
        """
    @ConfigFlags.setter
    def ConfigFlags(self, arg0: int) -> None:
        pass
    @property
    def ConfigInputTextCursorBlink(self) -> bool:
        """
        :type: bool
        """
    @ConfigInputTextCursorBlink.setter
    def ConfigInputTextCursorBlink(self, arg0: bool) -> None:
        pass
    @property
    def ConfigInputTextEnterKeepActive(self) -> bool:
        """
        :type: bool
        """
    @ConfigInputTextEnterKeepActive.setter
    def ConfigInputTextEnterKeepActive(self, arg0: bool) -> None:
        pass
    @property
    def ConfigInputTrickleEventQueue(self) -> bool:
        """
        :type: bool
        """
    @ConfigInputTrickleEventQueue.setter
    def ConfigInputTrickleEventQueue(self, arg0: bool) -> None:
        pass
    @property
    def ConfigMacOSXBehaviors(self) -> bool:
        """
        :type: bool
        """
    @ConfigMacOSXBehaviors.setter
    def ConfigMacOSXBehaviors(self, arg0: bool) -> None:
        pass
    @property
    def ConfigMemoryCompactTimer(self) -> float:
        """
        :type: float
        """
    @ConfigMemoryCompactTimer.setter
    def ConfigMemoryCompactTimer(self, arg0: float) -> None:
        pass
    @property
    def ConfigNavCaptureKeyboard(self) -> bool:
        """
        :type: bool
        """
    @ConfigNavCaptureKeyboard.setter
    def ConfigNavCaptureKeyboard(self, arg0: bool) -> None:
        pass
    @property
    def ConfigNavCursorVisibleAlways(self) -> bool:
        """
        :type: bool
        """
    @ConfigNavCursorVisibleAlways.setter
    def ConfigNavCursorVisibleAlways(self, arg0: bool) -> None:
        pass
    @property
    def ConfigNavCursorVisibleAuto(self) -> bool:
        """
        :type: bool
        """
    @ConfigNavCursorVisibleAuto.setter
    def ConfigNavCursorVisibleAuto(self, arg0: bool) -> None:
        pass
    @property
    def ConfigNavEscapeClearFocusItem(self) -> bool:
        """
        :type: bool
        """
    @ConfigNavEscapeClearFocusItem.setter
    def ConfigNavEscapeClearFocusItem(self, arg0: bool) -> None:
        pass
    @property
    def ConfigNavEscapeClearFocusWindow(self) -> bool:
        """
        :type: bool
        """
    @ConfigNavEscapeClearFocusWindow.setter
    def ConfigNavEscapeClearFocusWindow(self, arg0: bool) -> None:
        pass
    @property
    def ConfigNavMoveSetMousePos(self) -> bool:
        """
        :type: bool
        """
    @ConfigNavMoveSetMousePos.setter
    def ConfigNavMoveSetMousePos(self, arg0: bool) -> None:
        pass
    @property
    def ConfigNavSwapGamepadButtons(self) -> bool:
        """
        :type: bool
        """
    @ConfigNavSwapGamepadButtons.setter
    def ConfigNavSwapGamepadButtons(self, arg0: bool) -> None:
        pass
    @property
    def ConfigScrollbarScrollByPage(self) -> bool:
        """
        :type: bool
        """
    @ConfigScrollbarScrollByPage.setter
    def ConfigScrollbarScrollByPage(self, arg0: bool) -> None:
        pass
    @property
    def ConfigWindowsCopyContentsWithCtrlC(self) -> bool:
        """
        :type: bool
        """
    @ConfigWindowsCopyContentsWithCtrlC.setter
    def ConfigWindowsCopyContentsWithCtrlC(self, arg0: bool) -> None:
        pass
    @property
    def ConfigWindowsMoveFromTitleBarOnly(self) -> bool:
        """
        :type: bool
        """
    @ConfigWindowsMoveFromTitleBarOnly.setter
    def ConfigWindowsMoveFromTitleBarOnly(self, arg0: bool) -> None:
        pass
    @property
    def ConfigWindowsResizeFromEdges(self) -> bool:
        """
        :type: bool
        """
    @ConfigWindowsResizeFromEdges.setter
    def ConfigWindowsResizeFromEdges(self, arg0: bool) -> None:
        pass
    @property
    def DeltaTime(self) -> float:
        """
        :type: float
        """
    @DeltaTime.setter
    def DeltaTime(self, arg0: float) -> None:
        pass
    @property
    def DisplayFramebufferScale(self) -> Vec2:
        """
        :type: Vec2
        """
    @DisplayFramebufferScale.setter
    def DisplayFramebufferScale(self, arg0: Vec2) -> None:
        pass
    @property
    def DisplaySize(self) -> Vec2:
        """
        :type: Vec2
        """
    @DisplaySize.setter
    def DisplaySize(self, arg0: Vec2) -> None:
        pass
    @property
    def FontAllowUserScaling(self) -> bool:
        """
        :type: bool
        """
    @FontAllowUserScaling.setter
    def FontAllowUserScaling(self, arg0: bool) -> None:
        pass
    @property
    def FontDefault(self) -> ImFont:
        """
        :type: ImFont
        """
    @FontDefault.setter
    def FontDefault(self, arg0: ImFont) -> None:
        pass
    @property
    def FontGlobalScale(self) -> float:
        """
        :type: float
        """
    @FontGlobalScale.setter
    def FontGlobalScale(self, arg0: float) -> None:
        pass
    @property
    def Fonts(self) -> ImFontAtlas:
        """
        :type: ImFontAtlas
        """
    @Fonts.setter
    def Fonts(self, arg0: ImFontAtlas) -> None:
        pass
    @property
    def Framerate(self) -> float:
        """
        :type: float
        """
    @property
    def IniFilename(self) -> str:
        """
        :type: str
        """
    @IniFilename.setter
    def IniFilename(self, arg0: str) -> None:
        pass
    @property
    def IniSavingRate(self) -> float:
        """
        :type: float
        """
    @IniSavingRate.setter
    def IniSavingRate(self, arg0: float) -> None:
        pass
    @property
    def InputQueueSurrogate(self) -> int:
        """
        :type: int
        """
    @InputQueueSurrogate.setter
    def InputQueueSurrogate(self, arg0: int) -> None:
        pass
    @property
    def KeyAlt(self) -> bool:
        """
        :type: bool
        """
    @KeyAlt.setter
    def KeyAlt(self, arg0: bool) -> None:
        pass
    @property
    def KeyCtrl(self) -> bool:
        """
        :type: bool
        """
    @KeyCtrl.setter
    def KeyCtrl(self, arg0: bool) -> None:
        pass
    @property
    def KeyMods(self) -> int:
        """
        :type: int
        """
    @KeyMods.setter
    def KeyMods(self, arg0: int) -> None:
        pass
    @property
    def KeyRepeatDelay(self) -> float:
        """
        :type: float
        """
    @KeyRepeatDelay.setter
    def KeyRepeatDelay(self, arg0: float) -> None:
        pass
    @property
    def KeyRepeatRate(self) -> float:
        """
        :type: float
        """
    @KeyRepeatRate.setter
    def KeyRepeatRate(self, arg0: float) -> None:
        pass
    @property
    def KeyShift(self) -> bool:
        """
        :type: bool
        """
    @KeyShift.setter
    def KeyShift(self, arg0: bool) -> None:
        pass
    @property
    def KeySuper(self) -> bool:
        """
        :type: bool
        """
    @KeySuper.setter
    def KeySuper(self, arg0: bool) -> None:
        pass
    @property
    def LogFilename(self) -> str:
        """
        :type: str
        """
    @LogFilename.setter
    def LogFilename(self, arg0: str) -> None:
        pass
    @property
    def MetricsActiveWindows(self) -> int:
        """
        :type: int
        """
    @property
    def MetricsRenderIndices(self) -> int:
        """
        :type: int
        """
    @property
    def MetricsRenderVertices(self) -> int:
        """
        :type: int
        """
    @property
    def MetricsRenderWindows(self) -> int:
        """
        :type: int
        """
    @property
    def MouseClicked(self) -> ListWrapperBool:
        """
        :type: ListWrapperBool
        """
    @property
    def MouseClickedCount(self) -> ListWrapper<unsigned short>:
        """
        :type: ListWrapper<unsigned short>
        """
    @property
    def MouseClickedLastCount(self) -> ListWrapper<unsigned short>:
        """
        :type: ListWrapper<unsigned short>
        """
    @property
    def MouseClickedPos(self) -> ListWrapperImVec2:
        """
        :type: ListWrapperImVec2
        """
    @property
    def MouseClickedTime(self) -> ListWrapperDouble:
        """
        :type: ListWrapperDouble
        """
    @property
    def MouseCtrlLeftAsRightClick(self) -> bool:
        """
        :type: bool
        """
    @MouseCtrlLeftAsRightClick.setter
    def MouseCtrlLeftAsRightClick(self, arg0: bool) -> None:
        pass
    @property
    def MouseDelta(self) -> Vec2:
        """
        :type: Vec2
        """
    @property
    def MouseDoubleClickMaxDist(self) -> float:
        """
        :type: float
        """
    @MouseDoubleClickMaxDist.setter
    def MouseDoubleClickMaxDist(self, arg0: float) -> None:
        pass
    @property
    def MouseDoubleClickTime(self) -> float:
        """
        :type: float
        """
    @MouseDoubleClickTime.setter
    def MouseDoubleClickTime(self, arg0: float) -> None:
        pass
    @property
    def MouseDoubleClicked(self) -> ListWrapperBool:
        """
        :type: ListWrapperBool
        """
    @property
    def MouseDown(self) -> ListWrapperBool:
        """
        :type: ListWrapperBool
        """
    @property
    def MouseDownDuration(self) -> ListWrapper<float>:
        """
        :type: ListWrapper<float>
        """
    @property
    def MouseDownDurationPrev(self) -> ListWrapper<float>:
        """
        :type: ListWrapper<float>
        """
    @property
    def MouseDownOwned(self) -> ListWrapperBool:
        """
        :type: ListWrapperBool
        """
    @property
    def MouseDownOwnedUnlessPopupClose(self) -> ListWrapperBool:
        """
        :type: ListWrapperBool
        """
    @property
    def MouseDragMaxDistanceSqr(self) -> ListWrapper<float>:
        """
        :type: ListWrapper<float>
        """
    @property
    def MouseDragThreshold(self) -> float:
        """
        :type: float
        """
    @MouseDragThreshold.setter
    def MouseDragThreshold(self, arg0: float) -> None:
        pass
    @property
    def MouseDrawCursor(self) -> bool:
        """
        :type: bool
        """
    @MouseDrawCursor.setter
    def MouseDrawCursor(self, arg0: bool) -> None:
        pass
    @property
    def MousePos(self) -> Vec2:
        """
        :type: Vec2
        """
    @MousePos.setter
    def MousePos(self, arg0: Vec2) -> None:
        pass
    @property
    def MousePosPrev(self) -> Vec2:
        """
        :type: Vec2
        """
    @MousePosPrev.setter
    def MousePosPrev(self, arg0: Vec2) -> None:
        pass
    @property
    def MouseReleased(self) -> ListWrapperBool:
        """
        :type: ListWrapperBool
        """
    @property
    def MouseWheel(self) -> float:
        """
        :type: float
        """
    @MouseWheel.setter
    def MouseWheel(self, arg0: float) -> None:
        pass
    @property
    def MouseWheelH(self) -> float:
        """
        :type: float
        """
    @MouseWheelH.setter
    def MouseWheelH(self, arg0: float) -> None:
        pass
    @property
    def MouseWheelRequestAxisSwap(self) -> bool:
        """
        :type: bool
        """
    @MouseWheelRequestAxisSwap.setter
    def MouseWheelRequestAxisSwap(self, arg0: bool) -> None:
        pass
    @property
    def NavActive(self) -> bool:
        """
        :type: bool
        """
    @property
    def NavVisible(self) -> bool:
        """
        :type: bool
        """
    @property
    def PenPressure(self) -> float:
        """
        :type: float
        """
    @PenPressure.setter
    def PenPressure(self, arg0: float) -> None:
        pass
    @property
    def WantCaptureKeyboard(self) -> bool:
        """
        :type: bool
        """
    @WantCaptureKeyboard.setter
    def WantCaptureKeyboard(self, arg0: bool) -> None:
        pass
    @property
    def WantCaptureMouse(self) -> bool:
        """
        :type: bool
        """
    @WantCaptureMouse.setter
    def WantCaptureMouse(self, arg0: bool) -> None:
        pass
    @property
    def WantCaptureMouseUnlessPopupClose(self) -> bool:
        """
        :type: bool
        """
    @WantCaptureMouseUnlessPopupClose.setter
    def WantCaptureMouseUnlessPopupClose(self, arg0: bool) -> None:
        pass
    @property
    def WantSaveIniSettings(self) -> bool:
        """
        :type: bool
        """
    @WantSaveIniSettings.setter
    def WantSaveIniSettings(self, arg0: bool) -> None:
        pass
    @property
    def WantSetMousePos(self) -> bool:
        """
        :type: bool
        """
    @WantSetMousePos.setter
    def WantSetMousePos(self, arg0: bool) -> None:
        pass
    @property
    def WantTextInput(self) -> bool:
        """
        :type: bool
        """
    @WantTextInput.setter
    def WantTextInput(self, arg0: bool) -> None:
        pass
    pass
class ImDrawList():
    def AddBezierCubic(self, p1: Vec2, p2: Vec2, p3: Vec2, p4: Vec2, col: int, thickness: float, num_segments: int = 0) -> None: ...
    def AddBezierQuadratic(self, p1: Vec2, p2: Vec2, p3: Vec2, col: int, thickness: float, num_segments: int = 0) -> None: ...
    def AddCircle(self, center: Vec2, radius: float, col: int, num_segments: int = 0, thickness: float = 1.0) -> None: ...
    def AddCircleFilled(self, center: Vec2, radius: float, col: int, num_segments: int = 0) -> None: ...
    def AddConcavePolyFilled(self, arg0: Vec2List, arg1: int) -> None: ...
    def AddConvexPolyFilled(self, points: Vec2List, col: int) -> None: ...
    def AddEllipse(self, center: Vec2, radius: Vec2, col: int, rot: float = 0.0, num_segments: int = 0, thickness: float = 1.0) -> None: ...
    def AddEllipseFilled(self, center: Vec2, radius: Vec2, col: int, rot: float = 0.0, num_segments: int = 0) -> None: ...
    def AddImage(self, user_texture_id: Texture, p_min: Vec2, p_max: Vec2, uv_min: Vec2 = Vec2(0, 0), uv_max: Vec2 = Vec2(1, 1), col: int = 4294967295) -> None: ...
    def AddImageQuad(self, user_texture_id: Texture, p1: Vec2, p2: Vec2, p3: Vec2, p4: Vec2, uv1: Vec2 = Vec2(0, 0), uv2: Vec2 = Vec2(1, 0), uv3: Vec2 = Vec2(0, 1), uv4: Vec2 = Vec2(1, 1), col: int = 4294967295) -> None: ...
    def AddImageRounded(self, user_texture_id: Texture, p_min: Vec2, p_max: Vec2, uv_min: Vec2, uv_max: Vec2, col: int, rounding: float, flags: int = 0) -> None: ...
    def AddLine(self, p1: Vec2, p2: Vec2, col: int, thickness: float = 1.0) -> None: ...
    def AddNgon(self, center: Vec2, radius: float, col: int, num_segments: int, thickness: float = 1.0) -> None: ...
    def AddNgonFilled(self, center: Vec2, radius: float, col: int, num_segments: int) -> None: ...
    def AddPolyline(self, points: Vec2List, col: int, flags: int, thickness: float) -> None: ...
    def AddQuad(self, p1: Vec2, p2: Vec2, p3: Vec2, p4: Vec2, col: int, thickness: float = 1.0) -> None: ...
    def AddQuadFilled(self, p1: Vec2, p2: Vec2, p3: Vec2, p4: Vec2, col: int) -> None: ...
    def AddRect(self, p_min: Vec2, p_max: Vec2, col: int, rounding: float = 0.0, flags: int = 0, thickness: float = 1.0) -> None: ...
    def AddRectFilled(self, p_min: Vec2, p_max: Vec2, col: int, rounding: float, flags: int = 0) -> None: ...
    def AddRectFilledMultiColor(self, p_min: Vec2, p_max: Vec2, col_upr_left: int, col_upr_right: int, col_bot_right: int, col_bot_left: int) -> None: ...
    def AddText(self, pos: Vec2, col: int, text: str, font: typing.Optional[ImFont] = None, font_size: float = 1.0, wrap_width: float = 0.0, cpu_fine_clip_rect: typing.Optional[Vec4] = None) -> None: ...
    def AddTriangle(self, p1: Vec2, p2: Vec2, p3: Vec2, col: int, thickness: float = 1.0) -> None: ...
    def AddTriangleFilled(self, p1: Vec2, p2: Vec2, p3: Vec2, col: int) -> None: ...
    def ChannelsMerge(self) -> None: ...
    def ChannelsSetCurrent(self, n: int) -> None: ...
    def ChannelsSplit(self, count: int) -> None: ...
    def PathArcTo(self, center: Vec2, radius: float, a_min: float, a_max: float, num_segments: int = 0) -> None: ...
    def PathArcToFast(self, center: Vec2, radius: float, a_min_of_12: int, a_max_of_12: int) -> None: ...
    def PathBezierCubicCurveTo(self, p2: Vec2, p3: Vec2, p4: Vec2, num_segments: int = 0) -> None: ...
    def PathBezierQuadraticCurveTo(self, p2: Vec2, p3: Vec2, num_segments: int = 0) -> None: ...
    def PathClear(self) -> None: ...
    def PathEllipticalArcTo(self, center: Vec2, radius: Vec2, rot: float, a_min: float, a_max: float, num_segments: int = 0) -> None: ...
    def PathFillConcave(self, col: int) -> None: ...
    def PathFillConvex(self, col: int) -> None: ...
    def PathLineTo(self, pos: Vec2) -> None: ...
    def PathLineToMergeDuplicate(self, pos: Vec2) -> None: ...
    def PathRect(self, rect_min: Vec2, rect_max: Vec2, rounding: float = 0.0, flags: int = 0) -> None: ...
    def PathStroke(self, col: int, flags: int = 0, thickness: float = 1.0) -> None: ...
    def PopClipRect(self) -> None: ...
    def PopTextureID(self) -> None: ...
    def PushClipRect(self, clip_rect_min: Vec2, clip_rect_max: Vec2, intersect_with_current_clip_rect: bool = False) -> None: ...
    def PushClipRectFullScreen(self) -> None: ...
    def PushTextureID(self, arg0: int) -> None: ...
    @property
    def Flags(self) -> int:
        """
        :type: int
        """
    @Flags.setter
    def Flags(self, arg0: int) -> None:
        pass
    pass
class ImFont():
    def CalcTextSizeA(self, text: str, max_width: float = 3.4028234663852886e+38, wrap_width: float = -1.0) -> Vec2: ...
    def FindGlyph(self, c: int) -> ImFontGlyph: ...
    def FindGlyphNoFallback(self, c: int) -> ImFontGlyph: ...
    def GetCharAdvance(self, c: int) -> float: ...
    def GetDebugName(self) -> str: ...
    def IsLoaded(self) -> bool: ...
    def RenderChar(self, draw_list: ImDrawList, size: float, pos: Vec2, col: int, c: int) -> None: ...
    @property
    def Ascent(self) -> float:
        """
        :type: float
        """
    @Ascent.setter
    def Ascent(self, arg0: float) -> None:
        pass
    @property
    def ConfigData(self) -> ImFontConfig:
        """
        :type: ImFontConfig
        """
    @ConfigData.setter
    def ConfigData(self, arg0: ImFontConfig) -> None:
        pass
    @property
    def ConfigDataCount(self) -> int:
        """
        :type: int
        """
    @ConfigDataCount.setter
    def ConfigDataCount(self, arg0: int) -> None:
        pass
    @property
    def ContainerAtlas(self) -> ImFontAtlas:
        """
        :type: ImFontAtlas
        """
    @ContainerAtlas.setter
    def ContainerAtlas(self, arg0: ImFontAtlas) -> None:
        pass
    @property
    def Descent(self) -> float:
        """
        :type: float
        """
    @Descent.setter
    def Descent(self, arg0: float) -> None:
        pass
    @property
    def DirtyLookupTables(self) -> bool:
        """
        :type: bool
        """
    @DirtyLookupTables.setter
    def DirtyLookupTables(self, arg0: bool) -> None:
        pass
    @property
    def EllipsisChar(self) -> int:
        """
        :type: int
        """
    @EllipsisChar.setter
    def EllipsisChar(self, arg0: int) -> None:
        pass
    @property
    def EllipsisCharCount(self) -> int:
        """
        :type: int
        """
    @EllipsisCharCount.setter
    def EllipsisCharCount(self, arg0: int) -> None:
        pass
    @property
    def EllipsisCharStep(self) -> float:
        """
        :type: float
        """
    @EllipsisCharStep.setter
    def EllipsisCharStep(self, arg0: float) -> None:
        pass
    @property
    def EllipsisWidth(self) -> float:
        """
        :type: float
        """
    @EllipsisWidth.setter
    def EllipsisWidth(self, arg0: float) -> None:
        pass
    @property
    def FallbackAdvanceX(self) -> float:
        """
        :type: float
        """
    @FallbackAdvanceX.setter
    def FallbackAdvanceX(self, arg0: float) -> None:
        pass
    @property
    def FallbackChar(self) -> int:
        """
        :type: int
        """
    @FallbackChar.setter
    def FallbackChar(self, arg0: int) -> None:
        pass
    @property
    def FallbackGlyph(self) -> ImFontGlyph:
        """
        :type: ImFontGlyph
        """
    @FallbackGlyph.setter
    def FallbackGlyph(self, arg0: ImFontGlyph) -> None:
        pass
    @property
    def FontSize(self) -> float:
        """
        :type: float
        """
    @FontSize.setter
    def FontSize(self, arg0: float) -> None:
        pass
    @property
    def Glyphs(self) -> ImVector<ImFontGlyph>:
        """
        :type: ImVector<ImFontGlyph>
        """
    @Glyphs.setter
    def Glyphs(self, arg0: ImVector<ImFontGlyph>) -> None:
        pass
    @property
    def IndexAdvanceX(self) -> ImVector<float>:
        """
        :type: ImVector<float>
        """
    @IndexAdvanceX.setter
    def IndexAdvanceX(self, arg0: ImVector<float>) -> None:
        pass
    @property
    def IndexLookup(self) -> ImVector<unsigned short>:
        """
        :type: ImVector<unsigned short>
        """
    @IndexLookup.setter
    def IndexLookup(self, arg0: ImVector<unsigned short>) -> None:
        pass
    @property
    def MetricsTotalSurface(self) -> int:
        """
        :type: int
        """
    @MetricsTotalSurface.setter
    def MetricsTotalSurface(self, arg0: int) -> None:
        pass
    @property
    def Scale(self) -> float:
        """
        :type: float
        """
    @Scale.setter
    def Scale(self, arg0: float) -> None:
        pass
    pass
class ImFontAtlas():
    def AddCustomRectFontGlyph(self, font: ImFont, id: int, width: int, height: int, advance_x: float, offset: Vec2 = Vec2(0, 0)) -> int: ...
    def AddCustomRectRegular(self, width: int, height: int) -> int: ...
    def AddFont(self, font_cfg: ImFontConfig) -> ImFont: ...
    def AddFontDefault(self, font_cfg: typing.Optional[ImFontConfig] = None) -> ImFont: ...
    def AddFontFromFileTTF(self, filename: str, size_pixels: float, font_cfg: typing.Optional[ImFontConfig] = None, glyph_ranges: typing.Optional[WCharList] = None) -> ImFont: ...
    def Build(self) -> bool: ...
    def Clear(self) -> None: ...
    def ClearFonts(self) -> None: ...
    def ClearInputData(self) -> None: ...
    def ClearTexData(self) -> None: ...
    def IsBuilt(self) -> bool: ...
    def SetTexID(self, id: int) -> None: ...
    pass
class ImFontConfig():
    def __init__(self) -> None: ...
    @property
    def EllipsisChar(self) -> int:
        """
        :type: int
        """
    @EllipsisChar.setter
    def EllipsisChar(self, arg0: int) -> None:
        pass
    @property
    def FontBuilderFlags(self) -> int:
        """
        :type: int
        """
    @FontBuilderFlags.setter
    def FontBuilderFlags(self, arg0: int) -> None:
        pass
    @property
    def FontDataOwnedByAtlas(self) -> bool:
        """
        :type: bool
        """
    @FontDataOwnedByAtlas.setter
    def FontDataOwnedByAtlas(self, arg0: bool) -> None:
        pass
    @property
    def FontDataSize(self) -> int:
        """
        :type: int
        """
    @FontDataSize.setter
    def FontDataSize(self, arg0: int) -> None:
        pass
    @property
    def FontNo(self) -> int:
        """
        :type: int
        """
    @FontNo.setter
    def FontNo(self, arg0: int) -> None:
        pass
    @property
    def GlyphExtraSpacing(self) -> Vec2:
        """
        :type: Vec2
        """
    @GlyphExtraSpacing.setter
    def GlyphExtraSpacing(self, arg0: Vec2) -> None:
        pass
    @property
    def GlyphMaxAdvanceX(self) -> float:
        """
        :type: float
        """
    @GlyphMaxAdvanceX.setter
    def GlyphMaxAdvanceX(self, arg0: float) -> None:
        pass
    @property
    def GlyphMinAdvanceX(self) -> float:
        """
        :type: float
        """
    @GlyphMinAdvanceX.setter
    def GlyphMinAdvanceX(self, arg0: float) -> None:
        pass
    @property
    def GlyphOffset(self) -> Vec2:
        """
        :type: Vec2
        """
    @GlyphOffset.setter
    def GlyphOffset(self, arg0: Vec2) -> None:
        pass
    @property
    def MergeMode(self) -> bool:
        """
        :type: bool
        """
    @MergeMode.setter
    def MergeMode(self, arg0: bool) -> None:
        pass
    @property
    def OversampleH(self) -> int:
        """
        :type: int
        """
    @OversampleH.setter
    def OversampleH(self, arg0: int) -> None:
        pass
    @property
    def OversampleV(self) -> int:
        """
        :type: int
        """
    @OversampleV.setter
    def OversampleV(self, arg0: int) -> None:
        pass
    @property
    def PixelSnapH(self) -> bool:
        """
        :type: bool
        """
    @PixelSnapH.setter
    def PixelSnapH(self, arg0: bool) -> None:
        pass
    @property
    def RasterizerDensity(self) -> float:
        """
        :type: float
        """
    @RasterizerDensity.setter
    def RasterizerDensity(self, arg0: float) -> None:
        pass
    @property
    def RasterizerMultiply(self) -> float:
        """
        :type: float
        """
    @RasterizerMultiply.setter
    def RasterizerMultiply(self, arg0: float) -> None:
        pass
    @property
    def SizePixels(self) -> float:
        """
        :type: float
        """
    @SizePixels.setter
    def SizePixels(self, arg0: float) -> None:
        pass
    pass
class ImFontGlyph():
    @property
    def AdvanceX(self) -> float:
        """
        :type: float
        """
    @AdvanceX.setter
    def AdvanceX(self, arg0: float) -> None:
        pass
    @property
    def Codepoint(self) -> int:
        """
        :type: int
        """
    @Codepoint.setter
    def Codepoint(self, arg1: int) -> None:
        pass
    @property
    def Colored(self) -> int:
        """
        :type: int
        """
    @Colored.setter
    def Colored(self, arg1: int) -> None:
        pass
    @property
    def U0(self) -> float:
        """
        :type: float
        """
    @U0.setter
    def U0(self, arg0: float) -> None:
        pass
    @property
    def U1(self) -> float:
        """
        :type: float
        """
    @U1.setter
    def U1(self, arg0: float) -> None:
        pass
    @property
    def V0(self) -> float:
        """
        :type: float
        """
    @V0.setter
    def V0(self, arg0: float) -> None:
        pass
    @property
    def V1(self) -> float:
        """
        :type: float
        """
    @V1.setter
    def V1(self, arg0: float) -> None:
        pass
    @property
    def Visible(self) -> int:
        """
        :type: int
        """
    @Visible.setter
    def Visible(self, arg1: int) -> None:
        pass
    @property
    def X0(self) -> float:
        """
        :type: float
        """
    @X0.setter
    def X0(self, arg0: float) -> None:
        pass
    @property
    def X1(self) -> float:
        """
        :type: float
        """
    @X1.setter
    def X1(self, arg0: float) -> None:
        pass
    @property
    def Y0(self) -> float:
        """
        :type: float
        """
    @Y0.setter
    def Y0(self, arg0: float) -> None:
        pass
    @property
    def Y1(self) -> float:
        """
        :type: float
        """
    @Y1.setter
    def Y1(self, arg0: float) -> None:
        pass
    pass
class ImKey():
    """
    Members:

      None_

      Tab

      LeftArrow

      RightArrow

      UpArrow

      DownArrow

      PageUp

      PageDown

      Home

      End

      Insert

      Delete

      Backspace

      Space

      Enter

      Escape

      LeftCtrl

      LeftShift

      LeftAlt

      LeftSuper

      RightCtrl

      RightShift

      RightAlt

      RightSuper

      Menu

      _0

      _1

      _2

      _3

      _4

      _5

      _6

      _7

      _8

      _9

      A

      B

      C

      D

      E

      F

      G

      H

      I

      J

      K

      L

      M

      N

      O

      P

      Q

      R

      S

      T

      U

      V

      W

      X

      Y

      Z

      F1

      F2

      F3

      F4

      F5

      F6

      F7

      F8

      F9

      F10

      F11

      F12

      F13

      F14

      F15

      F16

      F17

      F18

      F19

      F20

      F21

      F22

      F23

      F24

      Apostrophe

      Comma

      Minus

      Period

      Slash

      Semicolon

      Equal

      LeftBracket

      Backslash

      RightBracket

      GraveAccent

      CapsLock

      ScrollLock

      NumLock

      PrintScreen

      Pause

      Keypad0

      Keypad1

      Keypad2

      Keypad3

      Keypad4

      Keypad5

      Keypad6

      Keypad7

      Keypad8

      Keypad9

      KeypadDecimal

      KeypadDivide

      KeypadMultiply

      KeypadSubtract

      KeypadAdd

      KeypadEnter

      KeypadEqual

      AppBack

      AppForward

      GamepadStart

      GamepadBack

      GamepadFaceLeft

      GamepadFaceRight

      GamepadFaceUp

      GamepadFaceDown

      GamepadDpadLeft

      GamepadDpadRight

      GamepadDpadUp

      GamepadDpadDown

      GamepadL1

      GamepadR1

      GamepadL2

      GamepadR2

      GamepadL3

      GamepadR3

      GamepadLStickLeft

      GamepadLStickRight

      GamepadLStickUp

      GamepadLStickDown

      GamepadRStickLeft

      GamepadRStickRight

      GamepadRStickUp

      GamepadRStickDown

      MouseLeft

      MouseRight

      MouseMiddle

      MouseX1

      MouseX2

      MouseWheelX

      MouseWheelY

      Mod_None

      Mod_Ctrl

      Mod_Shift

      Mod_Alt

      Mod_Super

      Mod_Mask_

      NamedKey_BEGIN

      NamedKey_END
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    A: imgui.ImKey # value = <ImKey.A: 546>
    Apostrophe: imgui.ImKey # value = <ImKey.Apostrophe: 596>
    AppBack: imgui.ImKey # value = <ImKey.AppBack: 629>
    AppForward: imgui.ImKey # value = <ImKey.AppForward: 630>
    B: imgui.ImKey # value = <ImKey.B: 547>
    Backslash: imgui.ImKey # value = <ImKey.Backslash: 604>
    Backspace: imgui.ImKey # value = <ImKey.Backspace: 523>
    C: imgui.ImKey # value = <ImKey.C: 548>
    CapsLock: imgui.ImKey # value = <ImKey.CapsLock: 607>
    Comma: imgui.ImKey # value = <ImKey.Comma: 597>
    D: imgui.ImKey # value = <ImKey.D: 549>
    Delete: imgui.ImKey # value = <ImKey.Delete: 522>
    DownArrow: imgui.ImKey # value = <ImKey.DownArrow: 516>
    E: imgui.ImKey # value = <ImKey.E: 550>
    End: imgui.ImKey # value = <ImKey.End: 520>
    Enter: imgui.ImKey # value = <ImKey.Enter: 525>
    Equal: imgui.ImKey # value = <ImKey.Equal: 602>
    Escape: imgui.ImKey # value = <ImKey.Escape: 526>
    F: imgui.ImKey # value = <ImKey.F: 551>
    F1: imgui.ImKey # value = <ImKey.F1: 572>
    F10: imgui.ImKey # value = <ImKey.F10: 581>
    F11: imgui.ImKey # value = <ImKey.F11: 582>
    F12: imgui.ImKey # value = <ImKey.F12: 583>
    F13: imgui.ImKey # value = <ImKey.F13: 584>
    F14: imgui.ImKey # value = <ImKey.F14: 585>
    F15: imgui.ImKey # value = <ImKey.F15: 586>
    F16: imgui.ImKey # value = <ImKey.F16: 587>
    F17: imgui.ImKey # value = <ImKey.F17: 588>
    F18: imgui.ImKey # value = <ImKey.F18: 589>
    F19: imgui.ImKey # value = <ImKey.F19: 590>
    F2: imgui.ImKey # value = <ImKey.F2: 573>
    F20: imgui.ImKey # value = <ImKey.F20: 591>
    F21: imgui.ImKey # value = <ImKey.F21: 592>
    F22: imgui.ImKey # value = <ImKey.F22: 593>
    F23: imgui.ImKey # value = <ImKey.F23: 594>
    F24: imgui.ImKey # value = <ImKey.F24: 595>
    F3: imgui.ImKey # value = <ImKey.F3: 574>
    F4: imgui.ImKey # value = <ImKey.F4: 575>
    F5: imgui.ImKey # value = <ImKey.F5: 576>
    F6: imgui.ImKey # value = <ImKey.F6: 577>
    F7: imgui.ImKey # value = <ImKey.F7: 578>
    F8: imgui.ImKey # value = <ImKey.F8: 579>
    F9: imgui.ImKey # value = <ImKey.F9: 580>
    G: imgui.ImKey # value = <ImKey.G: 552>
    GamepadBack: imgui.ImKey # value = <ImKey.GamepadBack: 632>
    GamepadDpadDown: imgui.ImKey # value = <ImKey.GamepadDpadDown: 640>
    GamepadDpadLeft: imgui.ImKey # value = <ImKey.GamepadDpadLeft: 637>
    GamepadDpadRight: imgui.ImKey # value = <ImKey.GamepadDpadRight: 638>
    GamepadDpadUp: imgui.ImKey # value = <ImKey.GamepadDpadUp: 639>
    GamepadFaceDown: imgui.ImKey # value = <ImKey.GamepadFaceDown: 636>
    GamepadFaceLeft: imgui.ImKey # value = <ImKey.GamepadFaceLeft: 633>
    GamepadFaceRight: imgui.ImKey # value = <ImKey.GamepadFaceRight: 634>
    GamepadFaceUp: imgui.ImKey # value = <ImKey.GamepadFaceUp: 635>
    GamepadL1: imgui.ImKey # value = <ImKey.GamepadL1: 641>
    GamepadL2: imgui.ImKey # value = <ImKey.GamepadL2: 643>
    GamepadL3: imgui.ImKey # value = <ImKey.GamepadL3: 645>
    GamepadLStickDown: imgui.ImKey # value = <ImKey.GamepadLStickDown: 650>
    GamepadLStickLeft: imgui.ImKey # value = <ImKey.GamepadLStickLeft: 647>
    GamepadLStickRight: imgui.ImKey # value = <ImKey.GamepadLStickRight: 648>
    GamepadLStickUp: imgui.ImKey # value = <ImKey.GamepadLStickUp: 649>
    GamepadR1: imgui.ImKey # value = <ImKey.GamepadR1: 642>
    GamepadR2: imgui.ImKey # value = <ImKey.GamepadR2: 644>
    GamepadR3: imgui.ImKey # value = <ImKey.GamepadR3: 646>
    GamepadRStickDown: imgui.ImKey # value = <ImKey.GamepadRStickDown: 654>
    GamepadRStickLeft: imgui.ImKey # value = <ImKey.GamepadRStickLeft: 651>
    GamepadRStickRight: imgui.ImKey # value = <ImKey.GamepadRStickRight: 652>
    GamepadRStickUp: imgui.ImKey # value = <ImKey.GamepadRStickUp: 653>
    GamepadStart: imgui.ImKey # value = <ImKey.GamepadStart: 631>
    GraveAccent: imgui.ImKey # value = <ImKey.GraveAccent: 606>
    H: imgui.ImKey # value = <ImKey.H: 553>
    Home: imgui.ImKey # value = <ImKey.Home: 519>
    I: imgui.ImKey # value = <ImKey.I: 554>
    Insert: imgui.ImKey # value = <ImKey.Insert: 521>
    J: imgui.ImKey # value = <ImKey.J: 555>
    K: imgui.ImKey # value = <ImKey.K: 556>
    Keypad0: imgui.ImKey # value = <ImKey.Keypad0: 612>
    Keypad1: imgui.ImKey # value = <ImKey.Keypad1: 613>
    Keypad2: imgui.ImKey # value = <ImKey.Keypad2: 614>
    Keypad3: imgui.ImKey # value = <ImKey.Keypad3: 615>
    Keypad4: imgui.ImKey # value = <ImKey.Keypad4: 616>
    Keypad5: imgui.ImKey # value = <ImKey.Keypad5: 617>
    Keypad6: imgui.ImKey # value = <ImKey.Keypad6: 618>
    Keypad7: imgui.ImKey # value = <ImKey.Keypad7: 619>
    Keypad8: imgui.ImKey # value = <ImKey.Keypad8: 620>
    Keypad9: imgui.ImKey # value = <ImKey.Keypad9: 621>
    KeypadAdd: imgui.ImKey # value = <ImKey.KeypadAdd: 626>
    KeypadDecimal: imgui.ImKey # value = <ImKey.KeypadDecimal: 622>
    KeypadDivide: imgui.ImKey # value = <ImKey.KeypadDivide: 623>
    KeypadEnter: imgui.ImKey # value = <ImKey.KeypadEnter: 627>
    KeypadEqual: imgui.ImKey # value = <ImKey.KeypadEqual: 628>
    KeypadMultiply: imgui.ImKey # value = <ImKey.KeypadMultiply: 624>
    KeypadSubtract: imgui.ImKey # value = <ImKey.KeypadSubtract: 625>
    L: imgui.ImKey # value = <ImKey.L: 557>
    LeftAlt: imgui.ImKey # value = <ImKey.LeftAlt: 529>
    LeftArrow: imgui.ImKey # value = <ImKey.LeftArrow: 513>
    LeftBracket: imgui.ImKey # value = <ImKey.LeftBracket: 603>
    LeftCtrl: imgui.ImKey # value = <ImKey.LeftCtrl: 527>
    LeftShift: imgui.ImKey # value = <ImKey.LeftShift: 528>
    LeftSuper: imgui.ImKey # value = <ImKey.LeftSuper: 530>
    M: imgui.ImKey # value = <ImKey.M: 558>
    Menu: imgui.ImKey # value = <ImKey.Menu: 535>
    Minus: imgui.ImKey # value = <ImKey.Minus: 598>
    Mod_Alt: imgui.ImKey # value = <ImKey.Mod_Alt: 16384>
    Mod_Ctrl: imgui.ImKey # value = <ImKey.Mod_Ctrl: 4096>
    Mod_Mask_: imgui.ImKey # value = <ImKey.Mod_Mask_: 61440>
    Mod_None: imgui.ImKey # value = <ImKey.None_: 0>
    Mod_Shift: imgui.ImKey # value = <ImKey.Mod_Shift: 8192>
    Mod_Super: imgui.ImKey # value = <ImKey.Mod_Super: 32768>
    MouseLeft: imgui.ImKey # value = <ImKey.MouseLeft: 655>
    MouseMiddle: imgui.ImKey # value = <ImKey.MouseMiddle: 657>
    MouseRight: imgui.ImKey # value = <ImKey.MouseRight: 656>
    MouseWheelX: imgui.ImKey # value = <ImKey.MouseWheelX: 660>
    MouseWheelY: imgui.ImKey # value = <ImKey.MouseWheelY: 661>
    MouseX1: imgui.ImKey # value = <ImKey.MouseX1: 658>
    MouseX2: imgui.ImKey # value = <ImKey.MouseX2: 659>
    N: imgui.ImKey # value = <ImKey.N: 559>
    NamedKey_BEGIN: imgui.ImKey # value = <ImKey.Tab: 512>
    NamedKey_END: imgui.ImKey # value = <ImKey.NamedKey_END: 666>
    None_: imgui.ImKey # value = <ImKey.None_: 0>
    NumLock: imgui.ImKey # value = <ImKey.NumLock: 609>
    O: imgui.ImKey # value = <ImKey.O: 560>
    P: imgui.ImKey # value = <ImKey.P: 561>
    PageDown: imgui.ImKey # value = <ImKey.PageDown: 518>
    PageUp: imgui.ImKey # value = <ImKey.PageUp: 517>
    Pause: imgui.ImKey # value = <ImKey.Pause: 611>
    Period: imgui.ImKey # value = <ImKey.Period: 599>
    PrintScreen: imgui.ImKey # value = <ImKey.PrintScreen: 610>
    Q: imgui.ImKey # value = <ImKey.Q: 562>
    R: imgui.ImKey # value = <ImKey.R: 563>
    RightAlt: imgui.ImKey # value = <ImKey.RightAlt: 533>
    RightArrow: imgui.ImKey # value = <ImKey.RightArrow: 514>
    RightBracket: imgui.ImKey # value = <ImKey.RightBracket: 605>
    RightCtrl: imgui.ImKey # value = <ImKey.RightCtrl: 531>
    RightShift: imgui.ImKey # value = <ImKey.RightShift: 532>
    RightSuper: imgui.ImKey # value = <ImKey.RightSuper: 534>
    S: imgui.ImKey # value = <ImKey.S: 564>
    ScrollLock: imgui.ImKey # value = <ImKey.ScrollLock: 608>
    Semicolon: imgui.ImKey # value = <ImKey.Semicolon: 601>
    Slash: imgui.ImKey # value = <ImKey.Slash: 600>
    Space: imgui.ImKey # value = <ImKey.Space: 524>
    T: imgui.ImKey # value = <ImKey.T: 565>
    Tab: imgui.ImKey # value = <ImKey.Tab: 512>
    U: imgui.ImKey # value = <ImKey.U: 566>
    UpArrow: imgui.ImKey # value = <ImKey.UpArrow: 515>
    V: imgui.ImKey # value = <ImKey.V: 567>
    W: imgui.ImKey # value = <ImKey.W: 568>
    X: imgui.ImKey # value = <ImKey.X: 569>
    Y: imgui.ImKey # value = <ImKey.Y: 570>
    Z: imgui.ImKey # value = <ImKey.Z: 571>
    _0: imgui.ImKey # value = <ImKey._0: 536>
    _1: imgui.ImKey # value = <ImKey._1: 537>
    _2: imgui.ImKey # value = <ImKey._2: 538>
    _3: imgui.ImKey # value = <ImKey._3: 539>
    _4: imgui.ImKey # value = <ImKey._4: 540>
    _5: imgui.ImKey # value = <ImKey._5: 541>
    _6: imgui.ImKey # value = <ImKey._6: 542>
    _7: imgui.ImKey # value = <ImKey._7: 543>
    _8: imgui.ImKey # value = <ImKey._8: 544>
    _9: imgui.ImKey # value = <ImKey._9: 545>
    __members__: dict # value = {'None_': <ImKey.None_: 0>, 'Tab': <ImKey.Tab: 512>, 'LeftArrow': <ImKey.LeftArrow: 513>, 'RightArrow': <ImKey.RightArrow: 514>, 'UpArrow': <ImKey.UpArrow: 515>, 'DownArrow': <ImKey.DownArrow: 516>, 'PageUp': <ImKey.PageUp: 517>, 'PageDown': <ImKey.PageDown: 518>, 'Home': <ImKey.Home: 519>, 'End': <ImKey.End: 520>, 'Insert': <ImKey.Insert: 521>, 'Delete': <ImKey.Delete: 522>, 'Backspace': <ImKey.Backspace: 523>, 'Space': <ImKey.Space: 524>, 'Enter': <ImKey.Enter: 525>, 'Escape': <ImKey.Escape: 526>, 'LeftCtrl': <ImKey.LeftCtrl: 527>, 'LeftShift': <ImKey.LeftShift: 528>, 'LeftAlt': <ImKey.LeftAlt: 529>, 'LeftSuper': <ImKey.LeftSuper: 530>, 'RightCtrl': <ImKey.RightCtrl: 531>, 'RightShift': <ImKey.RightShift: 532>, 'RightAlt': <ImKey.RightAlt: 533>, 'RightSuper': <ImKey.RightSuper: 534>, 'Menu': <ImKey.Menu: 535>, '_0': <ImKey._0: 536>, '_1': <ImKey._1: 537>, '_2': <ImKey._2: 538>, '_3': <ImKey._3: 539>, '_4': <ImKey._4: 540>, '_5': <ImKey._5: 541>, '_6': <ImKey._6: 542>, '_7': <ImKey._7: 543>, '_8': <ImKey._8: 544>, '_9': <ImKey._9: 545>, 'A': <ImKey.A: 546>, 'B': <ImKey.B: 547>, 'C': <ImKey.C: 548>, 'D': <ImKey.D: 549>, 'E': <ImKey.E: 550>, 'F': <ImKey.F: 551>, 'G': <ImKey.G: 552>, 'H': <ImKey.H: 553>, 'I': <ImKey.I: 554>, 'J': <ImKey.J: 555>, 'K': <ImKey.K: 556>, 'L': <ImKey.L: 557>, 'M': <ImKey.M: 558>, 'N': <ImKey.N: 559>, 'O': <ImKey.O: 560>, 'P': <ImKey.P: 561>, 'Q': <ImKey.Q: 562>, 'R': <ImKey.R: 563>, 'S': <ImKey.S: 564>, 'T': <ImKey.T: 565>, 'U': <ImKey.U: 566>, 'V': <ImKey.V: 567>, 'W': <ImKey.W: 568>, 'X': <ImKey.X: 569>, 'Y': <ImKey.Y: 570>, 'Z': <ImKey.Z: 571>, 'F1': <ImKey.F1: 572>, 'F2': <ImKey.F2: 573>, 'F3': <ImKey.F3: 574>, 'F4': <ImKey.F4: 575>, 'F5': <ImKey.F5: 576>, 'F6': <ImKey.F6: 577>, 'F7': <ImKey.F7: 578>, 'F8': <ImKey.F8: 579>, 'F9': <ImKey.F9: 580>, 'F10': <ImKey.F10: 581>, 'F11': <ImKey.F11: 582>, 'F12': <ImKey.F12: 583>, 'F13': <ImKey.F13: 584>, 'F14': <ImKey.F14: 585>, 'F15': <ImKey.F15: 586>, 'F16': <ImKey.F16: 587>, 'F17': <ImKey.F17: 588>, 'F18': <ImKey.F18: 589>, 'F19': <ImKey.F19: 590>, 'F20': <ImKey.F20: 591>, 'F21': <ImKey.F21: 592>, 'F22': <ImKey.F22: 593>, 'F23': <ImKey.F23: 594>, 'F24': <ImKey.F24: 595>, 'Apostrophe': <ImKey.Apostrophe: 596>, 'Comma': <ImKey.Comma: 597>, 'Minus': <ImKey.Minus: 598>, 'Period': <ImKey.Period: 599>, 'Slash': <ImKey.Slash: 600>, 'Semicolon': <ImKey.Semicolon: 601>, 'Equal': <ImKey.Equal: 602>, 'LeftBracket': <ImKey.LeftBracket: 603>, 'Backslash': <ImKey.Backslash: 604>, 'RightBracket': <ImKey.RightBracket: 605>, 'GraveAccent': <ImKey.GraveAccent: 606>, 'CapsLock': <ImKey.CapsLock: 607>, 'ScrollLock': <ImKey.ScrollLock: 608>, 'NumLock': <ImKey.NumLock: 609>, 'PrintScreen': <ImKey.PrintScreen: 610>, 'Pause': <ImKey.Pause: 611>, 'Keypad0': <ImKey.Keypad0: 612>, 'Keypad1': <ImKey.Keypad1: 613>, 'Keypad2': <ImKey.Keypad2: 614>, 'Keypad3': <ImKey.Keypad3: 615>, 'Keypad4': <ImKey.Keypad4: 616>, 'Keypad5': <ImKey.Keypad5: 617>, 'Keypad6': <ImKey.Keypad6: 618>, 'Keypad7': <ImKey.Keypad7: 619>, 'Keypad8': <ImKey.Keypad8: 620>, 'Keypad9': <ImKey.Keypad9: 621>, 'KeypadDecimal': <ImKey.KeypadDecimal: 622>, 'KeypadDivide': <ImKey.KeypadDivide: 623>, 'KeypadMultiply': <ImKey.KeypadMultiply: 624>, 'KeypadSubtract': <ImKey.KeypadSubtract: 625>, 'KeypadAdd': <ImKey.KeypadAdd: 626>, 'KeypadEnter': <ImKey.KeypadEnter: 627>, 'KeypadEqual': <ImKey.KeypadEqual: 628>, 'AppBack': <ImKey.AppBack: 629>, 'AppForward': <ImKey.AppForward: 630>, 'GamepadStart': <ImKey.GamepadStart: 631>, 'GamepadBack': <ImKey.GamepadBack: 632>, 'GamepadFaceLeft': <ImKey.GamepadFaceLeft: 633>, 'GamepadFaceRight': <ImKey.GamepadFaceRight: 634>, 'GamepadFaceUp': <ImKey.GamepadFaceUp: 635>, 'GamepadFaceDown': <ImKey.GamepadFaceDown: 636>, 'GamepadDpadLeft': <ImKey.GamepadDpadLeft: 637>, 'GamepadDpadRight': <ImKey.GamepadDpadRight: 638>, 'GamepadDpadUp': <ImKey.GamepadDpadUp: 639>, 'GamepadDpadDown': <ImKey.GamepadDpadDown: 640>, 'GamepadL1': <ImKey.GamepadL1: 641>, 'GamepadR1': <ImKey.GamepadR1: 642>, 'GamepadL2': <ImKey.GamepadL2: 643>, 'GamepadR2': <ImKey.GamepadR2: 644>, 'GamepadL3': <ImKey.GamepadL3: 645>, 'GamepadR3': <ImKey.GamepadR3: 646>, 'GamepadLStickLeft': <ImKey.GamepadLStickLeft: 647>, 'GamepadLStickRight': <ImKey.GamepadLStickRight: 648>, 'GamepadLStickUp': <ImKey.GamepadLStickUp: 649>, 'GamepadLStickDown': <ImKey.GamepadLStickDown: 650>, 'GamepadRStickLeft': <ImKey.GamepadRStickLeft: 651>, 'GamepadRStickRight': <ImKey.GamepadRStickRight: 652>, 'GamepadRStickUp': <ImKey.GamepadRStickUp: 653>, 'GamepadRStickDown': <ImKey.GamepadRStickDown: 654>, 'MouseLeft': <ImKey.MouseLeft: 655>, 'MouseRight': <ImKey.MouseRight: 656>, 'MouseMiddle': <ImKey.MouseMiddle: 657>, 'MouseX1': <ImKey.MouseX1: 658>, 'MouseX2': <ImKey.MouseX2: 659>, 'MouseWheelX': <ImKey.MouseWheelX: 660>, 'MouseWheelY': <ImKey.MouseWheelY: 661>, 'Mod_None': <ImKey.None_: 0>, 'Mod_Ctrl': <ImKey.Mod_Ctrl: 4096>, 'Mod_Shift': <ImKey.Mod_Shift: 8192>, 'Mod_Alt': <ImKey.Mod_Alt: 16384>, 'Mod_Super': <ImKey.Mod_Super: 32768>, 'Mod_Mask_': <ImKey.Mod_Mask_: 61440>, 'NamedKey_BEGIN': <ImKey.Tab: 512>, 'NamedKey_END': <ImKey.NamedKey_END: 666>}
    pass
class InputFlags():
    None_ = 0
    Repeat = 1
    RouteActive = 1024
    RouteAlways = 8192
    RouteFocused = 2048
    RouteFromRootWindow = 131072
    RouteGlobal = 4096
    RouteOverActive = 32768
    RouteOverFocused = 16384
    RouteUnlessBgFocused = 65536
    Tooltip = 262144
    pass
class InputTextFlags():
    AllowTabInput = 32
    AlwaysOverwrite = 2048
    AutoSelectAll = 4096
    CallbackAlways = 1048576
    CallbackCharFilter = 2097152
    CallbackCompletion = 262144
    CallbackEdit = 8388608
    CallbackHistory = 524288
    CallbackResize = 4194304
    CharsDecimal = 1
    CharsHexadecimal = 2
    CharsNoBlank = 16
    CharsScientific = 4
    CharsUppercase = 8
    CtrlEnterForNewLine = 256
    DisplayEmptyRefVal = 16384
    ElideLeft = 131072
    EnterReturnsTrue = 64
    EscapeClearsAll = 128
    NoHorizontalScroll = 32768
    NoUndoRedo = 65536
    None_ = 0
    ParseEmptyRefVal = 8192
    Password = 1024
    ReadOnly = 512
    pass
class IntList():
    """
    Thin wrapper over a std::vector<int>
    """
    def __getitem__(self, index: int) -> int: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, vals: list[int] = []) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, index: int, val: int) -> None: ...
    def append(self, val: int) -> None: 
        """
        Append a value to the end
        """
    def clear(self) -> None: ...
    def pop(self) -> int: 
        """
        Pop a value from the end
        """
    def resize(self, size: int) -> None: 
        """
        Resize the vector, dropping any lost values
        """
    pass
class IntRef():
    """
    A pass-by-ref wrapper for an int
    """
    def __init__(self, val: int = 0) -> None: ...
    def __str__(self) -> str: ...
    @property
    def val(self) -> int:
        """
        The wrapped value

        :type: int
        """
    @val.setter
    def val(self, arg0: int) -> None:
        """
        The wrapped value
        """
    pass
class ItemFlags():
    AllowDuplicateId = 32
    AutoClosePopups = 16
    ButtonRepeat = 8
    NoNav = 2
    NoNavDefaultFocus = 4
    NoTabStop = 1
    None_ = 0
    pass
class KeyData():
    @property
    def AnalogValue(self) -> float:
        """
        :type: float
        """
    @property
    def Down(self) -> bool:
        """
        :type: bool
        """
    @property
    def DownDuration(self) -> float:
        """
        :type: float
        """
    @property
    def DownDurationPrev(self) -> float:
        """
        :type: float
        """
    pass
class ListClipper():
    def Begin(self, items_count: int, items_height: float = -1.0) -> None: ...
    def End(self) -> None: ...
    def IncludeItemByIndex(self, item_index: int) -> None: ...
    def IncludeItemsByIndex(self, item_begin: int, item_end: int) -> None: ...
    def SeekCursorForItem(self, item_index: int) -> None: ...
    def Step(self) -> bool: ...
    def __init__(self) -> None: ...
    @property
    def DisplayEnd(self) -> int:
        """
        :type: int
        """
    @property
    def DisplayStart(self) -> int:
        """
        :type: int
        """
    pass
class ListWrapperBool():
    def __getitem__(self, arg0: int) -> bool: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperDouble():
    def __getitem__(self, arg0: int) -> float: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperImVec2():
    def __getitem__(self, arg0: int) -> ImVec2: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class ListWrapperTCSS():
    def __getitem__(self, arg0: int) -> ImGuiTableColumnSortSpecs: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    pass
class MouseButton():
    Left = 0
    Middle = 2
    Right = 1
    pass
class MouseCursor():
    Arrow = 0
    Hand = 7
    None_ = -1
    NotAllowed = 8
    ResizeAll = 2
    ResizeEW = 4
    ResizeNESW = 5
    ResizeNS = 3
    ResizeNWSE = 6
    TextInput = 1
    pass
class MouseSource():
    Mouse = 0
    Pen = 2
    TouchScreen = 1
    pass
class MultiSelectFlags():
    BoxSelect1d = 64
    BoxSelect2d = 128
    BoxSelectNoScroll = 256
    ClearOnClickVoid = 1024
    ClearOnEscape = 512
    NavWrapX = 65536
    NoAutoClear = 16
    NoAutoClearOnReselect = 32
    NoAutoSelect = 8
    NoRangeSelect = 4
    NoSelectAll = 2
    None = 0
    None_ = 0
    ScopeRect = 4096
    ScopeWindow = 2048
    SelectOnClick = 8192
    SelectOnClickRelease = 16384
    SingleSelect = 1
    pass
class MultiSelectIO():
    @property
    def ItemsCount(self) -> int:
        """
        :type: int
        """
    @property
    def NavIdItem(self) -> int:
        """
        :type: int
        """
    @property
    def NavIdSelected(self) -> bool:
        """
        :type: bool
        """
    @property
    def RangeSrcItem(self) -> int:
        """
        :type: int
        """
    @property
    def RangeSrcReset(self) -> bool:
        """
        :type: bool
        """
    @RangeSrcReset.setter
    def RangeSrcReset(self, arg0: bool) -> None:
        pass
    @property
    def Requests(self) -> ImVector<ImGuiSelectionRequest>:
        """
        :type: ImVector<ImGuiSelectionRequest>
        """
    pass
class PopupFlags():
    AnyPopup = 3072
    AnyPopupId = 1024
    AnyPopupLevel = 2048
    MouseButtonDefault_ = 1
    MouseButtonLeft = 0
    MouseButtonMask_ = 31
    MouseButtonMiddle = 2
    MouseButtonRight = 1
    NoOpenOverExistingPopup = 128
    NoOpenOverItems = 256
    NoReopen = 32
    None_ = 0
    pass
class SelectableFlags():
    AllowDoubleClick = 4
    AllowOverlap = 16
    Disabled = 8
    Highlight = 32
    NoAutoClosePopups = 1
    None_ = 0
    SpanAllColumns = 2
    pass
class SelectionRequest():
    @property
    def RangeDirection(self) -> int:
        """
        :type: int
        """
    @property
    def RangeFirstItem(self) -> int:
        """
        :type: int
        """
    @property
    def RangeLastItem(self) -> int:
        """
        :type: int
        """
    @property
    def Selected(self) -> bool:
        """
        :type: bool
        """
    @property
    def Type(self) -> ImGuiSelectionRequestType:
        """
        :type: ImGuiSelectionRequestType
        """
    pass
class SelectionRequestType():
    None_ = 0
    SetAll = 1
    SetRange = 2
    pass
class SliderFlags():
    AlwaysClamp = 1536
    ClampOnInput = 512
    ClampZeroRange = 1024
    InvalidMask_ = 1879048207
    Logarithmic = 32
    NoInput = 128
    NoRoundToFormat = 64
    NoSpeedTweaks = 2048
    None_ = 0
    WrapAround = 256
    pass
class SortDirection():
    Ascending = 1
    Descending = 2
    None_ = 0
    pass
class StrList():
    """
    Thin wrapper over a std::vector<const char*>
    """
    def __getitem__(self, index: int) -> str: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, vals: list[str] = []) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, index: int, val: str) -> None: ...
    def append(self, val: str) -> None: 
        """
        Append a value to the end
        """
    def clear(self) -> None: ...
    def pop(self) -> str: 
        """
        Pop a value from the end
        """
    def resize(self, size: int) -> None: 
        """
        Resize the vector, dropping any lost values
        """
    pass
class StrRef():
    """
    Thin wrapper over a std::vector<char>
    """
    @typing.overload
    def __init__(self, maxSize: int) -> None: 
        """
        Initialize an empty string with reserved size

        Initialize with an input string. If maxSize=0, then maxSize=len(val)
        """
    @typing.overload
    def __init__(self, value: str, maxSize: int = 0) -> None: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    def append(self, val: str) -> None: 
        """
        Append a value to the end
        """
    def copy(self) -> str: 
        """
        Get a copy of the string
        """
    def pop(self) -> str: 
        """
        Pop a value from the end
        """
    def resize(self, size: int) -> None: 
        """
        Resize the vector, dropping any lost values
        """
    def set(self, newVal: str, maxSize: int = 0) -> None: 
        """
        Assign a new value to the string. If maxSize=0,the maxSize will remain unchanged and extra chars will be dropped
        """
    def view(self) -> str: 
        """
        Get a reference to the string, only valid while this object exists
        """
    pass
class Style():
    def ScaleAllSizes(self, scale_factor: float) -> None: ...
    def __init__(self) -> None: ...
    @property
    def Alpha(self) -> float:
        """
        :type: float
        """
    @Alpha.setter
    def Alpha(self, arg0: float) -> None:
        pass
    @property
    def AntiAliasedFill(self) -> bool:
        """
        :type: bool
        """
    @AntiAliasedFill.setter
    def AntiAliasedFill(self, arg0: bool) -> None:
        pass
    @property
    def AntiAliasedLines(self) -> bool:
        """
        :type: bool
        """
    @AntiAliasedLines.setter
    def AntiAliasedLines(self, arg0: bool) -> None:
        pass
    @property
    def AntiAliasedLinesUseTex(self) -> bool:
        """
        :type: bool
        """
    @AntiAliasedLinesUseTex.setter
    def AntiAliasedLinesUseTex(self, arg0: bool) -> None:
        pass
    @property
    def ButtonTextAlign(self) -> Vec2:
        """
        :type: Vec2
        """
    @ButtonTextAlign.setter
    def ButtonTextAlign(self, arg0: Vec2) -> None:
        pass
    @property
    def CellPadding(self) -> Vec2:
        """
        :type: Vec2
        """
    @CellPadding.setter
    def CellPadding(self, arg0: Vec2) -> None:
        pass
    @property
    def ChildBorderSize(self) -> float:
        """
        :type: float
        """
    @ChildBorderSize.setter
    def ChildBorderSize(self, arg0: float) -> None:
        pass
    @property
    def ChildRounding(self) -> float:
        """
        :type: float
        """
    @ChildRounding.setter
    def ChildRounding(self, arg0: float) -> None:
        pass
    @property
    def CircleTessellationMaxError(self) -> float:
        """
        :type: float
        """
    @CircleTessellationMaxError.setter
    def CircleTessellationMaxError(self, arg0: float) -> None:
        pass
    @property
    def ColorButtonPosition(self) -> ImGuiDir:
        """
        :type: ImGuiDir
        """
    @ColorButtonPosition.setter
    def ColorButtonPosition(self, arg0: ImGuiDir) -> None:
        pass
    @property
    def Colors(self) -> ListWrapper<ImVec4>:
        """
        :type: ListWrapper<ImVec4>
        """
    @property
    def ColumnsMinSpacing(self) -> float:
        """
        :type: float
        """
    @ColumnsMinSpacing.setter
    def ColumnsMinSpacing(self, arg0: float) -> None:
        pass
    @property
    def CurveTessellationTol(self) -> float:
        """
        :type: float
        """
    @CurveTessellationTol.setter
    def CurveTessellationTol(self, arg0: float) -> None:
        pass
    @property
    def DisabledAlpha(self) -> float:
        """
        :type: float
        """
    @DisabledAlpha.setter
    def DisabledAlpha(self, arg0: float) -> None:
        pass
    @property
    def DisplaySafeAreaPadding(self) -> Vec2:
        """
        :type: Vec2
        """
    @DisplaySafeAreaPadding.setter
    def DisplaySafeAreaPadding(self, arg0: Vec2) -> None:
        pass
    @property
    def DisplayWindowPadding(self) -> Vec2:
        """
        :type: Vec2
        """
    @DisplayWindowPadding.setter
    def DisplayWindowPadding(self, arg0: Vec2) -> None:
        pass
    @property
    def FrameBorderSize(self) -> float:
        """
        :type: float
        """
    @FrameBorderSize.setter
    def FrameBorderSize(self, arg0: float) -> None:
        pass
    @property
    def FramePadding(self) -> Vec2:
        """
        :type: Vec2
        """
    @FramePadding.setter
    def FramePadding(self, arg0: Vec2) -> None:
        pass
    @property
    def FrameRounding(self) -> float:
        """
        :type: float
        """
    @FrameRounding.setter
    def FrameRounding(self, arg0: float) -> None:
        pass
    @property
    def GrabMinSize(self) -> float:
        """
        :type: float
        """
    @GrabMinSize.setter
    def GrabMinSize(self, arg0: float) -> None:
        pass
    @property
    def GrabRounding(self) -> float:
        """
        :type: float
        """
    @GrabRounding.setter
    def GrabRounding(self, arg0: float) -> None:
        pass
    @property
    def HoverDelayNormal(self) -> float:
        """
        :type: float
        """
    @HoverDelayNormal.setter
    def HoverDelayNormal(self, arg0: float) -> None:
        pass
    @property
    def HoverDelayShort(self) -> float:
        """
        :type: float
        """
    @HoverDelayShort.setter
    def HoverDelayShort(self, arg0: float) -> None:
        pass
    @property
    def HoverFlagsForTooltipMouse(self) -> int:
        """
        :type: int
        """
    @HoverFlagsForTooltipMouse.setter
    def HoverFlagsForTooltipMouse(self, arg0: int) -> None:
        pass
    @property
    def HoverFlagsForTooltipNav(self) -> int:
        """
        :type: int
        """
    @HoverFlagsForTooltipNav.setter
    def HoverFlagsForTooltipNav(self, arg0: int) -> None:
        pass
    @property
    def HoverStationaryDelay(self) -> float:
        """
        :type: float
        """
    @HoverStationaryDelay.setter
    def HoverStationaryDelay(self, arg0: float) -> None:
        pass
    @property
    def IndentSpacing(self) -> float:
        """
        :type: float
        """
    @IndentSpacing.setter
    def IndentSpacing(self, arg0: float) -> None:
        pass
    @property
    def ItemInnerSpacing(self) -> Vec2:
        """
        :type: Vec2
        """
    @ItemInnerSpacing.setter
    def ItemInnerSpacing(self, arg0: Vec2) -> None:
        pass
    @property
    def ItemSpacing(self) -> Vec2:
        """
        :type: Vec2
        """
    @ItemSpacing.setter
    def ItemSpacing(self, arg0: Vec2) -> None:
        pass
    @property
    def LogSliderDeadzone(self) -> float:
        """
        :type: float
        """
    @LogSliderDeadzone.setter
    def LogSliderDeadzone(self, arg0: float) -> None:
        pass
    @property
    def MouseCursorScale(self) -> float:
        """
        :type: float
        """
    @MouseCursorScale.setter
    def MouseCursorScale(self, arg0: float) -> None:
        pass
    @property
    def PopupBorderSize(self) -> float:
        """
        :type: float
        """
    @PopupBorderSize.setter
    def PopupBorderSize(self, arg0: float) -> None:
        pass
    @property
    def PopupRounding(self) -> float:
        """
        :type: float
        """
    @PopupRounding.setter
    def PopupRounding(self, arg0: float) -> None:
        pass
    @property
    def ScrollbarRounding(self) -> float:
        """
        :type: float
        """
    @ScrollbarRounding.setter
    def ScrollbarRounding(self, arg0: float) -> None:
        pass
    @property
    def ScrollbarSize(self) -> float:
        """
        :type: float
        """
    @ScrollbarSize.setter
    def ScrollbarSize(self, arg0: float) -> None:
        pass
    @property
    def SelectableTextAlign(self) -> Vec2:
        """
        :type: Vec2
        """
    @SelectableTextAlign.setter
    def SelectableTextAlign(self, arg0: Vec2) -> None:
        pass
    @property
    def SeparatorTextAlign(self) -> Vec2:
        """
        :type: Vec2
        """
    @SeparatorTextAlign.setter
    def SeparatorTextAlign(self, arg0: Vec2) -> None:
        pass
    @property
    def SeparatorTextBorderSize(self) -> float:
        """
        :type: float
        """
    @SeparatorTextBorderSize.setter
    def SeparatorTextBorderSize(self, arg0: float) -> None:
        pass
    @property
    def SeparatorTextPadding(self) -> Vec2:
        """
        :type: Vec2
        """
    @SeparatorTextPadding.setter
    def SeparatorTextPadding(self, arg0: Vec2) -> None:
        pass
    @property
    def TabBarBorderSize(self) -> float:
        """
        :type: float
        """
    @TabBarBorderSize.setter
    def TabBarBorderSize(self, arg0: float) -> None:
        pass
    @property
    def TabBarOverlineSize(self) -> float:
        """
        :type: float
        """
    @TabBarOverlineSize.setter
    def TabBarOverlineSize(self, arg0: float) -> None:
        pass
    @property
    def TabBorderSize(self) -> float:
        """
        :type: float
        """
    @TabBorderSize.setter
    def TabBorderSize(self, arg0: float) -> None:
        pass
    @property
    def TabMinWidthForCloseButton(self) -> float:
        """
        :type: float
        """
    @TabMinWidthForCloseButton.setter
    def TabMinWidthForCloseButton(self, arg0: float) -> None:
        pass
    @property
    def TabRounding(self) -> float:
        """
        :type: float
        """
    @TabRounding.setter
    def TabRounding(self, arg0: float) -> None:
        pass
    @property
    def TableAngledHeadersAngle(self) -> float:
        """
        :type: float
        """
    @TableAngledHeadersAngle.setter
    def TableAngledHeadersAngle(self, arg0: float) -> None:
        pass
    @property
    def TableAngledHeadersTextAlign(self) -> Vec2:
        """
        :type: Vec2
        """
    @TableAngledHeadersTextAlign.setter
    def TableAngledHeadersTextAlign(self, arg0: Vec2) -> None:
        pass
    @property
    def TouchExtraPadding(self) -> Vec2:
        """
        :type: Vec2
        """
    @TouchExtraPadding.setter
    def TouchExtraPadding(self, arg0: Vec2) -> None:
        pass
    @property
    def WindowBorderSize(self) -> float:
        """
        :type: float
        """
    @WindowBorderSize.setter
    def WindowBorderSize(self, arg0: float) -> None:
        pass
    @property
    def WindowMenuButtonPosition(self) -> ImGuiDir:
        """
        :type: ImGuiDir
        """
    @WindowMenuButtonPosition.setter
    def WindowMenuButtonPosition(self, arg0: ImGuiDir) -> None:
        pass
    @property
    def WindowMinSize(self) -> Vec2:
        """
        :type: Vec2
        """
    @WindowMinSize.setter
    def WindowMinSize(self, arg0: Vec2) -> None:
        pass
    @property
    def WindowPadding(self) -> Vec2:
        """
        :type: Vec2
        """
    @WindowPadding.setter
    def WindowPadding(self, arg0: Vec2) -> None:
        pass
    @property
    def WindowRounding(self) -> float:
        """
        :type: float
        """
    @WindowRounding.setter
    def WindowRounding(self, arg0: float) -> None:
        pass
    @property
    def WindowTitleAlign(self) -> Vec2:
        """
        :type: Vec2
        """
    @WindowTitleAlign.setter
    def WindowTitleAlign(self, arg0: Vec2) -> None:
        pass
    pass
class StyleVar():
    Alpha = 0
    ButtonTextAlign = 28
    CellPadding = 17
    ChildBorderSize = 8
    ChildRounding = 7
    DisabledAlpha = 1
    FrameBorderSize = 13
    FramePadding = 11
    FrameRounding = 12
    GrabMinSize = 20
    GrabRounding = 21
    IndentSpacing = 16
    ItemInnerSpacing = 15
    ItemSpacing = 14
    PopupBorderSize = 10
    PopupRounding = 9
    ScrollbarRounding = 19
    ScrollbarSize = 18
    SelectableTextAlign = 29
    SeparatorTextAlign = 31
    SeparatorTextBorderSize = 30
    SeparatorTextPadding = 32
    TabBarBorderSize = 24
    TabBorderSize = 23
    TabRounding = 22
    TableAngledHeadersAngle = 26
    TableAngledHeadersTextAlign = 27
    WindowBorderSize = 4
    WindowMinSize = 5
    WindowPadding = 2
    WindowRounding = 3
    WindowTitleAlign = 6
    pass
class TabBarFlags():
    AutoSelectNewTabs = 2
    DrawSelectedOverline = 64
    FittingPolicyDefault_ = 128
    FittingPolicyMask_ = 384
    FittingPolicyResizeDown = 128
    FittingPolicyScroll = 256
    NoCloseWithMiddleMouseButton = 8
    NoTabListScrollingButtons = 16
    NoTooltip = 32
    None_ = 0
    Reorderable = 1
    TabListPopupButton = 4
    pass
class TabItemFlags():
    Leading = 64
    NoCloseWithMiddleMouseButton = 4
    NoPushId = 8
    NoReorder = 32
    NoTooltip = 16
    None_ = 0
    SetSelected = 2
    Trailing = 128
    UnsavedDocument = 1
    pass
class TableBgTarget():
    CellBg = 3
    None_ = 0
    RowBg0 = 1
    RowBg1 = 2
    pass
class TableColumnFlags():
    DefaultHide = 2
    DefaultSort = 4
    Disabled = 1
    IndentDisable = 131072
    IndentEnable = 65536
    IsEnabled = 16777216
    IsHovered = 134217728
    IsSorted = 67108864
    IsVisible = 33554432
    NoClip = 256
    NoHeaderLabel = 4096
    NoHeaderWidth = 8192
    NoHide = 128
    NoReorder = 64
    NoResize = 32
    NoSort = 512
    NoSortAscending = 1024
    NoSortDescending = 2048
    None_ = 0
    PreferSortAscending = 16384
    PreferSortDescending = 32768
    WidthFixed = 16
    WidthStretch = 8
    pass
class TableColumnSortSpecs():
    def __init__(self) -> None: ...
    @property
    def ColumnIndex(self) -> int:
        """
        :type: int
        """
    @ColumnIndex.setter
    def ColumnIndex(self, arg0: int) -> None:
        pass
    @property
    def ColumnUserID(self) -> int:
        """
        :type: int
        """
    @ColumnUserID.setter
    def ColumnUserID(self, arg0: int) -> None:
        pass
    @property
    def SortDirection(self) -> ImGuiSortDirection:
        """
        :type: ImGuiSortDirection
        """
    @SortDirection.setter
    def SortDirection(self, arg1: ImGuiSortDirection) -> None:
        pass
    @property
    def SortOrder(self) -> int:
        """
        :type: int
        """
    @SortOrder.setter
    def SortOrder(self, arg0: int) -> None:
        pass
    pass
class TableFlags():
    Borders = 1920
    BordersH = 384
    BordersInner = 640
    BordersInnerH = 128
    BordersInnerV = 512
    BordersOuter = 1280
    BordersOuterH = 256
    BordersOuterV = 1024
    BordersV = 1536
    ContextMenuInBody = 32
    Hideable = 4
    NoBordersInBody = 2048
    NoBordersInBodyUntilResize = 4096
    NoClip = 1048576
    NoHostExtendX = 65536
    NoHostExtendY = 131072
    NoKeepColumnsVisible = 262144
    NoPadInnerX = 8388608
    NoPadOuterX = 4194304
    NoSavedSettings = 16
    None_ = 0
    PadOuterX = 2097152
    PreciseWidths = 524288
    Reorderable = 2
    Resizable = 1
    RowBg = 64
    ScrollX = 16777216
    ScrollY = 33554432
    SizingFixedFit = 8192
    SizingFixedSame = 16384
    SizingStretchProp = 24576
    SizingStretchSame = 32768
    SortMulti = 67108864
    SortTristate = 134217728
    Sortable = 8
    pass
class TableRowFlags():
    Headers = 1
    None_ = 0
    pass
class TableSortSpecs():
    def __init__(self) -> None: ...
    @property
    def Specs(self) -> ListWrapperTCSS:
        """
        :type: ListWrapperTCSS
        """
    @property
    def SpecsDirty(self) -> bool:
        """
        :type: bool
        """
    @SpecsDirty.setter
    def SpecsDirty(self, arg0: bool) -> None:
        pass
    pass
class Texture():
    @property
    def height(self) -> int:
        """
        :type: int
        """
    @height.setter
    def height(self, arg0: int) -> None:
        pass
    @property
    def texID(self) -> int:
        """
        :type: int
        """
    @texID.setter
    def texID(self, arg0: int) -> None:
        pass
    @property
    def width(self) -> int:
        """
        :type: int
        """
    @width.setter
    def width(self, arg0: int) -> None:
        pass
    pass
class TreeNodeFlags():
    AllowOverlap = 4
    Bullet = 512
    CollapsingHeader = 26
    DefaultOpen = 32
    FramePadding = 1024
    Framed = 2
    LabelSpanAllColumns = 32768
    Leaf = 256
    NavLeftJumpsBackHere = 131072
    NoAutoOpenOnLog = 16
    NoTreePushOnOpen = 8
    None_ = 0
    OpenOnArrow = 128
    OpenOnDoubleClick = 64
    Selected = 1
    SpanAllColumns = 16384
    SpanAvailWidth = 2048
    SpanFullWidth = 4096
    SpanLabelWidth = 8192
    pass
class Vec2():
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float) -> None: ...
    @property
    def x(self) -> float:
        """
        :type: float
        """
    @x.setter
    def x(self, arg0: float) -> None:
        pass
    @property
    def y(self) -> float:
        """
        :type: float
        """
    @y.setter
    def y(self, arg0: float) -> None:
        pass
    pass
class Vec2List():
    """
    Thin wrapper over a std::vector<ImVec2>
    """
    def __getitem__(self, index: int) -> ImVec2: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, vals: list[ImVec2] = []) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, index: int, val: ImVec2) -> None: ...
    def append(self, val: ImVec2) -> None: 
        """
        Append a value to the end
        """
    def clear(self) -> None: ...
    def pop(self) -> ImVec2: 
        """
        Pop a value from the end
        """
    def resize(self, size: int) -> None: 
        """
        Resize the vector, dropping any lost values
        """
    pass
class Vec4():
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None: ...
    @property
    def w(self) -> float:
        """
        :type: float
        """
    @w.setter
    def w(self, arg0: float) -> None:
        pass
    @property
    def x(self) -> float:
        """
        :type: float
        """
    @x.setter
    def x(self, arg0: float) -> None:
        pass
    @property
    def y(self) -> float:
        """
        :type: float
        """
    @y.setter
    def y(self, arg0: float) -> None:
        pass
    @property
    def z(self) -> float:
        """
        :type: float
        """
    @z.setter
    def z(self, arg0: float) -> None:
        pass
    pass
class Viewport():
    @property
    def Flags(self) -> int:
        """
        :type: int
        """
    @property
    def Pos(self) -> Vec2:
        """
        :type: Vec2
        """
    @property
    def Size(self) -> Vec2:
        """
        :type: Vec2
        """
    @property
    def WorkPos(self) -> Vec2:
        """
        :type: Vec2
        """
    @property
    def WorkSize(self) -> Vec2:
        """
        :type: Vec2
        """
    pass
class ViewportFlags():
    IsPlatformMonitor = 2
    IsPlatformWindow = 1
    None_ = 0
    OwnedByApp = 4
    pass
class WCharList():
    """
    Thin wrapper over a std::vector<ImWchar>
    """
    def __getitem__(self, index: int) -> int: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, vals: list[int] = []) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, index: int, val: int) -> None: ...
    def append(self, val: int) -> None: 
        """
        Append a value to the end
        """
    def clear(self) -> None: ...
    def pop(self) -> int: 
        """
        Pop a value from the end
        """
    def resize(self, size: int) -> None: 
        """
        Resize the vector, dropping any lost values
        """
    pass
class WindowFlags():
    AlwaysAutoResize = 64
    AlwaysHorizontalScrollbar = 32768
    AlwaysVerticalScrollbar = 16384
    HorizontalScrollbar = 2048
    MenuBar = 1024
    NoBackground = 128
    NoBringToFrontOnFocus = 8192
    NoCollapse = 32
    NoDecoration = 43
    NoFocusOnAppearing = 4096
    NoInputs = 197120
    NoMouseInputs = 512
    NoMove = 4
    NoNav = 196608
    NoNavFocus = 131072
    NoNavInputs = 65536
    NoResize = 2
    NoSavedSettings = 256
    NoScrollWithMouse = 16
    NoScrollbar = 8
    NoTitleBar = 1
    None_ = 0
    UnsavedDocument = 262144
    pass
def AcceptDragDropPayload(type: str, flags: int = 0) -> ImGuiPayload:
    pass
def AlignTextToFramePadding() -> None:
    pass
def ArrowButton(str_id: str, dir: int) -> bool:
    pass
def Begin(name: str, p_open: typing.Optional[BoolRef] = None, flags: int = 0) -> bool:
    pass
@typing.overload
def BeginChild(id: int, size: Vec2 = Vec2(0, 0), child_flags: int = 0, window_flags: int = 0) -> bool:
    pass
@typing.overload
def BeginChild(str_id: str, size: Vec2 = Vec2(0, 0), child_flags: int = 0, window_flags: int = 0) -> bool:
    pass
def BeginCombo(label: str, preview_value: str, flags: int = 0) -> bool:
    pass
def BeginDisabled(disabled: bool = True) -> None:
    pass
def BeginDragDropSource(flags: int = 0) -> bool:
    pass
def BeginDragDropTarget() -> bool:
    pass
def BeginGroup() -> None:
    pass
def BeginItemTooltip() -> bool:
    pass
def BeginListBox(label: str, size: Vec2 = Vec2(0, 0)) -> bool:
    pass
def BeginMainMenuBar() -> bool:
    pass
def BeginMenu(label: str, enabled: bool = True) -> bool:
    pass
def BeginMenuBar() -> bool:
    pass
def BeginPopup(str_id: str, flags: int = 0) -> bool:
    pass
def BeginPopupContextItem(str_id: typing.Optional[str] = None, popup_flags: int = 1) -> bool:
    pass
def BeginPopupContextVoid(str_id: typing.Optional[str] = None, popup_flags: int = 1) -> bool:
    pass
def BeginPopupContextWindow(str_id: typing.Optional[str] = None, popup_flags: int = 1) -> bool:
    pass
def BeginPopupModal(name: str, p_open: typing.Optional[BoolRef] = None, flags: int = 0) -> bool:
    pass
def BeginTabBar(str_id: str, flags: int = 0) -> bool:
    pass
def BeginTabItem(label: str, p_open: typing.Optional[BoolRef] = None, flags: int = 0) -> bool:
    pass
def BeginTable(str_id: str, column: int, flags: int = 0, outer_size: Vec2 = Vec2(0, 0), inner_width: float = 0.0) -> bool:
    pass
def BeginTooltip() -> bool:
    pass
def Bullet() -> None:
    pass
def BulletText(text: str) -> None:
    pass
def Button(label: str, size: Vec2 = Vec2(0, 0)) -> bool:
    pass
def CalcItemWidth() -> float:
    pass
def CalcTextSize(text: str, hide_text_after_double_hash: bool = False, wrap_width: float = -1.0) -> Vec2:
    pass
def CheckBox(label: str, cur_state: BoolRef) -> bool:
    pass
def CheckBoxFlags(label: str, cur_flags: IntRef, flags_value: int) -> bool:
    pass
def CloseCurrentPopup() -> None:
    pass
@typing.overload
def CollapsingHeader(label: str, flags: int = 0) -> bool:
    pass
@typing.overload
def CollapsingHeader(label: str, p_visible: BoolRef, flags: int = 0) -> bool:
    pass
def ColorButton(desc_id: str, col: Vec4, flags: int = 0, size: Vec2 = Vec2(0, 0)) -> bool:
    pass
def ColorConvertFloat4ToU32(inColor: Vec4) -> int:
    pass
def ColorConvertHSVtoRGB(h: float, s: float, v: float) -> tuple:
    pass
def ColorConvertRGBtoHSV(r: float, g: float, b: float) -> tuple:
    pass
def ColorConvertU32ToFloat4(inColor: int) -> Vec4:
    pass
def ColorEdit3(label: str, col: Vec4, flags: int = 0) -> bool:
    pass
def ColorEdit4(label: str, col: Vec4, flags: int = 0) -> bool:
    pass
def ColorPicker3(label: str, col: Vec4, flags: int = 0) -> bool:
    pass
def ColorPicker4(label: str, col: Vec4, flags: int = 0, ref_col: typing.Optional[Vec4] = None) -> bool:
    pass
def CreateContext(shared_font_atlas: typing.Optional[ImFontAtlas] = None) -> Context:
    pass
def DebugFlashStyleColor(idx: int) -> None:
    pass
def DebugStartItemPicker() -> None:
    pass
def DebugTextEncoding(text: str) -> None:
    pass
def DestroyContext(ctx: typing.Optional[Context] = None) -> None:
    pass
def DragFloat(label: str, value: FloatRef, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: int = 0) -> bool:
    pass
def DragFloat2(label: str, value: FloatList, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: int = 0) -> bool:
    pass
def DragFloat3(label: str, value: FloatList, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: int = 0) -> bool:
    pass
def DragFloat4(label: str, value: FloatList, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: int = 0) -> bool:
    pass
def DragFloatRange2(label: str, v_current_min: FloatRef, v_current_max: FloatRef, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', format_max: typing.Optional[str] = None, flags: int = 0) -> bool:
    pass
def DragInt(label: str, value: IntRef, v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: int = 0) -> bool:
    pass
def DragInt2(label: str, value: IntList, v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: int = 0) -> bool:
    pass
def DragInt3(label: str, value: IntList, v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: int = 0) -> bool:
    pass
def DragInt4(label: str, value: IntList, v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', flags: int = 0) -> bool:
    pass
def DragIntRange2(label: str, v_current_min: IntRef, v_current_max: IntRef, v_speed: float = 1.0, v_min: int = 0, v_max: int = 0, format: str = '%d', format_max: typing.Optional[str] = None, flags: int = 0) -> tuple:
    pass
def Dummy(size: Vec2) -> None:
    pass
def End() -> None:
    pass
def EndChild() -> None:
    pass
def EndCombo() -> None:
    pass
def EndDisabled() -> None:
    pass
def EndDragDropSource() -> None:
    pass
def EndDragDropTarget() -> None:
    pass
def EndFrame() -> None:
    pass
def EndGroup() -> None:
    pass
def EndListBox() -> None:
    pass
def EndMainMenuBar() -> None:
    pass
def EndMenu() -> None:
    pass
def EndMenuBar() -> None:
    pass
def EndPopup() -> None:
    pass
def EndTabBar() -> None:
    pass
def EndTabItem() -> None:
    pass
def EndTable() -> None:
    pass
def EndTooltip() -> None:
    pass
def GetBackgroundDrawList() -> ImDrawList:
    pass
def GetClipboardText() -> str:
    pass
@typing.overload
def GetColorU32(col: Vec4) -> int:
    pass
@typing.overload
def GetColorU32(col: int, alpha_mul: float = 1.0) -> int:
    pass
@typing.overload
def GetColorU32(idx: int, alpha_mul: float = 1.0) -> int:
    pass
def GetContentRegionAvail() -> Vec2:
    pass
def GetCurrentContext() -> Context:
    pass
def GetCursorPos() -> Vec2:
    pass
def GetCursorPosX() -> float:
    pass
def GetCursorPosY() -> float:
    pass
def GetCursorScreenPos() -> Vec2:
    pass
def GetCursorStartPos() -> Vec2:
    pass
def GetDragDropPayload() -> ImGuiPayload:
    pass
def GetDrawData() -> ImDrawData:
    pass
def GetDrawListSharedData() -> ImDrawListSharedData:
    pass
def GetFont() -> ImFont:
    pass
def GetFontSize() -> float:
    pass
def GetFontTexUvWhitePixel() -> Vec2:
    pass
def GetForegroundDrawList() -> ImDrawList:
    pass
def GetFrameCount() -> int:
    pass
def GetFrameHeight() -> float:
    pass
def GetFrameHeightWithSpacing() -> float:
    pass
@typing.overload
def GetID(int_id: int) -> int:
    pass
@typing.overload
def GetID(ptr_id: capsule) -> int:
    pass
@typing.overload
def GetID(str_id: str) -> int:
    pass
@typing.overload
def GetID(str_id_begin: str, str_id_end: str) -> int:
    pass
def GetIO() -> IO:
    pass
def GetItemID() -> int:
    pass
def GetItemRectMax() -> Vec2:
    pass
def GetItemRectMin() -> Vec2:
    pass
def GetItemRectSize() -> Vec2:
    pass
def GetKeyName(key: ImKey) -> str:
    pass
def GetKeyPressedAmount(key: ImKey, repeat_delay: float, rate: float) -> int:
    pass
def GetMainViewport() -> Viewport:
    pass
def GetMouseCursor() -> int:
    pass
def GetMouseDragDelta(button: int = 0, locl_threshold: float = -1.0) -> Vec2:
    pass
def GetMousePos() -> Vec2:
    pass
def GetMousePosOnOpeningCurrentPopup() -> Vec2:
    pass
def GetScrollMaxX() -> float:
    pass
def GetScrollMaxY() -> float:
    pass
def GetScrollX() -> float:
    pass
def GetScrollY() -> float:
    pass
def GetStateStorage() -> ImGuiStorage:
    pass
def GetStyle() -> Style:
    pass
def GetStyleColorName(idx: int) -> str:
    pass
def GetStyleColorVec4(idx: int) -> Vec4:
    pass
def GetTextLineHeight() -> float:
    pass
def GetTextLineHeightWithSpacing() -> float:
    pass
def GetTime() -> float:
    pass
def GetTreeNodeToLabelSpacing() -> float:
    pass
def GetVersion() -> str:
    pass
def GetWindowDrawList() -> ImDrawList:
    pass
def GetWindowHeight() -> float:
    pass
def GetWindowPos() -> Vec2:
    pass
def GetWindowSize() -> Vec2:
    pass
def GetWindowWidth() -> float:
    pass
def Image(texID: Texture, size: Vec2, uv0: Vec2 = Vec2(0, 0), uv1: Vec2 = Vec2(1, 1), tint_col: Vec4 = Vec4(1, 1, 1, 1), border_col: Vec4 = Vec4(0, 0, 0, 0)) -> None:
    pass
def ImageButton(str_id: str, texID: Texture, size: Vec2, uv0: Vec2 = Vec2(0, 0), uv1: Vec2 = Vec2(1, 1), bg_col: Vec4 = Vec4(0, 0, 0, 0), tint_col: Vec4 = Vec4(1, 1, 1, 1)) -> bool:
    pass
def Indent(indent_w: float = 0.0) -> None:
    pass
def InitContextForGLFW(window: capsule, glsl_version: typing.Optional[str] = None) -> None:
    pass
def InputFloat(label: str, v: FloatRef, step: float = 0.0, step_fast: float = 0.0, format: str = '%.3f', flags: int = 0) -> bool:
    """
    Input for a single float value
    """
def InputFloat2(label: str, v: FloatList, format: str = '%.3f', flags: int = 0) -> bool:
    """
    Input for a pair of float values
    """
def InputFloat3(label: str, v: FloatList, format: str = '%.3f', flags: int = 0) -> bool:
    """
    Input for a triplet of floats
    """
def InputFloat4(label: str, v: FloatList, format: str = '%.3f', flags: int = 0) -> bool:
    """
    Input for four floats
    """
def InputInt(label: str, v: IntRef, step: int = 1, step_fast: int = 100, flags: int = 0) -> bool:
    """
    Input for a single int
    """
def InputInt2(label: str, v: IntList, flags: int = 0) -> bool:
    """
    Input for a pair of ints
    """
def InputInt3(label: str, v: IntList, flags: int = 0) -> bool:
    """
    Input for a triplet of ints
    """
def InputInt4(label: str, v: IntList, flags: int = 0) -> bool:
    """
    Input for four ints
    """
def InputText(label: str, value: StrRef, flags: int = 0) -> bool:
    """
    Single line text input
    """
def InputTextMultiline(label: str, value: StrRef, size: Vec2 = Vec2(0, 0), flags: int = 0) -> bool:
    """
    Multiline text input
    """
def InputTextWithHint(label: str, hint: str, value: StrRef, flags: int = 0) -> bool:
    """
    Single line text input with placeholder hint
    """
def InvisibleButton(str_id: str, size: Vec2, flags: int = 0) -> bool:
    pass
def IsAnyItemActive() -> bool:
    pass
def IsAnyItemFocused() -> bool:
    pass
def IsAnyItemHovered() -> bool:
    pass
def IsItemActivated() -> bool:
    pass
def IsItemActive() -> bool:
    pass
def IsItemClicked(mouse_button: int = 0) -> bool:
    pass
def IsItemDeactivated() -> bool:
    pass
def IsItemDeactivatedAfterEdit() -> bool:
    pass
def IsItemEdited() -> bool:
    pass
def IsItemFocused() -> bool:
    pass
def IsItemHovered(flags: int = 0) -> bool:
    pass
def IsItemToggledOpen() -> bool:
    pass
def IsItemVisible() -> bool:
    pass
def IsKeyChordPressed(key_chord: int) -> bool:
    pass
def IsKeyDown(key: ImKey) -> bool:
    pass
def IsKeyPressed(key: ImKey, repeat: bool = True) -> bool:
    pass
def IsKeyReleased(key: ImKey) -> bool:
    pass
def IsMouseClicked(button: int, repeat: bool) -> bool:
    pass
def IsMouseDoubleClicked(button: int) -> bool:
    pass
def IsMouseDown(button: int) -> bool:
    pass
def IsMouseDragging(button: int, lock_threshold: float = -1.0) -> bool:
    pass
def IsMouseHoveringRect(r_min: Vec2, r_max: Vec2, clip: bool = True) -> bool:
    pass
def IsMousePosValid(mouse_pos: typing.Optional[Vec2] = None) -> bool:
    pass
def IsMouseReleased(button: int) -> bool:
    pass
def IsMouseReleasedWithDelay(button: int, delay: float) -> bool:
    pass
def IsPopupOpen(str_id: str, flags: int = 0) -> bool:
    pass
@typing.overload
def IsRectVisible(rect_min: Vec2, rect_max: Vec2) -> bool:
    pass
@typing.overload
def IsRectVisible(size: Vec2) -> bool:
    pass
def IsWindowAppearing() -> bool:
    pass
def IsWindowCollapsed() -> bool:
    pass
def IsWindowFocused(flags: int = 0) -> bool:
    pass
def IsWindowHovered(flags: int = 0) -> bool:
    pass
def LabelText(label: str, text: str) -> None:
    pass
def LoadIniSettingsFromDisk(filename: str) -> None:
    pass
def LoadIniSettingsFromMemory(data: str) -> None:
    pass
def LoadTexture(data: bytes, width: int, height: int, numChannels: int = 3, mipMapLevel: int = 0) -> Texture:
    pass
def LoadTextureFile(filename: str, requestedChannels: int = 0, mipMapLevel: int = 0) -> Texture:
    pass
def LogButtons() -> None:
    pass
def LogFinish() -> None:
    pass
def LogText(text: str) -> None:
    pass
def LogToClipboard(auto_open_depth: int = -1) -> None:
    pass
def LogToFile(auto_open_depth: int = -1, filename: typing.Optional[str] = None) -> None:
    pass
def LogToTTY(auto_open_depth: int = -1) -> None:
    pass
def MenuItem(label: str, shortcut: typing.Optional[str] = None, selected: bool = False, enabled: bool = True) -> bool:
    pass
def NewFrame() -> None:
    pass
def NewLine() -> None:
    pass
@typing.overload
def OpenPopup(id: int, popup_flags: int = 0) -> None:
    pass
@typing.overload
def OpenPopup(str_id: str, popup_flags: int = 0) -> None:
    pass
def OpenPopupOnItemClick(str_id: typing.Optional[str] = None, popup_flags: int = 1) -> None:
    pass
def PopClipRect() -> None:
    pass
def PopFont() -> None:
    pass
def PopID() -> None:
    pass
def PopItemFlag() -> None:
    pass
def PopItemWidth() -> None:
    pass
def PopStyleColor(arg0: int) -> None:
    pass
def PopStyleVar(count: int = 1) -> None:
    pass
def PopTextWrapPos() -> None:
    pass
def ProgressBar(fraction: float, size_arg: Vec2 = Vec2(-FLT_MIN, 0), overlay: typing.Optional[str] = None) -> None:
    pass
def PushClipRect(clip_rect_min: Vec2, clip_rect_max: Vec2, intersect_with_current_clip_rect: bool) -> None:
    pass
def PushFont(font: ImFont) -> None:
    pass
@typing.overload
def PushID(int_id: int) -> None:
    pass
@typing.overload
def PushID(ptr_id: capsule) -> None:
    pass
@typing.overload
def PushID(str_id: str) -> None:
    pass
@typing.overload
def PushID(str_id_begin: str, str_id_end: str) -> None:
    pass
def PushItemFlag(option: int, enabled: bool) -> None:
    pass
def PushItemWidth(item_width: float) -> None:
    pass
@typing.overload
def PushStyleColor(idx: int, col: Vec4) -> None:
    pass
@typing.overload
def PushStyleColor(idx: int, col: int) -> None:
    pass
@typing.overload
def PushStyleVar(idx: int, val: Vec2) -> None:
    pass
@typing.overload
def PushStyleVar(idx: int, val: float) -> None:
    pass
def PushStyleVarX(idx: int, val: float) -> None:
    pass
def PushStyleVarY(idx: int, val: float) -> None:
    pass
def PushTextWrapPos(wrap_local_pos_x: float = 0.0) -> None:
    pass
@typing.overload
def RadioButton(label: str, v: IntRef, v_button: int) -> bool:
    """
    Create a radio button, returns true if pressed


                Shorthand for

                .. code-block:: python

                    curButton = 0
                    if imgui.RadioButton("label", curButton == 1):
                        curButton = 1
    """
@typing.overload
def RadioButton(label: str, value: bool) -> bool:
    pass
def Render(window: capsule, clear_color: Vec4) -> None:
    pass
def ResetMouseDragDelta(button: int = 0) -> None:
    pass
def SameLine(offset_from_start_x: float = 0.0, spacing: float = 1.0) -> None:
    pass
def SaveIniSettingsToDisk(filename: str) -> None:
    pass
def SaveIniSettingsToMemory() -> str:
    pass
def Selectable(label: str, selected: bool = False, flags: int = 0, size: Vec2 = Vec2(0, 0)) -> bool:
    pass
def Separator() -> None:
    pass
def SeparatorText(label: str) -> None:
    pass
def SetClipboardText(text: str) -> None:
    pass
def SetColorEditOptions(flags: int) -> None:
    pass
def SetCurrentContext(ctx: Context) -> None:
    pass
def SetCursorPos(pos: Vec2) -> None:
    pass
def SetCursorPosX(local_x: float) -> None:
    pass
def SetCursorPosY(local_y: float) -> None:
    pass
def SetCursorScreenPos(arg0: Vec2) -> None:
    pass
def SetDragDropPayload(type: str, data: capsule, size: int, cond: int = 0) -> bool:
    pass
def SetItemDefaultFocus() -> None:
    pass
def SetItemKeyOwner(key: ImKey) -> None:
    pass
def SetItemTooltip(value: str) -> None:
    pass
def SetKeyboardFocusHere(offset: int = 0) -> None:
    pass
def SetMouseCursor(cursor_type: int) -> None:
    pass
def SetNextFrameWantCaptureKeyboard(want_capture_keyboard: bool) -> None:
    pass
def SetNextFrameWantCaptureMouse(want_capture_mouse: bool) -> None:
    pass
def SetNextItemAllowOverlap() -> None:
    pass
def SetNextItemOpen(is_open: bool, cond: int = 0) -> None:
    pass
def SetNextItemShortcut(key_chord: int, flags: int = 0) -> None:
    pass
def SetNextItemStorageID(storage_id: int) -> None:
    pass
def SetNextItemWidth(item_width: float) -> None:
    pass
def SetNextWindowBgAlpha(alpha: float) -> None:
    pass
def SetNextWindowCollapsed(collapsed: bool, cond: int = 0) -> None:
    pass
def SetNextWindowContentSize(size: Vec2) -> None:
    pass
def SetNextWindowFocus() -> None:
    pass
def SetNextWindowPos(pos: Vec2, cond: int = 0, pivot: Vec2 = Vec2(0, 0)) -> None:
    pass
def SetNextWindowScroll(scroll: Vec2) -> None:
    pass
def SetNextWindowSize(size: Vec2, cond: int = 0) -> None:
    pass
def SetScrollFromPosX(local_x: float, center_x_ratio: float = 0.5) -> None:
    pass
def SetScrollFromPosY(local_x: float, center_y_ratio: float = 0.5) -> None:
    pass
def SetScrollHereX(center_x_ratio: float = 0.5) -> None:
    pass
def SetScrollHereY(center_y_ratio: float = 0.5) -> None:
    pass
def SetScrollX(scroll_x: float) -> None:
    pass
def SetScrollY(scroll_y: float) -> None:
    pass
def SetStateStorage(storage: ImGuiStorage) -> None:
    pass
def SetTabItemClosed(tab_or_docked_window_label: str) -> None:
    pass
def SetTooltip(value: str) -> None:
    pass
@typing.overload
def SetWindowCollapsed(collapsed: bool, cond: int = 0) -> None:
    pass
@typing.overload
def SetWindowCollapsed(name: str, collapsed: bool, cond: int = 0) -> None:
    pass
@typing.overload
def SetWindowFocus() -> None:
    pass
@typing.overload
def SetWindowFocus(name: str) -> None:
    pass
@typing.overload
def SetWindowPos(name: str, pos: Vec2, cond: int = 0) -> None:
    pass
@typing.overload
def SetWindowPos(pos: Vec2, cond: int = 0) -> None:
    pass
@typing.overload
def SetWindowSize(name: str, pos: Vec2, cond: int = 0) -> None:
    pass
@typing.overload
def SetWindowSize(size: Vec2, cond: int = 0) -> None:
    pass
def Shortcut(key_chord: int, flags: int = 0) -> bool:
    pass
def ShowAboutWindow(p_open: typing.Optional[BoolRef] = None) -> None:
    pass
def ShowDebugLogWindow(p_open: typing.Optional[BoolRef] = None) -> None:
    pass
def ShowDemoWindow(p_open: typing.Optional[BoolRef] = None) -> None:
    pass
def ShowFontSelector(label: str) -> None:
    pass
def ShowMetricsWindow(p_open: typing.Optional[BoolRef] = None) -> None:
    pass
def ShowStackToolWindow(p_open: typing.Optional[BoolRef] = None) -> None:
    pass
def ShowStyleEditor(ref: typing.Optional[Style] = None) -> None:
    pass
def ShowStyleSelector(label: str) -> bool:
    pass
def ShowUserGuide() -> None:
    pass
def Shutdown() -> None:
    pass
def SliderAngle(label: str, v_rad: float, v_deg_min: float = -360.0, v_deg_max: float = 360.0, format: str = '%.0f deg', flags: int = 0) -> tuple:
    pass
def SliderFloat(label: str, v: FloatRef, v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> bool:
    pass
def SliderFloat2(label: str, v: FloatList, v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> bool:
    pass
def SliderFloat3(label: str, v: FloatList, v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> bool:
    pass
def SliderFloat4(label: str, v: FloatList, v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> tuple:
    pass
def SliderInt(label: str, v: IntRef, v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> bool:
    pass
def SliderInt2(label: str, v: IntList, v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> bool:
    pass
def SliderInt3(label: str, v: IntList, v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> bool:
    pass
def SliderInt4(label: str, v: IntList, v_min: int, v_max: int, format: str = '%d', flags: int = 0) -> bool:
    pass
def SmallButton(label: str) -> bool:
    pass
def Spacing() -> None:
    pass
def StyleColorsClassic(dst: typing.Optional[Style] = None) -> None:
    pass
def StyleColorsDark(dst: typing.Optional[Style] = None) -> None:
    pass
def StyleColorsLight(dst: typing.Optional[Style] = None) -> None:
    pass
def TabItemButton(label: str, flags: int = 0) -> bool:
    pass
def TableGetColumnCount() -> int:
    pass
def TableGetColumnFlags(column_n: int = -1) -> int:
    pass
def TableGetColumnIndex() -> int:
    pass
def TableGetColumnName(column_n: int = -1) -> str:
    pass
def TableGetHoveredColumn() -> int:
    pass
def TableGetRowIndex() -> int:
    pass
def TableGetSortSpecs() -> TableSortSpecs:
    pass
def TableHeader(label: str) -> None:
    pass
def TableHeadersRow() -> None:
    pass
def TableNextColumn() -> bool:
    pass
def TableNextRow(row_flags: int = 0, mind_row_height: float = 0.0) -> None:
    pass
def TableSetBgColor(target: int, color: int, column_n: int = -1) -> None:
    pass
def TableSetColumnEnabled(column_n: int, v: bool) -> None:
    pass
def TableSetColumnIndex(column_n: int) -> bool:
    pass
def TableSetupColumn(label: str, flags: int = 0, init_width_or_weight: float = 0.0, user_id: int = 0) -> None:
    pass
def TableSetupScrollFreeze(cols: int, rows: int) -> None:
    pass
def Text(text: str) -> None:
    pass
def TextColored(col: Vec4, text: str) -> None:
    pass
def TextDisabled(text: str) -> None:
    pass
def TextLink(label: str) -> bool:
    pass
def TextLinkOpenURL(label: str, url: str) -> None:
    pass
def TextWrapped(text: str) -> None:
    pass
@typing.overload
def TreeNode(label: str) -> bool:
    pass
@typing.overload
def TreeNode(str_id: str, fmt: str) -> bool:
    pass
@typing.overload
def TreeNodeEx(label: str, flags: int = 0) -> bool:
    pass
@typing.overload
def TreeNodeEx(str_id: str, flags: int, fmt: str) -> bool:
    pass
def TreePop() -> None:
    pass
def TreePush(str_id: str) -> None:
    pass
def Unindent(indent_w: float = 0.0) -> None:
    pass
def UnloadTexture(texture: Texture) -> None:
    pass
def VSliderFloat(label: str, size: Vec2, v: float, v_min: float, v_max: float, format: str = '%.3f', flags: int = 0) -> tuple:
    pass
def VSliderInt(label: str, size: Vec2, v: IntRef, v_min: int, v_max: int, format: str = '%.3f', flags: int = 0) -> bool:
    pass
FLT_MAX = 3.4028234663852886e+38
