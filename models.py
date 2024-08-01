from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nim = Column(String)
    presensi = Column(Integer)
    nilai_tugas = Column(Integer)
    nilai_uts = Column(Integer)
    nilai_uas = Column(Integer)
    total_nilai = Column(Integer)
    rata_rata = Column(Integer)
    nilai_huruf = Column(String)
    status = Column(String)
