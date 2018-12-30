import bpy
from .utils import draw_glyph

class GREASEPENCIL_OT_reanimate(bpy.types.Operator):
    bl_label = "Reanimate"
    bl_idname = "grease_writer.reanimate"
    bl_description = "(Re)animates the strokes for a grease-pencil object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(self, context):
        obj = bpy.context.view_layer.objects.active
        gpencil = obj.data
        if (len(gpencil.layers) > 0 and
            len(gpencil.layers[0].frames) > 0):
                return True
        else:
            return False

    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        gpencil = obj.data

        layer = gpencil.layers[0]
        frame = layer.frames[-1]
        glyph_strokes = []
        for stroke in frame.strokes:
            verts = []
            for point in stroke.points:
                verts.append([point.co.x, point.co.y])
            glyph_strokes.append(verts)

        layer.clear()
        try:
            bpy.context.scene.frame_current = gpencil.layers[0].frames[0].frame_number + 1
        except IndexError:
            pass

        draw_glyph(glyph_strokes)

        return {"FINISHED"}
