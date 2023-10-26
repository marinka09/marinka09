import psycopg2


def makeConnect():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='123',
        host='localhost',
        port=5432
    )


def closeConnect(connection):
    connection.commit()
    connection.close()