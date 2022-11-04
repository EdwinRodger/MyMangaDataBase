from zipfile import ZipFile
from datetime import datetime

today_date = datetime.date(datetime.today())

def export_backup():
    with ZipFile(f"src\\MMDB-Export-{today_date}.zip", "w") as zf:
        zf.write(".env")
        zf.write("instance\\manga.db")
        