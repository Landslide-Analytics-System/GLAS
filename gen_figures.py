from core.figures.srtm_map import MapGenerator
from core.figures.global_srtm_map import GlobalMapGenerator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--world", action="store_true")
parser.add_argument("--local", type=str)
args = parser.parse_args()

print(args)
assert args.world != args.local, "Pick one of --world or --local but not both"

if args.world:
    global_gen = GlobalMapGenerator()
    global_gen.GenerateGlobalMaps(stride=50)
    global_gen.ShowSaveElevation("figures/GlobalElevationMap")
    global_gen.ShowSaveSlope("figures/GlobalElevationMap")
elif args.local:
    local_gen = MapGenerator()
    local_gen.loadData(args.local)
    # options are ['slope_riserun', 'slope_percentage', 'slope_degrees', 'slope_radians']
    local_gen.calcSlope("slope_riserun")
    local_gen.showElevationMap()
    local_gen.showSlopeMap()

# unless you have insane amounts of memory you should probably pick a stride >= 10
# local_gen.GenerateGlobalElevationMap(stride=100)