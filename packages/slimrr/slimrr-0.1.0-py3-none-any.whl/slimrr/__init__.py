# -*- coding: utf-8 -*-

# the version of software
# this is used by the setup.py script
from .version import __version__

__all__ = [
    'euler',
    'integer',
    'matrix33',
    'matrix44',
    'quaternion',
    'trig',
    'utils',
    'vector',
    'vector2',
    'vector3',
    'vector4',
    'Matrix33',
    'Matrix44',
    'Quaternion',
    'Vector3',
    'Vector4',
]

from . import (
    euler,
    integer,
    matrix33,
    matrix44,
    quaternion,
    trig,
    utils,
    vector,
    vector2,
    vector3,
    vector4,
)

from .objects import (
    Matrix33,
    Matrix44,
    Quaternion,
    Vector2,
    Vector3,
    Vector4
)

# because of circular imports, we cannot put these inside each module
# so insert them here
setattr(matrix33, 'Matrix33', Matrix33)
setattr(matrix44, 'Matrix44', Matrix44)
setattr(quaternion, 'Quaternion', Quaternion)
setattr(vector2, 'Vector2', Vector2)
setattr(vector3, 'Vector3', Vector3)
setattr(vector4, 'Vector4', Vector4)

