from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(100), nullable=False)
    presensi = db.Column(db.Float, nullable=False)
    nilai_tugas = db.Column(db.Float, nullable=False)
    nilai_uts = db.Column(db.Float, nullable=False)
    nilai_uas = db.Column(db.Float, nullable=False)
    total_nilai = db.Column(db.Float, nullable=False)
    rata_rata = db.Column(db.Float, nullable=False)
    nilai_huruf = db.Column(db.String(2), nullable=False)
    status = db.Column(db.String(20), nullable=False)

def calculate_total_and_status(presensi, nilai_tugas, nilai_uts, nilai_uas):
    total_nilai = presensi + nilai_tugas + nilai_uts + nilai_uas
    rata_rata = total_nilai / 4
    if rata_rata >= 85:
        nilai_huruf = 'A'
    elif rata_rata >= 70:
        nilai_huruf = 'B'
    elif rata_rata >= 55:
        nilai_huruf = 'C'
    elif rata_rata >= 40:
        nilai_huruf = 'D'
    else:
        nilai_huruf = 'E'
    status = 'Lulus' if rata_rata >= 55 else 'Tidak Lulus'
    return total_nilai, rata_rata, nilai_huruf, status

@app.route('/')
def index():
    products = Product.query.all()
    edit_product_id = request.args.get('edit_id')
    product_to_edit = None
    if edit_product_id:
        product_to_edit = Product.query.get(edit_product_id)
    return render_template('rekap-data.html', products=products, product=product_to_edit)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    nim = request.form['nim']
    presensi = float(request.form['presensi'])
    nilai_tugas = float(request.form['nilai_tugas'])
    nilai_uts = float(request.form['nilai_uts'])
    nilai_uas = float(request.form['nilai_uas'])
    
    total_nilai, rata_rata, nilai_huruf, status = calculate_total_and_status(presensi, nilai_tugas, nilai_uts, nilai_uas)
    
    new_product = Product(name=name, nim=nim, presensi=presensi, nilai_tugas=nilai_tugas, 
                          nilai_uts=nilai_uts, nilai_uas=nilai_uas, total_nilai=total_nilai, 
                          rata_rata=rata_rata, nilai_huruf=nilai_huruf, status=status)
    db.session.add(new_product)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST'])
def edit_product(id):
    product = Product.query.get(id)
    product.name = request.form['name']
    product.nim = request.form['nim']
    product.presensi = float(request.form['presensi'])
    product.nilai_tugas = float(request.form['nilai_tugas'])
    product.nilai_uts = float(request.form['nilai_uts'])
    product.nilai_uas = float(request.form['nilai_uas'])
    
    product.total_nilai, product.rata_rata, product.nilai_huruf, product.status = calculate_total_and_status(
        product.presensi, product.nilai_tugas, product.nilai_uts, product.nilai_uas)
    
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0', port=5005)

    #app.run(debug=True,host='0.0.0.0', port=5005)
