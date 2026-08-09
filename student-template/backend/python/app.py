
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

from database import get_db_connection

app = Flask(__name__)


@app.route('/api/inventory/alerts', methods=['GET'])
def get_alerts():
    """
    Return all products where quantity <= reorder_level.
    """
    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT id, product_name, quantity, reorder_level
                FROM inventory
                WHERE quantity <= reorder_level
            """)

            alerts = cursor.fetchall()

        return jsonify(alerts), 200

    except psycopg2.Error as e:
        app.logger.error("Database error: %s", e)
        return jsonify({"error": "Database error"}), 500

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

