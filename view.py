
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


