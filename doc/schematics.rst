.. _schematics:

==========
Schematics
==========


Introduction
============

High quality schematics can be generated from a netlist using
Circuitikz for LaTeX diagrams.  This is much easier than writing
Circuitikz commands directly in LaTeX.

A semi-automatic component placement is used with hints required to
designate component orientation and explicit wires to link nodes of
the same potential but with different coordinates.

Here's an example:
   >>> from lcapy import Circuit
   >>> cct = Circuit()
   >>> cct.add('V 1 0 {V(s)}; down') 
   >>> cct.add('R 1 2; right') 
   >>> cct.add('C 2 0_2; down') 
   >>> cct.add('W 0 0_2; right') 
   >>> cct.draw('schematic.pdf')

Note, the orientation hints are appended to the netlist strings with a
semicolon delimiter.  The drawing direction is with respect to the
first node.  The component W is a wire.  Nodes with an underscore in
their name are not drawn with a closed blob.

The image generated by this netlist is:

.. image:: examples/schematics/schematic.png
   :width: 4cm


Here's another example, this time loading the netlist from a file:
   >>> from lcapy import Circuit
   >>> cct = Circuit('voltage-divider.sch')
   >>> cct.draw('voltage-divider.pdf')

Here are the contents of the file 'voltage-divider.sch'::

   Vi 1 0_1; down
   R1 1 2; right, size=1.5
   R2 2 0; down
   P1 2_2 0_2; down, v=V_o
   W 2 2_2; right
   W 0_1 0; right
   W 0 0_2; right

Here, P1 defines a port.  This is shown as a pair of open blobs.  The
wires do not need unique names.

.. image:: examples/schematics/voltage-divider.png
   :width: 5cm


Component orientation
---------------------

Lcapy uses a semi-automated component layout.  Each component requires
a specified orientation: up, down, left, or right.  In addition,
attributes can be added to override color, size, etc.

The drawing direction provides a constraint.  For example, the nodes
of components with a vertical orientation have the same x coordinate,
whereas nodes of horizontal components have the same y coordinate.

The component orientation is specified by a rotation angle.  This
angle is degrees anticlockwise with zero degrees being along the
positive x axis.  For example,

   >>> cct.add('D1 1 2; rotate=45')

The component orientation can also be specified by a direction keyword: 

- right (0 degrees)

- left  (180 degrees)

- up    (90 degrees)

- down  (-90 degrees)

For example:

.. literalinclude:: examples/schematics/Dright.sch

.. image:: examples/schematics/Dright.png
   :width: 2.5cm

.. literalinclude:: examples/schematics/Ddown.sch

.. image:: examples/schematics/Ddown.png
   :width: 1.5cm

Note, the drawing direction is from the positive node to the negative
node.

Here's an example of how to draw a diode bridge:

.. literalinclude:: examples/schematics/Dbridge.sch

.. image:: examples/schematics/Dbridge.png
   :width: 4cm


Components can be mirrored about the x-axis using the mirror
attribute.  For example, to switch the order of the inverting and
non-inverting inputs of an opamp use:

   >>> cct.add('E1 1 2 opamp 3 0; right, mirror')


Component size
--------------

By default each component has a minimum size of 1. This can be
stretched to satisfy a node constraint.  The minimum size is specified
using the size keyword, for example:

   >>> cct.add('R1 1 2; right, size=2')

The size argument is used as a scale factor for the component node
spacing.  The size can also be specified by adding a value to the
`left`, `right`, `up`, or `down` arguments.  For example:

   >>> cct.add('R1 1 2; right=2')

Here's a comparison of resistors of different sizes.

.. literalinclude:: examples/schematics/resistors1.sch

.. image:: examples/schematics/resistors1.png
   :width: 14cm

By default, a component with size 1 has its nodes spaced by 2 units.
This can be changed using the `node_spacing` option of the schematic.
For example,

.. literalinclude:: examples/schematics/resistors2.sch

.. image:: examples/schematics/resistors2.png
   :width: 10.5cm

Be default, a component has a length of 1.5 units.  This can be
changed using the `cpt_size` option of the schematic.  For example,

.. literalinclude:: examples/schematics/resistors3.sch

.. image:: examples/schematics/resistors3.png
   :width: 14cm

.. literalinclude:: examples/schematics/resistors4.sch

.. image:: examples/schematics/resistors4.png
   :width: 7cm

The size of components can scaled with the `scale` attribute:

.. literalinclude:: examples/schematics/resistors6.sch

.. image:: examples/schematics/resistors6.png
   :width: 14cm

The overall schematic can be scaled with the `scale` option of the schematic:

.. literalinclude:: examples/schematics/resistors5.sch

.. image:: examples/schematics/resistors5.png
   :width: 7cm


Nodes
-----

Nodes are shown by a blob.  By default, only the primary nodes (those
without an underscore in them) are shown by default.  This is
equivalent to:

    >>> cct.draw(draw_nodes='primary')

All nodes can be drawn using:

    >>> cct.draw(draw_nodes='all')

Only the nodes where there are more than two branches can be drawn using:

    >>> cct.draw(draw_nodes='connections')

No nodes can be drawn using:

    >>> cct.draw(draw_nodes=False)

By default, only the primary nodes are labelled.  All nodes can be
labelled (this is useful for debugging) using:

    >>> cct.draw(label_nodes='all')

No nodes can be labelled using:

    >>> cct.draw(label_nodes=False)

Only nodes starting with a letter can be labelled using:

    >>> cct.draw(label_nodes='alpha')

In this case nodes with names such as `in` and `out` will be displayed
but not numeric node names.

These options can be stored with the schematic netlist, for example::

  C1 1 0 100e-12; down, size=1.5, v={5\,kV}
  R1 1 6 1500; right
  R2 2 4 1e12; down
  C2 3 5 5e-9; down
  W 2 3; right
  W 0 4; right
  W 4 5; right
  SW 6 2 no; right, l=, size=1.5
  ; draw_nodes=connections, label_nodes=False, label_ids=False


Components
==========

Only linear, time-invariant, components can be analyzed.


Diodes
------

Diodes can be drawn but not simulated.   A standard diode is described using:

     Dname Np Nm

Other diodes are specified with an additional argument:

     Dname Np Nm schottky|led|zener|tunnel|photo 


Here's an example:

.. literalinclude:: examples/schematics/diodes.sch

.. image:: examples/schematics/diodes.png
   :width: 10cm


Gyrators
--------

.. literalinclude:: examples/schematics/GY1.sch

.. image:: examples/schematics/GY1.png
   :width: 2cm


Integrated circuits
-------------------

ICs can be drawn but not simulated.  Here's an example:

.. literalinclude:: examples/schematics/ic1.sch

.. image:: examples/schematics/ic1.png
   :width: 8cm

In this example, the `chip2121` keyword specifies a block with two
pins on the left, one on the bottom, two on the right, and one at the
top.  The pins are enumerated anti-clockwise from top-left.  Since the
pin names start with a dot the associated node names are prefixed by
the name of the chip, for example, `U1.PIO1`.

With the `pins` attribute set to `auto` the pins are labelled with
their names unless the pin name starts with an underscore.

The supported chips are:
 - `chip1310`
 - `chip2121`
 - `chip3131`
 - `chip4141`
 - `buffer`
 - `inverter`

Here's another example where the pin labels are explicitly defined
with the `pins` attribute:

.. literalinclude:: examples/schematics/stepup.sch

.. image:: examples/schematics/stepup.png
   :width: 8cm


Meters
------

Here's an example using a voltmeter and an ammeter:

.. literalinclude:: examples/schematics/meters2.sch

.. image:: examples/schematics/meters2.png
   :width: 5cm


Opamps
------

Opamps can be drawn using the `opamp` argument to a VCCS.   For example:

.. literalinclude:: examples/schematics/opamp1.sch

.. image:: examples/schematics/opamp1.png
   :width: 5cm

The size can be controlled with the `scale` and `size` options.  The
positions of the inverting and non-inverting inputs can be flipped
with the `mirror` option.

.. literalinclude:: examples/schematics/opamp2.sch

.. image:: examples/schematics/opamp2.png
   :width: 5cm


.. literalinclude:: examples/schematics/opamp3.sch

.. image:: examples/schematics/opamp3.png
   :width: 5cm


.. literalinclude:: examples/schematics/opamp4.sch

.. image:: examples/schematics/opamp4.png
   :width: 5cm

Fully differential opamps can be drawn in a similar manner using the
fdopamp argument to a VCCS.  For example:

.. literalinclude:: examples/schematics/fdopamp1.sch

.. image:: examples/schematics/fdopamp1.png
   :width: 5cm


Switches
--------

Switches can be drawn but they are ignored for analysis since they
make the circuit time-varying.

The general format is:

     SWname Np Nm nc|no|push

Here's an example:

.. literalinclude:: examples/schematics/switches.sch

.. image:: examples/schematics/switches.png
   :width: 8cm


Transformers
------------

.. literalinclude:: examples/schematics/TF1.sch

.. image:: examples/schematics/TF1.png
   :width: 1.4cm

.. literalinclude:: examples/schematics/TFcore1.sch

.. image:: examples/schematics/TFcore1.png
   :width: 1.4cm

.. literalinclude:: examples/schematics/TFtap1.sch

.. image:: examples/schematics/TFtap1.png
   :width: 3cm

.. literalinclude:: examples/schematics/TFtapcore1.sch

.. image:: examples/schematics/TFtapcore1.png
   :width: 3cm


Transistors
-----------

Transistors (BJT, JFET, and MOSFET) can be drawn but not analyzed.  Both
are added to the netlist using a syntax similar to that of SPICE.  A BJT
is described using:
    
     Qname NC NB NE npn|pnp

where NC, NB, and NE denote the collector, base, and emitter nodes.
A MOSFET is described using:

     Mname ND NG NS nmos|pmos

where ND, NG, and NS denote the drain, gate, and source nodes.

A JFET is described using:

     Jname ND NG NS njf|pjf

where ND, NG, and NS denote the drain, gate, and source nodes.

Here's an example:

.. literalinclude:: examples/schematics/transistors.sch


.. image:: examples/schematics/transistors.png
   :width: 16cm


Transmission lines
------------------

A transmission line is a two-port device.  Here's an example:

.. literalinclude:: examples/schematics/tline3.sch

.. image:: examples/schematics/tline3.png
   :width: 8cm


Wires
=====

Wires are useful for schematic formatting, for example,

   W 1 2; right

Here an anonymous wire is created since it has no identifier.

The line style of wires can be changed, such as dashed or dotted (see
:ref:`linestyles`).

Wires can be implicitly added using the `offset` attribute.  Here's an
example to draw two parallel resistors:

.. literalinclude:: examples/schematics/parallel.sch

.. image:: examples/schematics/parallel.png
   :width: 5cm
     

Arrows
------

Arrows can be drawn on wires using the `startarrow` and `endarrow` attributes.
There are many arrow styles, see the tikz manual.  For example,

.. literalinclude:: examples/schematics/arrows.sch

.. image:: examples/schematics/arrows.png
   :width: 5cm


Implicit wires
--------------

Implicit wires are commonly employed for power supply and ground
connections.  They have the `implicit` attribute.


Block diagrams
==============

Block diagrams can be constructed with the following components:
 - `TF` transfer function
 - `SPpp`, `SPpm`, `SPppp`, `SPpmm`, `SPppm` summing points
 - `MX` mixer
 - `box` rectangular box
 - `circle` circle (or ellipse)

Here's an example showing negative feedback:

.. literalinclude:: examples/schematics/negative-feedback3.sch

.. image:: examples/schematics/negative-feedback3.png
   :width: 8cm


Summing points
--------------

There are a number of summing point varieties: `SPpp`, `SPpm`,
`SPppp`, `SPpmm`, `SPppm`.  The `p` suffix stands for plus, the `m`
suffix stands for minus.  The other variations can be generated using
the `mirror` attribute.

Here's an example:

.. literalinclude:: examples/schematics/SP4.sch

.. image:: examples/schematics/SP4.png
   :width: 2.5cm


Mixers
------

Here's a example of a mixer:

.. literalinclude:: examples/schematics/MX1.sch

.. image:: examples/schematics/MX1.png
   :width: 3cm


Boxes and circles
-----------------

`box` and `circle` have default anchor nodes based on the centre (`c`)
and sixteen directions of the compass: `n`, `nne`, `ne`, `ene`, `e`,
`ese`, `se`, `sse`, `s`, `ssw`, `sw`, `wsw`, `w`, `wnw`, `nw`, `nww`.

The aspect ratio of a box can be controlled with the `aspect`
attribute.

Here's an example of their use:

.. literalinclude:: examples/schematics/fir5.sch

.. image:: examples/schematics/fir5.png
   :width: 5cm


The label can be replaced by an image, using the `image` keyword.  For example,

.. literalinclude:: examples/schematics/image1.sch


Annotation
==========

Schematics can be annotated using additional tikz commands in the
netlist.  These are delimited by a line starting with two semicolons,
for example:

.. literalinclude:: examples/schematics/fit1.sch

This example draws dashed boxes around the nodes 0, 1, and 6 and 2, 3,
4, and 5:

.. image:: examples/schematics/fit1.png
   :width: 7cm

Alternatively, the boxes can be fit around named components, for
example::

    ;;\node[blue,draw,dashed,inner sep=5mm, fit=(R2) (C2), label=CMOS input model]{};


Styles
======

Three component styles are supported: `american` (default), `british`, and
`european`.  The style is set by a style argument to the `draw` method
or by a schematic option.  For example,

.. literalinclude:: examples/schematics/lpf1-buffer-loaded3.sch

.. image:: examples/schematics/lpf1-buffer-loaded3.png
   :width: 10.5cm
 

Colors
------

By default the components are drawn in black.  This can be overridden
with the color attribute, for example:

   >>> cct.add('R1 1 2; right, color=blue')


.. _linestyles:

Line styles
-----------

The line style of wires can be changed using the tikz attributes, `dashed`, `dotted`, `thick`, `ultra thick`, `line width`, and many others.  For example,

.. literalinclude:: examples/schematics/wirestyles.sch

.. image:: examples/schematics/wirestyles.png
   :width: 8cm


Labels
------

Each component has a component identifier label and a value label.
These can be augmented by explicit voltage and current labels.

- i=label -- annotate current through component with label
 
- v=label -- annotate voltage across component with label

- l=label -- component label

The label name can be displayed using LaTeX math mode by enclosing the
name between dollar signs.  Thus superscripts and subscripts can be
employed.  For example,

>>> cct.add('R1 1 2; right, i=$I_1$, v=$V_{R_1}$')

The label position, current and voltage direction can be controlled
with attributes _ ^ < and >, for example i^<=I_1.  See the Circuitikz
manual for details.

By default, if a component has a value label it is displayed,
otherwise the component identifier is displayed.  Both can be
displayed using:

    >>> cct.draw(label_ids=True, label_values=True)

Schematic options are separated using a comma.  If you need a comma,
say in a label, enclose the field in braces.  For example:

    >>> C1 1 0 100e-12; down, size=1.5, v={5\,kV}

Math-mode labels need to be enclosed in `$...$`.  There is an
experimental feature that is activated when the label starts with a
single un-matched `$`.  In this case, Lcapy tries to generate a nice LaTeX label.
For example, words in sub- and superscripts are converted into a roman
font using `mathrm`.  This feature is also activated if the label is
not enclosed in `$...$` but includes an `^` or `_`.

Voltage labels can be annotated between pairs of nodes using an
open-circuit component.   For example,

    >>> O1 1 0; down, v=V_1


Component attributes
--------------------

- `size`: scale factor for distance between component's nodes

- `scale`: scale factor for length of component

- `rotate`: angle in degrees to rotate component anti-clockwise

- `mirror`: mirror component in x-axis (opamps, transistors)

- `invisible`: do not draw

- `color`: component color

- `variable`: for variable resistors, inductors, and capacitors

- `fixed`: do not stretch

- `aspect`: set aspect ratio for boxes

- `pins`: define pin labels for ICs

- `offset`: distance to orthogonally offset component (useful for parallel components)
  

Here's an example using the variable attribute:

.. literalinclude:: examples/schematics/variable1.sch

.. image:: examples/schematics/variable1.png
   :width: 5cm


Schematic attributes
--------------------

- `node_spacing`: scale factor for distance between component nodes (default 2)

- `cpt_size`: length of component (default 1.5)

- `scale`: scale factor (default 1)

- `help_lines`: spacing between help lines (default 0 to disable)

- `draw_nodes`: specifies which nodes to draw (default `primary`). Its argument can either be `all`, `connections` (nodes that connect at least two components), `none`, or `primary` (node names without an underscore).

- `label_nodes`: specifies which nodes to label (default `primary`).  Its argument can either be `all`, `alpha` (node names starting with a letter), `none`, or `primary` (node names without an underscore).

- `label_ids`: specifies whether component ids are drawn (default `true`)

- `label_values`: specifies whether component values are drawn (default `true`)

- `style`: specifies the component style.  This is either `american`,  `british`, or `european` (default `american`).

Schematic attributes apply to the whole schematic.  They can be specified by starting a netlist with a semicolon, for example,

    ;help_lines=1, draw_nodes=connections

The schematic attributes can be overridden using arguments to the `draw` method.  For example,
 
    >>> sch.draw(draw_nodes='alpha')


Includes
========

Large schematics can be composed by including smaller schematics using the `.include` directive, for example::
   
   .include part1.sch
   .include part2.sch

Each of the smaller schematics can be included into their own namespace to avoid conflicts, for example::

   .include LC1.sch as s1
   .include LC1.sch as s2
   W s1.2 s2.1; right=0.1
   W s1.3 s2.0; right=0.1



Namespaces
==========

Hierarchical namespaces are supported, for example::

   a.R1 1 2; right
   b.R1 1 2; right

This creates two resistors: `a.R1` with nodes `a.1` and `a.2` and `b.R1` with nodes `b.1` and `a.2`.   They can be joined using::

   W a.2 b.1; right

When node names start with a dot, they are defined relative to the
name of the component, for example::

   R1 .p .m; right
   W 1 R1.p; right
   W R1.m 2; right



Examples
========

.. literalinclude:: examples/schematics/opamp-inverting-amplifier.sch

.. image:: examples/schematics/opamp-inverting-amplifier.png
   :width: 5cm


.. literalinclude:: examples/schematics/opamp-noninverting-amplifier.sch

.. image:: examples/schematics/opamp-noninverting-amplifier.png
   :width: 5cm


.. literalinclude:: examples/schematics/opamp-inverting-integrator.sch

.. image:: examples/schematics/opamp-inverting-integrator.png
   :width: 5cm


.. literalinclude:: examples/schematics/cmos1.sch

.. image:: examples/schematics/cmos1.png
   :width: 5cm


.. literalinclude:: examples/schematics/D4.sch

.. image:: examples/schematics/D4.png
   :width: 3.5cm


.. literalinclude:: examples/schematics/pic6.sch

.. image:: examples/schematics/pic6.png
   :width: 3.5cm


.. literalinclude:: examples/schematics/K1.sch

.. image:: examples/schematics/K1.png
   :width: 2.5cm


.. literalinclude:: examples/schematics/VRL2.sch

.. image:: examples/schematics/VRL2.png
   :width: 8cm


.. literalinclude:: examples/schematics/lpf1-buffer-loaded2.sch

.. image:: examples/schematics/lpf1-buffer-loaded2.png
   :width: 10.5cm


.. literalinclude:: examples/schematics/sallen-key-lpf1.sch

.. image:: examples/schematics/sallen-key-lpf1.png
   :width: 9cm


.. literalinclude:: examples/schematics/cmos-backdrive2.sch

.. image:: examples/schematics/cmos-backdrive2.png
   :width: 9cm


.. literalinclude:: examples/schematics/pierce-oscillator.sch

.. image:: examples/schematics/pierce-oscillator.png
   :width: 4cm



File formats
============

Lcapy uses the filename extension to determine the file format to
produce.  This must be one of tex, schtex, png, svg, or pdf.  The schtex
format is useful for including schematics into LaTeX documents.  The
tex format generates a standalone LaTeX file.  If no filename is
specified, the schematic is displayed on the screen.



schtex.py
=========

`schtex.py` is a Python script that will generate a schematic from a
netlist file.  For example, here's how a PNG file can be generated:

   >>> schtex.py Dbridge.sch Dbridge.png

The generated stand-alone LaTeX file can be obtained using:

   >>> schtex.py Dbridge.sch Dbridge.tex

If you wish to include the schematic into a LaTeX file use:

   >>> schtex.py Dbridge.sch Dbridge.schtex

and then include the file with `\\input{Dbridge.schtex}`.

`schtex.py` has many command line options to configure the drawing.
These override the options specified in the netlist file.  For example:

   >>> schtex.py --draw_nodes=connections --label_nodes=false --cpt-size=1 --help_lines=1 Dbridge.sch Dbridge.pdf


Drawing tips
============

Lcapy uses a semi-automated approach to component layout.  For each
component it needs its orientation and size.  By default the size
is 1.  This is the minimum distance between its nodes (for a one-port
device). If the component can be stretched, Lcapy will increase but
never decrease this distance.

The x and y positions of nodes are computed independently using a
graph.  An error can occur if components have the wrong orientation
since this makes the graph inconsistent.  Unfortunately, it is not
trivial to find the offending component so it is best to draw a
schematic incrementally and to test it as you go.  A sketch on a piece
of paper showing the nodes is useful.

Problems can occur using components, such as integrated circuits and
opamps, that cannot be stretched.  Usually this is due to a conflict
between constraints.  A solution is to reduce the size of the
component if it can be stretched, such as a wire or resistor.
Sometimes it is necessary to add a short interconnecting wire.

The stretching of components can be prevented by specifying the
`fixed` attribute.

Additional constraints can be supplied by using an invisible
component, for example, an open-circuit.

Grid lines can be added to a schematic using some Tikz markup.  For
example::

   ;;\draw[help lines] (0,0) grid [xstep=0.1, ystep=0.1] (10,5);  
  
