from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "secret_key"


# DB初期化
def init_db():

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    # ユーザーテーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # 筋トレ記録テーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        menu TEXT,
        reps INTEGER,
        weight INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ログイン画面
@app.route("/login")
def login_page():
    return render_template("login.html")


# ログイン処理
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        session["user_id"] = user[0]

        return redirect("/")

    else:

        return "ログイン失敗"


# 新規登録画面
@app.route("/register")
def register_page():
    return render_template("register.html")


# 新規登録処理
@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (username, password)
        VALUES (?, ?)
        """,
        (username, password)
    )

    conn.commit()
    conn.close()

    return redirect("/login")


# ログアウト
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ホーム
@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    selected_menu = request.args.get("menu")

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    # 種目一覧取得
    cursor.execute(
        """
        SELECT DISTINCT menu
        FROM workouts
        WHERE user_id = ?
        """,
        (user_id,)
    )

    menus = cursor.fetchall()

    # フィルター
    if selected_menu:

        cursor.execute(
            """
            SELECT id, date, menu, reps, weight
            FROM workouts
            WHERE user_id = ? AND menu = ?
            """,
            (user_id, selected_menu)
        )

    else:

        cursor.execute(
            """
            SELECT id, date, menu, reps, weight
            FROM workouts
            WHERE user_id = ?
            """,
            (user_id,)
        )

    workouts = cursor.fetchall()

    conn.close()

    labels = []
    weights = []

    for workout in workouts:
        labels.append(workout[1])
        weights.append(workout[4])

    return render_template(
        "index.html",
        workouts=workouts,
        labels=labels,
        weights=weights,
        menus=menus,
        selected_menu=selected_menu
    )


# 記録追加
@app.route("/record", methods=["POST"])
def record():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    date = request.form["date"]
    menu = request.form["menu"]
    reps = request.form["reps"]
    weight = request.form["weight"]

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO workouts
        (user_id, date, menu, reps, weight)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, date, menu, reps, weight)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# 編集画面
@app.route("/edit/<int:id>")
def edit(id):

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, date, menu, reps, weight
        FROM workouts
        WHERE id = ?
        """,
        (id,)
    )

    workout = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        workout=workout
    )


# 更新
@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    date = request.form["date"]
    menu = request.form["menu"]
    reps = request.form["reps"]
    weight = request.form["weight"]

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE workouts
        SET date = ?, menu = ?, reps = ?, weight = ?
        WHERE id = ?
        """,
        (date, menu, reps, weight, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# 削除
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("workout.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM workouts WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
with app.app_context():
    cursor = db.connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    
    db.connection.commit()