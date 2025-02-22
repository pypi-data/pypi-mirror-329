"""
Charz
=====

An object oriented terminal game engine

Includes
--------

- Annotations (from package `colex`)
  - `ColorValue`
- Math (from package `linflex`)
  - `lerp`
  - `sign`
  - `clamp`
  - `Vec2`
  - `Vec2i`
  - `Vec3`
- Modules
  - `text`
    - `fill`
    - `flip_h`
    - `flip_v`
    - `fill_lines`
    - `flip_lines_h`
    - `flip_lines_v`
    - `rotate`
  - `colex`    (dependency)
  - `keyboard` (optional dependency)
- Framework
  - `Engine`
  - `Clock`
  - `DeltaClock`
  - `Screen`
- Datastructures
  - `Animation`
  - `AnimationSet`
  - `Hitbox`
- Functions
  - `load_texture`
- Components
  - `Transform`
  - `Texture`
  - `Color`
  - `Animated`
  - `Collider`
- Nodes
  - `Camera`
  - `Node`
  - `Node2D`
  - `Sprite`
  - `Label`
  - `AnimatedSprite`
"""

__all__ = [
    "Engine",
    "Clock",
    "DeltaClock",
    "Screen",
    "Camera",
    "Node",
    "Node2D",
    "Transform",
    "lerp",
    "sign",
    "clamp",
    "Vec2",
    "Vec2i",
    "Vec3",
    "load_texture",
    "Texture",
    "Color",
    "ColorValue",
    "Label",
    "Sprite",
    "Animated",
    "AnimatedSprite",
    "Animation",
    "AnimationSet",
    "Collider",
    "Hitbox",
    "text",
]

# re-exports
from linflex import lerp, sign, clamp, Vec2, Vec2i, Vec3
from colex import ColorValue

# exports
from ._engine import Engine
from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._camera import Camera
from ._node import Node
from ._animation import Animation, AnimationSet
from ._components._transform import Transform
from ._components._texture import load_texture, Texture
from ._components._color import Color
from ._components._animated import Animated
from ._components._collision import Collider, Hitbox
from ._prefabs._node2d import Node2D
from ._prefabs._label import Label
from ._prefabs._sprite import Sprite
from ._prefabs._animated_sprite import AnimatedSprite
from . import text
