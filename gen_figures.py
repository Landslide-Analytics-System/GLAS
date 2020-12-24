# from core.figures.srtm_map import MapGenerator

# gen = MapGenerator()
# gen.loadData("N41W123.hgt")
# # options are ['slope_riserun', 'slope_percentage', 'slope_degrees', 'slope_radians']
# gen.calcSlope("slope_riserun")
# gen.showElevationMap()
# gen.showSlopeMap()

# todo: add argparse so we can do --global-elevation and --global-slope and --local N34E088.hgt and stuff


from core.figures.global_srtm_map import GlobalMapGenerator

gen = GlobalMapGenerator()
# unless you have insane amounts of memory you should probably pick a stride >= 10
gen.GenerateGlobalElevationMap(stride=100)