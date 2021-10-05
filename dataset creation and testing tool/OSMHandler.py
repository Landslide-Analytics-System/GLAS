import osmium as osm
import pandas as pd


class OSMHandler(osm.SimpleHandler):
    def __init__(self, tags):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []
        self.tags = tags

    def tag_inventory(self, elem, elem_type):
        for tag in elem.tags:
            self.osm_data.append([elem_type,
                                  elem.id,
                                  elem.version,
                                  elem.visible,
                                  pd.Timestamp(elem.timestamp),
                                  elem.uid,
                                  elem.user,
                                  elem.changeset,
                                  len(elem.tags),
                                  tag.k,
                                  tag.v])

    def node(self, n):
        self.tag_inventory(n, "node")

    def way(self, w):
        self.tag_inventory(w, "way")

    def relation(self, r):
        self.tag_inventory(r, "relation")

    def count(self):
        data_colnames = ['type', 'id', 'version', 'visible', 'ts', 'uid',
                         'user', 'chgset', 'ntags', 'tagkey', 'tagvalue']
        df = pd.DataFrame(self.osm_data, columns=data_colnames)
        count = 0
        for idx, i in enumerate(df.tagkey.unique()):
            for tag in self.tags:
                if tag in i:
                    count += int(df.tagkey.value_counts()[idx])
                    break
        return count

    def getTags(self):
        data_colnames = ['type', 'id', 'version', 'visible', 'ts', 'uid',
                         'user', 'chgset', 'ntags', 'tagkey', 'tagvalue']
        df = pd.DataFrame(self.osm_data, columns=data_colnames)
        tags = {}
        for idx, i in enumerate(df.tagkey.unique()):
            found = False
            for tag in self.tags:
                if tag in i:
                    found = True
                    break
            if found:
                tags[i] = df.tagkey.value_counts()[idx]
        return tags
