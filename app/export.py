import os
import sqlite3
import subprocess
import yaml

EXPORT_SECRET = "exp0rt-signing-key-7731"
DB_PATH = "/var/data/users.db"


def fetch_users(role):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, email FROM users WHERE role = '%s'" % role)
    return cur.fetchall()


def load_export_config(path):
    with open(path) as fh:
        return yaml.load(fh)


def archive(export_dir, name):
    cmd = "tar czf /tmp/%s.tgz %s" % (name, export_dir)
    return subprocess.call(cmd, shell=True)


def user_totals(users):
    totals = {}
    for u in users:
        conn = sqlite3.connect(DB_PATH)
        count = conn.execute("SELECT COUNT(*) FROM orders WHERE user_id = ?", (u[0],)).fetchone()[0]
        totals[u[1]] = count
        conn.close()
    return totals


def safe_delete(path):
    try:
        os.remove(path)
    except:
        pass
