.. image:: https://i.imgur.com/VKEhIx3.gif

.. contents::

Installation
============
**This only works on Blender 2.8**

1. Download the latest .zip file from the releases_ page
2. Open Blender and go to Edit > Preferences > Install Add-on from File... Then navigate to the .zip file you downloaded and select it
3. Check the box that appears next to "Grease Writer"
4. Click the "Save Preferences" button at the bottom.

.. image:: https://i.imgur.com/iRZpjX4.jpg

.. _releases: https://www.github.com/doakey3/GreaseWriter/releases

Usage
=====
Writing
-------
The UI is in the scene properties window. Edit the settings and enter some text into the text box or select a text file to write from, then click the "Write" button.

.. image:: https://i.imgur.com/YExDtjr.gif

Decorate
--------
Create an animated decorator for the grease pencil object such as an underline or an ellipse.

.. image:: https://i.imgur.com/9vBdmkD.gif

(Re)Animating
-------------
If you draw on a grease pencil object, you can automatically animate it by clicking the "Reanimate" button. Strokes will be drawn in the order they were created. The result is similar to what happens when a Build Modifier is applied to the grease pencil, except that pauses between stokes are added to emulate the hand drawn effect.

.. image:: https://i.imgur.com/uMj0rup.gif

Stipple It
----------
Redraws the strokes with stippled lines

.. image:: https://i.imgur.com/o2s6XTy.gif

Tracing
-------
Select a tracer object and click trace. The tracer object's X and Y position will change to keep up with the animated grease pencil as it is being drawn.

.. image:: https://i.imgur.com/JyvBYeV.gif
