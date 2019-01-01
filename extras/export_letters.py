import bpy
import os
import io
import math
from contextlib import redirect_stdout
import sys
import bmesh


def update_progress(job_title, progress):
    length = 20
    block = int(round(length * progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title,
        "#" * block + "-" * (length-block),
        "%.2f" % (progress * 100))

    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


def verts2points(verts):
    points = []
    for vert in verts:
        point = [vert.co.x, vert.co.y, vert.co.z]
        points.append(point)
    return points


def get_glyph_size(vertices):
    """
    Get the size of a glyph
    """
    x_points = []
    y_points = []
    for vert in vertices:
        x_points.append(vert.co.x)
        y_points.append(vert.co.y)

    min_x = min(x_points)
    max_x = max(x_points)

    min_y = min(y_points)
    max_y = max(y_points)

    return min_x, max_x, min_y, max_y


def get_islands(obj):
    """
    Gets a list of vertices grouped by islands
    """
    edges = list(obj.data.edges)

    islands = []
    found = False
    while len(edges) > 0:
        if found == False:
            islands.append(list(edges[0].vertices))
            edges.pop(0)

        found = False
        i = 0
        while i < len(edges):
            for vert in edges[i].vertices:
                if vert in islands[-1]:
                    islands[-1].extend(list(edges[i].vertices))
                    edges.pop(i)
                    found = True
                    break
            i += 1

    for i in range(len(islands)):
        islands[i] = list(set(islands[i]))
    return islands


def convert_curve(obj):
    """
    Duplicate a curve and convert the duplicate to a mesh
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.duplicate()

    bpy.ops.object.convert(target='MESH')


def angle_between_points(p0, p1, p2):
    a = (p1[0] - p0[0])**2 + (p1[1] - p0[1])**2
    b = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
    c = (p2[0] - p0[0])**2 + (p2[1] - p0[1])**2

    angle = math.acos((a + b - c) / math.sqrt(4 * a * b)) * 180 / math.pi
    return angle


def get_angles(verts):
    """
    Get a list of angles for each vertex in a looped mesh object
    """
    angles = []
    for i in range(len(verts)):
        if i == 0:
            A = [verts[-1].co.x, verts[-1].co.y]
        else:
            A = [verts[i - 1].co.x, verts[i - 1].co.y]

        B = [verts[i].co.x, verts[i].co.y]

        if i == len(verts) - 1:
            C = [verts[0].co.x, verts[0].co.y]
        else:
            C = [verts[i + 1].co.x, verts[i + 1].co.y]

        ABC_angle = angle_between_points(A, B, C)
        angles.append(ABC_angle)
    return angles


def get_lowers(numbers, threshold):
    """
    Returns a list of numbers lower than threshold
    """
    lowers = []
    for num in numbers:
        if num <= threshold:
            lowers.append(num)
    return lowers


def clean_mesh(obj):
    convert_curve(obj)
    mesh_obj = bpy.context.view_layer.objects.active
    islands = get_islands(mesh_obj)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(mesh_obj.data)

    i = 0
    while i < len(islands):
        verts = []
        for index in islands[i]:
            bm.verts.ensure_lookup_table()
            verts.append(bm.verts[index])

        angles = get_angles(verts)
        threshold = 2

        if min(angles) > threshold:
            for f in range(1, len(islands[i + 1])):
                index = islands[i + 1][f]
                bm.verts[index - 1].select = True
            islands.pop(i + 1)

        else:
            if len(get_lowers(angles, threshold)) == 2:
                for x in range(2, len(angles)):
                    if angles[x] > threshold:
                        bm.verts.ensure_lookup_table()
                        bm.verts[islands[i][x] - 1].select = True
                    elif angles[x] < threshold:
                        break
        i += 1

    bpy.ops.mesh.delete()
    bpy.ops.object.mode_set(mode='OBJECT')

    return mesh_obj


def export_glyph(obj, folder, looped_font=False):
    name = obj.name
    path = os.path.join(folder, name + '.glyph')

    if looped_font == False:
        convert_curve(obj)
    else:
        try:
            clean_mesh(obj)
        except IndexError:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.delete()
            convert_curve(obj)

    duplicate = bpy.context.view_layer.objects.active
    islands = get_islands(duplicate)
    left, right, bottom, top = get_glyph_size(duplicate.data.vertices)
    points = verts2points(duplicate.data.vertices)

    for i in range(len(points)):
        points[i][0] -= left

    decimals = 5
    glyph_strokes = []
    for i in range(len(islands)):
        glyph_strokes.append([])
        for p in range(len(points)):
            if p in islands[i]:
                v = points[p]
                v[0] = round(v[0], decimals)
                v[1] = round(v[1], decimals)
                v[2] = 0
                glyph_strokes[-1].append(v)

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        bpy.ops.object.delete()

    text = ''
    for stroke in glyph_strokes:
        text += str(stroke) + '\n'
    text.strip()

    with open(path, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    objs = bpy.data.objects
    name = os.path.basename(bpy.data.filepath).replace('.blend', '')
    folder = os.path.dirname(bpy.data.filepath)

    path = os.path.join(folder, name)

    if not os.path.isdir(path):
        os.makedirs(path)

    for i in range(len(objs)):
        export_glyph(objs[i], path, looped_font=True)
        update_progress("Making Glyphs", i / len(objs))
    update_progress("Making Glyphs", 1)

