import bpy
import os
import copy
from .utils import draw_glyph

def get_char_name(char):
    character_dict = {
        "!": "exclamation",
        "#": "pound",
        "$": "dollar",
        "%": "percentage",
        "&": "ampersand",
        "'": "quotesingle",
        "(": "parenthesisleft",
        ")": "parenthesisright",
        "*": "asterisk",
        "+": "plus",
        ",": "comma",
        "-": "minus",
        ".": "period",
        "/": "slash",
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        ":": "colon",
        ";": "semicolon",
        "<": "lessthan",
        "=": "equal",
        ">": "greaterthan",
        "?": "question",
        "@": "at",
        "A": "a-uppercase",
        "B": "b-uppercase",
        "C": "c-uppercase",
        "D": "d-uppercase",
        "E": "e-uppercase",
        "F": "f-uppercase",
        "G": "g-uppercase",
        "H": "h-uppercase",
        "I": "i-uppercase",
        "J": "j-uppercase",
        "K": "k-uppercase",
        "L": "l-uppercase",
        "M": "m-uppercase",
        "N": "n-uppercase",
        "O": "o-uppercase",
        "P": "p-uppercase",
        "Q": "q-uppercase",
        "R": "r-uppercase",
        "S": "s-uppercase",
        "T": "t-uppercase",
        "U": "u-uppercase",
        "V": "v-uppercase",
        "W": "w-uppercase",
        "X": "x-uppercase",
        "Y": "y-uppercase",
        "Z": "z-uppercase",
        "[": "bracketleft",
        "\\": "backslash",
        "]": "bracketright",
        "^": "caret",
        "_": "underscore",
        "`": "grave",
        "a": "a-lowercase",
        "b": "b-lowercase",
        "c": "c-lowercase",
        "d": "d-lowercase",
        "e": "e-lowercase",
        "f": "f-lowercase",
        "g": "g-lowercase",
        "h": "h-lowercase",
        "i": "i-lowercase",
        "j": "j-lowercase",
        "k": "k-lowercase",
        "l": "l-lowercase",
        "m": "m-lowercase",
        "n": "n-lowercase",
        "o": "o-lowercase",
        "p": "p-lowercase",
        "q": "q-lowercase",
        "r": "r-lowercase",
        "s": "s-lowercase",
        "t": "t-lowercase",
        "u": "u-lowercase",
        "v": "v-lowercase",
        "w": "w-lowercase",
        "x": "x-lowercase",
        "y": "y-lowercase",
        "z": "z-lowercase",
        "{": "curlyleft",
        "|": "verticalbar",
        "}": "curlyright",
        "~": "tilde",
        "Δ": "delta",
        "←": "arrowleft",
        "↑": "arrowup",
        "→": "arrowright",
        "↓": "arrowdown",
        "☐": "box",
        "♀": "female",
        "♂": "male",
        '"': "quotedouble",
    }
    try:
        return character_dict[char]
    except KeyError:
        return character_dict['☐']


def get_glyph_width(vert_collection):
    verts = []
    for group in vert_collection:
        verts.extend(group)
    return max(verts, key=lambda v: v[0])[0]


def get_m_size():
    gpencil = bpy.context.active_object.data
    font = gpencil.font
    letter_folder = os.path.join(os.path.dirname(__file__), 'fonts', font)
    glyph_name = get_char_name('M') + '.glyph'
    path = os.path.join(letter_folder, glyph_name)

    with open(os.path.join(letter_folder, glyph_name)) as f:
        char_text = f.read().strip()
    lines = char_text.split('\n')

    verts = []
    for line in lines:
        curve_verts = eval(line)
        for vert in curve_verts:
            verts.append(vert)
    max_x = max(verts, key=lambda v: v[0])[0]
    max_y = max(verts, key=lambda v: v[1])[1]
    return max_x, max_y


class GREASEPENCIL_OT_write(bpy.types.Operator):
    bl_label = "Write"
    bl_idname = "grease_writer.write"
    bl_description = "Create drawn-animated text"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(self, context):
        gpencil = bpy.context.view_layer.objects.active.data
        if gpencil.source_text != '':
            return True
        else:
            return False

    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        gpencil = obj.data

        text = bpy.data.texts[gpencil.source_text].as_string().strip()

        font = gpencil.font
        letter_folder = os.path.join(os.path.dirname(__file__), 'fonts', font)

        m_width, m_height = get_m_size()
        speed = gpencil.draw_speed
        kerning = gpencil.kerning
        line_height = gpencil.line_height
        thickness = gpencil.write_thickness
        color = gpencil.write_color

        current_x = 0
        current_y = 0

        glyph_strokes = []

        for char in text:
            if char == " ":
                current_x += m_width
            elif char == "\n":
                current_y -= m_height * line_height
                current_x = 0
            else:
                glyph_name = get_char_name(char) + ".glyph"
                with open(os.path.join(letter_folder, glyph_name)) as f:
                    char_text = f.read().strip()
                lines = char_text.split('\n')

                glyph_verts = []
                for line in lines:
                    verts = eval(line)
                    glyph_verts.append(copy.deepcopy(verts))

                    for vert in verts:
                        vert[0] += current_x + (thickness / 1000)
                        vert[1] += current_y - (m_height * line_height)
                    glyph_strokes.append(verts)

                current_x += get_glyph_width(glyph_verts) + (m_width * kerning)

        draw_glyph(glyph_strokes)

        return {"FINISHED"}
