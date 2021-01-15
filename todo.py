from flask import Flask,render_template,redirect,url_for,request #Flask Kütüphanesini ekliyorum.
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy Kütüphanesi ekliyorum.

app = Flask(__name__) #Uygulamamızın Flask olduğunu belirtiyoruz.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/m__ba/Desktop/Todo_App/todo.db" #URI'yı buraya dahil edeceğiz.
db = SQLAlchemy(app)

@app.route("/") #anasayfa yönlendirme kod satırımız
def index():
    todos = Todo.query.all() #Oluşturduğumuz Todo classındaki tüm sorguları todos değişkenine atıyoruz.
    return render_template("index.html", todos=todos) # todos değişkenini başka bir todos değişkenine aktararak index.html sayfasına yönlendiriyoruz.

@app.route("/complete/<string:id>") #todo güncelleme kod satırımız
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first() #todo id'ye göre işlem filtrelemesi

    todo.complete = not todo.complete #todo durum değişikliği
    db.session.commit() #todo db güncelleme
    return redirect(url_for("index")) # anasayfaya yönlendirme

@app.route("/delete/<string:id>") #todo silme kod satırımız
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first() #todo id'ye göre işlem filtrelemesi

    db.session.delete(todo) #todo silme işlemi
    db.session.commit() #todo db güncelleme
    return redirect(url_for("index")) # anasayfaya yönlendirme

@app.route("/add", methods=["POST"]) #todo ekleme kod satırımız
def addTodo():
    title= request.form.get("title") #todo title ekleme kodu
    newtodo = Todo(title = title,complete = False) 
    db.session.add(newtodo) # girilen todo'yu veritabanına ekleme
    db.session.commit() #todo db güncelleme
    return redirect(url_for("index"))  # anasayfaya yönlendirme

class Todo(db.Model): #sınıf oluşturma aşaması.
    id = db.Column(db.Integer, primary_key=True) #eşsiz id'mizin integer türünü ve birincil anahtar olduğunu belirtme.
    title = db.Column(db.String(80)) #todo app'imizde başlık sütunumuz.
    complete = db.Column(db.Boolean) #todo app'imizde tamamlandı/tamamlanmadı sütunumuz.

if __name__ == "__main__": #Projemizin başlamasını sağlayan komut satırı.
    db.create_all() #oluşturduğumuz class'ı sqlite'a dahil eden komut.   
    app.run(debug = True)