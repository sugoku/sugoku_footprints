# sugoku - footprint generator
# DS1128-S80BP
# SPDX-License-Identifier: MIT

from KicadModTree import *

fp_name = "DS1128-S80BP"
fp_description = "RJ45 Connector 8P, 1 Port"
fp_tags = "RJ45 8P Connfly DS1128"

kicad_mod = Footprint(fp_name)
kicad_mod.setDescription(fp_description)
kicad_mod.setTags(fp_tags)

length = 15.88  # x, mm
width = 21.4  # y, mm

# small pins are 8P separated into two rows, 2.54mm spacing between each pin and 1.27mm stagger between each row (row nearest to center is more left)
# 0.9mm diameter
# large mounting holes are 3.25mm, shield pins are 1.6mm (in diameter)
# we will probably use the actual center of the connector as the origin
pad_type = Pad.TYPE_THT
pad_shape_1 = Pad.SHAPE_RECT
pad_shape = Pad.SHAPE_CIRCLE
def padshape(i): return pad_shape if i else pad_shape_1

pad_size_small = (1.5, 1.5)
pad_drill_small = 0.9
pad_xdiff_small = 2.54
pad_ydiff_small = 2.54
pad_rowoffset_small = 1.27
pad_count_small = 4
pad_yoffset_small = 8.89 - pad_ydiff_small
# 2 rows

pad_size_mount = (3.4, 3.4)
pad_drill_mount = 3.25
pad_xdiff_mount = 11.43
# no y offset because the mounting pegs are center aligned

pad_size_shield = (2.4, 2.4)
pad_drill_shield = 1.6
pad_xdiff_shield = length
pad_yoffset_shield = 3.68

# small pins, start from bottom left
for i in range(2):
    startx = -1 * (pad_xdiff_small * ((pad_count_small - 1) / 2) + ((-1)**(i%2)) * (pad_rowoffset_small / 2))
    y = -1 * (pad_yoffset_small + pad_ydiff_small*i)
    for j in range(pad_count_small):
        x = startx + j * pad_xdiff_small
        n = 1+(j*2+i)
        kicad_mod.append(Pad(number=n, type=Pad.TYPE_THT, shape=padshape(n-1),
                at=[x, y], size=pad_size_small, drill=pad_drill_small, layers=Pad.LAYERS_THT))

# mounting holes
for i in range(2):
    kicad_mod.append(Pad(type=Pad.TYPE_THT, shape=pad_shape,
            at=[((-1)**((i+1)%2)) * pad_xdiff_mount / 2, 0], size=pad_size_mount, drill=pad_drill_mount, layers=Pad.LAYERS_THT))

# shield pins
for i in range(2):
    kicad_mod.append(Pad(number="SH", type=Pad.TYPE_THT, shape=pad_shape,
            at=[((-1)**((i+1)%2)) * pad_xdiff_shield / 2, pad_yoffset_shield], size=pad_size_shield, drill=pad_drill_shield, layers=Pad.LAYERS_THT))

bounds_start = (-length/2, -width/2)
bounds_end = (length/2, width/2)

courtyard_spacing = 0.5

kicad_mod.append(RectLine(start=bounds_start, end=bounds_end, layer='F.SilkS'))
kicad_mod.append(RectLine(start=[i - courtyard_spacing for i in bounds_start], end=[i + courtyard_spacing for i in bounds_end], layer='F.CrtYd'))

kicad_mod.append(Text(type='reference', text='REF**', at=(0, bounds_start[1] - courtyard_spacing - 1.5), layer='F.SilkS'))
kicad_mod.append(Text(type='value', text=fp_name, at=(0, bounds_end[1] + courtyard_spacing + 1.5), layer='F.Fab'))

fh = KicadFileHandler(kicad_mod)
fh.writeFile(f'{fp_name}.kicad_mod')