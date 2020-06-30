from MySQLdb import connect

db = connect(
    host='35.236.114.231',
    user='pscraper',
    db='pscraper_db',
    password='G6y5eiaXe8euyVC'
)
cursor = db.cursor()
cursor.execute('''
select group_concat(id) from pscraper_history 
group by vin, price, seller_id,mileage, marketplace 
having (count(vin)>1)
''')
for r in cursor.fetchall():
    for id_ in r[0].split(',')[1:]:
        if id_:
            cursor.execute(f'DELETE FROM pscraper_history WHERE id={id}')
            db.commit()
db.commit()
db.close()
