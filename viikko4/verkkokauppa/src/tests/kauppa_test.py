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

    def test_aloita_asiointi_nollaa_edellisen_ostoksen(self):
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


        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)  # Lisätään tuote, ID = 1
        kauppa.tilimaksu("Matti", "12345")  # Suoritetaan maksu

        self.pankki_mock.tilisiirto.assert_called_with("Matti", ANY, "12345", ANY, 5)  # Ekan ostoksen summa on 5

        # Aloitetaan uusi asiointi ja varmistetaan, että tiedot on nollattu
        kauppa.aloita_asiointi()
        kauppa.tilimaksu("Matti", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("Matti", ANY, "12345", ANY, 0)  # Uuden ostoksen summa on 0

    def test_pyydetaan_uusi_viite_jokaiseen_maksuun(self):
        self.viitegeneraattori_mock.uusi.side_effect = [2, 3, 4]

        # Määritellään varaston saldo-metodin toiminta
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 7
            if tuote_id == 3:
                return 9

        # Määritellään varaston hae_tuote-metodin toiminta
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            if tuote_id == 3:
                return Tuote(3, "olut", 2)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("tupu", "1111")

        self.pankki_mock.tilisiirto.assert_called_with(ANY, 2, "1111", ANY, ANY)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("hupu", "1234")

        self.pankki_mock.tilisiirto.assert_called_with(ANY, 3, "1234", ANY, ANY)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(3)
        kauppa.tilimaksu("lupu", "4444")

        self.pankki_mock.tilisiirto.assert_called_with(ANY, 4, "4444", ANY, ANY)

        # Tarkistetaan, että viitegeneraattorin metodia uusi on kutsuttu kolme kertaa
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)

    def test_poista_korista_poistaa_tuotteen_korista_ja_palauttaa_varastoon(self):
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

        # Suoritetaan testattava toiminto
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.poista_korista(2)

        # Varmistetaan, että hae_tuote kutsuttiin oikealla ID:llä
        self.varasto_mock.hae_tuote.assert_called_with(2)

        # Tallennetaan haettu tuote tarkistusta varten
        palautettava_tuote = self.varasto_mock.hae_tuote(2)

        # Varmistetaan, että varasto.palauta_varastoon kutsuttiin oikealla tuotteella
        self.varasto_mock.palauta_varastoon.assert_called_with(palautettava_tuote)
