import bpy
from mathutils import Vector

gpencil = bpy.data.grease_pencil.new('gpencil')

layer = gpencil.layers.new("alayer", set_active=True)
frame = layer.frames.new(bpy.context.scene.frame_current)
stroke = frame.strokes.new()
stroke.line_width = 300
stroke.display_mode = '3DSPACE'
stroke.material_index = 0


points = [
    [2, 0],
    [8, 5]
]

for point in points:
    stroke.points.add(gpencil, 1)
    stroke.points[-1].co.x = point[0]
    stroke.points[-1].co.y = point[1]  

obj = bpy.data.objects.new('agobject', gpencil)
bpy.context.scene.collection.objects.link(obj)
mat = bpy.data.materials.new('mymaterial')
bpy.data.materials.create_gpencil_data(mat)
obj.data.materials.append(mat)
