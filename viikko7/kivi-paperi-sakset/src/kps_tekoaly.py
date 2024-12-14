from kps_parempi_tekoaly import KPSParempiTekoaly
from tekoaly import Tekoaly


class KPSTekoaly(KPSParempiTekoaly):
    def __init__(self):
        self._tekoaly = Tekoaly() # Asetetaan huonompi tekoäly
