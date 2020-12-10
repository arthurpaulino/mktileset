import os
import sys

import struct

def get_png_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            return
        return struct.unpack('>ii', head[16:24])

def write(f, s, ow=False):
    f = open(f, "w" if ow else "a")
    f.write(s + "\n")
    f.close()

def q(s):
    return "\"" + s + "\""

file_name = sys.argv[1]
tile_size = int(sys.argv[2])

w, h = get_png_image_size(file_name)
if w != tile_size * 12 or h % (tile_size * 4) != 0:
    print("invalid img or tile size")
    exit()
root_name = file_name.split(".")[0]
tres_name = root_name + ".tres"
write(tres_name, "[gd_resource type=" + q("TileSet") + " load_steps=3 format=2]\n", True)
write(tres_name, "[ext_resource path=" + q("res://" + file_name) + " type=" + q("Texture") + " id=1]\n\n\n")
write(tres_name, "[sub_resource type=" + q("ConvexPolygonShape2D") +" id=1]")
write(tres_name, "points = PoolVector2Array( 0, 0, " +\
str(tile_size) + ", 0, " + str(tile_size) + ", " + str(tile_size) + ", 0, " + str(tile_size) + " )\n")
write(tres_name, "[resource]")
write(tres_name, "0/name = " + q("autotile"))
write(tres_name, "0/texture = ExtResource( 1 )\n\
0/tex_offset = Vector2( 0, 0 )\n\
0/modulate = Color( 1, 1, 1, 1 )\n\
0/region = Rect2( 0, 0, " + str(w) + ", " + str(h) + " )\n\
0/tile_mode = 1\n\
0/autotile/bitmask_mode = 1")

def get_bitmask_flags(i):
    return "Vector2( 0, 0 ), 144, Vector2( 0, 1 ), 146, Vector2( 0, 2 ), 18, Vector2( 0, 3 ), 16, Vector2( 1, 0 ), 176, Vector2( 1, 1 ), 178, Vector2( 1, 2 ), 50, Vector2( 1, 3 ), 48, Vector2( 2, 0 ), 184, Vector2( 2, 1 ), 186, Vector2( 2, 2 ), 58, Vector2( 2, 3 ), 56, Vector2( 3, 0 ), 152, Vector2( 3, 1 ), 154, Vector2( 3, 2 ), 26, Vector2( 3, 3 ), 24, Vector2( 4, 0 ), 187, Vector2( 4, 1 ), 434, Vector2( 4, 2 ), 182, Vector2( 4, 3 ), 250, Vector2( 5, 0 ), 440, Vector2( 5, 1 ), 510, Vector2( 5, 2 ), 447, Vector2( 5, 3 ), 62, Vector2( 6, 0 ), 248, Vector2( 6, 1 ), 507, Vector2( 6, 2 ), 255, Vector2( 6, 3 ), 59, Vector2( 7, 0 ), 190, Vector2( 7, 1 ), 218, Vector2( 7, 2 ), 155, Vector2( 7, 3 ), 442, Vector2( 8, 0 ), 432, Vector2( 8, 1 ), 438, Vector2( 8, 2 ), 446, Vector2( 8, 3 ), 54, Vector2( 9, 0 ), 506, Vector2( 9, 1 ), 254, Vector2( 9, 2 ), 443, Vector2( 9, 3 ), 63, Vector2( 10, 0 ), 504, Vector2( 10, 2 ), 511, Vector2( 10, 3 ), 191, Vector2( 11, 0 ), 216, Vector2( 11, 1 ), 251, Vector2( 11, 2 ), 219, Vector2( 11, 3 ), 27".replace(
        ", 0 )", ", " + str(i*4) + " )"
    ).replace(
        ", 1 )", ", " + str(i*4 + 1) + " )"
    ).replace(
        ", 2 )", ", " + str(i*4 + 2) + " )"
    ).replace(
        ", 3 )", ", " + str(i*4 + 3) + " )"
    )

all_bitmask_flags = ""

for i_tileset in range(h // (tile_size * 4)):
    if i_tileset > 0:
        all_bitmask_flags += ", "
    all_bitmask_flags += get_bitmask_flags(i_tileset)


all_bitmask_flags = "[ " + all_bitmask_flags + " ]"


write(tres_name, "0/autotile/bitmask_flags = " + all_bitmask_flags)


write(tres_name, "0/autotile/icon_coordinate = Vector2( 0, 3 )\n\
0/autotile/tile_size = Vector2( " + str(tile_size) + ", " + str(tile_size) + " )\n\
0/autotile/spacing = 0\n\
0/autotile/occluder_map = [  ]\n\
0/autotile/navpoly_map = [  ]\n\
0/autotile/priority_map = [  ]\n\
0/autotile/z_index_map = [  ]\n\
0/occluder_offset = Vector2( 0, 0 )\n\
0/navigation_offset = Vector2( 0, 0 )\n\
0/shape_offset = Vector2( 0, 0 )\n\
0/shape_transform = Transform2D( 1, 0, 0, 1, 0, 0 )\n\
0/shape = SubResource( 1 )\n\
0/shape_one_way = false\n\
0/shape_one_way_margin = 1.0")


collision_tuples = [
    (0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3),
    (3, 0), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (5, 0), (5, 3), (6, 0), (6, 3),
    (7, 1), (7, 2), (8, 0), (8, 1), (8, 3), (9, 3), (10, 0), (11, 0), (11, 2), (11, 3)
]

all_shapes = ""


for i_tileset in range(h // (tile_size * 4)):
    for idx, t in enumerate(collision_tuples):
        if i_tileset + idx > 0:
            all_shapes += ", "
        all_shapes += "{\n\
"+ q("autotile_coord") + ": Vector2( " + str(t[0]) + ", " + str(t[1] + 4 * i_tileset) + " ),\n\
"+ q("one_way") + ": false,\n\
"+ q("one_way_margin") + ": 1.0,\n\
"+ q("shape") + ": SubResource( 1 ),\n\
"+ q("shape_transform") + ": Transform2D( 1, 0, 0, 1, 0, 0 )\n\
}"

all_shapes = "[ " + all_shapes + " ]"

write(tres_name, "0/shapes = " + all_shapes)
write(tres_name, "0/z_index = 0")
