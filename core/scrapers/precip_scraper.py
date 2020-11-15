import os
from core.utils.flags import FLAGS

class PreciptationScraper:
    def __init__(self):
        self.data = None

    def collect(self):
        self.data = [i for i in range(10)]
        with open(os.path.join(FLAGS.precip_data_save_loc, 'data.txt'), 'w') as f:
            f.write(str(self.data) + '\n')