from .Cross import Cross
from .Difference import Difference
from .Intersection import Intersection
from .Join import Join
from .Union import Union

from .Add import Add
from .And import And
from .ArrowLeft import ArrowLeft
from .ConditionalSet import ConditionalSet
from .Divide import Divide
from .Division import Division
from .Equal import Equal
from .GreaterThan import GreaterThan
from .GreaterThanEqual import GreaterThanEqual
from .LessThan import LessThan
from .LessThanEqual import LessThanEqual
from .Minus import Minus
from .Multiply import Multiply
from .Or import Or
from .Unequal import Unequal

# inverse binding strength
LOGIC_BINARY_OPERATORS = sorted([
    Or, And,
    Equal, Unequal,
    GreaterThan, GreaterThanEqual, LessThan, LessThanEqual,
    ArrowLeft,
    Add, Minus, Multiply, Divide
], key=lambda x: x.order, reverse=True)

RA_BINARY_OPERATORS = [
    Difference,
    Union,
    Intersection,
    Join,
    Cross,
    Division
]

DC_SET = ConditionalSet
