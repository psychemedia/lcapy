from schematic import Schematic

sch = Schematic()

sch.add('P1 1 0.1')
sch.add('R1 3 1; right')
sch.add('L1 2 3; right')
sch.add('C1 3 0; down')
sch.add('P2 2 0.2')

sch.draw(draw_nodes=False, label_nodes=False)
