from core.susceptibility.susceptibility_map import SusceptibilityMap
res = 25 # one degree by one degree square ends up with this many pixels per side
lat_options = 116 # 56 S --> 59 N
lon_options = 360 # 0 --> 179 E & W

susmap = SusceptibilityMap(res=res)
# susmap.CalcSlopeData("data/elevation/mercator/slope")
susmap.LoadSlopeMap("data/saves/2900x9000-slope-map.npy")
susmap.SaveSlopeData(f'data/saves/{res*lat_options}x{res*lon_options}-slope-map.npy')
susmap.SaveSlopeMap(1, f'data/saves/{res*lat_options}x{res*lon_options}-slope-map.png')
susmap.ShowSlopeMap(2)

# susmap.CalcForestData("data/forest")
susmap.LoadForestMap("data/saves/2900x9000-forest-map.npy")
susmap.SaveForestData(f'data/saves/{res*lat_options}x{res*lon_options}-forest-map.npy')
susmap.SaveForestMap(f'data/saves/{res*lat_options}x{res*lon_options}-forest-map.png')
susmap.ShowForestMap()

# susmap.CalcOSMData("data/osm")
# susmap.SaveOSMMap(f'data/forest/{res*lat_options[0]}x{res*lon_options[1]}-osm-map.npy')
# susmap.ShowOSMMap()

susmap.BuildSusmap(2)
susmap.SaveSusmapData(f'data/saves/{res*lat_options}x{res*lon_options}-susceptibility-map.npy')
susmap.SaveSusmap(1, f'data/saves/{res*lat_options}x{res*lon_options}-susceptibility-map.png')
susmap.ShowSusmap(1)