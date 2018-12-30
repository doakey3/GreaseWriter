import bpy
from .process_stroke_verts_linearly import process_stroke_verts_linearly

def draw_glyph(glyph_strokes):
    obj = bpy.context.view_layer.objects.active
    gpencil = obj.data
    speed = gpencil.draw_speed
    thickness = gpencil.write_thickness
    color = gpencil.write_color

    if len(gpencil.layers) > 0:
            layer = gpencil.layers[0]
            layer.clear()
    else:
        layer = gpencil.layers.new('strokes', set_active=True)

    frame = layer.frames.new(bpy.context.scene.frame_current)

    bpy.context.scene.frame_current += 1

    mat_index = None
    obj_mat_names = []
    for mat in obj.data.materials:
        obj_mat_names.append(mat.name)

    for i in range(len(bpy.data.materials)):
        try:
            mat_col = bpy.data.materials[i].grease_pencil.color
            if mat_col[0] == color[0] and mat_col[1] == color[1] and mat_col[2] == color[2]:
                if bpy.data.materials[i].name in obj_mat_names:
                    mat_index = obj_mat_names.index(bpy.data.materials[i].name)
                else:
                    obj.data.materials.append(bpy.data.materials[i])
                    mat_index = len(obj.data.materials) - 1
        except AttributeError:
            pass

    if mat_index == None:
        new_mat = bpy.data.materials.new('write color')
        bpy.data.materials.create_gpencil_data(new_mat)
        new_mat.grease_pencil.color[0] = color[0]
        new_mat.grease_pencil.color[1] = color[1]
        new_mat.grease_pencil.color[2] = color[2]
        obj.data.materials.append(new_mat)
        mat_index = len(obj.data.materials) - 1

    for i in range(len(glyph_strokes)):
        stroke_verts = glyph_strokes[i]
        framed_strokes = process_stroke_verts_linearly(stroke_verts, speed)

        # Give extra frames between strokes
        if i > 0:
            last_vert = glyph_strokes[i - 1][-1]
            new_vert = glyph_strokes[i][0]
            count = len(process_stroke_verts_linearly([last_vert, new_vert], speed)) - 1
            bpy.context.scene.frame_current += count

        stopper = 0
        if i == len(glyph_strokes) - 1:
            stopper = 1

        for x in range(len(framed_strokes) - stopper):
            frame = layer.frames.new(bpy.context.scene.frame_current)

            for y in range(i):
                stroke = frame.strokes.new()
                stroke.line_width = thickness
                stroke.display_mode = '3DSPACE'
                stroke.material_index = mat_index

                for vert in glyph_strokes[y]:
                    stroke.points.add(gpencil, 1)
                    stroke.points[-1].co.x = vert[0]
                    stroke.points[-1].co.y = vert[1]

            stroke = frame.strokes.new()
            stroke.line_width = thickness
            stroke.display_mode = '3DSPACE'
            stroke.material_index = mat_index

            for vert in framed_strokes[x]:
                stroke.points.add(gpencil, 1)
                stroke.points[-1].co.x = vert[0]
                stroke.points[-1].co.y = vert[1]

            bpy.context.scene.frame_current += 1

    frame = layer.frames.new(bpy.context.scene.frame_current)
    for stroke_verts in glyph_strokes:
        stroke = frame.strokes.new()
        stroke.line_width = thickness
        stroke.display_mode = '3DSPACE'
        stroke.material_index = mat_index

        for vert in stroke_verts:
            stroke.points.add(gpencil, 1)
            stroke.points[-1].co.x = vert[0]
            stroke.points[-1].co.y = vert[1]

