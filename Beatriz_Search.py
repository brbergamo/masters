#!/usr/bin/env python3

from flask import Flask, request, render_template
import mariadb

app = Flask(__name__)

DB_CONFIG = {
    "host": "bioed-new.bu.edu",
    "user": "bbergamo",
    "password": "bolinho1",
    "database": "miRNA",
    "port": 4253
}

@app.route("/", methods=["GET"])
def search():
    mirna1 = request.args.get("mirna1", "").strip()
    mirna2 = request.args.get("mirna2", "").strip()
    max_score = request.args.get("max_score", "-0.1")

    error_msg = ""
    results = []
    summary = ""
    table_html = ""

    if mirna1 and mirna2:
        try:
            connection = mariadb.connect(**DB_CONFIG)
            cursor = connection.cursor()

            # Check if both miRNAs exist
            cursor.execute("SELECT DISTINCT name FROM miRNA WHERE name IN (%s, %s);", (mirna1, mirna2))
            found = [row[0] for row in cursor.fetchall()]

            if mirna1 not in found or mirna2 not in found:
                error_msg = f"One or both miRNAs not found in database: {mirna1}, {mirna2}"
            else:
                query = """
                    SELECT t1.gid, g.name, t1.score as score1, t2.score as score2
                    FROM targets t1
                    JOIN targets t2 ON t1.gid = t2.gid
                    JOIN gene g ON t1.gid = g.gid
                    JOIN miRNA m1 ON t1.mid = m1.mid
                    JOIN miRNA m2 ON t2.mid = m2.mid
                    WHERE m1.name = %s
                    AND m2.name = %s
                    AND t1.score <= %s
                    AND t2.score <= %s
                    AND t1.score IS NOT NULL
                    AND t2.score IS NOT NULL
                    ORDER BY (t1.score + t2.score) ASC;

                """
                cursor.execute(query, (mirna1, mirna2, max_score, max_score))
                results = cursor.fetchall()

                summary = f"There are {len(results)} genes targeted by both miRNAs {mirna1} and {mirna2} with scores ≤ {max_score}."

            cursor.close()
            connection.close()

        except mariadb.Error as e:
            error_msg = f"Database error: {str(e)}"
    elif "mirna1" in request.args or "mirna2" in request.args:
        error_msg = "Please enter both miRNA names."

    return render_template("Beatriz_Search.html",
                           error_msg=error_msg,
                           results=results,
                           mirna1=mirna1,
                           mirna2=mirna2,
                           max_score=max_score,
                           summary=summary)
