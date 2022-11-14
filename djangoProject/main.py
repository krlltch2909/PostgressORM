import psycopg2 as pg
import dotenv

def main():
    conn = pg.connect(dbname='demo',
                      user='ann',
                      password='qwerty',
                      host='95.165.30.171',
                      port='54321'
                      )

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TASKS')
    records = cursor.fetchall()

    print(records)
    print(type(records))

    for row in records:
        print(row)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()



