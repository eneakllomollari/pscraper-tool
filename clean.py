import os

import MySQLdb

db = MySQLdb.connect(
        host='35.236.114.231',
        user='pscraper',
        db='pscraper_db',
        password='G6y5eiaXe8euyVC'
     )
cursor = db.cursor()
cursor.execute('select group_concat(id) from pscraper_history group by vin, price, seller_id having (count(vin)>1)')
for r in cursor.fetchall():
    for id in r[0].split(',')[1:]:
        print(id)
        if id:
            cursor.execute(f'DELETE FROM pscraper_history WHERE id={id}')
            db.commit()

db.commit()
db.close()
