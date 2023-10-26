from model import Model
import psycopg2

tables = {
    1: 'User',
    2: 'Ticket',
    3: 'Event',
}


class View:

    def __init__(self, table, records):
        self.table = table
        self.records = records

    @staticmethod
    def list():
        print('''
        1 => User
        2 => Ticket
        3 => Event
        ''')

    @staticmethod
    def list_for_task1():
        print('''
            1 => User
            2 => Ticket
            3 => Event
            ''')

    @staticmethod
    def attribute_list_for_search(table):
        if table == 1:
            print('''
            please write on which column you want to search (userID, name or birth date)
            ''')
        elif table == 2:
            print('''
            please write on which column you want to search (ticketID, price or type)
            ''')
        elif table == 3:
            print('''
            please write on which column you want to search (eventID, User_userID, tickectID, date or purpose)
            ''')


    @staticmethod
    def attribute_list(table):
        if table == 1:
            print('''
                1 => name
                2 => birth date
                3 => userID
                ''')
        elif table == 2:
            print('''
                1 => ticketID
                2 => price
                3 => type
                ''')
        elif table == 3:
            print('''
                1 => eventID
                2 => User_userID
                3 => tickectID
                4 => date
                5 => purpose
                ''')


    @staticmethod
    def attribute_list_for_update(table):
        if table == 1:
            print('''
                    1 => name
                    2 => birth date
                    ''')
        elif table == 2:
            print('''
                    1 => price
                    2 => type
                    ''')
        elif table == 3:
            print('''
                    1 => date
                    2 => purpose
                    ''')

    def show(self):
        print("____________________")
        if self.table == 1:
            for row in self.records:
                print("User ID = ", row[0])
                print("Name = ", row[1])
                print("Birth date = ", row[2])
                print("____________________")
        elif self.table == 2:
            for row in self.records:
                print("Ticket ID = ", row[0])
                print("Price of the ticket = ", row[1])
                print("Type of the ticket = ", row[2])
                print("User ID = ", row[3])
                print("____________________")
        elif self.table == 3:
            for row in self.records:
                print("Event ID = ", row[0])
                print("Date = ", row[1])
                print("Purpose = ", row[2])
                print("Ticket ID = ", row[3])
                print("____________________")

        else:
            print('\nIncorrect input, try again.')

    # Method that prints the result of select query
    def showSelect(self):
        if self.table == 1:
            for row in self.records:
                print("User = ", row[0])
                print("Date of event = ", row[1])
                print("____________________")
        elif self.table == 2:
            for row in self.records:
                print("Price = ", row[0])
                print("Type = ", row[1])
                print("____________________")
        elif self.table == 3:
            for row in self.records:
                print("User = ", row[0])
                print("Date = ", row[1])
                print("Purpose = ", row[2])
                print("____________________")
        else:
            print('\nIncorrect input, try again.')


class Menu:
    # Main Method that calls main menu of the controller

    @staticmethod
    def mainmenu():
        exit = False
        print("Welcome!")
        while not exit:
            print('''
            Main menu
            0 => Show one table
            1 => Show all table
            2 => Insert data
            3 => Delete data
            4 => Update data
            5 => Select data
            6 => Randomize data
            7 => Exit''')
            choice = input('Make your choice => ')
            if choice == '0':
                View.list()
                table = input('Choose table number => ')
                table = Model.validTable(table)
                records = Model.showOneTable(table)
                obj = View(table, records)
                obj.show()
            elif choice == '1':
                for i in range(1, 4, 1):
                    records = Model.showOneTable(i)
                    obj = View(i, records)
                    obj.show()
            elif choice == '2':
                end_insert = False
                while not end_insert:
                    try:
                        View.list_for_task1()
                        table = input("Choose table number => ")
                        table = Model.validTable(table)
                        if table == 1:
                            usname = "'" + input("Name = ") + "'"
                            usbirth_date = "'" + input("Birth date = ") + "'"
                            usid = "'" + input('User ID = ') + "'"
                            Model.insert_for_table1(usname, usbirth_date, usid)
                        elif table == 2:
                            poid = "'" + input('Ticket ID = ') + "'"
                            poname = "'" + input('Price of the ticket = ') + "'"
                            potopic = "'" + input('Type = ') + "'"
                            pouser = "'" + input('User ID = ') + "'"
                            Model.insert_for_table2(poid, poname, potopic, pouser)
                        elif table == 3:
                            coid = "'" + input('Event  ID = ') + "'"
                            codate = "'" + input('Date = ') + "'"
                            cotext = "'" + input('Purpose = ') + "'"
                            copost = "'" + input('ticketID = ') + "'"

                            Model.insert_for_table3(coid, codate, cotext, copost)
                        else:
                            print('Incorrect input, try again.')
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                    incorrect = True
                    while incorrect:
                        num = input('Continue insertion? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_insert = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '3':
                end_delete = False
                while not end_delete:
                    try:
                        View.list_for_task1()
                        table = input("Choose table number => ")
                        table = Model.validTable(table)
                        if table == 1:
                            usid = "'" + input('Attribute to delete User ID = ') + "'"
                            Model.delete_for_table1(usid)
                        elif table == 2:
                            poid = "'" + input('Attribute to delete Ticket ID = ') + "'"
                            Model.delete_for_table2(poid)
                        elif table == 3:
                            coid = "'" + input('Attribute to delete Event ID = ') + "'"
                            Model.delete_for_table3(coid)
                        else:
                            print('Incorrect input, try again.')
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                    incorrect = True
                    while incorrect:
                        num = input('Continue deletion? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_delete = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '4':
                end_update = False
                while not end_update:
                    try:
                        View.list_for_task1()
                        table = input("Choose table number => ")
                        table = Model.validTable(table)
                        if table == 1:
                            usid = "'" + input('Attribute to update(where) User ID = ') + "'"
                            View.attribute_list_for_update(1)
                            in_restart = True
                            while in_restart:
                                num = input('Number of attribute =>')
                                if num == '1':
                                    value = "'" + input('New value of attribute = ') + "'"
                                    set = '"name" = {}'.format(value)
                                    in_restart = False
                                elif num == '2':
                                    value = "'" + input('New value of attribute = ') + "'"
                                    set = '"birth date" = {}'.format(value)
                                    in_restart = False
                                else:
                                    print('Incorrect input, try again.')
                                Model.update_for_table1(usid, set)
                        elif table == 2:
                            poid = "'" + input('Attribute to update(where) Ticket ID = ') + "'"
                            View.attribute_list_for_update(2)
                            in_restart = True
                            while in_restart:
                                num = input('Number of attribute =>')
                                if num == '1':
                                    value = "'" + input('New value of attribute = ') + "'"
                                    set = '"price"= {}'.format(value)
                                    in_restart = False
                                elif num == '2':
                                    value = "'" + input('New value of attribute = ') + "'"
                                    set = '"type"= {}'.format(value)
                                    in_restart = False
                                else:
                                    print('Incorrect input, try again.')
                                Model.update_for_table2(poid, set)
                        elif table == 3:
                            coid = "'" + input('Attribute to update(where) Comment ID = ') + "'"
                            View.attribute_list_for_update(3)
                            in_restart = True
                            while in_restart:
                                num = input('Number of attribute =>')
                                if num == '1':
                                    value = "'" + input('New value of attribute = ') + "'"
                                    set = '"date"= {}'.format(value)
                                    in_restart = False
                                elif num == '2':
                                    value = "'" + input('New value of attribute = ') + "'"
                                    set = '"purpose"= {}'.format(value)
                                    in_restart = False
                                else:
                                    print('Incorrect input, try again.')
                                Model.update_for_table3(coid, set)
                        else:
                            print('Incorrect input, try again.')
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                    incorrect = True
                    while incorrect:
                        num = input('Continue updation? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_update = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '5':
                end_select = False
                while not end_select:
                    try:
                        print('1 => Show date and purpose of event which are under the *user name* ')
                        print('2 => Show date and purpose of event which is under the *ticket type*')
                        choice = input('Your choice is ')
                        choice = int(choice)
                        if choice == 1:
                            user = input('Enter required user name = ')
                            records = Model.select1(user)
                            obj = View(choice, records)
                            obj.showSelect()
                        elif choice == 2:
                            ticket = input('Enter required type ticket = ')
                            records = Model.select2(ticket)
                            obj = View(choice, records)
                            obj.showSelect()

                        else:
                            print('Try again')
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                        Model.select()
                    incorrect = True
                    while incorrect:
                        num = input('Continue selection? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_select = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '6':
                end_random = False
                while not end_random:
                    try:
                        View.list()
                        table = input("Choose table number => ")
                        table = Model.validTable(table)
                        num = int(input('How much datas do you want to add => '))
                        Model.random(table, num)
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                        Model.random(table, num)
                    incorrect = True
                    while incorrect:
                        num = input('Continue randomization? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_random = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                        else:
                            print('Incorrect input, try again.')
            elif choice == '7':
                exit = True
            else:
                print('Incorrect input, try again.')
            incorrect = True
            while incorrect:
                end = input('Continue work with DB? 1 - Yes; 2 - No. = >')
                if end == '2':
                    incorrect = False
                    exit = True
                elif end == '1':
                    incorrect = False
                else:
                    print('Incorrect input, try again.')
