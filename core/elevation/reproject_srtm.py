from osgeo import gdal
import subprocess
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# Reprojecting SRTM data from WGS84 to EPSG:3395 (Mercator)
# gdal_translate <filename>.hgt <filename>.tif
# gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3395 -r bilinear <in>.tif <out>.tif

class SRTMReprojector():
    def __init__(self):
        self.logfile = open("reproject_log.txt", "w+")
        
    def ReprojectFile(self, src_filepath, dest_filepath):
        filename = dest_filepath.split("/")[-1]
        translate_command = "gdal_translate {0} interm.tif".format(src_filepath)
        reproject_command = "gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3395 -r bilinear interm.tif {0}".format(dest_filepath)
       
        # logging
        subprocess.call("echo \"\"", shell=True, stdout=self.logfile)
        subprocess.call("echo " + "-"*10 + "reprojecting " + filename + "-"*10 + "\n\n\n", shell=True, stdout=self.logfile)
        subprocess.call("echo \"\"", shell=True, stdout=self.logfile)
        
        #reprojecting
        subprocess.call(translate_command, shell=True, stdout=self.logfile)
        subprocess.call(reproject_command,  shell=True, stdout=self.logfile)
        subprocess.call("rm interm.tif", shell=True, stdout=self.logfile)
    
    def ShowFileAsImage(self, filepath):
        ds = gdal.Open(filepath)
        data = ds.GetRasterBand(1).ReadAsArray()
        # todo: Implement cutoff of top/bottom n%
        plt.imshow(data)
        plt.colorbar()
        plt.show()
    
    def ReprojectAllFiles(self, data_dir):
        filenames = os.listdir(data_dir)
        #iterate over all filenames
        for filename in tqdm(filenames):
            tif_filename = filename[:-4] + ".tif"
            if filename[-4:] == ".hgt":
                self.ReprojectFile(os.path.join(data_dir, filename), os.path.join(data_dir, "mercator", tif_filename))