from tqdm import tqdm
import os
import rasterio
import numpy as np
import cv2
import matplotlib.pyplot as plt

# parse in slope, forest, osm data for a single unit square and produce susceptibility map for it
# scale up and sample the resolution


class SusceptibilityMap:
    def __init__(self, res):
        self.slope_data = None
        self.forest_data = None
        self.osm_data = None
        self.susc_data = None
        self.map_res = res
        self.lat_options = 116
        self.lon_options = 360

    def CalcSlopeData(self, slope_dir):
        self.slope_dir = slope_dir
        slope_files = [i for i in os.listdir(slope_dir) if i[-4:] == ".tif"]

        print("Reading in slope data...")
        max_N = 59
        max_W = 180
        max_S = 56
        max_E = 179

        # N59 --> N00
        # S01 --> S56
        # E000 --> E179
        # W180 --> W001

        # Initialize array global elevation
        # self.slope_data = np.zeros(( self.map_res*(max_S+max_N+1), self.map_res*(max_E+max_W+1) ))
        self.slope_data = np.zeros(
            (self.map_res*self.lat_options, self.map_res*self.lon_options))

        print("Output Image Shape:", self.slope_data.shape)
        print("Output Image Size (GBs):", self.slope_data.nbytes / 1e9)

        for slope_file in tqdm(slope_files):
            # print("Parsing file " + slope_file)
            lat_letter = slope_file[0]
            lon_letter = slope_file[3]
            lat = int(slope_file[1:3])
            lon = int(slope_file[4:7])

            if lat_letter == "S":
                # Shift south down by max_N, but south starts at S01 so we translate up by 1 too
                lat_trans = max_N + lat - 1
            else:
                # Bigger N lat means further up. E.g. N59 is at index 0 and is higher than N00
                lat_trans = max_N - lat

            if lon_letter == "E":
                # Shift east right by max_W
                lon_trans = max_W + lon
            else:
                # Bigger W lon means further left. E.g. W180 is at index 0 and is more left than W001
                lon_trans = max_W - lon

            # load in data from file as resized
            with rasterio.open(os.path.join(slope_dir, slope_file)) as f:
                slope_file_data = f.read(1)

            slope_file_data = cv2.resize(
                slope_file_data, (self.map_res, self.map_res))
            # making sure any bad slope values < 0 snap to 0
            slope_file_data[slope_file_data < 0] = 0

            # generate bounds (lon/lat --> x/y for data from this file for the giant array)
            lat_bounds = [self.map_res*lat_trans, self.map_res*(lat_trans+1)]
            lon_bounds = [self.map_res*lon_trans, self.map_res*(lon_trans+1)]

            try:
                self.slope_data[lat_bounds[0]:lat_bounds[1],
                                lon_bounds[0]:lon_bounds[1]] = slope_file_data
            except:
                print("REFERENCE ERROR: " + slope_file)
                print("lat: ", lat_bounds)
                print("lon: ", lon_bounds)

    def LoadSlopeMap(self, slope_map_dir):
      self.slope_data = np.load(slope_map_dir)

    def ShowSlopeMap(self, x):
        assert 0<=x<=99, "Recheck the graph trim value. Must be between 0 and 99"
        vmin_calc, vmax_calc = np.nanpercentile(self.slope_data, [x, 100-x])
        plt.figure(figsize=(20, 8))
        plt.imshow(self.slope_data, vmin=vmin_calc, vmax=vmax_calc, cmap="magma")
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    def SaveSlopeData(self, save_dir):
        print("Saving slope data...")
        np.save(save_dir, self.slope_data)
    
    def SaveSlopeMap(self, x, save_dir):
        print("Saving slope map...")
        assert 0<=x<=99, "Recheck the graph trim value. Must be between 0 and 99"
        vmin_calc, vmax_calc = np.nanpercentile(self.slope_data, [x, 100-x])
        plt.figure(figsize=(20, 8))
        plt.imshow(self.slope_data, vmin=vmin_calc, vmax=vmax_calc, cmap="magma")
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(save_dir, dpi=300)

    def CalcForestData(self, forest_dir):
      self.forest_data = np.zeros((self.map_res*self.lat_options, self.map_res*self.lon_options))

      print("Reading Forest Data...")
      print("Output Image Shape:", self.forest_data.shape)
      print("Output Image Size (GBs):", self.forest_data.nbytes / 1e9)

      for forest_file in tqdm(os.listdir(forest_dir)):
        # these files are 10 degree x 10 degree so our forest_res = 10xres
        forest_res = 10*self.map_res
        forest_file_data = cv2.resize(rasterio.open(os.path.join(forest_dir, forest_file)).read(1), (forest_res, forest_res))
        forest_file_data[forest_file_data < 0] = 0

        lat_letter = forest_file[-10]
        lon_letter = forest_file[-5]
        lat = int(forest_file[-12:-10])
        lon = int(forest_file[-8:-5])
        # print(lat_letter, lat, lon_letter, lon)

        max_N = 60
        max_W = 180

        if lat_letter == "N":
          lat_trans = max_N - lat
        else:
          lat_trans = max_N + lat - 10
          
        if lon_letter == "E":
          lon_trans = max_W + lon
        else:
          lon_trans = max_W - lon

        # we still use self.map_res for graphing becuase lat_trans+10 cancels the effect of the 10x magnitude
        lat_bounds = [self.map_res*lat_trans, self.map_res*(lat_trans+10)]
        lon_bounds = [self.map_res*lon_trans, self.map_res*(lon_trans+10)]
        # print(lat_bounds, lon_bounds)
        # print("data shape: ", forest_file_data.shape)
        try:
          self.forest_data[lat_bounds[0]:lat_bounds[1], lon_bounds[0]:lon_bounds[1]] = forest_file_data
        except:
          print("REFERENCE ERROR: " + forest_file)
          print("lat: ", lat_bounds)
          print("lon: ", lon_bounds)
    
    def LoadForestMap(self, forest_map_dir):
      self.forest_data = np.load(forest_map_dir)

    def ShowForestMap(self):
        plt.figure(figsize=(20, 8))
        plt.imshow(self.forest_data, cmap="magma")
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    def SaveForestData(self, save_dir):
      print("Saving forest data...")
      np.save(save_dir, self.forest_data)
    
    def SaveForestMap(self, save_dir):
      print("Saving forest map...")
      plt.figure(figsize=(20, 8))
      plt.imshow(self.slope_data, cmap="magma")
      plt.colorbar()
      plt.tight_layout()
      plt.savefig(save_dir, dpi=300)
    
    def BuildSusmap(self, slope_x):
      # cap top and bottom x% of data, normalize, and add argument wise
      # 1) calc percentile vals
      slopemin, slopemax = np.nanpercentile(self.slope_data, [slope_x, 100-slope_x])
      # cap the vals
      self.slope_data[self.slope_data < slopemin] = slopemin
      self.slope_data[self.slope_data > slopemax] = slopemax
      # normalize vals
      self.slope_data /= self.slope_data.max()
      self.forest_data /= self.forest_data.max()

      self.susc_data = 0.171*self.slope_data + 0.151*self.forest_data
      self.susc_data /= self.susc_data.max()
    
    def SaveSusmapData(self, save_dir):
      print("Saving susceptibility data")
      np.save(save_dir, self.susc_data)
    
    def ShowSusmap(self, x):
      assert 0<=x<=99, "Recheck the graph trim value. Must be between 0 and 99"
      vmin_calc, vmax_calc = np.nanpercentile(self.susc_data, [x, 100-x])
      plt.figure(figsize=(20, 8))
      plt.imshow(self.susc_data, vmin=vmin_calc, vmax=vmax_calc, cmap="magma")
      plt.colorbar()
      plt.tight_layout()
      plt.show()
    
    def SaveSusmap(self, x, save_dir):
      print("Saving Susceptibility map...")
      assert 0<=x<=99, "Recheck the graph trim value. Must be between 0 and 99"
      vmin_calc, vmax_calc = np.nanpercentile(self.susc_data, [x, 100-x])
      plt.figure(figsize=(20, 8))
      plt.imshow(self.susc_data, vmin=vmin_calc, vmax=vmax_calc, cmap="magma")
      plt.colorbar()
      plt.tight_layout()
      plt.savefig(save_dir, dpi=300)

    # see other file for osm code cuz it's nasty and unorganized and won't fit into these nice little methods



# look into this to see how to cap top and bottom x% vals in np array - from richdem
"""
def rdShow(rda, ignore_colours=[], show=True, axes=True, cmap='gray', vmin=None, vmax=None, xmin=None, xmax=None, ymin=None, ymax=None, zxmin=None, zxmax=None, zymin=None, zymax=None, figsize=(4,4), zcolor='red', zloc=1):
  if type(rda) is np.ndarray:
    rda = rdarray(rda)
  elif type(rda) is not rdarray:
    raise Exception("A richdem.rdarray or numpy.ndarray is required!")

  try:
    import matplotlib.pyplot as plt
    import matplotlib
  except:
    raise Exception("matplotlib must be installed to use rdShow!")

  zoom_vars = [zxmin, zxmax, zymin, zymax]
  some_zoom = any(x is not None for x in zoom_vars)
  all_zoom  = all(x is not None for x in zoom_vars)

  if some_zoom and not all_zoom:
    raise Exception("All zoom limits must be set for zooming to work!")
  elif all_zoom:
    try:
      #from mpl_toolkits.axes_grid1.inset_locator import mark_inset
      from mpl_toolkits.axes_grid1.inset_locator import inset_axes
      from matplotlib.patches import Rectangle
    except:
      raise Exception("mpl_toolkits.axes_grid1 must be available!")

  disparr = np.array(rda, copy=True)
  disparr[disparr==rda.no_data] = np.nan
  for c in ignore_colours:
    disparr[disparr==c] = np.nan
  vmin_calc, vmax_calc = np.nanpercentile(disparr, [2, 98])
  if vmin is None:
    vmin = vmin_calc
  if vmax is None:
    vmax = vmax_calc

  fig, (ax, cax) = plt.subplots(ncols=2,figsize=figsize, gridspec_kw={"width_ratios":[1, 0.05]})

  #current_cmap = matplotlib.cm.get_cmap()
  #current_cmap.set_bad(color='red')
  iax = ax.imshow(disparr, vmin=vmin, vmax=vmax, cmap=cmap)
  ax.set_xlim(xmin=xmin, xmax=xmax)
  ax.set_ylim(ymin=ymin, ymax=ymax)

  if all_zoom:
    axins = inset_axes(ax, width=2, height=2, loc=zloc, borderpad=0) #, bbox_to_anchor=(0.9, -0.05, 1, 1), bbox_transform=ax.transAxes, borderpad=0)
    axins.set_xlim(xmin=zxmin,xmax=zxmax) 
    axins.set_ylim(ymin=zymin,ymax=zymax)
    plt.setp(axins.get_xticklabels(), visible=False)
    plt.setp(axins.get_yticklabels(), visible=False)
    plt.setp(axins.get_xticklines(),  visible=False)
    plt.setp(axins.get_yticklines(),  visible=False)
    #mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec='r', lw=2, ls=None) #ec='1.0' = top of colormap
    ax.add_patch(Rectangle((zxmin, zymin), zxmax-zxmin, zymax-zymin, facecolor='none', edgecolor=zcolor, lw=2))#, transform=fig.transFigure, facecolor='none'))
    plt.setp(tuple(axins.spines.values()), color=zcolor, lw=2)
    axins.imshow(disparr, vmin=vmin, vmax=vmax, cmap=cmap)


  fig.colorbar(iax, cax=cax)

  plt.tight_layout()

  if not axes:
    ax.axis('off')
  if show:
    plt.show()
  return {"vmin": vmin, "vmax": vmax}

"""
