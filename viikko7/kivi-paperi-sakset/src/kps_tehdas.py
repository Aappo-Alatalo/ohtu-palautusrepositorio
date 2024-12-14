from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from tuomari import Tuomari
from tekoaly_parannettu import TekoalyParannettu
from tekoaly import Tekoaly


class KPS_Tehdas:
    @staticmethod
    def luo_peli(pelityyppi):
        dumari = Tuomari()
        if pelityyppi == "a":
            return KPSPelaajaVsPelaaja(dumari)
        elif pelityyppi == "b":
            tyhma_tekoaly = Tekoaly()
            return KPSTekoaly(dumari, tyhma_tekoaly)
        elif pelityyppi == "c":
            fiksu_tekoaly = TekoalyParannettu(10)
            return KPSTekoaly(dumari, fiksu_tekoaly)
        else:
            return None