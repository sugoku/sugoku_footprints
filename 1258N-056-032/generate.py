# sugoku - footprint generator
# 1258N-056-032
# SPDX-License-Identifier: MIT

from KicadModTree import *

fp_name = "1258N-056-032"
fp_description = "Card Edge Connector, 3.96mm Pitch, DIP, 56 pin"
fp_tags = "THT DIP 3.96mm 56pin"

kicad_mod = Footprint(fp_name)
kicad_mod.setDescription(fp_description)
kicad_mod.setTags(fp_tags)

# pad size:
# oval, through-hole
# 2.4mm X, 2.6mm Y (connector viewed horizontally)
# hole size 1.25mm circular
pad_type = Pad.TYPE_THT
pad_shape_1 = Pad.SHAPE_RECT
pad_shape = Pad.SHAPE_OVAL
pad_size = (2.4, 2.6)
pad_drill = 1.25
pad_xdiff = 3.96
pad_ydiff = 5.08
pad_count = 56
pad_rows = 2

for i in range(pad_count):
    kicad_mod.append(Pad(number=i+1, type=pad_type, shape=(pad_shape_1 if not i else pad_shape), at=((i // pad_rows)*(pad_xdiff), (i % pad_rows)*(pad_ydiff)), size=pad_size, drill=pad_drill, layers=Pad.LAYERS_THT))

full_length = 132.48  # A
long_edge_to_pin = (full_length - pad_xdiff * (pad_count//pad_rows - 1)) / 2  # (A - E) / 2
mounting_hole_diff = 126.13  # B
long_edge_to_mounting_hole = (full_length - mounting_hole_diff) / 2  # (A - B) / 2

full_width = 10
short_edge_to_pin = (full_width - ((pad_rows - 1) * pad_ydiff)) / 2

# 0, 0 is anchored at pin 1 of the connector
x_edge_start = -long_edge_to_pin
y_edge_start = -short_edge_to_pin
bounds_start = (x_edge_start, y_edge_start)
bounds_end = (x_edge_start + full_length, y_edge_start + full_width)

courtyard_spacing = 0.5

kicad_mod.append(RectLine(start=bounds_start, end=bounds_end, layer='F.SilkS'))
kicad_mod.append(RectLine(start=[i - courtyard_spacing for i in bounds_start], end=[i + courtyard_spacing for i in bounds_end], layer='F.CrtYd'))

mounting_hole_diameter = 3.5
kicad_mod.append(Circle(center=(x_edge_start + long_edge_to_mounting_hole, pad_ydiff / 2), radius=mounting_hole_diameter/2, layer='F.SilkS'))
kicad_mod.append(Circle(center=(x_edge_start + long_edge_to_mounting_hole + mounting_hole_diff, pad_ydiff / 2), radius=mounting_hole_diameter/2, layer='F.SilkS'))

kicad_mod.append(Text(type='reference', text='REF**', at=(x_edge_start + full_length/2, y_edge_start - courtyard_spacing - 1.5), layer='F.SilkS'))
kicad_mod.append(Text(type='value', text=fp_name, at=(x_edge_start + full_length/2, y_edge_start + full_width + courtyard_spacing + 1.5), layer='F.Fab'))

fh = KicadFileHandler(kicad_mod)
fh.writeFile(f'{fp_name}.kicad_mod')