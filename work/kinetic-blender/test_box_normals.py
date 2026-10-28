"""Regression: authored closed boxes must face outward for lighting bakes."""
import ast
from pathlib import Path
import bpy
import bmesh

source=Path(__file__).with_name('build_kinetic_studio.py')
tree=ast.parse(source.read_text(encoding='utf-8'))
COL=bpy.context.scene.collection
exec(compile(ast.Module(body=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in {'finish','box'}],type_ignores=[]),'tested_box_helper','exec'))
ob=box('Outward normal regression box',(0,0,0),(1,2,3),None)
mesh=bmesh.new();mesh.from_mesh(ob.data)
assert abs(mesh.calc_volume(signed=True)-6)<1e-6,'Box faces point inward'
assert all(face.normal.dot(face.calc_center_median())>0 for face in mesh.faces)
mesh.free()
print('KINETIC_BOX_NORMALS_PASS')
