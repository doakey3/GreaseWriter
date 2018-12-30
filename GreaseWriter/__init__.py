import bpy

from .operators import *

bl_info = {
    "name": "Grease Writer",
    "description": "Automatic hand-drawn text animation",
    "author": "doakey3",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/doakey3/GreaseDraw",
    "tracker_url": "https://github.com/doakey3/GreaseDraw/issues",
    "category": "Animation",
    "location": "Properties, Grease Pencil Data"
}

class GREASEPENCIL_PT_greasewriter(bpy.types.Panel):
    bl_label = "Grease Writer"
    bl_idname = "GREASEPENCIL_PT_greasewriter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        if type(context.active_object.data).__name__ == "GreasePencil":
            return True
        else:
            return False

    def draw(self, context):
        scene = context.scene
        gpencil = context.active_object.data
        layout = self.layout
        layout.prop(gpencil, 'draw_speed')
        layout.prop(gpencil, 'kerning')
        layout.prop(gpencil, 'line_height')
        layout.prop(gpencil, 'write_thickness')
        layout.prop(gpencil, 'write_color')
        #layout.prop(gpencil, 'interpolation_mode')
        layout.prop(gpencil, 'font')
        row = layout.row()
        row.operator("grease_writer.write", icon="FILE_TEXT")
        row.prop_search(gpencil, 'source_text', bpy.data, "texts", text="")
        row = layout.row()
        row.operator("grease_writer.decorate", icon="LIGHT_SUN")
        row.prop(gpencil, "decorator_style", text="")
        layout.operator("grease_writer.reanimate", icon="HAND")
        row = layout.row()
        row.operator("grease_writer.trace", icon="PIVOT_CURSOR")
        row.prop_search(gpencil, 'tracer_obj', scene, "objects", text="")


def init_props():
    bpy.types.GreasePencil.draw_speed = bpy.props.FloatProperty(
        name="Draw Speed",
        description="The distance a stroke lengthens with each frame of animation",
        default=0.1,
        min=0.01
    )

    bpy.types.GreasePencil.kerning = bpy.props.FloatProperty(
        name="Kerning",
        description="Affects the distance between characters. Default is 0.5 x the width of letter M",
        default=0.5,
        min=0
    )

    bpy.types.GreasePencil.line_height = bpy.props.FloatProperty(
        name="Line Height",
        description="Affects the height of a line. Default is 1.25 x the height of the letter M",
        default=1.25,
        min=0
    )

    bpy.types.GreasePencil.write_thickness = bpy.props.IntProperty(
        name="Thickness",
        description="Affects the default line thickness.",
        default=100,
        min=1
    )

    bpy.types.GreasePencil.write_color = bpy.props.FloatVectorProperty(
       subtype='COLOR_GAMMA',
       name="Color",
       description="Color to use when writing",
       size=3,
       default=(0, 0, 0),
       min=0.0,
       max=1.0
    )

    """
    It might be cool to someday have different interpolation modes.
    For now, linear is ok

    interpolation_modes = [
        ("linear", "Linear", "Draw all strokes at the given draw speed"),
        ("derivative", "Derivative", "Draw strokes at a rate that varies based on the stroke's rate of change in direction; the more curvaceous, the slower the draw"),
        ("random", "Random", "Draw with a random speed that is +/- the given draw speed"),
    ]

    bpy.types.GreasePencil.interpolation_mode = bpy.props.EnumProperty(
        name="Interpolation",
        items=interpolation_modes,
        description="Select a mode for calculating how fast strokes should be drawn",
        default="linear",
    )
    """

    fonts = [
        ("consolas", "Consolas", "A monospace font based on Consolas")
    ]

    bpy.types.GreasePencil.font = bpy.props.EnumProperty(
        name="Font",
        items=fonts,
        description="The font to be used for writing",
        default="consolas",
    )

    bpy.types.GreasePencil.source_text = bpy.props.StringProperty(
        name="source_text",
        description="The text to be written with grease pencil"
    )

    decorators = [
        ("underline", "Underline", "Draw an underline beneath the grease pencil layer"),
        ("over-underline", "Over-underline", "Draw an overline and underline"),
        ("box", "Box", "Draw a box around the grease pencil layer"),
        ("ellipse", "Ellipse", "Draw an ellipse around the grease pencil layer"),
        ("circle", "Circle", "Draw a circle around the grease pencil layer"),
        ("strike-through", "Strike-through", "Horizontally strike out the grease pencil layer"),
        ("x-out", "X-out", "X out the grease pencil layer"),
        ("helioid", "Helioid", "Make a sun-like decorator (spiked ellipse)")
    ]

    bpy.types.GreasePencil.decorator_style = bpy.props.EnumProperty(
        name="Decorators",
        items=decorators,
        description="The decorator to draw",
        default="underline",
    )

    bpy.types.GreasePencil.tracer_obj = bpy.props.StringProperty()


classes = [
    GREASEPENCIL_PT_greasewriter,
    GREASEPENCIL_OT_reanimate,
    GREASEPENCIL_OT_write,
    GREASEPENCIL_OT_trace,
    GREASEPENCIL_OT_decorate
]

def register():
    init_props()

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
