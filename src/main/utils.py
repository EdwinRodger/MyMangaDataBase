from zipfile import ZipFile
from datetime import datetime
import os

today_date = datetime.date(datetime.today())


def export_backup():
    with ZipFile(f"src\\MMDB-Export-{today_date}.zip", "w") as zf:
        zf.write(".env")
        zf.write("instance\\manga.db")


def delete_export():
    for backup in os.listdir("."):
        if "MMDB-Export-" in backup:
            os.remove(f"{backup}")
    for backup in os.listdir("src/"):
        if "MMDB-Export-" in backup:
            os.remove(f"src\\{backup}")


def extract_backup(filename):
    ZipFile(filename).extractall()
    os.remove(filename)
