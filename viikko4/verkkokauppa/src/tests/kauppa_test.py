import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self):
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_kaksi_eri_tuotetta_ostos(self):
        # Määritellään viitegeneraattorin palauttama arvo
        self.viitegeneraattori_mock.uusi.return_value = 42

        # Määritellään varaston saldo-metodin toiminta
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 5

        # Määritellään varaston hae_tuote-metodin toiminta
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # Alustetaan kauppa käyttäen setUp-metodista tulevia mockeja
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # Asioinnin kulku
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)  # Lisätään maito
        kauppa.lisaa_koriin(2)  # Lisätään leipä
        kauppa.tilimaksu("pekka", "12345")

        # Varmistetaan, että pankin metodia kutsutaan oikeilla argumenteilla
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 8)

    def test_kaksi_samaa_tuotetta_ostos(self):
        # Määritellään viitegeneraattorin palauttama arvo
        self.viitegeneraattori_mock.uusi.return_value = 42

        # Määritellään varaston saldo-metodin toiminta
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # Määritellään varaston hae_tuote-metodin toiminta
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # Alustetaan kauppa käyttäen setUp-metodista tulevia mockeja
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # Asioinnin kulku
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)  # Lisätään maito
        kauppa.lisaa_koriin(1)  # Lisätään toinen maito
        kauppa.tilimaksu("pekka", "12345")

        # Varmistetaan, että pankin metodia kutsutaan oikeilla argumenteilla
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 10)

    def test_kaksi_eri_tuotetta_toinen_loppu_ostos(self):
        # Määritellään viitegeneraattorin palauttama arvo
        self.viitegeneraattori_mock.uusi.return_value = 42

        # Määritellään varaston saldo-metodin toiminta
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0

        # Määritellään varaston hae_tuote-metodin toiminta
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # Alustetaan kauppa käyttäen setUp-metodista tulevia mockeja
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # Asioinnin kulku
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)  # Lisätään maito
        kauppa.lisaa_koriin(2)  # Lisätään leipä (LEIVÄT ON LOPPU)
        kauppa.tilimaksu("pekka", "12345")

        # Varmistetaan, että pankin metodia kutsutaan oikeilla argumenteilla
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)