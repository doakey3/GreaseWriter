import math
from markdown2 import markdown


def make_toc_label(label, description):
    """
    Make a table-of-contents item with a link to the operator and
    description for it's tooltip.
    """
    description = reflow_paragraph(description, 31)

    hla = label.replace(' ', '_')
    html_link = ''.join([
        '<a name="top_', hla, '" href="#', hla, '" title="' + description + '">',
        label, '</a>'])
    return html_link


def reflow_paragraph(text, space, leading_space=''):
    '''
    Reflow a flattened paragraph so it fits inside horizontal
    space
    '''
    words = text.split(' ')
    growing_string = leading_space
    output_list = []

    while len(words) > 0:
        if growing_string == leading_space:
            growing_string += words[0]
            words.pop(0)
        elif len(growing_string + ' ' + words[0]) <= space:
            growing_string += ' ' + words[0]
            words.pop(0)
        else:
            output_list.append(growing_string + '\n')
            growing_string = leading_space
    output_list.append(growing_string)
    return ''.join(output_list)


def make_toc(info):
    """
    Generate a table of contents from the operator info
    """
    toc = ['<table>']

    labels = []

    for key in sorted(info.keys()):
        label = info[key]['name']
        description = info[key]['description']
        labels.append(make_toc_label(label, description))

    columns = [[], [], [], []]
    row_count = math.ceil(len(labels) / len(columns))

    i = 0
    col = 0
    while i < len(labels):
        for x in range(row_count):
            try:
                columns[col].append(labels[i])
                i += 1
            except IndexError:
                break
        col += 1

    dead_column = False
    column_width = str(int((1 / len(columns)) * 888)) + 'px'
    for row in range(row_count):
        toc.append('    <tr>')

        for col in range(len(columns)):
            try:
                toc.append('        <td width=' + column_width + '>' + columns[col][row] + '</td>')
            except IndexError:
                if dead_column == False:
                    remaining_rows = row_count - row
                    toc.append('        <td width=' + column_width + ' rowspan="' + str(remaining_rows) + '"></td>')
                    dead_column = True
        toc.append('    </tr>')
    toc.append('</table>')

    return '\n'.join(toc)


def make_seg_label(label):
    """
    Make the title label for an operator segment with a link back to the
    matching table of contents label
    """
    hla = label.replace(' ', '_')
    seg_label = ''.join([
        '    ', '<h3>', '<a name="', hla, '" href="#top_', hla, '">',
        label, '</a>', '</h3>'])
    return seg_label


def make_shortcuts_table(op_dict):
    """
    Make a table showing all the keyboard shortcuts, their functions,
    and a demo for a given operator
    """
    shortcuts = []
    functions = []
    demo = op_dict['demo']

    for i in range(len(op_dict['shortcuts'])):
        shortcuts.append(op_dict['shortcuts'][i].split(';')[0].strip())
        functions.append(op_dict['shortcuts'][i].split(';')[1].strip())

    for i in range(len(shortcuts)):
        hotkeys = shortcuts[i].split(' ')
        for x in range(len(hotkeys)):
            hotkeys[x] = '<img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/' + hotkeys[x].strip().upper() + '.png" alt="' + hotkeys[x].strip().upper() + '">'
        shortcuts[i] = ''.join(hotkeys)

    hotkeys_width = str(int((888 - 256) * 0.33)) + 'px'
    function_width = str(int((888 - 256) * 0.66)) + 'px'
    table = ['<table>']
    table.append('    <tr>')
    table.append('        <th width=' + hotkeys_width + '>Shortcut</th>')

    if len(functions) > 0:
        table.append('        <th width=' + function_width + '>Function</th>')
    if demo != '':
        table.append('        <th width=256px>Demo</th>')

    for i in range(len(shortcuts)):
        table.append('    <tr>')

        table.append('        <td align="center">' + ''.join(shortcuts[i]) + '</td>')
        table.append('        <td>' + markdown(functions[i]) + '</td>')

        if i == 0 and demo != '':
            table.append('        <td align="center" rowspan="' + str(len(shortcuts)) + '">' + '<img src="' + demo + '"></td>')

        table.append('    </tr>')
    table.append('</table>')
    return '\n'.join(table)


def make_operator_segments(info):
    """
    Using the operator info, make segments that put all that info together.
    """
    segments = []

    for key in sorted(info.keys()):
        label = make_seg_label(info[key]['name'])
        description = markdown(info[key]['description'])
        shortcut_table = make_shortcuts_table(info[key])

        segments.append('\n'.join([label, description, shortcut_table]))
    return '\n'.join(segments)


def make_readme():
    """
    Generate a nice-looking readme.
    """

    readme_path = 'README.rst'

    title = """
<h1 align="center">
  VSE_Transform_Tools</br>
</h1>
"""

    intro = markdown("""
## Installation
1. Go to the [Releases](https://github.com/doakey3/VSE_Transform_Tools/releases) page and download the latest `VSE_Transform_Tools.zip`
2. Open Blender
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded .zip file and install
5. Check the box next to "VSE Transform Tools"
6. Save User Settings so the addon remains active every time you open Blender
""".strip(), extras=['cuddled_lists'])

    operator_info = {
        'vse_transform_tools.add_transform': {
            'name': 'Add Transform',
            'description': "A transform modifier must be added to a strip before the strip can be scaled or rotated by this addon. If you're planning to make keyframes to adjust the scale or the rotation, ensure that you are modifying a transform strip by adding one with this operator.",
            'shortcuts': ['T; Add Transform'],
            'demo': 'https://i.imgur.com/v4racQW.gif',
        },
        'vse_transform_tools.adjust_alpha': {
            'name': 'Adjust Alpha',
            'description': "",
            'shortcuts': ['Q; Begin alpha adjusting', 'Ctrl; Round to nearest tenth', 'RIGHTMOUSE; Escape alpha adjust mode', 'LEFTMOUSE; Set alpha, end alpha adjust mode', 'RET; Set Alpha, end alpha adjust mode', 'ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE PERIOD; Set alpha to value entered'],
            'demo': 'https://i.imgur.com/PNsjamH.gif',
        },
        'vse_transform_tools.autocrop': {
            'name': 'Autocrop',
            'description': "Sets the scene resolution to fit all visible content in the preview window without changing strip sizes.",
            'shortcuts': ['SHIFT C; Autocrop'],
            'demo': 'https://i.imgur.com/IarxF14.gif',
        },
        'vse_transform_tools.call_menu': {
            'name': 'Call Menu',
            'description': "Bring up the menu for inserting a keyframe. Alternatively, you may enable automatic keyframing. <br> ![Automatic Keyframe Insertion](https://i.imgur.com/kFtT1ja.jpg)",
            'shortcuts': ['I; Call menu'],
            'demo': 'https://i.imgur.com/9Cx6XKj.gif',
        },
        'vse_transform_tools.crop': {
            'name': 'Crop',
            'description': "",
            'shortcuts': ['C; Begin/Set cropping, adding a transform if needed', 'ESC; Escape crop mode', 'LEFTMOUSE; Click the handles to drag', 'RET; Set crop, end cropping', 'Alt C; Uncrop'],
            'demo': 'https://i.imgur.com/k4r2alY.gif',
        },
        'vse_transform_tools.delete': {
            'name': 'Delete',
            'description': "Deletes all selected strips as well as any strips that are inputs of those strips. For example, deleting a transform strip with this operator will also delete the strip it was transforming.",
            'shortcuts': ['DEL; Delete', 'Shift DEL; Delete strips and remove any other strips in the timeline with the same source. For scene strips, the scenes themselves will also be deleted.'],
            'demo': 'https://i.imgur.com/B0L7XoV.gif',
        },
        'vse_transform_tools.duplicate': {
            'name': 'Duplicate',
            'description': "Duplicates all selected strips and any strips that are inputs of those strips. Calls the Grab operator immediately after duplicating.",
            'shortcuts': ['Shift D; Duplicate'],
            'demo': 'https://i.imgur.com/IJh7v3z.gif',
        },
        'vse_transform_tools.grab': {
            'name': 'Grab',
            'description': "",
            'shortcuts': ['G; Grab', 'Shift; Hold to enable fine tuning', 'Ctrl; Hold to enable snapping', 'RIGHTMOUSE; Escape grab mode', 'Esc; Escape grab mode', 'LEFTMOUSE; Set position, end grab mode', 'RET; Set position, end grab mode', 'ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE PERIOD; Set position by value entered', 'X Y; Constrain grabbing to the respective axis', 'MIDDLEMOUSE; Constrain grabbing to axis', 'ALT G; Set position to 0,0'],
            'demo': 'https://i.imgur.com/yQCFI0s.gif',
        },
        'vse_transform_tools.group': {
            'name': 'Group',
            'description': "",
            'shortcuts': ['Ctrl G; Group together selected sequences', 'Alt Shift G; Ungroup selected meta strip'],
            'demo': ''
        },
        'vse_transform_tools.meta_toggle': {
            'name': 'Meta Toggle',
            'description': "Toggles the selected strip if it is a META. If the selected strip is not a meta, recursively checks inputs until a META strip is encountered and toggles it. If no META is found, this operator does nothing.",
            'shortcuts': ['TAB; Meta toggle'],
            'demo': 'https://i.imgur.com/ya0nEgV.gif',
        },
        'vse_transform_tools.mouse_track': {
            'name': 'Mouse Track',
            'description': 'Select a transform strip or a strip with "image offset" enabled. Press Alt+A to play, hold M to continuously add keyframes to transform strip while tracking the position of the mouse.',
            'shortcuts': ['M; Hold to add keyframes, release to stop'],
            'demo': 'https://i.imgur.com/6091cqv.gif',
        },
        'vse_transform_tools.pixelate': {
            'name': 'Pixelate',
            'description': "Pixelate a clip by adding 2 transform modifiers: 1 shrinking, 1 expanding.",
            'shortcuts': ['P; Pixelate'],
            'demo': 'https://i.imgur.com/u8nUPj6.gif',
        },
        'vse_transform_tools.rotate': {
            'name': 'Rotate',
            'description': "",
            'shortcuts': ['R; Begin rotating, adding transform if needed.', 'Shift; Hold to enable fine tuning', 'Ctrl; Hold to enable stepwise rotation', 'RIGHTMOUSE; Escape rotate mode', 'Esc; Escape rotate mode', 'LEFTMOUSE; Set rotation, end rotate mode', 'RET; Set rotation, end rotate mode', 'ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE PERIOD; Set rotation to value entered', 'ALT R; Set rotation to 0 degrees'],
            'demo': 'https://i.imgur.com/3ru1Xl6.gif',
        },
        'vse_transform_tools.scale': {
            'name': 'Scale',
            'description': "",
            'shortcuts': ['S; Begin scaling, adding transform if needed.', 'Shift; hold to enable fine tuning', 'Ctrl; Hold to enable snapping', 'RIGHTMOUSE; Escape scaling mode', 'ESC; escape scaling mode', 'LEFTMOUSE; Set scale, end scaling mode', 'RET; Set scale, end scaling mode', 'ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE PERIOD; Set scale by value entered', 'X Y; Constrain scaling to respective axis', 'MIDDLEMOUSE; Constrain scaling to axis', 'Alt S; Unscale'],
            'demo': 'https://i.imgur.com/oAxSEYB.gif',
        },
        'vse_transform_tools.select': {
            'name': 'Select',
            'description': "",
            'shortcuts': ['RIGHTMOUSE; Select visible strip', 'SHIFT; Enable multi selection', 'A; Toggle selection'],
            'demo': 'https://i.imgur.com/EVzmMAm.gif',
        },
        'vse_transform_tools.set_cursor2d': {
            'name': 'Set Cursor 2D',
            'description': "Set the pivot point (point of origin) location. This will affect how strips are rotated and scaled.",
            'shortcuts': ['LEFTMOUSE; Cusor 2D to mouse position', 'Ctrl LEFTMOUSE; Snap cursor 2D to nearest strip corner or mid-point'],
            'demo': 'https://i.imgur.com/1uTD9C1.gif',
        },
        'vse_transform_tools.track_transform': {
            'name': 'Track Transform',
            'description': 'Use a pair of track points to pin a strip to another. The UI for this tool is located in the menu to the right of the sequencer in the Tools submenu. To pin rotation and/or scale, you must use 2 tracking points. <br> ![UI](https://i.imgur.com/wEZLu8a.jpg)',
            'shortcuts': [';'],
            'demo': 'https://i.imgur.com/nWto3hH.gif',
        },
    }

    toc_title = "<h2>Operators</h2>"

    table_of_contents = make_toc(operator_info)

    operator_segments = make_operator_segments(operator_info)

    html = '\n'.join([title, intro, toc_title, table_of_contents, operator_segments])

    lines = html.split('\n')
    for i in range(len(lines)):
        lines[i] = '    ' + lines[i]

    readme = '.. raw:: html\n\n' + '\n'.join(lines)

    with open(readme_path, 'w') as f:
        f.write(readme)

if __name__ == "__main__":
    make_readme()
