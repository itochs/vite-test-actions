from flask import Flask, make_response
import psycopg2
import os

from psycopg2.extras import DictCursor


app = Flask(__name__)


def get_connection():
    host = os.environ.get("PGHOST")
    dbname = os.environ.get("PGDATABASE")
    user = os.environ.get("PGUSER")
    password = os.environ.get("PGPASSWORD")
    return psycopg2.connect(host=host, dbname=dbname, user=user, password=password)


def add_project(uid: int):
    new_id = None
    sql = "insert into test (uid) values (%s) returning id"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("drop table if exists test cascade")
            cur.execute("create table test (id serial primary key, uid int)")
            cur.execute(sql, (uid,))
            returning = cur.fetchone()
            new_id = dict(returning) if returning is not None else None
        conn.commit()

    return new_id


@app.route("/")
def hello():
    id = add_project(1)
    return make_response(f"hi! {id}")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
