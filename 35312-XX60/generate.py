# sugoku - footprint generator
# 35312-XX60 (02 to 15)
# SPDX-License-Identifier: MIT

from KicadModTree import *

fp_name = "35312-{:02d}60"
fp_description = "{}-pin 2.50mm Pitch Header, Vertical, Shrouded"
fp_tags = "THT 2.5mm {0}pin {0}P Molex"

PIN_START = 2
PIN_END = 15

LINE_WIDTH = 0.127

for pin_count in range(PIN_START, PIN_END+1):
    kicad_mod = Footprint(fp_name.format(pin_count))
    kicad_mod.setDescription(fp_description.format(pin_count))
    kicad_mod.setTags(fp_tags.format(pin_count))

    # pad size:
    # circle, through-hole
    # hole size 1.2mm circular
    # 2.5mm spacing
    pad_type = Pad.TYPE_THT
    pad_shape_1 = Pad.SHAPE_RECT
    pad_shape = Pad.SHAPE_OVAL
    def padshape(i): return pad_shape if i else pad_shape_1
    pad_size = (1.8, 1.8)
    pad_drill = 1.2
    pad_xdiff = 2.5

    for i in range(pin_count):
        kicad_mod.append(Pad(number=i+1, type=pad_type, shape=padshape(i), at=(i*(pad_xdiff), 0), size=pad_size, drill=pad_drill, layers=Pad.LAYERS_THT))

    pin_to_h_end = 2.48
    pin_to_bottom_end = 2.04
    width = 6.5
    bottom_extension = 0.6
    pin_to_top_end = (width - bottom_extension) - pin_to_bottom_end

    # 0, 0 is anchored at pin 1 of the connector
    bounds_start = (-pin_to_h_end, -pin_to_top_end)
    bounds_end = (pad_xdiff*(pin_count-1) + pin_to_h_end, pin_to_bottom_end)

    courtyard_spacing = 0.2

    kicad_mod.append(RectLine(start=bounds_start, end=bounds_end, layer='F.SilkS', width=LINE_WIDTH))
    kicad_mod.append(RectLine(start=[i - courtyard_spacing for i in bounds_start], end=[bounds_end[0] + courtyard_spacing, bounds_end[1] + courtyard_spacing + bottom_extension], layer='F.CrtYd'))

    kicad_mod.append(Text(type='reference', text='REF**', at=((bounds_end[0] + bounds_start[0])/2, bounds_start[1] - courtyard_spacing - 1), layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=fp_name.format(pin_count), at=((bounds_end[0] + bounds_start[0])/2, bounds_end[1] + courtyard_spacing + bottom_extension + 1), layer='F.Fab'))

    fh = KicadFileHandler(kicad_mod)
    fh.writeFile(f'{fp_name.format(pin_count)}.kicad_mod')