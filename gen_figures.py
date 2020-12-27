from core.figures.srtm_map import MapGenerator
from core.figures.global_srtm_map import GlobalMapGenerator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--global", action="store_true", dest="global_")
parser.add_argument("--local", type=str)
parser.add_argument("--mode", type=str)

args = parser.parse_args()

print(args)
assert args.global_ != args.local, "Pick one of --gloal or --local but not both"

# mode options are ['slope_riserun', 'slope_percentage', 'slope_degrees', 'slope_radians', 'aspect',
#                   'curvature', 'planform_curvature', 'profile_curvature']

if args.global_:
    global_gen = GlobalMapGenerator()
    global_gen.GenerateGlobalMaps(stride=50, mode=args.mode)
    global_gen.ShowSaveElevation("figures/GlobalElevationMap")
    global_gen.ShowSaveSlope("figures/GlobalSlopeMap")
elif args.local:
    local_gen = MapGenerator()
    local_gen.loadData(args.local)
    local_gen.calcSlope(args.mode)
    local_gen.showElevationMap()
    local_gen.showSlopeMap()