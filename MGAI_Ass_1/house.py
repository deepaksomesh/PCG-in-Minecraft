import random
from gdpc import Block, Editor, Box
from gdpc import geometry as geo
from gdpc import interface

ED = Editor(buffering=True)
# Here we read start and end coordinates of our build area
build_area = ED.getBuildArea()  # BUILDAREA
minX, minY, minZ = build_area.begin
maxX, maxY, maxZ = build_area.last


worldSlice = ED.loadWorldSlice(build_area.toRect(), cache=True)  # this takes a while

buildHeight = 0

# This dictionary contains different materials we use to build. we are mapping different components
# that goes well with each material style.
BUILDING = {
    "quartz_bricks": {
        "door": "warped_door",
        "window": "light_blue_stained_glass",
        "beam": "light_blue_terracotta",
        "bed": "light_blue_bed",
        "carpet": "red_carpet",
        "flower_1": "red_tulip",
        "flower_2": "orange_tulip"
    },
    "red_concrete": {
        "door": "birch_door",
        "window": "light_gray_stained_glass",
        "beam": "white_terracotta",
        "bed": "orange_bed",
        "carpet": "white_carpet",
        "flower_1": "dandelion",
        "flower_2": "poppy"
    },
    "white_terracotta": {
        "door": "acacia_door",
        "window": "black_stained_glass",
        "beam": "magenta_terracotta",
        "bed": "red_bed",
        "carpet": "light_blue_carpet",
        "flower_1": "blue_orchid",
        "flower_2": "red_tulip"
    },
    "light_blue_terracotta": {
        "door": "oak_door",
        "window": "purple_stained_glass",
        "beam": "quartz_bricks",
        "bed": "magenta_bed",
        "carpet": "green_carpet",
        "flower_1": "oxeye_daisy",
        "flower_2": "orange_tulip"
    },
    "magenta_terracotta": {
        "door": "spruce_door",
        "window": "cyan_stained_glass",
        "beam": "white_terracotta",
        "bed": "white_bed",
        "carpet": "gray_carpet",
        "flower_1": "azure_bluet",
        "flower_2": "white_tulip"
    }
}

chosen_block = random.choice(list(BUILDING.keys()))
chosen_door = BUILDING[chosen_block]["door"]
chosen_window = BUILDING[chosen_block]["window"]
chosen_slab = BUILDING[chosen_block]["beam"]
chosen_bed = BUILDING[chosen_block]["bed"]
chosen_carpet = BUILDING[chosen_block]["carpet"]
chosen_flower1 = BUILDING[chosen_block]["flower_1"]
chosen_flower2 = BUILDING[chosen_block]["flower_2"]
print(f"The chosen material is {chosen_block}")

def build_road():
    """ Here we calculate the average height around the player env and build the road """
    x_ctr = minX + (maxX - minX) // 2  # Getting center between min and max
    z_ctr = minZ + (maxZ - minZ) // 2
    heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    print("Calculating road height...")
    # Caclulating the average height along where we want to build our road
    y = heights[(x_ctr - minX, z_ctr - minZ)]
    for x in range(minX, maxX + 1):
        newy = heights[(x - minX, z_ctr - minZ)]
        y = (y + newy) // 2
    for z in range(minZ, maxZ + 1):
        newy = heights[(x_ctr - minX, z - minZ)]
        y = (y + newy) // 2

    global buildHeight
    buildHeight = y

    print(f"Teleporing player to the build location...")
    command = f"tp @p {x_ctr} {y + 2} {z_ctr}"
    interface.runCommand(command)

    print(f"clearing the ground at {y}.....where height {buildHeight} for {x_ctr}, {z_ctr}")

    print("Building road...")

    # east road
    geo.placeCuboid(ED, (x_ctr - 2, y, minZ), (x_ctr - 2, y, maxZ), Block("end_stone_bricks"))
    geo.placeCuboid(ED, (x_ctr - 1, y, minZ), (x_ctr + 1, y, maxZ), Block("polished_andesite"))
    geo.placeCuboid(ED, (x_ctr + 2, y, minZ), (x_ctr + 2, y, maxZ), Block("end_stone_bricks"))
    geo.placeCuboid(ED, (x_ctr - 2, y + 1, minZ), (x_ctr + 2, y + 3, maxZ), Block("air"))
    # north road
    geo.placeCuboid(ED, (minX, y, z_ctr - 2), (maxX, y, z_ctr - 2), Block("end_stone_bricks"))
    geo.placeCuboid(ED, (minX, y, z_ctr - 1), (maxX, y, z_ctr + 1), Block("polished_andesite"))
    geo.placeCuboid(ED, (minX, y, z_ctr + 2), (maxX, y, z_ctr + 2), Block("end_stone_bricks"))
    geo.placeCuboid(ED, (minX, y + 1, z_ctr - 2), (maxX, y + 3, z_ctr + 2), Block("air"))


def build_base():
    x_ctr = minX + (maxX - minX) // 2  # Getting center
    z_ctr = minZ + (maxZ - minZ) // 2
    y = buildHeight

    print("Building base for house to sit...")
    # Building a platform at the build height
    geo.placeCuboid(ED, (x_ctr - 14, y, z_ctr - 19), (x_ctr + 14, y, z_ctr + 19), Block("end_stone_bricks"))
    geo.placeCuboid(ED, (x_ctr - 13, y, z_ctr - 18), (x_ctr + 13, y, z_ctr + 18), Block("grass_block"))

    build_house(x_ctr - 5, z_ctr - 10)


def build_house(x, z):
    y = buildHeight

    print(f"Clearing the area and Building House at {x}, {z}...may take some time")
    geo.placeCylinder(ED, (x + 5, y + 1, z + 10), 33, 3, Block("air"))

    # Fence
    print("Building fence around and garden....")
    for i in range(-5, 16):
        ED.placeBlock((x + i, y + 1, z - 5), Block("spruce_fence"))
        ED.placeBlock((x + i, y + 1, z + 25), Block("spruce_fence"))
        if -4 <= i <= 14:
            ED.placeBlock((x + i, y + 1, z - 4), Block("tall_grass"))
            ED.placeBlock((x + i, y + 1, z + 24), Block("tall_grass"))
        if -3 <= i <= 13:
            ED.placeBlock((x + i, y + 1, z - 3), Block(chosen_flower1))
            ED.placeBlock((x + i, y + 1, z + 23), Block(chosen_flower1))
        if -2 <= i <= 12:
            ED.placeBlock((x + i, y + 1, z - 2), Block(chosen_flower2))
            ED.placeBlock((x + i, y + 1, z + 22), Block(chosen_flower2))

    for j in range(-5, 26):
        ED.placeBlock((x - 5, y + 1, z + j), Block("spruce_fence"))
        ED.placeBlock((x + 15, y + 1, z + j), Block("spruce_fence"))
        if -4 <= j <= 24:
            ED.placeBlock((x - 4, y + 1, z + j), Block("tall_grass"))
            ED.placeBlock((x + 14, y + 1, z + j), Block("tall_grass"))
        if -3 <= j <= 23:
            ED.placeBlock((x - 3, y + 1, z + j), Block("red_tulip"))
            ED.placeBlock((x + 13, y + 1, z + j), Block("red_tulip"))
        if -2 <= j <= 22:
            ED.placeBlock((x - 2, y + 1, z + j), Block("orange_tulip"))
            ED.placeBlock((x + 12, y + 1, z + j), Block("orange_tulip"))

    ED.placeBlock((x - 5, y + 1, z + 10), Block("spruce_fence_gate"))
    print("clearing the area inside fence....")
    geo.placeCylinder(ED, (x + 5, y + 4, z + 10), 33, 10, Block("air"))

    # Building
    print("Constructing Dutch house...")
    geo.placeCuboidHollow(ED, (x, y, z), (x + 10, y + 11, z + 20), Block(chosen_block))
    geo.placeCuboid(ED, (x, y, z), (x + 10, y, z + 20), Block(chosen_slab))  # Floor

    # Levels
    for i in range(1, 15):
        if i in [5]:
            geo.placeCuboid(ED, (x, y + i, z), (x + 10, y + i, z + 20), Block(chosen_block))
        if i in [6, 12]:
            geo.placeCuboid(ED, (x - 1, y + i, z - 1), (x + 11, y + i, z + 21), Block(chosen_slab))
            # geo.placeCuboid(ED, (x + 1, y + i, z + 1), (x + 9, y + i, z + 19), Block("emerald_block"))


    # Partition
    for i in range(11):
        for j in range(12):
            geo.placeCuboid(ED, (x + i, y + j, z + 9), (x + i, y + j, z + 11), Block(chosen_block))
            if i in [4, 6]:
                geo.placeCuboid(ED, (x + i, y + 0, z + 8), (x + i, y + 11, z + 12), Block(chosen_block))


    # Stairs
    direction = (1, 0)
    for i in range(6):  # 20 steps
        for j in range(11):
            geo.placeCuboid(ED, (x + i, y + j, z + 10), (x + i, y + j, z + 10), Block("air"))
        x_i = x + i * direction[0]
        z_i = z + 10 + i * direction[1]
        y_i = y + i  # Each step is 1 block higher
        ED.placeBlock((x_i, y_i, z_i), Block("brick_stairs", {"facing": "east"}))
    geo.placeCuboid(ED, (x + 5, y + 7, z + 8), (x + 5, y + 8, z + 12), Block("air"))
    ED.placeBlock((x + 5, y + 6, z + 9), Block("brick_stairs", {"facing": "north"}))
    ED.placeBlock((x + 5, y + 6, z + 11), Block("brick_stairs", {"facing": "south"}))

    # Doors
    ED.placeBlock((x, y + 1, z + 8), Block(chosen_door, {"facing": "west", "open": "true"}))
    ED.placeBlock((x, y + 1, z + 12), Block(chosen_door, {"facing": "west", "open": "true"}))
    ED.placeBlock((x + 5, y + 7, z + 8), Block(chosen_door, {"facing": "north", "open": "true"}))
    ED.placeBlock((x + 5, y + 7, z + 12), Block(chosen_door, {"facing": "south", "open": "true"}))

    # Glass
    # Front windows
    w = [1, 2]
    window = random.choice(w)
    print(f"choice of placing window {window}")
    geo.placeCuboid(ED, (x, y + 7, z + 10), (x, y + 10, z + 10), Block(chosen_window))
    for i in range(17):
        for j in range(20):
            if i in [2, 8]:
                if j in [5, 18]:
                    geo.placeCuboid(ED, (x, y + i, z + j), (x, y + i + 1, z + j), Block(chosen_window))
                if j in [2, 15]:
                    geo.placeCuboid(ED, (x, y + i, z + j), (x, y + i + 1, z + j + window), Block(chosen_window))

            if i in [8]:
                if j in [7, 13]:
                    geo.placeCuboid(ED, (x, y + i, z + j), (x, y + i + 1, z + j), Block(chosen_window))
            # Side Windows
            if i in [3, 5, 7]:
                if j in [2, 8]:
                    geo.placeCuboid(ED, (x + i, y + j, z), (x + i, y + j + 1, z), Block(chosen_window))
                    geo.placeCuboid(ED, (x + i, y + j, z + 20), (x + i, y + j + 1, z + 20), Block(chosen_window))
            # Interior
            # carpet
            if i in [1, 7]:
                if j in [2, 13]:
                    geo.placeCuboid(ED, (x + 2, y + i, z + j), (x + 8, y + i, z + j + 5), Block(chosen_carpet))
                # Bed
                if j in [4, 15]:
                    compass = ["east", "west", "north", "south"]
                    facing = random.choice(compass)
                    if facing in ["east", "west"]:
                        ED.placeBlock((x + 4, y + i, z + j), Block(chosen_bed, {"facing": facing}))
                        ED.placeBlock((x + 4, y + i, z + j + 1), Block(chosen_bed, {"facing": facing}))
                    if facing in ["north", "south"]:
                        ED.placeBlock((x + 4, y + i, z + j + 1), Block(chosen_bed, {"facing": facing}))
                        ED.placeBlock((x + 5, y + i, z + j + 1), Block(chosen_bed, {"facing": facing}))
                    print(f"Bed facing {facing}")

        # Bookshelf
        pos = [1, 3, 5, 7]
        x_pos = random.choice(pos)
        if i in [1, 7]:
            if x_pos == 1:
                ED.placeBlock((x + x_pos, y + i, z + 6), Block("bookshelf"))
                ED.placeBlock((x + x_pos, y + i, z + 14), Block("bookshelf"))
            else:
                ED.placeBlock((x + x_pos, y + i, z + 1), Block("bookshelf"))
                ED.placeBlock((x + x_pos, y + i, z + 19), Block("bookshelf"))

        # Beacon
        if i in [4, 10]:
            ED.placeBlock((x + 5, y + i, z + 16), Block("beacon"))
            ED.placeBlock((x + 5, y + i, z + 5), Block("beacon"))
    # stairs lamp
    ED.placeBlock((x + 3, y + 10, z + 10), Block("beacon"))


def main():
    try:

        build_road()
        build_base()

        print("Done!")

    except KeyboardInterrupt: # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")

if __name__ == '__main__':
    main()