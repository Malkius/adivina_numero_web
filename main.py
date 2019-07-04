import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db

app = Flask(__name__)
db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    if request.method == "GET":
        email_address = request.cookies.get("email")
        if email_address:
            user = db.query(User).filter_by(email=email_address).first()
        else:
            user = None
        return render_template("formulario.html", user=user)

    elif request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        secret_number = random.randint(1, 30)

        print(nombre)
        print(email)
        print(secret_number)

        user = User(name=nombre, email=email, secret_number=secret_number)
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for("formulario")))
        response.set_cookie("email", email)

        return response


@app.route("/juego", methods=["GET", "POST"])
def juego():
    if request.method == "GET":
        response = make_response(render_template("juego.html"))
        return response

    elif request.method == "POST":
        email_address = request.cookies.get("email")
        if email_address:
            user = db.query(User).filter_by(email=email_address).first()
        else:
            return "Lo siento, no te encuentro"

        if not user:
            return "Lo siento, no te encuentro"

        guess = int(request.form.get("guess"))
        if guess == user.secret_number:
            message = "Sí, el número es {0}, eres el nuevo Rappel.".format(str(user.secret_number))
            response = make_response(render_template("resultado.html", message=message))
            user.secret_number = str(random.randint(1, 30))
            db.add(user)
            db.commit()
            return response

        elif guess > int(user.secret_number):
            message = "Prueba algo más pequeño."
            return render_template("resultado.html", message=message)
        elif guess < int(user.secret_number):
            message = "Prueba algo más grande."
            return render_template("resultado.html", message=message)


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("formulario")))
    response.set_cookie("email", expires=0)

    return response


if __name__ == '__main__':
    app.run()
