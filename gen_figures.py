from core.figures.gen_map import MapGenerator

gen = MapGenerator()
gen.loadData("N41W123.hgt")
# options are ['slope_riserun', 'slope_percentage', 'slope_degrees', 'slope_radians']
gen.calcSlope("slope_riserun")
gen.showElevationMap()
gen.showSlopeMap()
