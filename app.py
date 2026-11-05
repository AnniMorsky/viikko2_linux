from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="Porkkanakakku1",
        database="exampledb"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS counter (id INT AUTO_INCREMENT PRIMARY KEY, hits INT)")
    cursor.execute("SELECT hits FROM counter WHERE id = 1")
    row = cursor.fetchone()
    
    if row is None:
        cursor.execute("INSERT INTO counter (hits) VALUES (1)")
        hits = 1
    else:
        hits = row[0] + 1
        cursor.execute("UPDATE counter SET hits = %s WHERE id = 1", (hits,))

    conn.commit()
    cursor.close()
    conn.close()
    
    return f"""
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <title>LEMP App - Viikko 2</title>
        <style>
            body {{ font-family: Comic Sans MS, sans-serif; margin: 40px; line-height: 1.6; background-color: #fcdd88; }}
            h1 {{ color: #d9a30f; }}
            .counter {{ font-size: 1.4em; font-weight: bold; color: #856308; margin: 20px 0; }}
            
        </style>
    </head>
    <body>
        <h1>Sivuston tila ja tiedot</h1>
        <div class="counter">Sivustolla käyty: {hits} kertaa</div>
        
        <div>
            <h3>Järjestelmän tiedot:</h3>
            <ul>
                <li>Käytettiin MySQL-tietokantaa </li>
                <li>Laskurin arvo tallennetaan MySQL-tietokannan counter-tauluun riville <code>id = 1</code>. Jokaisella sivulatauksella arvoa kasvatetaan SQL UPDATE -komennolla, joten tila säilyy pysyvästi.</li>
                <li>Testin tulos: Gunicorn-palvelu ja MySQL-tietokanta on määritetty käynnistymään automaattisesti järjestelmän mukana. Palvelimen uudelleenkäynnistyksen jälkeen laskurin lukema säilyi tietokannassa ja sovellus jatkoi toimintaansa ilman katkoksia.</li>
            </ul>
        </div>
        <a
            href='https://github.com/AnniMorsky/viikko2_linux'
            target='_blank'
            rel='noreferrer noopener nofollow'
        >
            Github-repository
        </a>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
