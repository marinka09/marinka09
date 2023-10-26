import controller
import time

tables = {
    1: 'User',
    2: 'Ticket',
    3: 'Event',
}

class Model:
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
        connection = controller.makeConnect()
        cursor = connection.cursor()
        table_name = '''"''' + tables[table] + '''"'''
        print(tables[table])
        show = 'select * from public.{}'.format(table_name)
        print("SQL query => ", show)
        print('')
        cursor.execute(show)
        records = cursor.fetchall()
        cursor.close()
        controller.closeConnect(connection)
        return records

    @staticmethod
    def insert_for_table1(usname, usbirth_date, usid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'This User ID already exists'"
            insert = 'DO $$ BEGIN if not exists (select "userID" from "User" where "userID" = {}) then INSERT ' \
                         'INTO "User"("userID", "name", "birth date") VALUES ({},{},{}); ' \
                         'raise notice {}; else raise notice {}; ' \
                         'end if; end $$;'.format(usid, usid, usname, usbirth_date, "'added'", notice)
            restart = False
        print('SQl query => ', insert)
        cursor.execute(insert)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def insert_for_table2(poid, poname, potopic, pouser):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'This Ticket ID already exists or this User ID does not exist'"
            insert = 'DO $$  BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) and not exists ' \
                     '(select "ticketID" from "Ticket" where "ticketID" = {}) THEN ' \
                     'INSERT INTO "Ticket"("ticketID", "price", "type", "userID" ) values ({}, {}, {}, {}); RAISE NOTICE {};' \
                     ' ELSE RAISE NOTICE {}; END IF; ' \
                     'END $$;'.format(pouser, poid, poid, poname, potopic, pouser,  "'added'", notice)
            restart = False
        print('SQl query => ', insert)
        cursor.execute(insert)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def insert_for_table3(coid, codate, cotext, copost):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'This Event ID already exists or this Ticket ID does not exist'"
            insert = 'DO $$  BEGIN IF EXISTS (select "ticketID" from "Ticket" where "ticketID" = {}) and not exists ' \
                     '(select "eventID" from "Event" where "eventID" = {}) THEN ' \
                     'INSERT INTO "Event"("eventID", "date", "purpose, ticket ID") values ({}, {}, {}, {}); RAISE NOTICE {};' \
                     ' ELSE RAISE NOTICE {}; END IF; END $$;'.format(copost, coid, coid, codate, cotext, copost,
                                                                     "'added'", notice)
            restart = False
        print('SQl query => ', insert)
        cursor.execute(insert)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def delete_for_table1(usid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            delete ='delete from "Event" where "ticketID" in (select "ticketID" from "Ticket" where "userID" = {});' \
                         'delete from "Ticket" where "userID" = {};' \
                         'delete from "User" where "userID" = {};'.format(usid, usid, usid)

            restart = False
        print("SQL query => ", delete)
        cursor.execute(delete)
        connection.commit()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def delete_for_table2(poid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            delete = 'delete from "Event" where "ticketID" = {};' \
                     'delete from "Ticket" where "ticketID" = {};'.format(poid, poid)
            restart = False
        print("SQL query => ", delete)
        cursor.execute(delete)
        connection.commit()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def delete_for_table3(coid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            delete = 'delete from "User" where "User_userID" = {};' \
                     'delete from "Event" where "eventID" = {};'.format(coid, coid)
            restart = False
        print("SQL query => ", delete)
        cursor.execute(delete)
        connection.commit()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def update_for_table1(usid, set):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'There is nothing to update'"
            update = 'DO $$ BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) THEN ' \
                         'update "User" set {} where "userID" = {}; ' \
                         'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(usid, set, usid, "'updated'", notice)
            restart = False
            pass
        print("SQL query => ", update)
        cursor.execute(update)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)
        pass

    @staticmethod
    def update_for_table2(poid, set):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'There is nothing to update'"
            update = 'DO $$ BEGIN IF EXISTS (select "ticketID" from "Ticket" where "ticketID" = {}) THEN ' \
                     'update "Ticket" set {} where "ticketID" = {}; ' \
                     'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                     'END $$;'.format(poid, set, poid, "'updated'", notice)
            restart = False
            pass
        print("SQL query => ", update)
        cursor.execute(update)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)
        pass

    @staticmethod
    def update_for_table3(coid, set):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'There is nothing to update'"
            update = 'DO $$ BEGIN IF EXISTS (select "eventID" from "Event" where "eventID" = {}) THEN ' \
                     'update "Event" set {} where "eventID" = {}; ' \
                     'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                     'END $$;'.format(coid, set, coid, "'updated'", notice)
            restart = False
            pass
        print("SQL query => ", update)
        cursor.execute(update)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)
        pass

    @staticmethod
    def select1(user):
        connection = controller.makeConnect()
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
        controller.closeConnect(connection)
        return records

    @staticmethod
    def select2(ticket):
        connection = controller.makeConnect()
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
        controller.closeConnect(connection)
        return records



    @staticmethod
    def random(table, num):
        connection = controller.makeConnect()
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
                insert = """INSERT INTO "Event" ("eventId", "date", "purpose", "ticketID")
                               SELECT
                                 {0},  -- Вставте eventId тут
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
        controller.closeConnect(connection)