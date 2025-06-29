# Galleria

Gallerian perusajatuksena on jakaa kuvia muiden käyttäjien kanssa.

Sovelluksen toiminnallisuuksia:
 * Sovellukseen voi luoda käyttäjän (Käyttäjän voi halutessaan myös poistaa)
 * Kuvahaku joko hakusanan tai kuvan luokittelun perusteella
 * Erilliset kuvasivut, joissa näkyy kuvan lisäksi siihen liittyvää tietoa (kuvaus, lisäysajankohta, kommentit yms.)
 * Erilliset käyttäjäsivut, joista näkee käyttäjän tietoja (kuvat, kommentit yms.)

Sovellukseen kirjautunut käyttäjä voi:
 * Lisätä ja poistaa kuviaan
 * Kommentoida omia ja muiden käyttäjien kuvia
 * Antaa arvosanan muiden käyttäjien kuville
 * Osallistua chat-keskusteluun muiden käyttäjien kanssa

Sovellusta voi käyttää myös kirjautumatta, mutta tällöin voi vain katsoa muiden lisäämiä kuvia ja muiden käyttäjien tietoja.

## KUINKA KÄYNNISTÄT SOVELLUKSEN (LINUX):
1. Kopioi sovelluksen repositorio laitteellesi ja mene hakemiston juureen (/Galleria).
2. Aja komento "$ source venv/bin/activate" käynnistääksesi Pythonin virtuaaliympäristön.
3. Asenna flask komennolla "$ pip install flask".
4. Valmistele tietokanta suorittamalla komennot "$ sqlite3 database.db < schema.sql" ja "$ sqlite3 database.db < init.sql".
5. Aja komento "$ flask run" ja voit siirtyä sovelluksen etusivulle.

## KURSSIIN LIITTYVÄÄ ASIAA:

VÄLIPALAUTUS 2 FEEDBACK:
 -Funktio get_classes muutettu käymään sanakirja läpi yhdellä iteraatiolla
 -Korjattu schema-tiedostoon puuttuvat pilkut
 -Korjattu bugi, jossa kuvan poistaminen ei poista kuvaan liittyviä kommentteja
 -Lisätty sivu, joka vahvistaa käyttäjän luomisen ja ohjaa takaisin etusivulle

 VÄLIPALAUTUS 3 FEEDBACK:
 -Estetty käyttäjän luominen ilman käyttäjänimeä tai salasanaa
 -Lisätty README:hin käynnistysohjeet
 -Siistitty koodista pois suomenkieliset muuttujien nimet
 -Paikattu CSRF-aukot
 -Lisätty flash-virheviestit
 -Poistettu turhat importit
 -Poistettu turhat else-haarat
 -Poistettu tietokantatiedosto versiohallinnasta

## PUUTTEITA / BUGEJA 
 * Sovellusta ei ole testattu suurella tietomäärällä
 * Sivutusta ei ole tehty
 * show_image.html:n yhden div:n luokka muuttuu "show_image":sta "box":ksi renderöinnin aikana