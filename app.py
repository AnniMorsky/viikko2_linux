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
    
    return f"<h1>Sivustolla käyty: {hits} kertaa</h1>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
