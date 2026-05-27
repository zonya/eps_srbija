# EPS Srbija (Nezvanična integracija)

Ova Home Assistant integracija omogućava povezivanje sa vašim nalogom na portalu "EPS Uvid u račun".

## 🚀 Mogućnosti
- Praćenje trenutnog stanja duga.
- Detaljan uvid u mesečnu potrošnju (kWh) po zonama (zelena, plava, crvena).
- Finansijski pregled mesečnih zaduženja (RSD).
- Prikaz sistemskih obaveštenja i aktivnih opomena.
- Automatsko ažuriranje podataka.

## 📥 Instalacija
1. Otvorite **HACS** u vašem Home Assistant-u.
2. Kliknite na tri tačkice u gornjem desnom uglu -> **Custom repositories**.
3. Unesite URL ovog repozitorijuma: `https://github.com/zonya/eps_srbija`
4. Izaberite kategoriju **Integration**.
5. Kliknite **Add** i nakon toga instalirajte integraciju.
6. Restartujte Home Assistant.
7. Idite u **Settings -> Devices & Services -> Add Integration** i pronađite **EPS Srbija**.

## 📊 Dashboard kartica
Za prikaz podataka na dashboard-u, koristite [ApexCharts Card](https://github.com/RomRider/apexcharts-card).

Preuzmite YAML kod za karticu iz priloženog fajla `dashboard_card.yaml` i zalepite ga u **Manual Card** na vašem dashboard-u.

## ⚠️ Napomena
Ovo je nezvanična integracija. Autor nije povezan sa Javnim preduzećem "Elektroprivreda Srbije". Korišćenje integracije je na sopstvenu odgovornost.
