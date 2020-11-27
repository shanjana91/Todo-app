from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#configure the DB (setup path/name)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite"
#create SQLAlchemy object
db=SQLAlchemy(app)

#create a user defined model using the parent model (db)
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    status=db.Column(db.Boolean)

@app.route("/")
def index():
    todo_list=Todo.query.all()
    #print(todo_list)
    return render_template("index.html",todo_list=todo_list)

@app.route("/add",methods=['POST'])
def add():
    #add todo items
    title=request.form.get("inputbox")
    new_todo=Todo(title=title,status=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #update status of the todo item
    todo_update=Todo.query.filter_by(id=todo_id).first()
    todo_update.status=not todo_update.status
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #delete the specific todo item
    todo_delete=Todo.query.filter_by(id=todo_id).first()
    try:
        db.session.delete(todo_delete)
    except:
        db.session.commit()
        return redirect(url_for("index"))
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)