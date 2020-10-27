import os
import difflib as dl
import pandas as pd
from upload_db import upload_fab_sites, get_api_by_cis


class FabricationSites:
    def __init__(self):
        self.df = upload_fab_sites()
        self.api_by_cis = get_api_by_cis()


    def match_cis(self):
        self.df['substance_active_match'] = self.df.substance_active.apply(
            lambda x: dl.get_close_matches(x.substance_active, self.api_by_cis[x.cis])[0],
            axis=1
        )