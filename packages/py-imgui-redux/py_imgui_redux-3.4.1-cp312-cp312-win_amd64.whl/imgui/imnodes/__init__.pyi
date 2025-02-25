"""ImNodes Library"""
from __future__ import annotations
import imgui.imnodes
import typing
import imgui

__all__ = [
    "AttributeFlags",
    "BeginInputAttribute",
    "BeginNode",
    "BeginNodeEditor",
    "BeginNodeTitleBar",
    "BeginOutputAttribute",
    "BeginStaticAttribute",
    "ClearLinkSelection",
    "ClearNodeSelection",
    "Col",
    "Context",
    "CreateContext",
    "DestroyContext",
    "EditorContextCreate",
    "EditorContextFree",
    "EditorContextGetPanning",
    "EditorContextMoveToNode",
    "EditorContextResetPanning",
    "EditorContextSet",
    "EndInputAttribute",
    "EndNode",
    "EndNodeEditor",
    "EndNodeTitleBar",
    "EndOutputAttribute",
    "EndStaticAttribute",
    "GetCurrentContext",
    "GetIO",
    "GetNodeDimensions",
    "GetNodeEditorSpacePos",
    "GetNodeGridSpacePos",
    "GetNodeScreenSpacePos",
    "GetSelectedLinks",
    "GetSelectedNodes",
    "GetStyle",
    "IO",
    "IsAnyAttributeActive",
    "IsAttributeActive",
    "IsEditorHovered",
    "IsLinkCreated",
    "IsLinkDestroyed",
    "IsLinkDropped",
    "IsLinkHovered",
    "IsLinkSelected",
    "IsLinkStarted",
    "IsNodeHovered",
    "IsNodeSelected",
    "IsPinHovered",
    "Link",
    "LoadCurrentEditorStateFromIniFile",
    "LoadEditorStateFromIniFile",
    "MiniMap",
    "MiniMapLocation",
    "NumSelectedLinks",
    "NumSelectedNodes",
    "PinShape",
    "PopAttributeFlag",
    "PopColorStyle",
    "PopStyleVar",
    "PushAttributeFlag",
    "PushColorStyle",
    "PushStyleVar",
    "SaveCurrentEditorStateToIniFile",
    "SaveCurrentEditorStateToIniString",
    "SaveEditStateToIniString",
    "SaveEditorStateToIniFile",
    "SelectLink",
    "SelectNode",
    "SetCurrentContext",
    "SetNodeDraggable",
    "SetNodeEditorSpacePos",
    "SetNodeGridSpacePos",
    "SetNodeScreenSpacePos",
    "SnapNodeToGrid",
    "Style",
    "StyleColorsClassic",
    "StyleColorsDark",
    "StyleColorsLight",
    "StyleFlags",
    "StyleVar"
]


class AttributeFlags():
    EnableLinkCreationOnSnap = 2
    EnableLinkDetachWithDragClick = 1
    None_ = 0
    pass
class Col():
    BoxSelector = 12
    BoxSelectorOutline = 13
    GridBackground = 14
    GridLine = 15
    GridLinePrimary = 16
    Link = 7
    LinkHovered = 8
    LinkSelected = 9
    MiniMapBackground = 17
    MiniMapBackgroundHovered = 18
    MiniMapCanvas = 27
    MiniMapCanvasOutline = 28
    MiniMapLink = 25
    MiniMapLinkSelected = 26
    MiniMapNodeBackground = 21
    MiniMapNodeBackgroundHovered = 22
    MiniMapNodeBackgroundSelected = 23
    MiniMapNodeOutline = 24
    MiniMapOutline = 19
    MiniMapOutlineHovered = 20
    NodeBackground = 0
    NodeBackgroundHovered = 1
    NodeBackgroundSelected = 2
    NodeOutline = 3
    Pin = 10
    PinHovered = 11
    TitleBar = 4
    TitleBarHovered = 5
    TitleBarSelected = 6
    pass
class Context():
    pass
class IO():
    def SetEmulateThreeButtonMouseMod(self, key: imgui.ImKey) -> None: ...
    def SetLinkDetachedWithModifierClick(self, key: imgui.ImKey) -> None: ...
    def SetMultipleSelectMod(self, key: imgui.ImKey) -> None: ...
    def UnsetEmulateThreeButtonMouseMod(self) -> None: ...
    def UnsetLinkDetachedWithModifierClick(self) -> None: ...
    def UnsetMultipleSelectMod(self) -> None: ...
    def __init__(self) -> None: ...
    @property
    def AltMouseButton(self) -> int:
        """
        :type: int
        """
    @AltMouseButton.setter
    def AltMouseButton(self, arg0: int) -> None:
        pass
    @property
    def AutoPanningSpeed(self) -> float:
        """
        :type: float
        """
    @AutoPanningSpeed.setter
    def AutoPanningSpeed(self, arg0: float) -> None:
        pass
    pass
class MiniMapLocation():
    BottomLeft = 0
    BottomRight = 1
    TopLeft = 2
    TopRight = 3
    pass
class PinShape():
    Circle = 0
    CircleFilled = 1
    Quad = 4
    QuadFilled = 5
    Triangle = 2
    TriangleFilled = 3
    pass
class Style():
    def __init__(self) -> None: ...
    @property
    def Colors(self) -> ListWrapper<unsigned int>:
        """
        :type: ListWrapper<unsigned int>
        """
    @property
    def Flags(self) -> int:
        """
        :type: int
        """
    @Flags.setter
    def Flags(self, arg0: int) -> None:
        pass
    @property
    def GridSpacing(self) -> float:
        """
        :type: float
        """
    @GridSpacing.setter
    def GridSpacing(self, arg0: float) -> None:
        pass
    @property
    def LinkHoverDistance(self) -> float:
        """
        :type: float
        """
    @LinkHoverDistance.setter
    def LinkHoverDistance(self, arg0: float) -> None:
        pass
    @property
    def LinkLineSegmentsPerLength(self) -> float:
        """
        :type: float
        """
    @LinkLineSegmentsPerLength.setter
    def LinkLineSegmentsPerLength(self, arg0: float) -> None:
        pass
    @property
    def LinkThickness(self) -> float:
        """
        :type: float
        """
    @LinkThickness.setter
    def LinkThickness(self, arg0: float) -> None:
        pass
    @property
    def MiniMapOffset(self) -> imgui.Vec2:
        """
        :type: imgui.Vec2
        """
    @MiniMapOffset.setter
    def MiniMapOffset(self, arg0: imgui.Vec2) -> None:
        pass
    @property
    def MiniMapPadding(self) -> imgui.Vec2:
        """
        :type: imgui.Vec2
        """
    @MiniMapPadding.setter
    def MiniMapPadding(self, arg0: imgui.Vec2) -> None:
        pass
    @property
    def NodeBorderThickness(self) -> float:
        """
        :type: float
        """
    @NodeBorderThickness.setter
    def NodeBorderThickness(self, arg0: float) -> None:
        pass
    @property
    def NodeCornerRounding(self) -> float:
        """
        :type: float
        """
    @NodeCornerRounding.setter
    def NodeCornerRounding(self, arg0: float) -> None:
        pass
    @property
    def NodePadding(self) -> imgui.Vec2:
        """
        :type: imgui.Vec2
        """
    @NodePadding.setter
    def NodePadding(self, arg0: imgui.Vec2) -> None:
        pass
    @property
    def PinCircleRadius(self) -> float:
        """
        :type: float
        """
    @PinCircleRadius.setter
    def PinCircleRadius(self, arg0: float) -> None:
        pass
    @property
    def PinHoverRadius(self) -> float:
        """
        :type: float
        """
    @PinHoverRadius.setter
    def PinHoverRadius(self, arg0: float) -> None:
        pass
    @property
    def PinLineThickness(self) -> float:
        """
        :type: float
        """
    @PinLineThickness.setter
    def PinLineThickness(self, arg0: float) -> None:
        pass
    @property
    def PinOffset(self) -> float:
        """
        :type: float
        """
    @PinOffset.setter
    def PinOffset(self, arg0: float) -> None:
        pass
    @property
    def PinQuadSideLength(self) -> float:
        """
        :type: float
        """
    @PinQuadSideLength.setter
    def PinQuadSideLength(self, arg0: float) -> None:
        pass
    @property
    def PinTriangleSideLength(self) -> float:
        """
        :type: float
        """
    @PinTriangleSideLength.setter
    def PinTriangleSideLength(self, arg0: float) -> None:
        pass
    pass
class StyleFlags():
    GridLines = 4
    GridLinesPrimary = 8
    GridSnapping = 16
    NodeOutline = 1
    None_ = 0
    pass
class StyleVar():
    GridSpacing = 0
    LinkHoverDistance = 6
    LinkLineSegmentsPerLength = 5
    LinkThickness = 4
    MiniMapOffset = 14
    MiniMapPadding = 13
    NodeBorderThickness = 3
    NodeCornerRounding = 1
    NodePadding = 2
    PinCircleRadius = 7
    PinHoverRadius = 11
    PinLineThickness = 10
    PinOffset = 12
    PinQuadSideLength = 8
    PinTriangleSideLength = 9
    pass
def BeginInputAttribute(id: int, shape: int = 1) -> None:
    pass
def BeginNode(id: int) -> None:
    pass
def BeginNodeEditor() -> None:
    pass
def BeginNodeTitleBar() -> None:
    pass
def BeginOutputAttribute(id: int, shape: int = 1) -> None:
    pass
def BeginStaticAttribute(id: int) -> None:
    pass
def ClearLinkSelection(link_id: typing.Optional[int] = None) -> None:
    pass
def ClearNodeSelection(node_id: typing.Optional[int] = None) -> None:
    pass
def CreateContext() -> Context:
    pass
def DestroyContext(ctx: typing.Optional[Context] = None) -> None:
    pass
def EditorContextCreate() -> ImNodesEditorContext:
    pass
def EditorContextFree(ctx: ImNodesEditorContext) -> None:
    pass
def EditorContextGetPanning() -> imgui.Vec2:
    pass
def EditorContextMoveToNode(node_id: int) -> None:
    pass
def EditorContextResetPanning(pos: imgui.Vec2) -> None:
    pass
def EditorContextSet(ctx: ImNodesEditorContext) -> None:
    pass
def EndInputAttribute() -> None:
    pass
def EndNode() -> None:
    pass
def EndNodeEditor() -> None:
    pass
def EndNodeTitleBar() -> None:
    pass
def EndOutputAttribute() -> None:
    pass
def EndStaticAttribute() -> None:
    pass
def GetCurrentContext() -> Context:
    pass
def GetIO() -> IO:
    pass
def GetNodeDimensions(id: int) -> imgui.Vec2:
    pass
def GetNodeEditorSpacePos(node_id: int) -> imgui.Vec2:
    pass
def GetNodeGridSpacePos(node_id: int) -> imgui.Vec2:
    pass
def GetNodeScreenSpacePos(node_id: int) -> imgui.Vec2:
    pass
@typing.overload
def GetSelectedLinks() -> imgui.IntList:
    pass
@typing.overload
def GetSelectedLinks(link_ids: imgui.IntList) -> None:
    pass
@typing.overload
def GetSelectedNodes() -> imgui.IntList:
    pass
@typing.overload
def GetSelectedNodes(node_ids: imgui.IntList) -> None:
    pass
def GetStyle() -> Style:
    pass
def IsAnyAttributeActive(attribute_id: imgui.IntRef = None) -> bool:
    """
    Returns true if any attribute is active, I.E. clicked on.
    If not None, sets the passed reference to the ID of the active attribute.
    """
def IsAttributeActive() -> bool:
    pass
def IsEditorHovered() -> bool:
    pass
@typing.overload
def IsLinkCreated(started_at_attribute_id: imgui.IntRef, ended_at_attribute_id: imgui.IntRef, created_from_snap: imgui.BoolRef = None) -> bool:
    pass
@typing.overload
def IsLinkCreated(started_at_node_id: imgui.IntRef, started_at_attribute_id: imgui.IntRef, ended_at_node_id: imgui.IntRef, ended_at_attribute_id: imgui.IntRef, created_from_snap: imgui.BoolRef = None) -> bool:
    pass
def IsLinkDestroyed(arg0: imgui.IntRef) -> bool:
    """
    linkID
    """
def IsLinkDropped(started_at_attribute_id: imgui.IntRef = None, including_detached_links: bool = True) -> bool:
    """
    Did the user drop the dragged link before attaching it to a pin?
    There are two different kinds of situations to consider when handling this event:
    1) a link which is created at a pin and then dropped
    2) an existing link which is detached from a pin and then dropped
    Use the including_detached_links flag to control whether this function triggers when the user
    detaches a link and drops it.
    """
def IsLinkHovered(link_id: imgui.IntRef) -> bool:
    pass
def IsLinkSelected(link_id: int) -> bool:
    pass
def IsLinkStarted(started_at_attribute_id: imgui.IntRef) -> bool:
    """
    Returns true if a new link has been started, but not completed.
    Sets the the passed reference to the ID of the starting attribute.
    """
def IsNodeHovered(node_id: imgui.IntRef) -> bool:
    pass
def IsNodeSelected(node_id: int) -> bool:
    pass
def IsPinHovered(attribute_id: imgui.IntRef) -> bool:
    pass
def Link(id: int, start_attribute_id: int, end_attribute_id: int) -> None:
    pass
def LoadCurrentEditorStateFromIniFile(file_name: str) -> None:
    pass
def LoadEditorStateFromIniFile(editor: ImNodesEditorContext, file_name: str) -> None:
    pass
def MiniMap(size_fraction: float = 0.20000000298023224, location: int = 2) -> None:
    pass
def NumSelectedLinks() -> int:
    pass
def NumSelectedNodes() -> int:
    pass
def PopAttributeFlag() -> None:
    pass
def PopColorStyle() -> None:
    pass
def PopStyleVar(count: int = 1) -> None:
    pass
def PushAttributeFlag(flags: int) -> None:
    pass
def PushColorStyle(item: int, color: int) -> None:
    pass
@typing.overload
def PushStyleVar(style_item: int, value: float) -> None:
    pass
@typing.overload
def PushStyleVar(style_item: int, value: imgui.Vec2) -> None:
    pass
def SaveCurrentEditorStateToIniFile(file_name: str) -> None:
    pass
def SaveCurrentEditorStateToIniString() -> str:
    pass
def SaveEditStateToIniString(editor: ImNodesEditorContext) -> str:
    pass
def SaveEditorStateToIniFile(editor: ImNodesEditorContext, file_name: str) -> None:
    pass
def SelectLink(link_id: int) -> None:
    pass
def SelectNode(node_id: int) -> None:
    pass
def SetCurrentContext(ctx: Context) -> None:
    pass
def SetNodeDraggable(node_id: int, draggable: bool) -> None:
    pass
def SetNodeEditorSpacePos(node_id: int, editor_space_pos: imgui.Vec2) -> None:
    pass
def SetNodeGridSpacePos(node_id: int, grid_pos: imgui.Vec2) -> None:
    pass
def SetNodeScreenSpacePos(node_id: int, scree_space_pos: imgui.Vec2) -> None:
    pass
def SnapNodeToGrid(node_id: int) -> None:
    pass
def StyleColorsClassic(dest: typing.Optional[Style] = None) -> None:
    pass
def StyleColorsDark(dest: typing.Optional[Style] = None) -> None:
    pass
def StyleColorsLight(dest: typing.Optional[Style] = None) -> None:
    pass
