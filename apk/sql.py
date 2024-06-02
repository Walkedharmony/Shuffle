# create_database.py
import sqlite3
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop table if exists to ensure a fresh start
    cursor.execute('DROP TABLE IF EXISTS participants')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY,
            image_name TEXT NOT NULL,
            full_name TEXT NOT NULL,
            nickname TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            city_origin TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    logging.debug("Table 'participants' created.")
    
    participants = [
        ('d4-1.jpg', 'Muhammad Ihsan P', 'Ihsan', 'Surabaya, 28-08-2004', 'Surabaya', '081933195345'),
        ('d4-2.jpg', 'Davina Amani Fatihah', 'Davina', 'Jombang, 15-12-2004', 'Jombang', '085231130855'),
        ('d4-3.jpg', 'Ahmad Raafi Fauzi', 'Raafi', 'Surabaya, 24-05-2005', 'Surabaya', '085733075509'),
        ('d4-4.jpg', 'Ary Pratama Paluga', 'Ary', 'Batam, 24-05-2004', 'Batam', '082122087269'),
        ('d4-5.jpg', 'Dimas Bayu Dwi Saputra', 'Bayu', 'Bojonegoro, 19-05-2004', 'Bojonegoro', '085850630532'),
        ('d4-6.jpg', 'Edwardana Frans Try Paska Hutajulu', 'Edward', 'Tanjung Balai Karimun, 14-04-2005', 'Tanjung Balai Karimun', '087744476850'),
        ('d4-7.jpg', 'Eferil Aditya Sugiharto Putro', 'Eferil', 'Sragen, 05-04-2004', 'Sragen', '082245698632'),
        ('d4-8.jpg', 'Muhammad Zidan Arifian', 'Zidan', 'Surabaya, 04-01-2005', 'Sidoarjo', '083892552767'),
        ('d4-9.jpg', 'Alvian Dwi Prasetya', 'Alvian', 'Sidoarjo, 25-04-2004', 'Sidoarjo', '081358222820'),
        ('d4-10.jpg', 'Ananda Ismul Azam', 'Danda', 'Gresik, 27-10-2003', 'Gresik', '0859175761551'),
        ('d4-11.jpg', 'Bintang Elang Pamungkas', 'Elang', 'Trenggalek, 27-12-2004', 'Trenggalek', '082143396908'),
        ('d4-12.jpg', 'Edwardo Pratenta Ginting', 'Edo', 'Gresik, 07-07-2005', 'Gresik', '085856911303'),
        ('d4-13.jpg', 'Fahmi Yahya Saputra', 'Fahmi', 'Surabaya, 25-05-2004', 'Surabaya', '081252646149'),
        ('d4-14.jpg', 'Fahrur Rozi', 'Rozi', 'Probolinggo, 23-04-2005', 'Probolinggo', '081390940809'),
        ('d4-15.jpg', 'Fikri Adrian Putra', 'Fikri', 'Lamongan, 25-01-2004', 'Lamongan', '082337652602'),
        ('d4-16.jpg', 'Moch. Rian Ardiansyah', 'Rian', 'Surabaya, 26-05-2003', 'Surabaya', '085731276763'),
        ('d4-17.jpg', 'Moh. Sufyan Tegar Pratama', 'Tegar', 'Jombang, 08-05-2005', 'Jombang', '082339758220'),
        ('d4-18.jpg', 'Mohammad Dimas Ardiansyah', 'Dimas', 'Lamongan, 25-04-2005', 'Gresik', '082332137432'),
        ('d4-19.jpg', 'Muhammad \'Athaya Akhdan', 'Ata', 'Jombang, 25-04-2005', 'Sidoarjo', '088996604986'),
        ('d4-20.jpg', 'Gerard Christofel Abimanyu Bramantyo', 'Gerard', 'Surabaya, 12-01-2006', 'Surabaya', '087701723218'),
        ('d4-21.jpg', 'Nanda Rachmad Hidayahtullah', 'Nanda', 'Tuban, 03-09-2004', 'Tuban', '087834104321'),
        ('d4-22.jpg', 'Muhammad Toriq Aghil', 'Toriq', 'Tulungagung, 20-04-2004', 'Tulungagung', '085806974814'),
        ('d4-23.jpg', 'Mario Saputra', 'Mario', 'Sumenep, 12-04-2006', 'Sumenep', '082333096437'),
        ('d4-24.jpg', 'Maulana Latif', 'Latif', 'Probolinggo, 06-05-2004', 'Probolinggo', '083132526468'),
        ('d4-25.jpg', 'Alfareza Dicky Saputra', 'Dicky', 'Ponorogo, 04-06-2004', 'Ponorogo', '083135592717'),
    ]
    
    cursor.executemany('''
        INSERT INTO participants (image_name, full_name, nickname, birth_date, city_origin, phone)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', participants)
    logging.debug("Participants data inserted into 'participants' table.")
    
    conn.commit()
    conn.close()
    logging.debug("Database created and populated with data.")

def check_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM participants')
    rows = cursor.fetchall()
    conn.close()
    logging.debug(f"Database contents: {rows}")

# Contoh penggunaan:
create_database('participants.db')
check_database('participants.db')
