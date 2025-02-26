import typing

from _typeshed import Incomplete

MArgDatabase: Incomplete
MArgList: Incomplete
MArgParser: Incomplete
MArrayDataBuilder: Incomplete
MArrayDataHandle: Incomplete
MAttributeIndex: Incomplete
MAttributePattern: Incomplete
MAttributeSpec: Incomplete
MAttributeSpecArray: Incomplete
MBoundingBox: Incomplete
MCacheSchema: Incomplete
MCallbackId: Incomplete
MCallbackIdArray: Incomplete
MCameraMessage: Incomplete
MColor: Incomplete
MColorArray: Incomplete
MCommandMessage: Incomplete
MConditionMessage: Incomplete
MContainerMessage: Incomplete
MDAGDrawOverrideInfo: Incomplete
MDagMessage: Incomplete
MDagPath: Incomplete
MDagPathArray: Incomplete
MDataBlock: Incomplete
MDataHandle: Incomplete
MDGMessage: Incomplete
MDoubleArray: Incomplete
MEulerRotation: Incomplete
MEvaluationNode: Incomplete
MEvaluationNodeIterator: Incomplete
MEventMessage: Incomplete
MExternalContentInfoTable: Incomplete
MExternalContentLocationTable: Incomplete
MFileObject: Incomplete
MFloatArray: Incomplete
MFloatPoint: Incomplete
MFloatPointArray: Incomplete
MFloatVector: Incomplete
MFloatVectorArray: Incomplete
MFnAssembly: Incomplete
MFnCamera: Incomplete
MFnComponent: Incomplete
MFnComponentListData: Incomplete
MFnContainerNode: Incomplete
MFnDagNode: Incomplete
MFnDisplayLayer: Incomplete
MFnDisplayLayerManager: Incomplete
MFnDoubleArrayData: Incomplete
MFnDoubleIndexedComponent: Incomplete
MFnGeometryData: Incomplete
MFnIntArrayData: Incomplete
MFnMatrixArrayData: Incomplete
MFnMatrixData: Incomplete
MFnMesh: Incomplete
MFnMeshData: Incomplete
MFnNurbsCurve: Incomplete
MFnNurbsCurveData: Incomplete
MFnNurbsSurface: Incomplete
MFnNurbsSurfaceData: Incomplete
MFnPlugin: Incomplete
MFnPluginData: Incomplete
MFnPointArrayData: Incomplete
MFnReference: Incomplete
MFnSet: Incomplete
MFnSingleIndexedComponent: Incomplete
MFnStringArrayData: Incomplete
MFnStringData: Incomplete
MFnTransform: Incomplete
MFnTripleIndexedComponent: Incomplete
MFnUInt64ArrayData: Incomplete
MFnVectorArrayData: Incomplete
MGlobal: Incomplete
MImage: Incomplete
MInt64Array: Incomplete
MIntArray: Incomplete
MItCurveCV: Incomplete
MItDag: Incomplete
MItDependencyGraph: Incomplete
MItDependencyNodes: Incomplete
MIteratorType: Incomplete
MItGeometry: Incomplete
MItMeshEdge: Incomplete
MItMeshFaceVertex: Incomplete
MItMeshPolygon: Incomplete
MItMeshVertex: Incomplete
MItSelectionList: Incomplete
MItSurfaceCV: Incomplete
MLockMessage: Incomplete
MMatrixArray: Incomplete
MMeshIntersector: Incomplete
MMeshIsectAccelParams: Incomplete
MMeshSmoothOptions: Incomplete
MMessage: Incomplete
MModelMessage: Incomplete
MNamespace: Incomplete
MNodeCacheDisablingInfo: Incomplete
MNodeCacheSetupInfo: Incomplete
MNodeClass: Incomplete
MNodeMessage: Incomplete
MObjectArray: Incomplete
MObjectHandle: Incomplete
MObjectSetMessage: Incomplete
MPlane: Incomplete
MPlugArray: Incomplete
MPoint: Incomplete
MPointArray: Incomplete
MPointOnMesh: Incomplete
MPolyMessage: Incomplete
MPxAttributePatternFactory: Incomplete
MPxCommand: Incomplete
MPxData: Incomplete
MPxGeometryData: Incomplete
MPxGeometryIterator: Incomplete
MPxNode: Incomplete
MPxSurfaceShape: Incomplete
MQuaternion: Incomplete
MRampAttribute: Incomplete
MRichSelection: Incomplete
MSceneMessage: Incomplete
MSelectionList: Incomplete
MSelectionMask: Incomplete
MSyntax: Incomplete
MTimeArray: Incomplete
MTimeRange: Incomplete
MTimerMessage: Incomplete
MUint64Array: Incomplete
MUintArray: Incomplete
MURI: Incomplete
MUserData: Incomplete
MUserEventMessage: Incomplete
MUuid: Incomplete
MVector: Incomplete
MVectorArray: Incomplete
MWeight: Incomplete

_MFnType: typing.TypeAlias = int

class MFnBase:
    @typing.overload
    def hasObj(self, type: _MFnType, /) -> bool: ...
    @typing.overload
    def hasObj(self, object: MObject, /) -> bool: ...
    def object(self) -> MObject: ...
    def setObject(self, object: MObject, /) -> typing.Self: ...
    def type(self) -> _MFnType: ...

class MObject:
    kNullObj: MObject

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MObject, /) -> None: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __ne__(self, value: object, /) -> bool: ...
    def apiType(self) -> _MFnType: ...
    def hasFn(self, fn: _MFnType, /) -> bool: ...
    def isNull(self) -> bool: ...
    @property
    def apiTypeStr(self) -> str: ...

class MTypeId:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MTypeId, /) -> None: ...
    @typing.overload
    def __init__(self, id: int, /) -> None: ...
    @typing.overload
    def __init__(self, prefix: int, id: int, /) -> None: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __ne__(self, value: object, /) -> bool: ...
    def id(self) -> int: ...

_DisconnectBehavior: typing.TypeAlias = typing.Literal[0, 1, 2]

class MFnAttribute(MFnBase):
    kDelete: typing.Literal[0]
    kReset: typing.Literal[1]
    kNothing: typing.Literal[2]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def accepts(self, type: MTypeId | _MFnType, /) -> bool: ...
    def acceptsAttribute(self, attr: MFnAttribute, /) -> bool: ...
    def addToCategory(self, category: str, /) -> bool: ...
    def getAddAttrCmd(self, longFlags: bool) -> str: ...
    def hasCategory(self, category: str, /) -> str: ...
    def pathName(self) -> str: ...
    def setNiceNameOverride(self, localizedName: str, /) -> None: ...
    @property
    def affectsAppearance(self) -> bool: ...
    @affectsAppearance.setter
    def affectsAppearance(self, value: bool) -> None: ...
    @property
    def affectsWorldSpace(self) -> bool: ...
    @affectsWorldSpace.setter
    def affectsWorldSpace(self, value: bool) -> None: ...
    @property
    def array(self) -> bool: ...
    @array.setter
    def array(self, value: bool) -> None: ...
    @property
    def cached(self) -> bool: ...
    @cached.setter
    def cached(self, value: bool) -> None: ...
    @property
    def channelBox(self) -> bool: ...
    @channelBox.setter
    def channelBox(self, value: bool) -> None: ...
    @property
    def connectable(self) -> bool: ...
    @connectable.setter
    def connectable(self, value: bool) -> None: ...
    @property
    def disconnectBehavior(self) -> _DisconnectBehavior: ...
    @disconnectBehavior.setter
    def disconnectBehavior(self, value: _DisconnectBehavior) -> None: ...
    @property
    def dynamic(self) -> bool: ...
    @property
    def enforcingUniqueName(self) -> bool: ...
    @property
    def extension(self) -> bool: ...
    @property
    def hidden(self) -> bool: ...
    @hidden.setter
    def hidden(self, value: bool) -> None: ...
    @property
    def indeterminant(self) -> bool: ...
    @indeterminant.setter
    def indeterminant(self, value: bool) -> None: ...
    @property
    def indexMatters(self) -> bool: ...
    @indexMatters.setter
    def indexMatters(self, value: bool) -> None: ...
    @property
    def internal(self) -> bool: ...
    @internal.setter
    def internal(self, value: bool) -> None: ...
    @property
    def isProxyAttribute(self) -> bool: ...
    @property
    def keyable(self) -> bool: ...
    @keyable.setter
    def keyable(self, value: bool) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def parent(self) -> bool: ...
    @parent.setter
    def parent(self, value: MObject) -> None: ...
    @property
    def readable(self) -> bool: ...
    @readable.setter
    def readable(self, value: bool) -> None: ...
    @property
    def renderSource(self) -> bool: ...
    @renderSource.setter
    def renderSource(self, value: bool) -> None: ...
    @property
    def shortName(self) -> str: ...
    @property
    def storable(self) -> bool: ...
    @storable.setter
    def storable(self, value: bool) -> None: ...
    @property
    def usedAsColor(self) -> bool: ...
    @usedAsColor.setter
    def usedAsColor(self, value: bool) -> None: ...
    @property
    def usedAsFilename(self) -> bool: ...
    @usedAsFilename.setter
    def usedAsFilename(self, value: bool) -> None: ...
    @property
    def usesArrayDataBuilder(self) -> bool: ...
    @usesArrayDataBuilder.setter
    def usesArrayDataBuilder(self, value: bool) -> None: ...
    @property
    def worldSpace(self) -> bool: ...
    @worldSpace.setter
    def worldSpace(self, value: bool) -> None: ...
    @property
    def writable(self) -> bool: ...
    @writable.setter
    def writable(self, value: bool) -> None: ...

_MFnDataType: typing.TypeAlias = typing.Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26,
]  # fmt: off

class MFnData:
    kInvalid: typing.Literal[0]
    kNumeric: typing.Literal[1]
    kPlugin: typing.Literal[2]
    kPluginGeometry: typing.Literal[3]
    kString: typing.Literal[4]
    kMatrix: typing.Literal[5]
    kStringArray: typing.Literal[6]
    kDoubleArray: typing.Literal[7]
    kFloatArray: typing.Literal[8]
    kIntArray: typing.Literal[9]
    kPointArray: typing.Literal[10]
    kVectorArray: typing.Literal[11]
    kMatrixArray: typing.Literal[12]
    kComponentList: typing.Literal[13]
    kMesh: typing.Literal[14]
    kLattice: typing.Literal[15]
    kNurbsCurve: typing.Literal[16]
    kNurbsSurface: typing.Literal[17]
    kSphere: typing.Literal[18]
    kDynArrayAttrs: typing.Literal[19]
    kDynSweptGeometry: typing.Literal[20]
    kSubdSurface: typing.Literal[21]
    kNObject: typing.Literal[22]
    kNId: typing.Literal[23]
    kAny: typing.Literal[24]
    kFalloffFunction: typing.Literal[25]
    kLast: typing.Literal[26]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...

_MFnNumericDataType: typing.TypeAlias = typing.Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
]  # fmt: off

class MFnNumericData(MFnData):
    kInvalid: typing.Literal[0]
    kBoolean: typing.Literal[1]
    kByte: typing.Literal[2]
    kChar: typing.Literal[3]
    kShort: typing.Literal[4]
    k2Short: typing.Literal[5]
    k3Short: typing.Literal[6]
    kInt: typing.Literal[7]
    kLong: typing.Literal[7]
    k2Int: typing.Literal[8]
    k2Long: typing.Literal[8]
    k3Int: typing.Literal[9]
    k3Long: typing.Literal[9]
    kInt64: typing.Literal[10]
    kFloat: typing.Literal[11]
    k2Float: typing.Literal[12]
    k3Float: typing.Literal[13]
    kDouble: typing.Literal[14]
    k2Double: typing.Literal[15]
    k3Double: typing.Literal[16]
    k4Double: typing.Literal[17]
    kAddr: typing.Literal[18]
    kLast: typing.Literal[19]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def create(self, type: _MFnNumericDataType, /) -> MObject: ...
    def getData(self) -> list[float]: ...
    def numericType(self) -> int: ...
    def setData(self, seq: list[float], /) -> typing.Self: ...

class MMatrix:
    kTolerance: float = 1e-10
    kIdentity: MMatrix

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MMatrix, /) -> None: ...
    @typing.overload
    def __init__(self, values: typing.Iterable[float], /) -> None: ...  # 16 floats
    @typing.overload
    def __init__(
        self,
        values: typing.Sequence[typing.Sequence[float]],
        /,
    ) -> None: ...  # 4 sequences of 4 float
    def __add__(self, value: MMatrix, /) -> MMatrix: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __getitem__(self, key: int, /) -> float: ...
    def __iadd__(self, value: MMatrix, /) -> typing.Self: ...
    def __imul__(self, value: MMatrix | float, /) -> typing.Self: ...
    def __isub__(self, value: MMatrix, /) -> typing.Self: ...
    def __len__(self) -> typing.Literal[16]: ...
    def __mul__(self, value: MMatrix | float, /) -> MMatrix: ...
    def __ne__(self, value: object, /) -> bool: ...
    def __rmul__(self, value: MMatrix | float, /) -> MMatrix: ...
    def __setitem__(self, key: int, value: float, /) -> None: ...
    def __sub__(self, value: MMatrix, /) -> MMatrix: ...
    def adjoint(self) -> MMatrix: ...
    def det3x3(self) -> float: ...
    def det4x4(self) -> float: ...
    def getElement(self, row: int, col: int, /) -> float: ...
    def homogenize(self) -> MMatrix: ...
    def inverse(self) -> MMatrix: ...
    def isEquivalent(
        self, other: MMatrix, /, tolerance: float = kTolerance
    ) -> bool: ...
    def isSingular(self) -> bool: ...
    def setElement(self, row: int, col: int, value: float, /) -> typing.Self: ...
    def setToIdentity(self) -> typing.Self: ...
    def setToProduct(self, left: MMatrix, right: MMatrix, /) -> typing.Self: ...
    def transpose(self) -> MMatrix: ...

class MFloatMatrix:
    kTolerance: float = 9.9999997473787e-06
    kIdentity: MMatrix

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MFloatMatrix, /) -> None: ...
    @typing.overload
    def __init__(self, values: typing.Iterable[float], /) -> None: ...  # 16 floats
    @typing.overload
    def __init__(
        self, values: typing.Sequence[typing.Sequence[float]], /
    ) -> None: ...  # 4 sequences of 4 float
    def __add__(self, value: MFloatMatrix, /) -> MFloatMatrix: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __getitem__(self, key: int, /) -> float: ...
    def __iadd__(self, value: MFloatMatrix, /) -> typing.Self: ...
    def __imul__(self, value: MFloatMatrix | float, /) -> typing.Self: ...
    def __isub__(self, value: MFloatMatrix, /) -> typing.Self: ...
    def __len__(self) -> typing.Literal[16]: ...
    def __mul__(self, value: MFloatMatrix | float, /) -> MFloatMatrix: ...
    def __ne__(self, value: object, /) -> bool: ...
    def __rmul__(self, value: MFloatMatrix | float, /) -> MFloatMatrix: ...
    def __setitem__(self, key: int, value: float, /) -> None: ...
    def __sub__(self, value: MFloatMatrix, /) -> MFloatMatrix: ...
    def adjoint(self) -> MFloatMatrix: ...
    def det3x3(self) -> float: ...
    def det4x4(self) -> float: ...
    def getElement(self, row: int, col: int, /) -> float: ...
    def homogenize(self) -> MFloatMatrix: ...
    def inverse(self) -> MFloatMatrix: ...
    def isEquivalent(
        self, other: MFloatMatrix, /, tolerance: float = kTolerance
    ) -> bool: ...
    def setElement(self, row: int, col: int, value: float, /) -> typing.Self: ...
    def setToIdentity(self) -> typing.Self: ...
    def setToProduct(
        self, left: MFloatMatrix, right: MFloatMatrix, /
    ) -> typing.Self: ...
    def transpose(self) -> MFloatMatrix: ...

_MTransformationMatrixRotationOrder: typing.TypeAlias = typing.Literal[
    0, 1, 2, 3, 4, 5, 6, 7,
]  # fmt: skip

class MTransformationMatrix:
    kTolerance: float = 1e-10
    kIdentity: MTransformationMatrix
    kInvalid: typing.Literal[0]
    kXYZ: typing.Literal[1]
    kYZX: typing.Literal[2]
    kZXY: typing.Literal[3]
    kXZY: typing.Literal[4]
    kYXZ: typing.Literal[5]
    kZYX: typing.Literal[6]
    kLast: typing.Literal[7]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MTransformationMatrix | MMatrix, /) -> None: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __ne__(self, value: object, /) -> bool: ...
    def asMatrix(self, interp: float = 1.0) -> MMatrix: ...
    def asMatrixInverse(self) -> MMatrix: ...
    def asRotateMatrix(self) -> MMatrix: ...
    def asScaleMatrix(self) -> MMatrix: ...
    def isEquivalent(
        self, other: MTransformationMatrix, /, tolerance: float = kTolerance
    ) -> bool: ...
    def reorderRotation(
        self, order: _MTransformationMatrixRotationOrder, /
    ) -> typing.Self: ...
    def rotateBy(
        self, rot: MQuaternion | MEulerRotation, space: _MSpaceSpace, /
    ) -> typing.Self: ...
    def rotateByComponents(
        self,
        seq: typing.Sequence[float],
        space: _MSpaceSpace,
        asQuaternion: bool = False,
        /,
    ) -> typing.Self: ...
    def rotatePivot(self, space: _MSpaceSpace, /) -> MPoint: ...
    def rotatePivotTranslation(self, space: _MSpaceSpace, /) -> MVector: ...
    @typing.overload
    def rotation(
        self, asQuaternion: typing.Literal[False] = False
    ) -> MEulerRotation: ...
    @typing.overload
    def rotation(self, asQuaternion: typing.Literal[True]) -> MQuaternion: ...
    @typing.overload
    def rotationComponents(
        self, asQuaternion: typing.Literal[False] = False
    ) -> list[int]: ...  # [x, y, z, order]
    @typing.overload
    def rotationComponents(
        self, asQuaternion: typing.Literal[True]
    ) -> list[int]: ...  # [x, y, z, w]
    def rotationOrder(self) -> _MTransformationMatrixRotationOrder: ...
    def rotationOrientation(self) -> MQuaternion: ...
    def scale(self, space: _MSpaceSpace, /) -> list[float]: ...  # [sx, sy, sz]
    def scaleBy(
        self,
        seq: typing.Sequence[float],  # [sx, sy, sz]
        space: _MSpaceSpace,
        /,
    ) -> typing.Self: ...
    def scalePivot(self, space: _MSpaceSpace, /) -> MPoint: ...
    def scalePivotTranslation(self, space: _MSpaceSpace, /) -> MVector: ...
    def setRotatePivot(
        self, trans: MPoint, space: _MSpaceSpace, balance: bool, /
    ) -> typing.Self: ...
    def setRotatePivotTranslation(
        self, trans: MVector, space: _MSpaceSpace, /
    ) -> typing.Self: ...
    def setRotation(self, rot: MQuaternion | MEulerRotation, /) -> typing.Self: ...
    @typing.overload
    def setRotationComponents(
        self,
        seq: typing.Sequence[float],  # [rx, ry, rz, order]
        asQuaternion: typing.Literal[False] = False,
        /,
    ) -> typing.Self: ...
    @typing.overload
    def setRotationComponents(
        self,
        seq: typing.Sequence[float],  # [qx, qy, qz, qw]
        /,
        asQuaternion: typing.Literal[True],
    ) -> typing.Self: ...
    def setRotationOrientation(self, rot: MQuaternion, /) -> typing.Self: ...
    def setScale(
        self,
        seq: typing.Sequence[float],  # [sx, sy, sz]
        space: _MSpaceSpace,
        /,
    ) -> typing.Self: ...
    def setScalePivot(
        self, pivot: MPoint, space: _MSpaceSpace, balance: bool, /
    ) -> typing.Self: ...
    def setScalePivotTranslation(
        self, trans: MVector, space: _MSpaceSpace, /
    ) -> typing.Self: ...
    def setShear(
        self,
        seq: typing.Sequence[float],  # [x, y, z]
        space: _MSpaceSpace,
        /,
    ) -> typing.Self: ...
    def setToRotationAxis(self, axis: MVector, rot: float, /) -> typing.Self: ...
    def setTranslation(self, trans: MVector, space: _MSpaceSpace, /) -> typing.Self: ...
    def shear(self, space: _MSpaceSpace, /) -> list[float]: ...
    def shearBy(
        self,
        seq: typing.Sequence[float],  # [x, y, z]
        space: _MSpaceSpace,
        /,
    ) -> typing.Self: ...
    def translateBy(self, vec: MVector, space: _MSpaceSpace, /) -> typing.Self: ...
    def translation(self, space: _MSpaceSpace, /) -> MVector: ...

_MSpaceSpace: typing.TypeAlias = typing.Literal[0, 1, 2, 3, 4, 5]

class MSpace:
    kInvalid: typing.Literal[0]
    kTransform: typing.Literal[1]
    kPreTransform: typing.Literal[2]
    kObject: typing.Literal[2]
    kPostTransform: typing.Literal[3]
    kWorld: typing.Literal[4]
    kLast: typing.Literal[5]

_MAngleUnit: typing.TypeAlias = typing.Literal[0, 1, 2, 3, 4, 5]

class MAngle:
    kInvalid: typing.Literal[0]
    kRadians: typing.Literal[1]
    kDegrees: typing.Literal[2]
    kAngMinutes: typing.Literal[3]
    kAngSeconds: typing.Literal[4]
    kLast: typing.Literal[5]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MAngle) -> None: ...
    @typing.overload
    def __init__(self, value: float, unit: _MAngleUnit = kRadians) -> None: ...
    def asAngMinutes(self) -> float: ...
    def asAngSeconds(self) -> float: ...
    def asDegrees(self) -> float: ...
    def asRadians(self) -> float: ...
    def asUnits(self, unit: _MAngleUnit, /) -> float: ...
    @staticmethod
    def internalToUI(internalValue: float, /) -> float: ...
    @staticmethod
    def internalUnit() -> _MAngleUnit: ...
    @staticmethod
    def setUIUnit(newUnit: _MAngleUnit, /) -> None: ...
    @staticmethod
    def uiToInternal(uiValue: float, /) -> float: ...
    @staticmethod
    def uiUnit() -> _MAngleUnit: ...
    @property
    def unit(self) -> _MAngleUnit: ...
    @unit.setter
    def unit(self, value: _MAngleUnit) -> None: ...
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, value: float) -> None: ...

_MDistanceUnit: typing.TypeAlias = typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class MDistance:
    kInvalid: typing.Literal[0]
    kInches: typing.Literal[1]
    kFeet: typing.Literal[2]
    kYards: typing.Literal[3]
    kMiles: typing.Literal[4]
    kMillimeters: typing.Literal[5]
    kCentimeters: typing.Literal[6]
    kKilometers: typing.Literal[7]
    kMeters: typing.Literal[8]
    kLast: typing.Literal[9]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MDistance) -> None: ...
    @typing.overload
    def __init__(self, value: float, unit: _MDistanceUnit = kCentimeters) -> None: ...
    def asFeet(self) -> float: ...
    def asInches(self) -> float: ...
    def asKilometers(self) -> float: ...
    def asMeters(self) -> float: ...
    def asMiles(self) -> float: ...
    def asMillimeters(self) -> float: ...
    def asUnits(self, unit: _MDistanceUnit, /) -> float: ...
    def asYards(self) -> float: ...
    @staticmethod
    def internalToUI(internalValue: float, /) -> float: ...
    @staticmethod
    def internalUnit() -> _MDistanceUnit: ...
    @staticmethod
    def setUIUnit(newUnit: _MDistanceUnit, /) -> None: ...
    @staticmethod
    def uiToInternal(uiValue: float, /) -> float: ...
    @staticmethod
    def uiUnit() -> _MDistanceUnit: ...
    @property
    def unit(self) -> _MDistanceUnit: ...
    @unit.setter
    def unit(self, value: _MDistanceUnit) -> None: ...
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, value: float) -> None: ...

_MTimeUnit: typing.TypeAlias = typing.Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
    37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
]  # fmt: skip

class MTime:
    kInvalid: typing.Literal[0]
    kHours: typing.Literal[1]
    kMinutes: typing.Literal[2]
    kSeconds: typing.Literal[3]
    kMilliseconds: typing.Literal[4]
    kGames: typing.Literal[5]  # NOTE: deprecated
    k15FPS: typing.Literal[5]
    kFilm: typing.Literal[6]  # NOTE: deprecated
    k24FPS: typing.Literal[6]
    kPALFrame: typing.Literal[7]  # NOTE: deprecated
    k25FPS: typing.Literal[7]
    kNTSCFrame: typing.Literal[8]  # NOTE: deprecated
    k30FPS: typing.Literal[8]
    kShowScan: typing.Literal[9]  # NOTE: deprecated
    k48FPS: typing.Literal[9]
    kPALField: typing.Literal[10]  # NOTE: deprecated
    k50FPS: typing.Literal[10]
    kNTSCField: typing.Literal[11]  # NOTE: deprecated
    k60FPS: typing.Literal[11]
    k2FPS: typing.Literal[12]
    k3FPS: typing.Literal[13]
    k4FPS: typing.Literal[14]
    k5FPS: typing.Literal[15]
    k6FPS: typing.Literal[16]
    k8FPS: typing.Literal[17]
    k10FPS: typing.Literal[18]
    k12FPS: typing.Literal[19]
    k16FPS: typing.Literal[20]
    k20FPS: typing.Literal[21]
    k40FPS: typing.Literal[22]
    k75FPS: typing.Literal[23]
    k80FPS: typing.Literal[24]
    k100FPS: typing.Literal[25]
    k120FPS: typing.Literal[26]
    k125FPS: typing.Literal[27]
    k150FPS: typing.Literal[28]
    k200FPS: typing.Literal[29]
    k240FPS: typing.Literal[30]
    k250FPS: typing.Literal[31]
    k300FPS: typing.Literal[32]
    k375FPS: typing.Literal[33]
    k400FPS: typing.Literal[34]
    k500FPS: typing.Literal[35]
    k600FPS: typing.Literal[36]
    k750FPS: typing.Literal[37]
    k1200FPS: typing.Literal[38]
    k1500FPS: typing.Literal[39]
    k2000FPS: typing.Literal[40]
    k3000FPS: typing.Literal[41]
    k6000FPS: typing.Literal[42]
    k23_976FPS: typing.Literal[43]
    k29_97FPS: typing.Literal[44]
    k29_97DF: typing.Literal[45]
    k47_952FPS: typing.Literal[46]
    k59_94FPS: typing.Literal[47]
    k44100FPS: typing.Literal[48]
    k48000FPS: typing.Literal[49]
    k90FPS: typing.Literal[50]
    k119_88FPS: typing.Literal[51]
    kUserDef: typing.Literal[52]
    kLast: typing.Literal[53]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MTime) -> None: ...
    @typing.overload
    def __init__(self, value: float, unit: _MTimeUnit = k24FPS) -> None: ...
    def __add__(self, value: MTime, /) -> MTime: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __qe__(self, value: MTime, /) -> bool: ...
    def __gt__(self, value: MTime, /) -> bool: ...
    def __iadd__(self, value: MTime, /) -> typing.Self: ...
    def __imul__(self, value: MTime, /) -> typing.Self: ...
    def __isub__(self, value: MTime, /) -> typing.Self: ...
    def __itruediv__(self, value: MTime, /) -> typing.Self: ...
    def __le__(self, value: MTime, /) -> bool: ...
    def __lt__(self, value: MTime, /) -> bool: ...
    def __mul__(self, value: MTime, /) -> MTime: ...
    def __ne__(self, value: object, /) -> bool: ...
    def __radd__(self, value: MTime, /) -> MTime: ...
    def __rmul__(self, value: MTime, /) -> MTime: ...
    def __rsub__(self, value: MTime, /) -> MTime: ...
    def __rtruediv__(self, value: MTime, /) -> MTime: ...
    def __sub__(self, value: MTime, /) -> MTime: ...
    def __truediv__(self, value: MTime, /) -> MTime: ...
    def asUnits(self, unit: _MTimeUnit, /) -> float: ...
    @staticmethod
    def setUIUnit(newUnit: _MTimeUnit, /) -> None: ...
    @staticmethod
    def ticksPerSecond() -> int: ...
    @staticmethod
    def uiUnit() -> _MTimeUnit: ...
    @property
    def unit(self) -> _MTimeUnit: ...
    @unit.setter
    def unit(self, value: _MTimeUnit) -> None: ...
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, value: float) -> None: ...

class MFnMessageAttribute(MFnAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def create(self, longName: str, shortName: str, /) -> MObject: ...

class MFnEnumAttribute(MFnAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def addField(self, name: str, value: int, /) -> typing.Self: ...
    def create(
        self, longName: str, shortName: str, /, defaultValue: int = 0
    ) -> MObject: ...
    def fieldName(self, value: int, /) -> str: ...
    def fieldValue(self, name: str, /) -> int: ...
    def getMax(self) -> int: ...
    def getMin(self) -> int: ...
    def setDefaultByName(self, name: str, /) -> typing.Self: ...
    @property
    def default(self) -> int: ...
    @default.setter
    def default(self, value: int) -> None: ...

class MFnCompoundAttribute(MFnAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def addChild(self, child: MObject, /) -> typing.Self: ...
    def child(self, index: int, /) -> MObject: ...
    def create(self, longName: str, shortName: str, /) -> MObject: ...
    def getAddAttrCmds(self, longNames: bool) -> list[str]: ...
    def numChildren(self) -> int: ...
    def removeChild(self, child: MObject, /) -> typing.Self: ...

class MFnGenericAttribute(MFnAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def addDataType(self, type: _MFnDataType, /) -> typing.Self: ...
    def addNumericType(self, type: _MFnNumericDataType, /) -> typing.Self: ...
    def addTypeId(self, typeId: MTypeId, /) -> typing.Self: ...
    def create(self, longName: str, shortName: str, /) -> MObject: ...
    def removeDataType(self, type: _MFnDataType, /) -> typing.Self: ...
    def removeNumericType(self, type: _MFnNumericDataType, /) -> typing.Self: ...
    def removeTypeId(self, typeId: MTypeId, /) -> typing.Self: ...

class MFnLightDataAttribute(MFnAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def child(self, index: int, /) -> MObject: ...
    def create(
        self,
        longName: str,
        shortName: str,
        direction: MObject,
        intensity: MObject,
        ambient: MObject,
        diffuse: MObject,
        specular: MObject,
        shadowFraction: MObject,
        preShadowIntensity: MObject,
        blindData: MObject,
        /,
    ) -> MObject: ...
    @property
    def default(self) -> Incomplete: ...
    @default.setter
    def default(self, value: Incomplete) -> None: ...

_MFnMatrixAttributeType: typing.TypeAlias = typing.Literal[0, 1]

class MFnMatrixAttribute(MFnAttribute):
    kFloat: typing.Literal[0]
    kDouble: typing.Literal[1]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def create(
        self,
        longName: str,
        shortName: str,
        /,
        type: _MFnMatrixAttributeType = kDouble,
    ) -> MObject: ...
    @property
    def default(self) -> MMatrix: ...
    @default.setter
    def default(self, value: MMatrix | MFloatMatrix) -> None: ...

class MFnNumericAttribute(MFnAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def child(self, index: int, /) -> MObject: ...
    def create(
        self, longName: str, shortName: str, type: int, /, defaultValue: float = 0
    ) -> MObject: ...
    def createAddr(
        self, longName: str, shortName: str, /, defaultValue: float = 0
    ) -> MObject: ...
    def createColor(self, longName: str, shortName: str, /) -> MObject: ...
    def createPoint(self, longName: str, shortName: str, /) -> MObject: ...
    def getMax(self) -> float | tuple[float, ...]: ...  # TODO: 2 to 4 floats
    def getMin(self) -> float | tuple[float, ...]: ...  # TODO: 2 to 4 floats
    def getSoftMax(self) -> float: ...
    def getSoftMin(self) -> float: ...
    def hasMax(self) -> bool: ...
    def hasMin(self) -> bool: ...
    def hasSoftMax(self) -> bool: ...
    def hasSoftMin(self) -> bool: ...
    def numericType(self) -> _MFnNumericDataType: ...
    def setMax(self, maxValue: float | typing.Sequence[float], /) -> typing.Self: ...
    def setMin(self, minValue: float | typing.Sequence[float], /) -> typing.Self: ...
    def setSoftMax(self, maxValue: float, /) -> typing.Self: ...
    def setSoftMin(self, minValue: float, /) -> typing.Self: ...
    @property
    def default(self) -> float | tuple[float, ...]: ...
    @default.setter
    def default(self, value: float | tuple[float, ...]) -> None: ...

_MFnUnitAttributeUnitType: typing.TypeAlias = typing.Literal[0, 1, 2, 3, 4]

class MFnUnitAttribute(MFnAttribute):
    kInvalid: typing.Literal[0]
    kAngle: typing.Literal[1]
    kDistance: typing.Literal[2]
    kTime: typing.Literal[3]
    kLast: typing.Literal[4]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    @typing.overload
    def create(
        self,
        longName: str,
        shortName: str,
        type: _MFnUnitAttributeUnitType,
        /,
        defaultValue: float = 0.0,
    ) -> MObject: ...
    @typing.overload
    def create(
        self,
        longName: str,
        shortName: str,
        defaultValue: MAngle | MTime | MDistance,
        /,
    ) -> MObject: ...
    def getMax(self) -> MAngle | MTime | MDistance: ...
    def getMin(self) -> MAngle | MTime | MDistance: ...
    def getSoftMax(self) -> MAngle | MTime | MDistance: ...
    def getSoftMin(self) -> MAngle | MTime | MDistance: ...
    def hasMax(self) -> bool: ...
    def hasMin(self) -> bool: ...
    def hasSoftMax(self) -> bool: ...
    def hasSoftMin(self) -> bool: ...
    def setMax(
        self, maxValue: float | MAngle | MTime | MDistance, /
    ) -> typing.Self: ...
    def setMin(
        self, maxValue: float | MAngle | MTime | MDistance, /
    ) -> typing.Self: ...
    def setSoftMax(
        self, maxValue: float | MAngle | MTime | MDistance, /
    ) -> typing.Self: ...
    def setSoftMin(
        self, maxValue: float | MAngle | MTime | MDistance, /
    ) -> typing.Self: ...
    def unitType(self) -> _MFnUnitAttributeUnitType: ...
    @property
    def default(self) -> MAngle | MTime | MDistance: ...
    @default.setter
    def default(self, value: MAngle | MTime | MDistance) -> None: ...

class MFnTypedAttribute(MFnAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, object: MObject, /) -> None: ...
    def attrType(self) -> _MFnDataType: ...
    def create(
        self,
        longName: str,
        shortName: str,
        type: MTypeId | _MFnDataType,
        defaultValue: MObject = MObject.kNullObj,
    ) -> _MFnDataType: ...
    @property
    def default(self) -> MObject: ...
    @default.setter
    def default(self, value: MObject) -> None: ...

class MDGContext:
    kNormal: MDGContext

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MDGContext, /) -> None: ...
    @typing.overload
    def __init__(self, time: MTime) -> None: ...
    def copy(self, source: MDGContext, /) -> typing.Self: ...
    @staticmethod
    def current() -> MDGContext: ...
    def getTime(self) -> MTime: ...
    def isCurrent(self) -> bool: ...
    def isNormal(self) -> bool: ...
    def makeCurrent(self) -> typing.Self: ...

class MDGModifier:
    def __init__(self) -> None: ...
    def addAttribute(self, node: MObject, attribute: MObject, /) -> typing.Self: ...
    def addExtensionAttribute(
        self, nodeClass: MNodeClass, attribute: MObject, /
    ) -> typing.Self: ...
    def commandToExecute(self, command: str, /) -> typing.Self: ...
    @typing.overload
    def connect(self, source: MPlug, dest: MPlug, /) -> typing.Self: ...
    @typing.overload
    def connect(
        self,
        sourceNode: MObject,
        sourceAttr: MObject,
        destNode: MObject,
        destAttr: MObject,
        /,
    ) -> typing.Self: ...
    @typing.overload
    def createNode(self, typeName: str, /) -> MObject: ...
    @typing.overload
    def createNode(self, typeId: MTypeId, /) -> MObject: ...
    @typing.overload
    def deleteNode(self, node: MObject, /) -> typing.Self: ...
    @typing.overload
    def deleteNode(self, node: MObject, includeParents: bool, /) -> typing.Self: ...
    @typing.overload
    def disconnect(self, source: MPlug, dest: MPlug, /) -> typing.Self: ...
    @typing.overload
    def disconnect(
        self,
        sourceNode: MObject,
        sourceAttr: MObject,
        destNode: MObject,
        destAttr: MObject,
        /,
    ) -> typing.Self: ...
    def doIt(self) -> typing.Self: ...
    def linkExtensionAttributeToPlugin(
        self, plugin: MObject, attribute: MObject, /
    ) -> typing.Self: ...
    def newPlugValue(self, plug: MPlug, value: MObject, /) -> typing.Self: ...
    def newPlugValueBool(self, plug: MPlug, value: bool, /) -> typing.Self: ...
    def newPlugValueChar(self, plug: MPlug, value: int, /) -> typing.Self: ...
    def newPlugValueDouble(self, plug: MPlug, value: float, /) -> typing.Self: ...
    def newPlugValueFloat(self, plug: MPlug, value: float, /) -> typing.Self: ...
    def newPlugValueInt(self, plug: MPlug, value: int, /) -> typing.Self: ...
    def newPlugValueMAngle(self, plug: MPlug, value: MAngle, /) -> typing.Self: ...
    def newPlugValueMDistance(
        self, plug: MPlug, value: MDistance, /
    ) -> typing.Self: ...
    def newPlugValueMTime(self, plug: MPlug, value: MTime, /) -> typing.Self: ...
    def newPlugValueShort(self, plug: MPlug, value: int, /) -> typing.Self: ...
    def newPlugValueString(self, plug: MPlug, value: str, /) -> typing.Self: ...
    @typing.overload
    def pythonCommandToExecute(
        self, callable: typing.Callable[[], typing.Any], /
    ) -> typing.Self: ...
    @typing.overload
    def pythonCommandToExecute(self, commandString: str, /) -> typing.Self: ...
    def removeAttribute(self, node: MObject, attribute: MObject, /) -> typing.Self: ...
    def removeExtensionAttribute(
        self, nodeClass: MNodeClass, attribute: MObject, /
    ) -> typing.Self: ...
    def removeExtensionAttributeIfUnset(
        self, nodeClass: MNodeClass, attribute: MObject, /
    ) -> typing.Self: ...
    def removeMultiInstance(
        self, plug: MPlug, breakConnections: bool, /
    ) -> typing.Self: ...
    def renameAttribute(
        self, node: MObject, attribute: MObject, shortName: str, longName: str, /
    ) -> typing.Self: ...
    def renameNode(self, node: MObject, newName: str, /) -> typing.Self: ...
    def setNodeLockState(self, node: MObject, newState: bool, /) -> typing.Self: ...
    def undoIt(self) -> typing.Self: ...
    def unlinkExtensionAttributeFromPlugin(
        self, plugin: MObject, attribute: MObject, /
    ) -> typing.Self: ...

class MDagModifier(MDGModifier):
    def __init__(self) -> None: ...
    @typing.overload
    def createNode(
        self, typeName: str, /, parent: MObject = MObject.kNullObj
    ) -> MObject: ...
    @typing.overload
    def createNode(
        self, typeId: MTypeId, /, parent: MObject = MObject.kNullObj
    ) -> MObject: ...
    def reparentNode(
        self, node: MObject, /, newParent: MObject = MObject.kNullObj
    ) -> typing.Self: ...

_MPlugMValueSelector: typing.TypeAlias = typing.Literal[0, 1, 2, 3]
_MPlugFreeToChangeState: typing.TypeAlias = typing.Literal[0, 1, 2]

class MPlug:
    kAll: typing.Literal[0]
    kNonDefault: typing.Literal[1]
    kChanged: typing.Literal[2]
    kLastAttrSelector: typing.Literal[3]

    kFreeToChange: typing.Literal[0]
    kNotFreeToChange: typing.Literal[1]
    kChildrenNotFreeToChange: typing.Literal[2]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: MPlug, /) -> None: ...
    @typing.overload
    def __init__(self, node: MObject, attribute: MObject, /) -> None: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __ne__(self, value: object, /) -> bool: ...
    def array(self) -> MPlug: ...
    def asBool(self, context: MDGContext = MDGContext.kNormal) -> bool: ...
    def asChar(self, context: MDGContext = MDGContext.kNormal) -> int: ...
    def asDouble(self, context: MDGContext = MDGContext.kNormal) -> float: ...
    def asFloat(self, context: MDGContext = MDGContext.kNormal) -> float: ...
    def asInt(self, context: MDGContext = MDGContext.kNormal) -> int: ...
    def asMAngle(self, context: MDGContext = MDGContext.kNormal) -> MAngle: ...
    def asMDataHandle(
        self, context: MDGContext = MDGContext.kNormal
    ) -> MDataHandle: ...
    def asMDistance(self, context: MDGContext = MDGContext.kNormal) -> MDistance: ...
    def asMObject(self, context: MDGContext = MDGContext.kNormal) -> MObject: ...
    def asMTime(self, context: MDGContext = MDGContext.kNormal) -> MTime: ...
    def asShort(self, context: MDGContext = MDGContext.kNormal) -> int: ...
    def asString(self, context: MDGContext = MDGContext.kNormal) -> str: ...
    def attribute(self) -> MObject: ...
    @typing.overload
    def child(self, attribute: MObject, /) -> MPlug: ...
    @typing.overload
    def child(self, index: int, /) -> MPlug: ...
    def connectedTo(self, asDest: bool, asSrc: bool, /) -> MPlugArray: ...
    def connectionByPhysicalIndex(self, index: int, /) -> MPlug: ...
    def constructHandle(self, block: MDataBlock, /) -> MDataHandle: ...
    def copy(self, plug: MPlug, /) -> MPlug: ...
    def destinations(self) -> MPlugArray: ...
    def destinationsWithConversions(self) -> MPlugArray: ...
    def destructHandle(self, handle: MDataHandle, /) -> typing.Self: ...
    def elementByLogicalIndex(self, index: int, /) -> MPlug: ...
    def elementByPhysicalIndex(self, index: int, /) -> MPlug: ...
    def evaluateNumElements(self) -> int: ...
    def getExistingArrayAttributeIndices(self) -> MIntArray: ...
    def getSetAttrCmds(
        self, valueSelector: _MPlugMValueSelector = kAll, useLongNames: bool = False
    ) -> list[str]: ...
    def isDefaultValue(self) -> bool: ...
    def isExactlyEqual(self, plug: MPlug) -> bool: ...
    def isFreeToChange(
        self, checkAncestors: bool = True, checkChildren: bool = True
    ) -> _MPlugFreeToChangeState: ...
    def logicalIndex(self) -> int: ...
    def name(self) -> str: ...
    def node(self) -> MObject: ...
    def numChildren(self) -> int: ...
    def numConnectedChildren(self) -> int: ...
    def numConnectedElements(self) -> int: ...
    def numElements(self) -> int: ...
    def parent(self) -> MPlug: ...
    def partialName(
        self,
        includeNodeName: bool = False,
        includeNonMandatoryIndices: bool = False,
        includeInstancedIndices: bool = False,
        useAlias: bool = False,
        useFullAttributePath: bool = False,
        useLongNames: bool = False,
    ) -> str: ...
    def proxied(self) -> MPlug: ...
    def selectAncestorLogicalIndex(
        self, index: int, /, attribute: MObject = MObject.kNullObj
    ) -> MPlug: ...
    def setAttribute(self, attr: MObject, /) -> typing.Self: ...
    def setBool(self, value: bool, /) -> typing.Self: ...
    def setChar(self, value: int, /) -> typing.Self: ...
    def setDouble(self, value: float, /) -> typing.Self: ...
    def setFloat(self, value: float, /) -> typing.Self: ...
    def setInt(self, value: int, /) -> typing.Self: ...
    def setMAngle(self, value: MAngle, /) -> typing.Self: ...
    def setMDataHandle(self, value: MDataHandle, /) -> typing.Self: ...
    def setMDistance(self, value: MDistance, /) -> typing.Self: ...
    def setMObject(self, value: MObject, /) -> typing.Self: ...
    def setMPxData(self, value: MPxData, /) -> typing.Self: ...
    def setMTime(self, value: MTime, /) -> typing.Self: ...
    def setNumElements(self, count: int, /) -> typing.Self: ...
    def setShort(self, value: int, /) -> typing.Self: ...
    def setString(self, value: str, /) -> typing.Self: ...
    def source(self) -> MPlug: ...
    def sourceWithConversion(self) -> MPlug: ...
    @property
    def info(self) -> str: ...
    @property
    def isArray(self) -> bool: ...
    @property
    def isCaching(self) -> bool: ...
    @isCaching.setter
    def isCaching(self, value: bool) -> None: ...
    @property
    def isChannelBox(self) -> bool: ...
    @isChannelBox.setter
    def isChannelBox(self, value: bool) -> None: ...
    @property
    def isChild(self) -> bool: ...
    @property
    def isCompound(self) -> bool: ...
    @property
    def isConnected(self) -> bool: ...
    @property
    def isDestination(self) -> bool: ...
    @property
    def isDynamic(self) -> bool: ...
    @property
    def isElement(self) -> bool: ...
    @property
    def isFromReferencedFile(self) -> bool: ...
    @property
    def isIgnoredWhenRendering(self) -> bool: ...
    @property
    def isKeyable(self) -> bool: ...
    @isKeyable.setter
    def isKeyable(self, value: bool) -> None: ...
    @property
    def isLocked(self) -> bool: ...
    @isLocked.setter
    def isLocked(self, value: bool) -> None: ...
    @property
    def isNetworked(self) -> bool: ...
    @property
    def isNull(self) -> bool: ...
    @property
    def isProcedural(self) -> bool: ...
    @property
    def isProxy(self) -> bool: ...
    @property
    def isSource(self) -> bool: ...

_MAttrClass: typing.TypeAlias = typing.Literal[1, 2, 3, 4]
_MdgTimerMetric: typing.TypeAlias = typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
_MdgTimerType: typing.TypeAlias = typing.Literal[0, 1, 2]
_MdgTimerState: typing.TypeAlias = typing.Literal[0, 1, 2, 3]

class MFnDependencyNode(MFnBase):
    kTimerMetrics: typing.Literal[9]
    kTimerTypes: typing.Literal[3]

    # MAttrClass
    kLocalDynamicAttr: typing.Literal[1]
    kNormalAttr: typing.Literal[2]
    kExtensionAttr: typing.Literal[3]
    kInvalidAttr: typing.Literal[4]

    # MdgTimerState
    kTimerOff: typing.Literal[0]
    kTimerOn: typing.Literal[1]
    kTimerUninitialized: typing.Literal[2]
    kTimerInvalidState: typing.Literal[3]

    # MdgTimerMetric
    kTimerMetric_callback: typing.Literal[0]
    kTimerMetric_compute: typing.Literal[1]
    kTimerMetric_dirty: typing.Literal[2]
    kTimerMetric_draw: typing.Literal[3]
    kTimerMetric_fetch: typing.Literal[4]
    kTimerMetric_callbackViaAPI: typing.Literal[5]
    kTimerMetric_callbackNotViaAPI: typing.Literal[6]
    kTimerMetric_computeDuringCallback: typing.Literal[7]
    kTimerMetric_computeNotDuringCallback: typing.Literal[8]

    # MdgTimerType
    kTimerType_self: typing.Literal[0]
    kTimerType_inclusive: typing.Literal[1]
    kTimerType_count: typing.Literal[2]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, node: MObject, /) -> None: ...
    def absoluteName(self) -> str: ...
    def addAttribute(self, attribute: MObject, /) -> typing.Self: ...
    def addExternalContentForFileAttr(
        self, table: MExternalContentInfoTable, attr: MObject, /
    ) -> typing.Self: ...
    def affectsAnimation(self) -> bool: ...
    def allocateFlag(self, plugin: str, /) -> int: ...
    @typing.overload
    def attribute(self, index: int, /) -> MObject: ...
    @typing.overload
    def attribute(self, name: str, /) -> MObject: ...
    def attributeClass(self, attribute: MObject, /) -> _MAttrClass: ...
    def attributeCount(self) -> int: ...
    def canBeWritten(self) -> bool: ...
    @staticmethod
    def classification(nodeType: str, /) -> str: ...
    @typing.overload
    def create(self, typeId: MTypeId, /, nodeName: str | None = None) -> MObject: ...
    @typing.overload
    def create(self, typeName: str, /, nodeName: str | None = None) -> MObject: ...
    def deallocateAllFlags(self, plugin: str, /) -> None: ...
    def deallocateFlag(self, plugin: str, flag: int, /) -> None: ...
    def dgCallbackIds(
        self, timerType: _MdgTimerType, callbackName: str, /
    ) -> tuple[MCallbackIdArray, MDoubleArray]: ...
    def dgCallbacks(self, type: _MdgTimerType, /) -> tuple[list[str], MDoubleArray]: ...
    def dgTimer(self, metric: _MdgTimerMetric, type: _MdgTimerType, /) -> float: ...
    def dgTimerOff(self) -> typing.Self: ...
    def dgTimerOn(self) -> typing.Self: ...
    def dgTimerQueryState(self) -> _MdgTimerState: ...
    def dgTimerReset(self) -> typing.Self: ...
    def findAlias(self, alias: str, /) -> MObject: ...
    def findPlug(self, attr: str | MObject, wantNetworkedPlug: bool, /) -> MObject: ...
    def getAffectedAttributes(self, attribute: MObject, /) -> MObjectArray: ...
    def getAffectingAttributes(self, attribute: MObject, /) -> MObjectArray: ...
    def getAliasAttr(self, force: bool, /) -> MObject: ...
    def getAliasList(self) -> tuple[tuple[str, str], ...]: ...
    def getConnections(self) -> MPlugArray: ...
    def getExternalContent(self, arg: Incomplete, /) -> Incomplete: ...
    def hasAttribute(self, name: str, /) -> bool: ...
    def hasUniqueName(self) -> bool: ...
    def isFlagSet(self, flag: int, /) -> bool: ...
    def isNewAttribute(self, attribute: MObject, /) -> bool: ...
    def isTrackingEdits(self) -> bool: ...
    def name(self) -> str: ...
    def plugsAlias(self, plug: MPlug, /) -> str: ...
    def removeAttribute(self, attribute: MObject, /) -> typing.Self: ...
    def reorderedAttribute(self, index: int, /) -> MObject: ...
    def setAffectsAnimation(self) -> typing.Self: ...
    def setAlias(
        self, alias: str, attrName: str, plug: MPlug, /, add: bool = True
    ) -> bool: ...
    def setDoNotWrite(self, flag: bool) -> typing.Self: ...
    def setExternalContent(
        self, table: MExternalContentLocationTable, /
    ) -> typing.Self: ...
    def setExternalContentForFileAttr(
        self, attr: MObject, table: MExternalContentLocationTable, /
    ) -> typing.Self: ...
    def setFlag(self, flag: int, state: bool, /) -> typing.Self: ...
    def setName(self, name: str, /) -> str: ...
    def setUuid(self, uuid: MUuid, /) -> typing.Self: ...
    def uniqueName(self) -> str: ...
    def userNode(self) -> MPxNode | None: ...
    def uuid(self) -> MUuid: ...
    @property
    def isDefaultNode(self) -> bool: ...
    @property
    def isFromReferencedFile(self) -> bool: ...
    @property
    def isLocked(self) -> bool: ...
    @isLocked.setter
    def isLocked(self, value: bool) -> None: ...
    @property
    def isShared(self) -> bool: ...
    @property
    def namespace(self) -> str: ...
    @property
    def pluginName(self) -> str: ...
    @property
    def typeId(self) -> MTypeId: ...
    @property
    def typeName(self) -> str: ...

class MFn:
    kACos: typing.Literal[1160]
    kAISEnvFacade: typing.Literal[978]
    kASin: typing.Literal[1162]
    kATan: typing.Literal[1163]
    kATan2: typing.Literal[1164]
    kAbsolute: typing.Literal[1159]
    kAddDoubleLinear: typing.Literal[5]
    kAdskMaterial: typing.Literal[1068]
    kAffect: typing.Literal[6]
    kAimConstraint: typing.Literal[111]
    kAimMatrix: typing.Literal[1140]
    kAir: typing.Literal[257]
    kAlignCurve: typing.Literal[41]
    kAlignManip: typing.Literal[913]
    kAlignSurface: typing.Literal[42]
    kAmbientLight: typing.Literal[303]
    kAnd: typing.Literal[1161]
    kAngle: typing.Literal[270]
    kAngleBetween: typing.Literal[21]
    kAngleToDoubleNode: typing.Literal[1157]
    kAnimBlend: typing.Literal[795]
    kAnimBlendInOut: typing.Literal[796]
    kAnimCurve: typing.Literal[7]
    kAnimCurveTimeToAngular: typing.Literal[8]
    kAnimCurveTimeToDistance: typing.Literal[9]
    kAnimCurveTimeToTime: typing.Literal[10]
    kAnimCurveTimeToUnitless: typing.Literal[11]
    kAnimCurveUnitlessToAngular: typing.Literal[12]
    kAnimCurveUnitlessToDistance: typing.Literal[13]
    kAnimCurveUnitlessToTime: typing.Literal[14]
    kAnimCurveUnitlessToUnitless: typing.Literal[15]
    kAnimLayer: typing.Literal[1021]
    kAnisotropy: typing.Literal[623]
    kAnnotation: typing.Literal[271]
    kAnyGeometryVarGroup: typing.Literal[115]
    kArcLength: typing.Literal[273]
    kAreaLight: typing.Literal[305]
    kArrayMapper: typing.Literal[528]
    kArrowManip: typing.Literal[123]
    kArubaTesselate: typing.Literal[1133]
    kAssembly: typing.Literal[1082]
    kAsset: typing.Literal[1019]
    kAttachCurve: typing.Literal[43]
    kAttachSurface: typing.Literal[44]
    kAttribute: typing.Literal[565]
    kAttribute2Double: typing.Literal[748]
    kAttribute2Float: typing.Literal[749]
    kAttribute2Int: typing.Literal[751]
    kAttribute2Short: typing.Literal[750]
    kAttribute3Double: typing.Literal[752]
    kAttribute3Float: typing.Literal[753]
    kAttribute3Int: typing.Literal[755]
    kAttribute3Short: typing.Literal[754]
    kAttribute4Double: typing.Literal[881]
    kAudio: typing.Literal[22]
    kAverage: typing.Literal[1165]
    kAverageCurveManip: typing.Literal[149]
    kAvgCurves: typing.Literal[45]
    kAvgNurbsSurfacePoints: typing.Literal[47]
    kAvgSurfacePoints: typing.Literal[46]
    kAxesActionManip: typing.Literal[124]
    kAxisFromMatrix: typing.Literal[1199]
    kBackground: typing.Literal[23]
    kBallProjectionManip: typing.Literal[125]
    kBarnDoorManip: typing.Literal[150]
    kBase: typing.Literal[1]
    kBaseLattice: typing.Literal[249]
    kBendLattice: typing.Literal[335]
    kBevel: typing.Literal[48]
    kBevelManip: typing.Literal[151]
    kBevelPlus: typing.Literal[900]
    kBezierCurve: typing.Literal[1055]
    kBezierCurveData: typing.Literal[1056]
    kBezierCurveToNurbs: typing.Literal[1058]
    kBinaryData: typing.Literal[747]
    kBirailSrf: typing.Literal[49]
    kBlend: typing.Literal[27]
    kBlendColorSet: typing.Literal[740]
    kBlendColors: typing.Literal[31]
    kBlendDevice: typing.Literal[30]
    kBlendFalloff: typing.Literal[1142]
    kBlendManip: typing.Literal[152]
    kBlendMatrix: typing.Literal[1138]
    kBlendNodeAdditiveRotation: typing.Literal[1034]
    kBlendNodeAdditiveScale: typing.Literal[1033]
    kBlendNodeBase: typing.Literal[1022]
    kBlendNodeBoolean: typing.Literal[1023]
    kBlendNodeDouble: typing.Literal[1024]
    kBlendNodeDoubleAngle: typing.Literal[1025]
    kBlendNodeDoubleLinear: typing.Literal[1026]
    kBlendNodeEnum: typing.Literal[1027]
    kBlendNodeFloat: typing.Literal[1028]
    kBlendNodeFloatAngle: typing.Literal[1029]
    kBlendNodeFloatLinear: typing.Literal[1030]
    kBlendNodeInt16: typing.Literal[1031]
    kBlendNodeInt32: typing.Literal[1032]
    kBlendNodeTime: typing.Literal[1053]
    kBlendShape: typing.Literal[336]
    kBlendTwoAttr: typing.Literal[28]
    kBlendWeighted: typing.Literal[29]
    kBlindData: typing.Literal[757]
    kBlindDataTemplate: typing.Literal[758]
    kBlinn: typing.Literal[373]
    kBlinnMaterial: typing.Literal[389]
    kBoundary: typing.Literal[53]
    kBox: typing.Literal[868]
    kBoxData: typing.Literal[867]
    kBrownian: typing.Literal[508]
    kBrush: typing.Literal[766]
    kBulge: typing.Literal[497]
    kBulgeLattice: typing.Literal[338]
    kBump: typing.Literal[32]
    kBump3d: typing.Literal[33]
    kButtonManip: typing.Literal[153]
    kCacheBase: typing.Literal[1000]
    kCacheBlend: typing.Literal[1001]
    kCacheFile: typing.Literal[988]
    kCacheTrack: typing.Literal[1002]
    kCacheableNode: typing.Literal[997]
    kCaddyManipBase: typing.Literal[1111]
    kCamera: typing.Literal[250]
    kCameraManip: typing.Literal[154]
    kCameraPlaneManip: typing.Literal[143]
    kCameraSet: typing.Literal[1012]
    kCameraView: typing.Literal[34]
    kCeil: typing.Literal[1166]
    kCenterManip: typing.Literal[134]
    kChainToSpline: typing.Literal[35]
    kCharacter: typing.Literal[689]
    kCharacterMap: typing.Literal[804]
    kCharacterMappingData: typing.Literal[743]
    kCharacterOffset: typing.Literal[690]
    kChecker: typing.Literal[498]
    kChoice: typing.Literal[36]
    kChooser: typing.Literal[773]
    kCircle: typing.Literal[54]
    kCircleManip: typing.Literal[126]
    kCirclePointManip: typing.Literal[231]
    kCircleSweepManip: typing.Literal[128]
    kClampColor: typing.Literal[39]
    kClampRange: typing.Literal[1167]
    kClientDevice: typing.Literal[1078]
    kClip: typing.Literal[810]
    kClipGhostShape: typing.Literal[1083]
    kClipLibrary: typing.Literal[781]
    kClipScheduler: typing.Literal[780]
    kClipToGhostData: typing.Literal[1084]
    kCloseCurve: typing.Literal[55]
    kCloseSurface: typing.Literal[57]
    kClosestPointOnMesh: typing.Literal[990]
    kClosestPointOnSurface: typing.Literal[56]
    kCloth: typing.Literal[499]
    kCloud: typing.Literal[509]
    kCluster: typing.Literal[251]
    kClusterFilter: typing.Literal[347]
    kClusterFlexor: typing.Literal[300]
    kCoiManip: typing.Literal[155]
    kCollision: typing.Literal[253]
    kColorBackground: typing.Literal[24]
    kColorMgtGlobals: typing.Literal[1102]
    kColorProfile: typing.Literal[1067]
    kColumnFromMatrix: typing.Literal[1204]
    kCombinationShape: typing.Literal[337]
    kCommCornerManip: typing.Literal[614]
    kCommCornerOperManip: typing.Literal[615]
    kCommEdgeOperManip: typing.Literal[612]
    kCommEdgePtManip: typing.Literal[611]
    kCommEdgeSegmentManip: typing.Literal[613]
    kComponent: typing.Literal[535]
    kComponentFalloff: typing.Literal[1145]
    kComponentListData: typing.Literal[584]
    kComponentManip: typing.Literal[675]
    kComponentMatch: typing.Literal[1150]
    kComposeMatrix: typing.Literal[1137]
    kCompoundAttribute: typing.Literal[575]
    kConcentricProjectionManip: typing.Literal[129]
    kCondition: typing.Literal[37]
    kCone: typing.Literal[96]
    kConstraint: typing.Literal[933]
    kContainer: typing.Literal[1014]
    kContainerBase: typing.Literal[1069]
    kContourProjectionManip: typing.Literal[1116]
    kContrast: typing.Literal[38]
    kControl: typing.Literal[486]
    kControllerTag: typing.Literal[1129]
    kCopyColorSet: typing.Literal[739]
    kCopyUVSet: typing.Literal[808]
    kCos: typing.Literal[1168]
    kCpManip: typing.Literal[156]
    kCrater: typing.Literal[510]
    kCreaseSet: typing.Literal[1091]
    kCreate: typing.Literal[40]
    kCreateBPManip: typing.Literal[838]
    kCreateBezierManip: typing.Literal[1054]
    kCreateCVManip: typing.Literal[157]
    kCreateColorSet: typing.Literal[737]
    kCreateEPManip: typing.Literal[158]
    kCreateSectionManip: typing.Literal[825]
    kCreateUVSet: typing.Literal[809]
    kCrossProduct: typing.Literal[1196]
    kCrossSectionEditManip: typing.Literal[826]
    kCrossSectionManager: typing.Literal[824]
    kCubicProjectionManip: typing.Literal[130]
    kCurve: typing.Literal[266]
    kCurveCVComponent: typing.Literal[536]
    kCurveCurveIntersect: typing.Literal[642]
    kCurveEPComponent: typing.Literal[537]
    kCurveEdManip: typing.Literal[159]
    kCurveFromMeshCoM: typing.Literal[935]
    kCurveFromMeshEdge: typing.Literal[641]
    kCurveFromSubdivEdge: typing.Literal[837]
    kCurveFromSubdivFace: typing.Literal[843]
    kCurveFromSurface: typing.Literal[58]
    kCurveFromSurfaceBnd: typing.Literal[59]
    kCurveFromSurfaceCoS: typing.Literal[60]
    kCurveFromSurfaceIso: typing.Literal[61]
    kCurveInfo: typing.Literal[62]
    kCurveKnotComponent: typing.Literal[538]
    kCurveNormalizerAngle: typing.Literal[1004]
    kCurveNormalizerLinear: typing.Literal[1005]
    kCurveParamComponent: typing.Literal[539]
    kCurveSegmentManip: typing.Literal[160]
    kCurveVarGroup: typing.Literal[116]
    kCustomEvaluatorClusterNode: typing.Literal[1131]
    kCylinder: typing.Literal[98]
    kCylindricalProjectionManip: typing.Literal[131]
    kDOF: typing.Literal[323]
    kDPbirailSrf: typing.Literal[50]
    kDagContainer: typing.Literal[1070]
    kDagNode: typing.Literal[107]
    kDagPose: typing.Literal[691]
    kDagSelectionItem: typing.Literal[562]
    kData: typing.Literal[583]
    kData2Double: typing.Literal[594]
    kData2Float: typing.Literal[595]
    kData2Int: typing.Literal[596]
    kData2Short: typing.Literal[597]
    kData3Double: typing.Literal[598]
    kData3Float: typing.Literal[599]
    kData3Int: typing.Literal[600]
    kData3Short: typing.Literal[601]
    kData4Double: typing.Literal[882]
    kDblTrsManip: typing.Literal[190]
    kDecayRegionCapComponent: typing.Literal[548]
    kDecayRegionComponent: typing.Literal[549]
    kDecomposeMatrix: typing.Literal[1136]
    kDefaultLightList: typing.Literal[317]
    kDeformBend: typing.Literal[626]
    kDeformBendManip: typing.Literal[632]
    kDeformFlare: typing.Literal[629]
    kDeformFlareManip: typing.Literal[635]
    kDeformFunc: typing.Literal[625]
    kDeformSine: typing.Literal[630]
    kDeformSineManip: typing.Literal[636]
    kDeformSquash: typing.Literal[628]
    kDeformSquashManip: typing.Literal[634]
    kDeformTwist: typing.Literal[627]
    kDeformTwistManip: typing.Literal[633]
    kDeformWave: typing.Literal[631]
    kDeformWaveManip: typing.Literal[637]
    kDeleteColorSet: typing.Literal[738]
    kDeleteComponent: typing.Literal[318]
    kDeleteUVSet: typing.Literal[801]
    kDeltaMush: typing.Literal[350]
    kDependencyNode: typing.Literal[4]
    kDetachCurve: typing.Literal[63]
    kDetachSurface: typing.Literal[64]
    kDeterminant: typing.Literal[1169]
    kDiffuseMaterial: typing.Literal[387]
    kDimension: typing.Literal[269]
    kDimensionManip: typing.Literal[232]
    kDirectedDisc: typing.Literal[276]
    kDirectionManip: typing.Literal[161]
    kDirectionalLight: typing.Literal[308]
    kDiscManip: typing.Literal[132]
    kDiskCache: typing.Literal[864]
    kDispatchCompute: typing.Literal[319]
    kDisplacementShader: typing.Literal[321]
    kDisplayLayer: typing.Literal[734]
    kDisplayLayerManager: typing.Literal[735]
    kDistance: typing.Literal[272]
    kDistanceBetween: typing.Literal[322]
    kDistanceManip: typing.Literal[639]
    kDivide: typing.Literal[1200]
    kDofManip: typing.Literal[162]
    kDotProduct: typing.Literal[1195]
    kDoubleAngleAttribute: typing.Literal[567]
    kDoubleArrayData: typing.Literal[585]
    kDoubleIndexedComponent: typing.Literal[715]
    kDoubleLinearAttribute: typing.Literal[569]
    kDoubleShadingSwitch: typing.Literal[620]
    kDoubleToAngleNode: typing.Literal[1158]
    kDrag: typing.Literal[258]
    kDropOffFunction: typing.Literal[827]
    kDropoffLocator: typing.Literal[282]
    kDropoffManip: typing.Literal[163]
    kDummy: typing.Literal[254]
    kDummyConnectable: typing.Literal[324]
    kDynAirManip: typing.Literal[725]
    kDynArrayAttrsData: typing.Literal[730]
    kDynAttenuationManip: typing.Literal[729]
    kDynBase: typing.Literal[721]
    kDynBaseFieldManip: typing.Literal[724]
    kDynEmitterManip: typing.Literal[722]
    kDynFieldsManip: typing.Literal[723]
    kDynGlobals: typing.Literal[770]
    kDynNewtonManip: typing.Literal[726]
    kDynParticleSetComponent: typing.Literal[560]
    kDynSpreadManip: typing.Literal[728]
    kDynSweptGeometryData: typing.Literal[744]
    kDynTurbulenceManip: typing.Literal[727]
    kDynamicConstraint: typing.Literal[994]
    kDynamicsController: typing.Literal[325]
    kEdgeComponent: typing.Literal[545]
    kEditCurve: typing.Literal[822]
    kEditCurveManip: typing.Literal[823]
    kEditMetadata: typing.Literal[1090]
    kEditsManager: typing.Literal[1098]
    kEmitter: typing.Literal[255]
    kEnableManip: typing.Literal[136]
    kEnumAttribute: typing.Literal[572]
    kEnvBall: typing.Literal[491]
    kEnvChrome: typing.Literal[493]
    kEnvCube: typing.Literal[492]
    kEnvFacade: typing.Literal[977]
    kEnvFogMaterial: typing.Literal[381]
    kEnvFogShape: typing.Literal[278]
    kEnvSky: typing.Literal[494]
    kEnvSphere: typing.Literal[495]
    kEqual: typing.Literal[1170]
    kExplodeNurbsShell: typing.Literal[693]
    kExpression: typing.Literal[327]
    kExtendCurve: typing.Literal[65]
    kExtendCurveDistanceManip: typing.Literal[164]
    kExtendSurface: typing.Literal[66]
    kExtendSurfaceDistanceManip: typing.Literal[717]
    kExtract: typing.Literal[328]
    kExtrude: typing.Literal[67]
    kExtrudeManip: typing.Literal[165]
    kFFD: typing.Literal[339]
    kFFblendSrf: typing.Literal[68]
    kFFfilletSrf: typing.Literal[69]
    kFacade: typing.Literal[975]
    kFalloffEval: typing.Literal[1149]
    kFfdDualBase: typing.Literal[340]
    kField: typing.Literal[256]
    kFileBackground: typing.Literal[25]
    kFileTexture: typing.Literal[500]
    kFilletCurve: typing.Literal[70]
    kFilter: typing.Literal[329]
    kFilterClosestSample: typing.Literal[330]
    kFilterEuler: typing.Literal[331]
    kFilterSimplify: typing.Literal[332]
    kFitBspline: typing.Literal[71]
    kFixedLineManip: typing.Literal[233]
    kFlexor: typing.Literal[299]
    kFloatAngleAttribute: typing.Literal[568]
    kFloatArrayData: typing.Literal[1038]
    kFloatLinearAttribute: typing.Literal[570]
    kFloatMatrixAttribute: typing.Literal[579]
    kFloatVectorArrayData: typing.Literal[1015]
    kFloor: typing.Literal[1171]
    kFlow: typing.Literal[72]
    kFluid: typing.Literal[915]
    kFluidData: typing.Literal[917]
    kFluidEmitter: typing.Literal[921]
    kFluidGeom: typing.Literal[916]
    kFluidTexture2D: typing.Literal[910]
    kFluidTexture3D: typing.Literal[909]
    kFollicle: typing.Literal[936]
    kForceUpdateManip: typing.Literal[696]
    kFosterParent: typing.Literal[1093]
    kFourByFourMatrix: typing.Literal[776]
    kFractal: typing.Literal[501]
    kFreePointManip: typing.Literal[133]
    kFreePointTriadManip: typing.Literal[137]
    kGammaCorrect: typing.Literal[333]
    kGenericAttribute: typing.Literal[576]
    kGeoConnectable: typing.Literal[326]
    kGeoConnector: typing.Literal[923]
    kGeomBind: typing.Literal[1101]
    kGeometric: typing.Literal[265]
    kGeometryConstraint: typing.Literal[113]
    kGeometryData: typing.Literal[713]
    kGeometryFilt: typing.Literal[334]
    kGeometryOnLineManip: typing.Literal[142]
    kGeometryVarGroup: typing.Literal[114]
    kGlobalCacheControls: typing.Literal[863]
    kGlobalStitch: typing.Literal[702]
    kGranite: typing.Literal[511]
    kGravity: typing.Literal[259]
    kGreasePencilSequence: typing.Literal[1089]
    kGreasePlane: typing.Literal[1087]
    kGreasePlaneRenderShape: typing.Literal[1088]
    kGreaterThan: typing.Literal[1172]
    kGrid: typing.Literal[502]
    kGroundPlane: typing.Literal[290]
    kGroupId: typing.Literal[356]
    kGroupParts: typing.Literal[357]
    kGuide: typing.Literal[358]
    kGuideLine: typing.Literal[301]
    kHairConstraint: typing.Literal[941]
    kHairSystem: typing.Literal[937]
    kHairTubeShader: typing.Literal[948]
    kHandleRotateManip: typing.Literal[216]
    kHardenPointCurve: typing.Literal[73]
    kHardwareReflectionMap: typing.Literal[887]
    kHardwareRenderGlobals: typing.Literal[527]
    kHardwareRenderingGlobals: typing.Literal[1072]
    kHeightField: typing.Literal[922]
    kHikEffector: typing.Literal[962]
    kHikFKJoint: typing.Literal[964]
    kHikFloorContactMarker: typing.Literal[984]
    kHikGroundPlane: typing.Literal[985]
    kHikHandle: typing.Literal[966]
    kHikIKEffector: typing.Literal[963]
    kHikSolver: typing.Literal[965]
    kHistorySwitch: typing.Literal[989]
    kHsvToRgb: typing.Literal[359]
    kHwShaderNode: typing.Literal[890]
    kHyperGraphInfo: typing.Literal[360]
    kHyperLayout: typing.Literal[361]
    kHyperLayoutDG: typing.Literal[1006]
    kHyperView: typing.Literal[362]
    kIkEffector: typing.Literal[119]
    kIkHandle: typing.Literal[120]
    kIkRPManip: typing.Literal[167]
    kIkSolver: typing.Literal[363]
    kIkSplineManip: typing.Literal[166]
    kIkSystem: typing.Literal[369]
    kIllustratorCurve: typing.Literal[74]
    kImageAdd: typing.Literal[660]
    kImageBlur: typing.Literal[666]
    kImageColorCorrect: typing.Literal[665]
    kImageData: typing.Literal[654]
    kImageDepth: typing.Literal[668]
    kImageDiff: typing.Literal[661]
    kImageDisplay: typing.Literal[669]
    kImageFilter: typing.Literal[667]
    kImageLoad: typing.Literal[655]
    kImageMotionBlur: typing.Literal[671]
    kImageMultiply: typing.Literal[662]
    kImageNetDest: typing.Literal[658]
    kImageNetSrc: typing.Literal[657]
    kImageOver: typing.Literal[663]
    kImagePlane: typing.Literal[370]
    kImageRender: typing.Literal[659]
    kImageSave: typing.Literal[656]
    kImageSource: typing.Literal[792]
    kImageUnder: typing.Literal[664]
    kImageView: typing.Literal[670]
    kImplicitCone: typing.Literal[895]
    kImplicitSphere: typing.Literal[896]
    kInsertKnotCrv: typing.Literal[75]
    kInsertKnotSrf: typing.Literal[76]
    kInstancer: typing.Literal[763]
    kInt64ArrayData: typing.Literal[815]
    kIntArrayData: typing.Literal[586]
    kIntersectSurface: typing.Literal[77]
    kInvalid: typing.Literal[0]
    kInverseLinearInterpolation: typing.Literal[1173]
    kIsoparmComponent: typing.Literal[540]
    kIsoparmManip: typing.Literal[146]
    kItemList: typing.Literal[564]
    kJiggleDeformer: typing.Literal[862]
    kJoint: typing.Literal[121]
    kJointCluster: typing.Literal[349]
    kJointClusterManip: typing.Literal[168]
    kJointTranslateManip: typing.Literal[229]
    kKeyframeDelta: typing.Literal[950]
    kKeyframeDeltaAddRemove: typing.Literal[953]
    kKeyframeDeltaBlockAddRemove: typing.Literal[954]
    kKeyframeDeltaBreakdown: typing.Literal[958]
    kKeyframeDeltaInfType: typing.Literal[955]
    kKeyframeDeltaMove: typing.Literal[951]
    kKeyframeDeltaScale: typing.Literal[952]
    kKeyframeDeltaTangent: typing.Literal[956]
    kKeyframeDeltaWeighted: typing.Literal[957]
    kKeyframeRegionManip: typing.Literal[1003]
    kKeyingGroup: typing.Literal[688]
    kLambert: typing.Literal[371]
    kLambertMaterial: typing.Literal[388]
    kLattice: typing.Literal[279]
    kLatticeComponent: typing.Literal[546]
    kLatticeData: typing.Literal[588]
    kLatticeGeom: typing.Literal[280]
    kLayeredShader: typing.Literal[376]
    kLayeredTexture: typing.Literal[805]
    kLeastSquares: typing.Literal[379]
    kLeather: typing.Literal[512]
    kLength: typing.Literal[1174]
    kLessThan: typing.Literal[1175]
    kLight: typing.Literal[302]
    kLightDataAttribute: typing.Literal[577]
    kLightFogMaterial: typing.Literal[380]
    kLightInfo: typing.Literal[378]
    kLightLink: typing.Literal[769]
    kLightList: typing.Literal[382]
    kLightManip: typing.Literal[169]
    kLightProjectionGeometry: typing.Literal[234]
    kLightSource: typing.Literal[383]
    kLightSourceMaterial: typing.Literal[391]
    kLimitManip: typing.Literal[135]
    kLineArrowManip: typing.Literal[235]
    kLineManip: typing.Literal[147]
    kLineModifier: typing.Literal[979]
    kLinearInterpolation: typing.Literal[1176]
    kLinearLight: typing.Literal[306]
    kLocator: typing.Literal[281]
    kLodGroup: typing.Literal[774]
    kLodThresholds: typing.Literal[772]
    kLog: typing.Literal[1177]
    kLookAt: typing.Literal[112]
    kLuminance: typing.Literal[384]
    kMCsolver: typing.Literal[364]
    kMPbirailSrf: typing.Literal[51]
    kMakeGroup: typing.Literal[385]
    kMandelbrot: typing.Literal[1085]
    kMandelbrot3D: typing.Literal[1086]
    kManip2DContainer: typing.Literal[192]
    kManipContainer: typing.Literal[148]
    kManipulator: typing.Literal[230]
    kManipulator2D: typing.Literal[205]
    kManipulator3D: typing.Literal[122]
    kMarble: typing.Literal[513]
    kMarker: typing.Literal[283]
    kMarkerManip: typing.Literal[210]
    kMaterial: typing.Literal[386]
    kMaterialFacade: typing.Literal[976]
    kMaterialInfo: typing.Literal[392]
    kMaterialTemplate: typing.Literal[393]
    kMatrixAdd: typing.Literal[394]
    kMatrixArrayData: typing.Literal[604]
    kMatrixAttribute: typing.Literal[578]
    kMatrixData: typing.Literal[589]
    kMatrixFloatData: typing.Literal[673]
    kMatrixHold: typing.Literal[395]
    kMatrixMult: typing.Literal[396]
    kMatrixPass: typing.Literal[397]
    kMatrixWtAdd: typing.Literal[398]
    kMax: typing.Literal[1178]
    kMembrane: typing.Literal[1039]
    kMergeVertsToolManip: typing.Literal[1040]
    kMesh: typing.Literal[296]
    kMeshComponent: typing.Literal[550]
    kMeshData: typing.Literal[590]
    kMeshEdgeComponent: typing.Literal[551]
    kMeshFaceVertComponent: typing.Literal[555]
    kMeshFrEdgeComponent: typing.Literal[553]
    kMeshGeom: typing.Literal[297]
    kMeshMapComponent: typing.Literal[818]
    kMeshPolygonComponent: typing.Literal[552]
    kMeshVarGroup: typing.Literal[117]
    kMeshVertComponent: typing.Literal[554]
    kMeshVtxFaceComponent: typing.Literal[746]
    kMessageAttribute: typing.Literal[580]
    kMidModifier: typing.Literal[399]
    kMidModifierWithMatrix: typing.Literal[400]
    kMin: typing.Literal[1179]
    kModel: typing.Literal[3]
    kModifyEdgeBaseManip: typing.Literal[839]
    kModifyEdgeCrvManip: typing.Literal[830]
    kModifyEdgeManip: typing.Literal[831]
    kModulo: typing.Literal[1180]
    kMorph: typing.Literal[352]
    kMotionPath: typing.Literal[445]
    kMotionPathManip: typing.Literal[170]
    kMountain: typing.Literal[503]
    kMoveUVShellManip2D: typing.Literal[711]
    kMoveVertexManip: typing.Literal[764]
    kMultDoubleLinear: typing.Literal[775]
    kMultiSubVertexComponent: typing.Literal[558]
    kMultilisterLight: typing.Literal[447]
    kMultiply: typing.Literal[1181]
    kMultiplyDivide: typing.Literal[448]
    kMultiplyPointByMatrix: typing.Literal[1197]
    kMultiplyVectorByMatrix: typing.Literal[1198]
    kMute: typing.Literal[932]
    kNBase: typing.Literal[999]
    kNCloth: typing.Literal[1008]
    kNComponent: typing.Literal[995]
    kNId: typing.Literal[1037]
    kNIdData: typing.Literal[1036]
    kNLE: typing.Literal[1096]
    kNObject: typing.Literal[1017]
    kNObjectData: typing.Literal[1016]
    kNParticle: typing.Literal[1009]
    kNRigid: typing.Literal[1010]
    kNamedObject: typing.Literal[2]
    kNearestPointOnCurve: typing.Literal[1066]
    kNegate: typing.Literal[1182]
    kNewton: typing.Literal[260]
    kNodeGraphEditorBookmarkInfo: typing.Literal[1119]
    kNodeGraphEditorBookmarks: typing.Literal[1118]
    kNodeGraphEditorInfo: typing.Literal[1117]
    kNoise: typing.Literal[880]
    kNonAmbientLight: typing.Literal[304]
    kNonDagSelectionItem: typing.Literal[563]
    kNonExtendedLight: typing.Literal[307]
    kNonLinear: typing.Literal[624]
    kNormalConstraint: typing.Literal[238]
    kNormalize: typing.Literal[1183]
    kNot: typing.Literal[1184]
    kNucleus: typing.Literal[998]
    kNumericAttribute: typing.Literal[566]
    kNumericData: typing.Literal[593]
    kNurbsBoolean: typing.Literal[694]
    kNurbsCircular2PtArc: typing.Literal[644]
    kNurbsCircular3PtArc: typing.Literal[643]
    kNurbsCube: typing.Literal[80]
    kNurbsCurve: typing.Literal[267]
    kNurbsCurveData: typing.Literal[592]
    kNurbsCurveGeom: typing.Literal[268]
    kNurbsCurveToBezier: typing.Literal[1057]
    kNurbsPlane: typing.Literal[79]
    kNurbsSquare: typing.Literal[622]
    kNurbsSurface: typing.Literal[294]
    kNurbsSurfaceData: typing.Literal[591]
    kNurbsSurfaceGeom: typing.Literal[295]
    kNurbsTesselate: typing.Literal[78]
    kNurbsToSubdiv: typing.Literal[761]
    kObjectAttrFilter: typing.Literal[681]
    kObjectBinFilter: typing.Literal[944]
    kObjectFilter: typing.Literal[677]
    kObjectMultiFilter: typing.Literal[678]
    kObjectNameFilter: typing.Literal[679]
    kObjectRenderFilter: typing.Literal[682]
    kObjectScriptFilter: typing.Literal[683]
    kObjectTypeFilter: typing.Literal[680]
    kOcean: typing.Literal[876]
    kOceanDeformer: typing.Literal[1127]
    kOceanShader: typing.Literal[899]
    kOffsetCos: typing.Literal[81]
    kOffsetCosManip: typing.Literal[171]
    kOffsetCurve: typing.Literal[82]
    kOffsetCurveManip: typing.Literal[172]
    kOffsetSurface: typing.Literal[645]
    kOffsetSurfaceManip: typing.Literal[653]
    kOldGeometryConstraint: typing.Literal[449]
    kOpaqueAttribute: typing.Literal[581]
    kOpenPBRSurface: typing.Literal[1209]
    kOpticalFX: typing.Literal[450]
    kOr: typing.Literal[1185]
    kOrientConstraint: typing.Literal[239]
    kOrientationComponent: typing.Literal[556]
    kOrientationLocator: typing.Literal[286]
    kOrientationMarker: typing.Literal[284]
    kOrthoGrid: typing.Literal[291]
    kPASolver: typing.Literal[365]
    kPIConstant: typing.Literal[1186]
    kPairBlend: typing.Literal[928]
    kParamDimension: typing.Literal[275]
    kParentConstraint: typing.Literal[242]
    kParentMatrix: typing.Literal[1207]
    kParticle: typing.Literal[311]
    kParticleAgeMapper: typing.Literal[451]
    kParticleCloud: typing.Literal[452]
    kParticleColorMapper: typing.Literal[453]
    kParticleIncandecenceMapper: typing.Literal[454]
    kParticleSamplerInfo: typing.Literal[807]
    kParticleTransparencyMapper: typing.Literal[455]
    kPartition: typing.Literal[456]
    kPassContributionMap: typing.Literal[788]
    kPfxGeometry: typing.Literal[946]
    kPfxHair: typing.Literal[947]
    kPfxToon: typing.Literal[972]
    kPhong: typing.Literal[374]
    kPhongExplorer: typing.Literal[375]
    kPhongMaterial: typing.Literal[390]
    kPickMatrix: typing.Literal[1139]
    kPivotComponent: typing.Literal[541]
    kPivotManip2D: typing.Literal[191]
    kPlace2dTexture: typing.Literal[457]
    kPlace3dTexture: typing.Literal[458]
    kPlanarProjectionManip: typing.Literal[207]
    kPlanarTrimSrf: typing.Literal[83]
    kPlane: typing.Literal[288]
    kPlugin: typing.Literal[582]
    kPluginBlendShape: typing.Literal[1122]
    kPluginCameraSet: typing.Literal[1013]
    kPluginClientDevice: typing.Literal[1079]
    kPluginConstraintNode: typing.Literal[1018]
    kPluginData: typing.Literal[602]
    kPluginDeformerNode: typing.Literal[616]
    kPluginDependNode: typing.Literal[459]
    kPluginEmitterNode: typing.Literal[732]
    kPluginFieldNode: typing.Literal[731]
    kPluginGeometryData: typing.Literal[768]
    kPluginGeometryFilter: typing.Literal[1121]
    kPluginHardwareShader: typing.Literal[891]
    kPluginHwShaderNode: typing.Literal[892]
    kPluginIkSolver: typing.Literal[762]
    kPluginImagePlaneNode: typing.Literal[1007]
    kPluginLocatorNode: typing.Literal[460]
    kPluginManipContainer: typing.Literal[697]
    kPluginManipulatorNode: typing.Literal[1035]
    kPluginMotionPathNode: typing.Literal[446]
    kPluginObjectSet: typing.Literal[925]
    kPluginParticleAttributeMapperNode: typing.Literal[1011]
    kPluginShape: typing.Literal[712]
    kPluginSkinCluster: typing.Literal[1120]
    kPluginSpringNode: typing.Literal[733]
    kPluginThreadedDevice: typing.Literal[1080]
    kPluginTransformNode: typing.Literal[914]
    kPlusMinusAverage: typing.Literal[461]
    kPointArrayData: typing.Literal[603]
    kPointConstraint: typing.Literal[240]
    kPointLight: typing.Literal[309]
    kPointManip: typing.Literal[236]
    kPointMatrixMult: typing.Literal[462]
    kPointOnCurveInfo: typing.Literal[84]
    kPointOnCurveManip: typing.Literal[208]
    kPointOnLineManip: typing.Literal[211]
    kPointOnPolyConstraint: typing.Literal[1061]
    kPointOnSurfaceInfo: typing.Literal[85]
    kPointOnSurfaceManip: typing.Literal[212]
    kPoleVectorConstraint: typing.Literal[243]
    kPolyAppend: typing.Literal[403]
    kPolyAppendVertex: typing.Literal[797]
    kPolyArrow: typing.Literal[980]
    kPolyAutoProj: typing.Literal[852]
    kPolyAutoProjManip: typing.Literal[968]
    kPolyAverageVertex: typing.Literal[851]
    kPolyAxis: typing.Literal[1156]
    kPolyBevel: typing.Literal[401]
    kPolyBevel2: typing.Literal[1099]
    kPolyBevel3: typing.Literal[1103]
    kPolyBevelCutback: typing.Literal[1208]
    kPolyBlindData: typing.Literal[759]
    kPolyBoolOp: typing.Literal[618]
    kPolyBridgeEdge: typing.Literal[996]
    kPolyCBoolOp: typing.Literal[1100]
    kPolyCaddyManip: typing.Literal[1112]
    kPolyChipOff: typing.Literal[404]
    kPolyCircularize: typing.Literal[1132]
    kPolyClean: typing.Literal[1125]
    kPolyCloseBorder: typing.Literal[405]
    kPolyCollapseEdge: typing.Literal[406]
    kPolyCollapseF: typing.Literal[407]
    kPolyColorDel: typing.Literal[742]
    kPolyColorMod: typing.Literal[741]
    kPolyColorPerVertex: typing.Literal[736]
    kPolyComponentData: typing.Literal[986]
    kPolyCone: typing.Literal[437]
    kPolyConnectComponents: typing.Literal[1062]
    kPolyContourProj: typing.Literal[1115]
    kPolyCreaseEdge: typing.Literal[960]
    kPolyCreateFacet: typing.Literal[443]
    kPolyCreateToolManip: typing.Literal[140]
    kPolyCreator: typing.Literal[435]
    kPolyCube: typing.Literal[438]
    kPolyCut: typing.Literal[902]
    kPolyCutManip: typing.Literal[906]
    kPolyCutManipContainer: typing.Literal[905]
    kPolyCylProj: typing.Literal[408]
    kPolyCylinder: typing.Literal[439]
    kPolyDelEdge: typing.Literal[409]
    kPolyDelFacet: typing.Literal[410]
    kPolyDelVertex: typing.Literal[411]
    kPolyDuplicateEdge: typing.Literal[974]
    kPolyEdgeToCurve: typing.Literal[1020]
    kPolyEditEdgeFlow: typing.Literal[1092]
    kPolyExtrudeEdge: typing.Literal[794]
    kPolyExtrudeFacet: typing.Literal[412]
    kPolyExtrudeManip: typing.Literal[1075]
    kPolyExtrudeManipContainer: typing.Literal[1076]
    kPolyExtrudeVertex: typing.Literal[927]
    kPolyFlipEdge: typing.Literal[793]
    kPolyFlipUV: typing.Literal[889]
    kPolyHelix: typing.Literal[987]
    kPolyHoleFace: typing.Literal[1060]
    kPolyLayoutUV: typing.Literal[853]
    kPolyMapCut: typing.Literal[413]
    kPolyMapDel: typing.Literal[414]
    kPolyMapSew: typing.Literal[415]
    kPolyMapSewMove: typing.Literal[854]
    kPolyMappingManip: typing.Literal[194]
    kPolyMergeEdge: typing.Literal[416]
    kPolyMergeFacet: typing.Literal[417]
    kPolyMergeUV: typing.Literal[911]
    kPolyMergeVert: typing.Literal[699]
    kPolyMesh: typing.Literal[440]
    kPolyMirror: typing.Literal[959]
    kPolyMirrorManipContainer: typing.Literal[907]
    kPolyModifierManip: typing.Literal[195]
    kPolyModifierManipContainer: typing.Literal[1113]
    kPolyMoveEdge: typing.Literal[418]
    kPolyMoveFacet: typing.Literal[419]
    kPolyMoveFacetUV: typing.Literal[420]
    kPolyMoveUV: typing.Literal[421]
    kPolyMoveUVManip: typing.Literal[193]
    kPolyMoveVertex: typing.Literal[422]
    kPolyMoveVertexManip: typing.Literal[196]
    kPolyMoveVertexUV: typing.Literal[423]
    kPolyNormal: typing.Literal[424]
    kPolyNormalPerVertex: typing.Literal[760]
    kPolyNormalizeUV: typing.Literal[888]
    kPolyPassThru: typing.Literal[1123]
    kPolyPinUV: typing.Literal[961]
    kPolyPipe: typing.Literal[983]
    kPolyPlanProj: typing.Literal[425]
    kPolyPlatonicSolid: typing.Literal[982]
    kPolyPoke: typing.Literal[903]
    kPolyPokeManip: typing.Literal[908]
    kPolyPrimitive: typing.Literal[436]
    kPolyPrimitiveMisc: typing.Literal[981]
    kPolyPrism: typing.Literal[969]
    kPolyProj: typing.Literal[426]
    kPolyProjectCurve: typing.Literal[1073]
    kPolyProjectionManip: typing.Literal[174]
    kPolyPyramid: typing.Literal[970]
    kPolyQuad: typing.Literal[427]
    kPolyReFormManip: typing.Literal[1155]
    kPolyReFormManipContainer: typing.Literal[1154]
    kPolyReduce: typing.Literal[771]
    kPolyRemesh: typing.Literal[1114]
    kPolySelectEditFeedbackManip: typing.Literal[1043]
    kPolySeparate: typing.Literal[463]
    kPolySewEdge: typing.Literal[698]
    kPolySmartExtrude: typing.Literal[1152]
    kPolySmartExtrudeManip: typing.Literal[1153]
    kPolySmooth: typing.Literal[428]
    kPolySmoothFacet: typing.Literal[700]
    kPolySmoothProxy: typing.Literal[945]
    kPolySoftEdge: typing.Literal[429]
    kPolySphProj: typing.Literal[430]
    kPolySphere: typing.Literal[441]
    kPolySpinEdge: typing.Literal[1059]
    kPolySplit: typing.Literal[431]
    kPolySplitEdge: typing.Literal[816]
    kPolySplitRing: typing.Literal[971]
    kPolySplitToolManip: typing.Literal[141]
    kPolySplitVert: typing.Literal[811]
    kPolyStraightenUVBorder: typing.Literal[912]
    kPolySubdEdge: typing.Literal[432]
    kPolySubdFacet: typing.Literal[433]
    kPolyToSubdiv: typing.Literal[686]
    kPolyToolFeedbackManip: typing.Literal[1042]
    kPolyToolFeedbackShape: typing.Literal[312]
    kPolyTorus: typing.Literal[442]
    kPolyTransfer: typing.Literal[850]
    kPolyTriangulate: typing.Literal[434]
    kPolyTweak: typing.Literal[402]
    kPolyTweakUV: typing.Literal[710]
    kPolyUVRectangle: typing.Literal[1071]
    kPolyUnite: typing.Literal[444]
    kPolyUnsmooth: typing.Literal[1151]
    kPolyVertexNormalManip: typing.Literal[197]
    kPolyWedgeFace: typing.Literal[904]
    kPoseInterpolatorManager: typing.Literal[1128]
    kPositionMarker: typing.Literal[285]
    kPostProcessList: typing.Literal[464]
    kPower: typing.Literal[1187]
    kPrecompExport: typing.Literal[789]
    kPrimitive: typing.Literal[86]
    kPrimitiveFalloff: typing.Literal[1141]
    kProjectCurve: typing.Literal[87]
    kProjectTangent: typing.Literal[88]
    kProjectTangentManip: typing.Literal[177]
    kProjection: typing.Literal[465]
    kProjectionManip: typing.Literal[173]
    kProjectionMultiManip: typing.Literal[176]
    kProjectionUVManip: typing.Literal[175]
    kPropModManip: typing.Literal[178]
    kPropMoveTriadManip: typing.Literal[138]
    kProximityFalloff: typing.Literal[1146]
    kProximityPin: typing.Literal[992]
    kProximityWrap: typing.Literal[354]
    kProxy: typing.Literal[108]
    kProxyManager: typing.Literal[967]
    kPsdFileTexture: typing.Literal[949]
    kQuadPtOnLineManip: typing.Literal[179]
    kQuadShadingSwitch: typing.Literal[926]
    kRBFsurface: typing.Literal[89]
    kRPsolver: typing.Literal[367]
    kRadial: typing.Literal[261]
    kRadius: typing.Literal[274]
    kRamp: typing.Literal[504]
    kRampBackground: typing.Literal[26]
    kRampShader: typing.Literal[897]
    kRbfSrfManip: typing.Literal[180]
    kReForm: typing.Literal[1130]
    kRebuildCurve: typing.Literal[90]
    kRebuildSurface: typing.Literal[91]
    kRecord: typing.Literal[466]
    kReference: typing.Literal[756]
    kReflect: typing.Literal[372]
    kRemapColor: typing.Literal[939]
    kRemapHsv: typing.Literal[940]
    kRemapValue: typing.Literal[938]
    kRenderBox: typing.Literal[869]
    kRenderCone: typing.Literal[97]
    kRenderGlobals: typing.Literal[523]
    kRenderGlobalsList: typing.Literal[524]
    kRenderLayer: typing.Literal[786]
    kRenderLayerManager: typing.Literal[787]
    kRenderPass: typing.Literal[784]
    kRenderPassSet: typing.Literal[785]
    kRenderQuality: typing.Literal[525]
    kRenderRect: typing.Literal[277]
    kRenderSetup: typing.Literal[522]
    kRenderSphere: typing.Literal[298]
    kRenderTarget: typing.Literal[790]
    kRenderUtilityList: typing.Literal[467]
    kRenderedImageSource: typing.Literal[791]
    kRenderingList: typing.Literal[1074]
    kReorderUVSet: typing.Literal[1134]
    kResolution: typing.Literal[526]
    kResultCurve: typing.Literal[16]
    kResultCurveTimeToAngular: typing.Literal[17]
    kResultCurveTimeToDistance: typing.Literal[18]
    kResultCurveTimeToTime: typing.Literal[19]
    kResultCurveTimeToUnitless: typing.Literal[20]
    kReverse: typing.Literal[468]
    kReverseCrvManip: typing.Literal[182]
    kReverseCurve: typing.Literal[92]
    kReverseCurveManip: typing.Literal[181]
    kReverseSurface: typing.Literal[93]
    kReverseSurfaceManip: typing.Literal[183]
    kRevolve: typing.Literal[94]
    kRevolveManip: typing.Literal[184]
    kRevolvedPrimitive: typing.Literal[95]
    kRevolvedPrimitiveManip: typing.Literal[185]
    kRgbToHsv: typing.Literal[469]
    kRigid: typing.Literal[314]
    kRigidConstraint: typing.Literal[313]
    kRigidDeform: typing.Literal[341]
    kRigidSolver: typing.Literal[470]
    kRock: typing.Literal[514]
    kRotateBoxManip: typing.Literal[214]
    kRotateLimitsManip: typing.Literal[217]
    kRotateManip: typing.Literal[215]
    kRotateUVManip2D: typing.Literal[708]
    kRotateVector: typing.Literal[1188]
    kRotationFromMatrix: typing.Literal[1206]
    kRound: typing.Literal[1189]
    kRoundConstantRadius: typing.Literal[646]
    kRoundConstantRadiusManip: typing.Literal[649]
    kRoundRadiusCrvManip: typing.Literal[648]
    kRoundRadiusManip: typing.Literal[647]
    kRowFromMatrix: typing.Literal[1203]
    kSCsolver: typing.Literal[366]
    kSPbirailSrf: typing.Literal[52]
    kSamplerInfo: typing.Literal[478]
    kScaleConstraint: typing.Literal[244]
    kScaleFromMatrix: typing.Literal[1205]
    kScaleLimitsManip: typing.Literal[218]
    kScaleManip: typing.Literal[219]
    kScalePointManip: typing.Literal[832]
    kScaleUVManip2D: typing.Literal[709]
    kScalingBoxManip: typing.Literal[220]
    kScreenAlignedCircleManip: typing.Literal[127]
    kScript: typing.Literal[640]
    kScriptManip: typing.Literal[221]
    kSculpt: typing.Literal[342]
    kSectionManip: typing.Literal[819]
    kSelectionItem: typing.Literal[561]
    kSelectionList: typing.Literal[609]
    kSelectionListData: typing.Literal[676]
    kSelectionListOperator: typing.Literal[684]
    kSequenceManager: typing.Literal[1050]
    kSequencer: typing.Literal[1051]
    kSet: typing.Literal[471]
    kSetGroupComponent: typing.Literal[559]
    kSetRange: typing.Literal[474]
    kSfRevolveManip: typing.Literal[842]
    kShaderGlow: typing.Literal[475]
    kShaderList: typing.Literal[476]
    kShadingEngine: typing.Literal[320]
    kShadingMap: typing.Literal[477]
    kShape: typing.Literal[248]
    kShapeEditorManager: typing.Literal[1126]
    kShapeFragment: typing.Literal[479]
    kShot: typing.Literal[1052]
    kShrinkWrapFilter: typing.Literal[1097]
    kSimpleVolumeShader: typing.Literal[480]
    kSin: typing.Literal[1190]
    kSingleIndexedComponent: typing.Literal[714]
    kSingleShadingSwitch: typing.Literal[619]
    kSketchPlane: typing.Literal[289]
    kSkin: typing.Literal[100]
    kSkinBinding: typing.Literal[1063]
    kSkinClusterFilter: typing.Literal[687]
    kSkinShader: typing.Literal[674]
    kSl60: typing.Literal[481]
    kSmear: typing.Literal[918]
    kSmoothCurve: typing.Literal[701]
    kSmoothStep: typing.Literal[1191]
    kSmoothTangentSrf: typing.Literal[783]
    kSnapUVManip2D: typing.Literal[1094]
    kSnapshot: typing.Literal[482]
    kSnapshotPath: typing.Literal[924]
    kSnapshotShape: typing.Literal[860]
    kSnow: typing.Literal[515]
    kSoftMod: typing.Literal[252]
    kSoftModFilter: typing.Literal[348]
    kSoftModManip: typing.Literal[638]
    kSolidFractal: typing.Literal[516]
    kSolidify: typing.Literal[353]
    kSphere: typing.Literal[99]
    kSphereData: typing.Literal[605]
    kSphericalProjectionManip: typing.Literal[222]
    kSplineSolver: typing.Literal[368]
    kSpotCylinderManip: typing.Literal[187]
    kSpotLight: typing.Literal[310]
    kSpotManip: typing.Literal[186]
    kSpring: typing.Literal[315]
    kSprite: typing.Literal[292]
    kSquareSrf: typing.Literal[718]
    kSquareSrfManip: typing.Literal[719]
    kStandardSurface: typing.Literal[377]
    kStateManip: typing.Literal[145]
    kStencil: typing.Literal[505]
    kStereoCameraMaster: typing.Literal[1049]
    kStitchAsNurbsShell: typing.Literal[692]
    kStitchSrf: typing.Literal[101]
    kStitchSrfManip: typing.Literal[695]
    kStoryBoard: typing.Literal[483]
    kStringArrayData: typing.Literal[607]
    kStringData: typing.Literal[606]
    kStringShadingSwitch: typing.Literal[919]
    kStroke: typing.Literal[765]
    kStrokeGlobals: typing.Literal[767]
    kStucco: typing.Literal[517]
    kStudioClearCoat: typing.Literal[920]
    kStyleCurve: typing.Literal[901]
    kSubCurve: typing.Literal[102]
    kSubSurface: typing.Literal[782]
    kSubVertexComponent: typing.Literal[557]
    kSubdAddTopology: typing.Literal[893]
    kSubdAutoProj: typing.Literal[878]
    kSubdBlindData: typing.Literal[803]
    kSubdBoolean: typing.Literal[828]
    kSubdCleanTopology: typing.Literal[894]
    kSubdCloseBorder: typing.Literal[865]
    kSubdDelFace: typing.Literal[859]
    kSubdExtrudeFace: typing.Literal[840]
    kSubdHierBlind: typing.Literal[802]
    kSubdLayoutUV: typing.Literal[874]
    kSubdMapCut: typing.Literal[873]
    kSubdMapSewMove: typing.Literal[875]
    kSubdMappingManip: typing.Literal[886]
    kSubdMergeVert: typing.Literal[866]
    kSubdModifier: typing.Literal[855]
    kSubdModifyEdge: typing.Literal[829]
    kSubdMoveEdge: typing.Literal[857]
    kSubdMoveFace: typing.Literal[858]
    kSubdMoveVertex: typing.Literal[856]
    kSubdPlanProj: typing.Literal[883]
    kSubdProjectionManip: typing.Literal[885]
    kSubdSplitFace: typing.Literal[870]
    kSubdSubdivideFace: typing.Literal[879]
    kSubdTweak: typing.Literal[884]
    kSubdTweakUV: typing.Literal[872]
    kSubdiv: typing.Literal[685]
    kSubdivCVComponent: typing.Literal[703]
    kSubdivCollapse: typing.Literal[806]
    kSubdivCompId: typing.Literal[799]
    kSubdivData: typing.Literal[812]
    kSubdivEdgeComponent: typing.Literal[704]
    kSubdivFaceComponent: typing.Literal[705]
    kSubdivGeom: typing.Literal[813]
    kSubdivMapComponent: typing.Literal[861]
    kSubdivReverseFaces: typing.Literal[817]
    kSubdivSurfaceVarGroup: typing.Literal[841]
    kSubdivToNurbs: typing.Literal[821]
    kSubdivToPoly: typing.Literal[720]
    kSubsetFalloff: typing.Literal[1147]
    kSubtract: typing.Literal[1201]
    kSum: typing.Literal[1192]
    kSummaryObject: typing.Literal[484]
    kSuper: typing.Literal[485]
    kSurface: typing.Literal[293]
    kSurfaceCVComponent: typing.Literal[542]
    kSurfaceEPComponent: typing.Literal[543]
    kSurfaceEdManip: typing.Literal[778]
    kSurfaceFaceComponent: typing.Literal[779]
    kSurfaceInfo: typing.Literal[103]
    kSurfaceKnotComponent: typing.Literal[544]
    kSurfaceLuminance: typing.Literal[487]
    kSurfaceRangeComponent: typing.Literal[547]
    kSurfaceShader: typing.Literal[488]
    kSurfaceVarGroup: typing.Literal[118]
    kSymmetryConstraint: typing.Literal[241]
    kSymmetryLocator: typing.Literal[834]
    kSymmetryMapCurve: typing.Literal[836]
    kSymmetryMapVector: typing.Literal[835]
    kTan: typing.Literal[1193]
    kTangentConstraint: typing.Literal[245]
    kTension: typing.Literal[351]
    kTexLattice: typing.Literal[200]
    kTexLatticeDeformManip: typing.Literal[199]
    kTexSmoothManip: typing.Literal[201]
    kTexSmudgeUVManip: typing.Literal[198]
    kTextButtonManip: typing.Literal[652]
    kTextCurves: typing.Literal[104]
    kTextManip: typing.Literal[929]
    kTexture2d: typing.Literal[496]
    kTexture3d: typing.Literal[507]
    kTextureBakeSet: typing.Literal[472]
    kTextureDeformer: typing.Literal[343]
    kTextureDeformerHandle: typing.Literal[344]
    kTextureEnv: typing.Literal[490]
    kTextureList: typing.Literal[489]
    kTextureManip3D: typing.Literal[223]
    kThreadedDevice: typing.Literal[1077]
    kThreePointArcManip: typing.Literal[650]
    kTime: typing.Literal[520]
    kTimeAttribute: typing.Literal[571]
    kTimeEditor: typing.Literal[1107]
    kTimeEditorAnimSource: typing.Literal[1110]
    kTimeEditorClip: typing.Literal[1106]
    kTimeEditorClipBase: typing.Literal[1104]
    kTimeEditorClipEvaluator: typing.Literal[1105]
    kTimeEditorInterpolator: typing.Literal[1109]
    kTimeEditorTracks: typing.Literal[1108]
    kTimeFunction: typing.Literal[942]
    kTimeToUnitConversion: typing.Literal[521]
    kTimeWarp: typing.Literal[1081]
    kToggleManip: typing.Literal[224]
    kToggleOnLineManip: typing.Literal[144]
    kToolContext: typing.Literal[1095]
    kToonLineAttributes: typing.Literal[973]
    kTorus: typing.Literal[617]
    kTowPointManip: typing.Literal[139]
    kTowPointOnCurveManip: typing.Literal[209]
    kTowPointOnSurfaceManip: typing.Literal[777]
    kTrackInfoManager: typing.Literal[1124]
    kTransferAttributes: typing.Literal[993]
    kTransferFalloff: typing.Literal[1144]
    kTransform: typing.Literal[110]
    kTransformBoxManip: typing.Literal[833]
    kTransformGeometry: typing.Literal[610]
    kTranslateBoxManip: typing.Literal[225]
    kTranslateLimitsManip: typing.Literal[226]
    kTranslateManip: typing.Literal[227]
    kTranslateManip2D: typing.Literal[206]
    kTranslateUVManip: typing.Literal[213]
    kTranslateUVManip2D: typing.Literal[707]
    kTranslationFromMatrix: typing.Literal[1202]
    kTriadManip: typing.Literal[237]
    kTrim: typing.Literal[105]
    kTrimLocator: typing.Literal[287]
    kTrimManip: typing.Literal[228]
    kTrimWithBoundaries: typing.Literal[934]
    kTriplanarProjectionManip: typing.Literal[188]
    kTripleIndexedComponent: typing.Literal[716]
    kTripleShadingSwitch: typing.Literal[621]
    kTrsInsertManip: typing.Literal[203]
    kTrsManip: typing.Literal[189]
    kTrsTransManip: typing.Literal[202]
    kTrsXformManip: typing.Literal[204]
    kTruncate: typing.Literal[1194]
    kTurbulence: typing.Literal[262]
    kTweak: typing.Literal[345]
    kTwoPointArcManip: typing.Literal[651]
    kTxSl: typing.Literal[518]
    kTypedAttribute: typing.Literal[574]
    kUInt64ArrayData: typing.Literal[814]
    kUVManip2D: typing.Literal[706]
    kUVPin: typing.Literal[991]
    kUfeProxyTransform: typing.Literal[1135]
    kUint64SingleIndexedComponent: typing.Literal[1041]
    kUintArrayData: typing.Literal[587]
    kUnderWorld: typing.Literal[109]
    kUniform: typing.Literal[263]
    kUniformFalloff: typing.Literal[1143]
    kUnitAttribute: typing.Literal[573]
    kUnitConversion: typing.Literal[529]
    kUnitToTimeConversion: typing.Literal[530]
    kUnknown: typing.Literal[532]
    kUnknownDag: typing.Literal[316]
    kUnknownTransform: typing.Literal[246]
    kUntrim: typing.Literal[106]
    kUnused1: typing.Literal[844]
    kUnused2: typing.Literal[845]
    kUnused3: typing.Literal[846]
    kUnused4: typing.Literal[847]
    kUnused5: typing.Literal[848]
    kUnused6: typing.Literal[849]
    kUseBackground: typing.Literal[531]
    kUvChooser: typing.Literal[798]
    kVectorArrayData: typing.Literal[608]
    kVectorProduct: typing.Literal[533]
    kVertexBakeSet: typing.Literal[473]
    kVertexWeightSet: typing.Literal[1065]
    kViewColorManager: typing.Literal[672]
    kViewManip: typing.Literal[930]
    kVolumeAxis: typing.Literal[800]
    kVolumeBindManip: typing.Literal[1064]
    kVolumeFog: typing.Literal[871]
    kVolumeLight: typing.Literal[898]
    kVolumeNoise: typing.Literal[877]
    kVolumeShader: typing.Literal[534]
    kVortex: typing.Literal[264]
    kWater: typing.Literal[506]
    kWeightFunctionData: typing.Literal[1148]
    kWeightGeometryFilt: typing.Literal[346]
    kWire: typing.Literal[355]
    kWood: typing.Literal[519]
    kWorld: typing.Literal[247]
    kWrapFilter: typing.Literal[745]
    kWriteToColorBuffer: typing.Literal[1045]
    kWriteToDepthBuffer: typing.Literal[1047]
    kWriteToFrameBuffer: typing.Literal[1044]
    kWriteToLabelBuffer: typing.Literal[1048]
    kWriteToVectorBuffer: typing.Literal[1046]
    kXformManip: typing.Literal[931]
    kXsectionSubdivEdit: typing.Literal[820]
