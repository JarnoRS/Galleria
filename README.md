# Galleria

Sovellus on samassa tilassa, mihin se jäi ennen edellisen toteutuksen aikana (periodi 4). Tarkoituksena jatkaa välipalautus 2:n jälkeen siitä, mihin se viime suorituskerralla jäi.

* TEHTY: 
    * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

    * Käyttäjä pystyy lisäämään sovellukseen tietokohteita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kuvia.
        -> Kuviin liittyvät tiedot (otsikko, kuvaus yms.) tehty, tekemättä itse kuvatiedostojen lisäys

    * Käyttäjä näkee sovellukseen lisätyt kuvat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kuvat.

    * Käyttäjä pystyy etsimään kuvia hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kuvia.
        -> Kuvia voi hakea hakusanalla, genrellä tai molemmilla

    * Käyttäjä pystyy valitsemaan kuvalle yhden tai useamman luokittelun (Esim. kuvan tyyli, käyttäjän lisäämä kuvaus, muiden käyttäjien antamat kommentit/arvostelut). Mahdolliset luokat ovat tietokannassa.

    * Käyttäjä pystyy antamaan kuvalle arvosanan (esim. 1-5). Kuvan saama keskiarvo esitetään kuvan yhteydessä.
        -> Toteutettu luomalla tietokantaan "grades"-taulu, johon käyttäjä voi antaa arvosanan kerran jokaiselle kuvalle. Arvosanaa voi muuttaa myöhemmin.

    * Kuviin liittyvä kommentointikenttä
        -> Toteutettu luomalla tietokantaan "comments"-taulu, josta kommentit haetaan katsottaessa kuvaa.

    * Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kuvat.
        -> Luotu suppea käyttäjäsivu.
        
* TO DO: 

    * Sovelluksessa on pääasiallisen tietokohteen lisäksi toissijainen tietokohde, joka täydentää pääasiallista tietokohdetta. Käyttäjä pystyy lisäämään toissijaisia tietokohteita omiin ja muiden käyttäjien tietokohteisiin liittyen.
        -> Nyt on tehtynä toissijainen tietokohde (SQL-tietokanta kuvaan liittyen) ja pitäisi lisätä ensisijainen tietokohde, eli kuvatiedostot.

VÄLIPALAUTUS 2 FEEDBACK:
 -Funktio get_classes muutettu käymään sanakirja läpi yhdellä iteraatiolla
 -Korjattu schema-tiedostoon puuttuvat pilkut
 -Korjattu bugi, jossa kuvan poistaminen ei poista kuvaan liittyviä kommentteja.
