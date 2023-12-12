import datetime
from sqlalchemy.orm import relationship
from db import Base, Session, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
import psycopg2
import time


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
s = Session()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'User'
    userID = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(Date)
    event = relationship("Event")

    def __init__(self, userID, name, birth_date):
        self.userID = userID
        self.name = name
        self.birth_date = birth_date

    def __repr__(self):
        return "<User(name='{}', birth_date={})>".format(self.name, self.birth_date)


class Ticket(Base):
    __tablename__ = 'Ticket'
    ticketID = Column(Integer, primary_key=True)
    price = Column(Integer)
    type = Column(String)
    userID = Column(Integer)
    event = relationship("Event")

    def __init__(self, ticketID, price, type, userID):
        self.ticketID = ticketID
        self.price = price
        self.type = type
        self.userID = userID

    def __repr__(self):
        return "<Ticket(price ='{}', type={})>".format(self.price, self.type)


class Event(Base):
    __tablename__ = 'Event'
    eventID = Column(Integer, primary_key=True)
    date = Column(Date)
    purpose = Column(String)

    ticketID = Column(Integer, ForeignKey('Ticket.ticketID'))
    User_userID = Column(Integer, ForeignKey('User.userID'))

    def __init__(self, eventID, date, purpose, ticketID):
        self.eventID = eventID
        self.date = date
        self.purpose = purpose
        self.ticketID = ticketID

    def __repr__(self):
        return "<Event(date={}, purpose='{}')>".format(self.date, self.purpose)




tables = {
    1: 'User',
    2: 'Ticket',
    3: 'Event',
}

class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    @staticmethod
    def validTable(table):
        incorrect = True
        while incorrect:
            if str(table).isdigit():
                table = int(table)
                if table >= 1 and table <= 3:
                    incorrect = False
                else:
                    print('Incorrect input, try again.')
            else:
                print('Incorrect input, try again.')
        return table

    @staticmethod
    def showOneTable(table):
        connection = makeConnect()
        cursor = connection.cursor()
        table_name = '''"''' + tables[table] + '''"'''
        print(tables[table])
        show = 'select * from public.{}'.format(table_name)
        print("SQL query => ", show)
        print('')
        cursor.execute(show)
        records = cursor.fetchall()
        cursor.close()
        closeConnect(connection)
        return records


    @staticmethod
    def insert_for_table1(userID: int, name: str, birth_date: datetime.date) -> None:
        user = User(userID=userID, name=name, birth_date=birth_date)
        s.add(user)
        s.commit()

    @staticmethod
    def insert_for_table2(ticketID: int, price: int, type: str, userID: int) -> None:
        ticket = Ticket(ticketID=ticketID, price=price, type=type, userID=userID)
        s.add(ticket)
        s.commit()

    @staticmethod
    def insert_for_table3(eventID: int, date: datetime.datetime, purpose: str, ticketID: int) -> None:
        event = Event(eventID=eventID, date=date, purpose=purpose, ticketID=ticketID)
        s.add(event)
        s.commit()

    @staticmethod
    def delete_for_table1(userID) -> None:
        sql_delete = s.query(User).filter_by(userID=userID).one()
        s.delete(sql_delete)
        s.commit()

    @staticmethod
    def delete_for_table2(ticketID) -> None:
        sql_delete = s.query(Ticket).filter_by(ticketID=ticketID).one()
        s.delete(sql_delete)
        s.commit()

    @staticmethod
    def delete_for_table3(eventID) -> None:
        sql_delete = s.query(Event).filter_by(eventID=eventID).one()
        s.delete(sql_delete)
        s.commit()

    @staticmethod
    def update_for_table1(userID: int, name: str, birth_date: datetime.datetime) -> None:
        s.query(User).filter_by(userID=userID).update({User.name: name, User.birth_date: birth_date})
        s.commit()

    @staticmethod
    def update_for_table2(ticketID: int, price: int, type: str) -> None:
        s.query(Ticket).filter_by(ticketID=ticketID).update({Ticket.price: price, Ticket.type: type})
        s.commit()

    @staticmethod
    def update_for_table3(eventID: int, date: datetime.datetime, purpose: str) -> None:
        s.query(Event).filter_by(eventID=eventID).update({Event.date: date, Event.purpose: purpose})
        s.commit()

    @staticmethod
    def select1(user):
        connection = makeConnect()
        cursor = connection.cursor()
        select = """select "name", "date", "purpose" from (select c."name", p."date", p."purpose"
                         from "Event" p right join "User" c on c."userID" = p."ticketID"
                             where c."name" LIKE '{}' group by c."name", p."date", p."purpose") as foo""".format(
            user)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        records = cursor.fetchall()
        print('Time of request = {} ms'.format(end))
        cursor.close()
        closeConnect(connection)
        return records

    @staticmethod
    def select2(ticket):
        connection = makeConnect()
        cursor = connection.cursor()
        select = """SELECT c."type", p."date", p."purpose"
                        FROM "Ticket" c
                        LEFT JOIN "Event" p ON c."ticketID" = p."ticketID"
                        WHERE c."type" LIKE '{}'""".format(ticket)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        records = cursor.fetchall()
        print('Time of request = {} ms'.format(end))
        cursor.close()
        closeConnect(connection)
        return records



    @staticmethod
    def random(table, num):
        connection = makeConnect()
        cursor = connection.cursor()
        incorrect = True
        while incorrect:
            if table == 1:
                insert = """INSERT INTO "User"("userID", "name", "birth date") 
SELECT
  gs.userID,
  chr(trunc(65 + random() * 26)::int) || chr(trunc(65 + random() * 26)::int),
  timestamp '2014-01-10 20:00:00' + random() * (timestamp '2014-01-20 20:00:00' - timestamp '2014-01-10 10:00:00')
FROM generate_series(1, 1) AS gs(userID)
LEFT JOIN "User" u ON gs.userID = u."userID"
WHERE random() > 0 AND u."userID" IS NULL""".format(num)

                incorrect = False
            elif table == 2:
                insert = """INSERT INTO "Ticket" ("ticketID", "price", "type", "userID")
                       SELECT
                         gs.ticketID,
                         trunc(random() * 100)::int,
                         chr(trunc(65 + random() * 26)::int) || chr(trunc(65 + random() * 26)::int),
                         generate_series(5, 7)
                       FROM generate_series(8, 10) AS gs(ticketID)
                       LEFT JOIN "Ticket" t ON gs.ticketID = t."ticketID"
                       WHERE t."ticketID" IS NULL
                       AND random() > 0;
                       """.format(num)
                incorrect = False
            elif table == 3:
                event_id = 2  # Замініть це значення на конкретне eventId
                insert = """INSERT INTO "Event" ("eventID", "date", "purpose", "ticketID")
                               SELECT
                                 {0},  -- Вставте eventID тут
                                 timestamp '2023-01-01' + random() * (timestamp '2023-12-31' - timestamp '2023-01-01'),
                                 chr(trunc(65 + random() * 26)::int) || chr(trunc(65 + random() * 26)::int),
                                 gs.ticketID
                               FROM generate_series(1, 5) AS gs(ticketID)
                               LEFT JOIN "Event" e ON gs.ticketID = e."ticketID"
                               WHERE e."eventId" IS NULL
                               AND random() > 0;""".format(event_id)
                incorrect = False
            else:
                print('Incorrect input, try again.')
        print("SQL query => ", insert)
        cursor.execute(insert)
        connection.commit()
        cursor.close()
        closeConnect(connection)