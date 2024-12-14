# Tähän tiedostoon yhdistetty luokat älykkäälle ja vähemmän älykkäälle tekoälylle
from kps import KiviPaperiSakset

class KPSTekoaly(KiviPaperiSakset):
    def __init__(self, dumari, tekoaly):
        super().__init__(dumari)
        self._tekoaly = tekoaly

    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return tokan_siirto