from flask import Flask, render_template, url_for, session, redirect, g, request
from flask_session import Session
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistationForm, LoginForm, AdminLoginForm, FilterForm, ChangePasswordForm, CheckoutForm
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)
    g.admin = session.get("admin_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None and g.admin is None:
            return redirect(url_for("login", next = request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        conflict_user = db.execute(
            """SELECT * FROM users
            WHERE user_id = ?;""", (user_id,)).fetchone()
        if conflict_user is not None:
            form.user_id.errors.append("Username already taken")
        else:
            db.execute("""
                INSERT INTO users (user_id, password)
                VALUES (?, ?);""", 
                (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute(
            """SELECT * FROM users WHERE user_id = ?;""",
        (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("No such Username!")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)


@app.route("/admin", methods=["GET", "POST"])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        password = form.password.data
        db = get_db()
        admin = db.execute(
            """SELECT * FROM admin WHERE admin_id = ?;""",
        (admin_id,)).fetchone()
        if admin is None:
            form.admin_id.errors.append("No such Username!")
        elif not check_password_hash(admin["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["admin_id"] = admin_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
        
        password = form.password.data
        db = get_db()
        db.execute("""
                INSERT INTO admin (admin_id, password)
                VALUES (?, ?);""", 
            (admin_id, generate_password_hash(password)))
        db.commit()
    return render_template("adminLogin.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html")

@app.route("/password", methods=["GET","POST"])
@login_required
def password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        old_password = form.old_password.data
        new_password = form.new_password.data
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE user_id = ?;", (username,)).fetchone()
        if user is None:
            form.username.errors.append("Username does not exist!")
        elif not check_password_hash(user['password'], old_password):
            form.old_password.errors.append("Incorrect old password!")
        else:
            db.execute("UPDATE users SET password = ? WHERE user_id = ?;", (generate_password_hash(new_password), username))
            db.commit()
            return redirect("account")
    return render_template("password.html", form=form)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/membership", methods=["GET", "POST"])
def membership():
    form = FilterForm()
    db = get_db()
    membership = db.execute("""SELECT * FROM memberships;""").fetchall()
    
    if form.validate_on_submit():
        filters = form.filters.data
        if filters == "<100":
            membership = db.execute("""SELECT * FROM memberships WHERE price < 100;""").fetchall()
        elif filters == "100-200":
            membership = db.execute("""SELECT * FROM memberships WHERE price BETWEEN 100 AND 200;""").fetchall()
        elif filters == "200-300":
            membership =  db.execute("""SELECT * FROM memberships WHERE price BETWEEN 200 AND 300;""").fetchall()
        elif filters == "300+":
            membership = db.execute("""SELECT * FROM memberships WHERE price > 300;""").fetchall()

    return render_template("membership.html", form=form, membership=membership)

@app.route("/pts")
def pts():
    db = get_db()
    pts = db.execute("""SELECT * FROM pts;""").fetchall()
    return render_template("pts.html", pts=pts)

@app.route("/pt/<int:pt_id>")
@login_required
def pt(pt_id):
    db = get_db()
    pt = db.execute("""SELECT * FROM pts WHERE pt_id = ?;""", (pt_id,)).fetchone()
    return render_template("pt.html", pt=pt)

@app.route("/classes")
def classes():
    db = get_db()
    classes = db.execute("""SELECT * FROM classes;""").fetchall()
    return render_template("classes.html", classes=classes)

@app.route("/class/<int:class_id>")
@login_required
def c(class_id):
    db = get_db()
    c = db.execute("""SELECT * FROM classes WHERE class_id = ?;""", (class_id,)).fetchone()
    t = db.execute("""SELECT * FROM classtimes;""").fetchall()
    return render_template("c.html", c=c, t=t)

@app.route("/add_to_cart/<int:membership_id>")
@login_required
def add_to_cart(membership_id):
    if "cart" not in session:
        session["cart"] = {"memberships": {}, "pts": {}, "classes": {}}

    if membership_id not in session["cart"]["memberships"]:
        session["cart"]["memberships"][membership_id] = 1
    else:
        session["cart"]["memberships"][membership_id] += 1

    names = {}
    total = 0
    db = get_db()
    for membership_id in session["cart"]["memberships"]:
        membership = db.execute("SELECT * FROM memberships WHERE membership_id = ?;", (membership_id, )).fetchone()
        #if membership is not None:
        name = membership["name"]
        names[membership_id] = name
        price = membership["price"]
        total += price
    
    if len(session["cart"]["memberships"]) > 0:
        error_message = "Cart already has a membership option. You can't have more than one membership option."
        return render_template("cart.html", cart=session["cart"], error_message=error_message, names=names, total=total)
    
    return redirect(url_for("cart"))

@app.route("/cart")
@login_required
def cart():
    if "cart" not in session:
        session["cart"] = {"memberships": {}, "pts": {}, "classes": {}}
    names = {}
    total = 0
    db = get_db()
    for membership_id in session["cart"]["memberships"]:
        membership = db.execute("""SELECT * FROM memberships 
                          WHERE membership_id = ?;""", (membership_id, )).fetchone()

        #if membership is not None:
        name = membership["name"]
        names[membership_id] = name
        price = membership["price"]
        total += price

    return render_template("cart.html", cart=session["cart"], names=names, total=total)

@app.route("/checkout")
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = CheckoutForm()
    message = ""
    checkout = None
    if form.validate_on_submit():
        if "cart" in session:
            db = get_db() 
            cart = session["cart"]
            for item_id, item in cart.items():
                db.execute("INSERT INTO checkout (item_id, name, price) VALUES (?, ?, ?)",
                           (item_id, item["name"], item["price"]))
            db.commit()
            session["cart"] = {}
            message = "Checkout Complete"
            return redirect(url_for("index"))
    return render_template("checkout.html", form=form, message=message, checkout=checkout)

@app.route("/remove_from_cart/<item_type>/<int:item_id>")
@login_required
def remove_from_cart(item_type, item_id):
    if "cart" not in session:
        return redirect(url_for('cart'))

    if item_type not in session["cart"] or item_id not in session["cart"][item_type]: # Used ChatGPT to help understand sessions to remove items from my cart.
        return redirect(url_for('cart'))

    session.pop("cart", None) # Got this .pop code from this site - https://www.techwithtim.net/tutorials/flask/sessions

    return redirect(url_for('cart'))