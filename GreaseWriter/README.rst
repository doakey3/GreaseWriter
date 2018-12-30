.. image:: https://i.imgur.com/VKEhIx3.gif

Installation
============
**This only works on Blender 2.8**

1. Download the latest .zip file from the releases_ page
2. Open Blender and go to Edit > Preferences > Install Add-on from File... Then navigate to the .zip file you downloaded and select it
3. Check the box that appears next to "Grease Writer"

.. _releases: https://www.github.com/doakey3/GreaseWriter/releases

Usage
=====
Writing
-------
1. Create a new Grease Pencil object in the 3D view (Shift + A > Grease Pencil > Blank)
2. With the Grease Pencil object selected, go to the data section of the Properties window where you will find the Grease Writer panel.
3. Create a text file with the desired text

  - Right-click at the edge of a window and split the area
  - Change the Window's view to the Text Editor
  - click the "New" button to start editing a text file

  .. image:: https://i.imgur.com/YqZd5Ji.gif

4. Enter the name of the Text file in the source text property in the Grease Writer panel
5. Adjust settings and click the "Write" button
6. Optionally add a decorator to the added text

.. image:: https://i.imgur.com/LpXjgNk.gif

Animating
---------
If you draw on a grease pencil object, you can automatically animate it by clicking the "Reanimate" button. Strokes will be drawn in the order they were created.

Tracing
-------
Select a tracer object and click trace. The tracer object's X and Y position will change to keep up with the animated grease pencil as it is being drawn.

.. image:: https://i.imgur.com/2XGSq6H.gif
