from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "studentsdb"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/students", methods=["GET"])
def get_actors():
    data = data_fetch("""select * from students""")
    return make_response(jsonify(data), 200)


@app.route("/students/<int:id>", methods=["GET"])
def get_student_by_id(id):
    data = data_fetch("""SELECT * FROM students where id = {}""".format(id))
    return make_response(jsonify(data), 200)


@app.route("/students/<int:id>/address", methods=["GET"])
def get_address_by_student(id):
    data = data_fetch(
        """
        SELECT students.first_name, students.last_name, town_city.city_name, province.province_name
        FROM students
        INNER JOIN student_details
        ON students.id = student_details.student_id
        INNER JOIN town_city
        ON student_details.town_city = town_city.id
        INNER JOIN province
        ON student_details.province = province.id
        WHERE student_details.student_id = {}
    """.format(
            id
        )
    )
    return make_response(
        jsonify({"student_id": id, "count": len(data), "address": data}), 200
    )


@app.route("/town_city", methods=["POST"])
def add_student():
    cur = mysql.connection.cursor()
    info = request.get_json()
    city_name = info["city_name"]
    cur.execute(
        """ INSERT INTO town_city (city_name) VALUE (%s)""",
        (city_name),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "town_city added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    cur.execute(
        """ UPDATE students SET first_name = %s, last_name = %s WHERE id = %s """,
        (first_name, last_name, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "student updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM students where id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "student deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/students/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
