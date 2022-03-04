import mysql.connector

mycon = mysql.connector.connect(
    host="localhost", user="root", passwd="rilp@2020", database="trainbooking")
cursor = mycon.cursor(buffered=True)
mycon.autocommit = True
from pyfiglet import Figlet
from getpass import getpass
import datetime
import pytz
import os
import random

##################################################################################################
# NUMBER CHECK
def number_check(num):
    length = len(num)
    if length > 10 or length < 10:
        return False
    else:
        return True


# GLOBAL VARIABLE
cached_username = []
cached_time = []

# TRAINS DB
trains = {
    "2022-03-01": ["DURONTO EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-02": ["DURONTO EXPRESS", "TEJAS EXPRESS"],
    "2022-03-03": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-04": ["DURONTO EXPRESS", "TEJAS EXPRESS"],
    "2022-03-05": ["DURONTO EXPRESS"],
    "2022-03-06": ["SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-07": ["SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-08": ["DURONTO EXPRESS", "TEJAS EXPRESS"],
    "2022-03-09": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-10": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS"],
    "2022-03-11": ["JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-12": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-13": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-14": ["JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-15": ["SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-16": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-17": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-18": ["DURONTO EXPRESS"],
    "2022-03-19": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-20": ["DURONTO EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-21": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-22": ["JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-23": ["DURONTO EXPRESS", "SHATABDI EXPRESS"],
    "2022-03-24": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-25": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-26": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-27": ["DURONTO EXPRESS", "TEJAS EXPRESS"],
    "2022-03-28": ["DURONTO EXPRESS", "SHATABDI EXPRESS", "JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-29": ["JAN SHATABDI EXPRESS", "TEJAS EXPRESS"],
    "2022-03-30": ["DURONTO EXPRESS", "SHATABDI EXPRESS"],
}


# PNR GENERATOR
def pnr(train):
    m = random.randint(0, 22)
    n = random.randint(0, 22)
    if train == "DURONTO EXPRESS":
        return "D{}{}".format(m, n)
    elif train == "SHATABDI EXPRESS":
        return "S{}{}".format(m, n)
    elif train == "JAN SHATABDI EXPRESS":
        return "J{}{}".format(m, n)
    elif train == "TEJAS EXPRESS":
        return "T{}{}".format(m, n)


#################################################################################################


def main():
    text = Figlet(font="big")
    print("==========================================================")
    print(text.renderText("TRAINZY"))
    print("==========================================================")
    print(
        """
        1. Sign In\n
        2. Sign Up\n
        3. Check PNR Status\n
        4. Close
        """
    )
    print("==========================================================")
    uc = int(input("Enter your choice (choose a number from the above options): "))

    if uc == 1:
        result1 = sign_in()
        if result1:
            main()
        else:
            main()
    elif uc == 2:
        result2 = sign_up()
        if result2:
            main()
        else:
            main()
    elif uc == 3:
        result3 = checkpnr()
        if result3:
            main()
        else:
            main()
    elif uc == 4:
        print("It was nice to have you onboard 😀")
    else:
        print("You choose a wrong option. Try again")
        main()


def sign_in():
    print("==========================================================")
    email = input("Enter your Email: ")
    pwd = getpass("Enter your Password (the password won't be visible for security reason): ")
    print("==========================================================")
    try:
        s1 = "select * from useraccount where email='{}' and password='{}'".format(email, pwd)
        cursor.execute(s1)
        data = cursor.fetchall()[0]
        data = list(data)

        name = data[0] + ' ' + data[1]
        current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

        cached_username.append(data[2])
        cached_time.append(current_time)

        main_area(name, current_time)
        return True
    except Exception as err:
        print(err)
        print("There is no account found with these details.")
        return False


def sign_up():
    print("==========================================================")
    fname = input("Enter your First Name: ")
    lname = input("Enter your Last Name: ")
    email = input("Enter your Email: ")

    emailcheck = "select * from useraccount where email='{}'".format(email)
    cursor.execute(emailcheck)
    data = cursor.fetchall()
    if data:
        print("An account already exists with this Email address. Try again")
        sign_up()
    else:
        pwd = getpass("Enter the Password (the password won't be visible for security reason): ")
        phno = input("Enter your Phone Number: ")
        numcheck = number_check(phno)
        if not numcheck:
            print("The phone number entered is not valid.")
            sign_up()
        else:
            gender = input("Enter your Gender (M,F,O): ")
            y = input("Enter your DOB Year (format-YYYY): ")
            m = input("Enter your DOB Month (format-MM): ")
            d = input("Enter your DOB Date (format-DD): ")
            age = int(input("Enter your Age: "))
            print("==========================================================")
            try:
                dob = y + '-' + m + '-' + d
                c1 = f"insert into useraccount values('{fname}', '{lname}', '{email}', '{pwd}', '{phno}', '{gender.upper()}', '{dob}',  {age})"

                cursor.execute(c1)
                print("✅ Account created successfully!")
                print("==========================================================")
                name = fname + ' ' + lname
                current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

                cached_username.append(email)
                cached_time.append(current_time)

                main_area(name, current_time)
                return True
            except Exception as err:
                print(err)
                print("Something went wrong. Try again")
                return False


def checkpnr():
    print("==========================================================")
    pnrno = input("Enter the PNR No: ")
    try:
        c1 = f"select trainexp, fromf, tod, datefd, status from railway where pnr='{pnrno}'"
        cursor.execute(c1)
        data = cursor.fetchall()[0]
        data = list(data)

        train = data[0]
        fromf = data[1]
        tod = data[2]
        datefd = data[3]
        status = data[4]

        print(f"TRAIN- {train} :: FROM- {fromf} :: TO- {tod} :: FOR- {datefd} :: STATUS- {status}")
        print("==========================================================")
        return True
    except:
        print("No ticket found with this PNR number")
        return False


def main_area(name, current_time):
    print("==========================================================")
    print(f"Welcome {name}\nLogged in at: {current_time}")
    print("==========================================================")
    print(
        """
        1. Book Tickets\n
        2. Manage Bookings\n
        3. Logout
        """
    )
    print("==========================================================")
    uc1 = int(input("Enter your choice (choose a number from the above options): "))

    if uc1 == 1:
        searchtrain()
    elif uc1 == 2:
        managetickets()
    elif uc1 == 3:
        cached_username.remove(cached_username[0])
        cached_time.remove(cached_time[0])

        print("✅ You have successfully logged out")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    else:
        print("You choose a wrong option. Try again")
        main_area()


def searchtrain():
    print("==========================================================")
    bookf = input("FROM: ")
    bookt = input("TO: ")
    bookd = input("Date of Travel (YYYY-MM-DD): ")

    ava_trains = trains[bookd]
    ava_trains_no = len(ava_trains)

    trains_lst = []
    count = 1
    for x in ava_trains:
        trains_lst.append("{}. {}".format(count, x))
        count += 1

    print(f"There are {ava_trains_no} available trains on {bookd}:\n")
    print("\n".join(trains_lst))
    print("==========================================================")
    train = input("Choose the train (enter the number associated with the train name)\n(You can write exit to stop): ")

    if train == "exit":
        main_area(cached_username[0], cached_time[0])
    else:
        train = int(train)
        try:
            train_name = ava_trains[train-1]
            book = booktickets(train_name, bookf, bookt, bookd)
            if book:
                main_area(cached_username[0], cached_time[0])
            else:
                main_area(cached_username[0], cached_time[0])
        except Exception as err:
            print(err)
            print("The number entered is invalid")
            searchtrain()


def booktickets(train, f, t, date):
    # No of users having booking on same date and on same train
    s1 = f"select * from railway where trainexp='{train}' and datefd='{date}'"
    cursor.execute(s1)
    data_lst = list(cursor.fetchall())
    data_length = len(data_lst)

    stat = 50 - data_length
    status = None
    if stat < 0:
        status = "WT"
    else:
        status = "C"

    print("==========================================================")
    ticketno = int(input("How many tickets you want to book? "))
    bookfname = input("Enter the ticket booker's First Name: ")
    booklname = input("Enter the ticket booker's Last Name: ")
    bookphn = input("Enter the ticket booker's Phone Number: ")
    bookage = input("Enter the ticket booker's Age: ")
    bookgen = input("Enter the ticket booker's Gender (M,F,O): ")
    bookf = f
    bookt = t
    bookdate = date
    pnrno = pnr(train)
    print("==========================================================")

    try:
        s2 = f"insert into railway values('{pnrno}', '{bookfname}', '{booklname}', '{bookphn}', '{cached_username[0]}', '{bookgen}', {bookage},  '{bookf}', '{bookt}', '{bookdate}', '{train}', '{status}')"
        cursor.execute(s2)
        print(
            "PNR: {}\n\n✅ You have successfully booked the ticket\nFrom: {}\nTo: {}\nFor date: {}\nNumber of Tickets: {}\nStatus: {}\nTrain: {}\n\nContact Details: {} and {}".format(
                pnrno, bookf, bookt, bookdate, ticketno, status, train, cached_username[0], bookphn))
        print("==========================================================")
        return True
    except Exception as err:
        print(err)
        print("There was an error booking the ticket")
        searchtrain()


def managetickets():
        s1 = f"select * from railway where email='{cached_username[0]}'"
        cursor.execute(s1)
        data = list(cursor.fetchall())

        bookings = []
        for x in data:
            time = x[9]
            bookings.append(x[0] + "  " + x[1]+" "+x[2] + "  " + x[3] + "    " + x[7] + "    " + x[8] + "   " +time.strftime('%m/%d/%Y') + "  " + x[10] + "  " + x[11])

        if len(data) < 1:
            print("There are no active bookings in your account.")
            main_area(cached_username[0], cached_time[0])
        else:
            print("There are total {} bookings for this account, which one you want to manage: ".format(len(data)))
            print("==========================================================")
            print("║ PNR ║   Name   ║    Number   ║  FROM  ║  TO  ║  DATE  ║    TRAIN    ║  STATUS  ║")
            print("\n".join(bookings))
            print("==========================================================")
            uc3 = input("Choose the booking which you want to manage (You can write exit to stop): ")

            if uc3 == "exit":
                main_area(cached_username[0], cached_time[0])
            else:
                uc3 = int(uc3)
                try:
                    ticket = data[uc3-1]
                    pnrno = ticket[0]
                    fname = ticket[1]
                    lname = ticket[2]
                    phn = ticket[3]
                    age = ticket[6]
                    gender = ticket[5]
                    fromf = ticket[7]
                    tod = ticket[8]
                    date = ticket[9]
                    email = ticket[4]
                    trainname = ticket[10]
                    status = ticket[11]

                    print(
                        """
                        1. PNR No. {}
                        2. Name: {}
                        3. Phone Number: {}
                        4. Age: {}
                        5. Gender: {}
                        6. From: {}
                        7. To: {}
                        8. Date: {}
                        9. Email: {}
                        10. Train: {}
                        11. Status: {}
                        """.format(pnrno, fname+" "+lname, phn, age, gender, fromf, tod, date.strftime('%m/%d/%Y'), email, trainname, status)
                    )
                    print("==========================================================")
                    print(
                        """
                        1. Do you want to cancel the booking?
                        2. Do you want to edit the booking?
                        3. Do you want to exit?
                        """
                    )
                    print("==========================================================")
                    uc4 = int(input("Choose the appropriate option from above: "))

                    if uc4 == 1:
                        s2 = "delete from railway where pnr='{}'".format(pnrno)
                        cursor.execute(s2)
                        print("==========================================================")
                        print("✅ Your booking with PNR No. {} has been cancelled".format(pnrno))
                        print("==========================================================")

                        main_area(cached_username[0], cached_time[0])
                    elif uc4 == 2:
                        while True:
                            e_wh = int(input("Which detail you want to edit? (Choose the field numbers): "))
                            if e_wh == 2:
                                fname_new = input("Enter the new First Name: ")
                                lname_new = input("Enter the new Last Name: ")
                                s3 = "update railway set fname='{}', lname='{}' where pnr='{}'".format(fname_new,lname_new, pnrno)
                                cursor.execute(s3)

                                print("✅ Edited the ticket booker's name")
                                stop = input("Want to continue editing? (Y/N)")

                                if stop == "Y":
                                    continue
                                elif stop == "N":
                                    main_area(cached_username[0], cached_time[0])
                                    break
                                else:
                                    print("Wrong option selected")
                                    break
                            elif e_wh == 3:
                                phn_new = input("Enter the new Phone Number: ")
                                s3 = "update railway set phno='{}'where pnr='{}'".format(phn_new, pnrno)
                                cursor.execute(s3)

                                print("✅ Edited the ticket booker's phone number")
                                stop = input("Want to continue editing? (Y/N)")

                                if stop == "Y":
                                    continue
                                elif stop == "N":
                                    main_area(cached_username[0], cached_time[0])
                                    break
                                else:
                                    print("Wrong option selected")
                                    break
                            elif e_wh == 4:
                                age_new = input("Enter the new Age: ")
                                s3 = "update railway set age='{}'where pnr='{}'".format(age_new, pnrno)
                                cursor.execute(s3)

                                print("✅ Edited the ticket booker's age")
                                stop = input("Want to continue editing? (Y/N)")

                                if stop == "Y":
                                    continue
                                elif stop == "N":
                                    main_area(cached_username[0], cached_time[0])
                                    break
                                else:
                                    print("Wrong option selected")
                                    break
                            elif e_wh == 5:
                                gender_new = input("Enter the new Gender: ")
                                s3 = "update railway set age='{}'where pnr='{}'".format(gender_new, pnrno)
                                cursor.execute(s3)

                                print("✅ Edited the ticket booker's gender")
                                stop = input("Want to continue editing? (Y/N)")

                                if stop == "Y":
                                    continue
                                elif stop == "N":
                                    main_area(cached_username[0], cached_time[0])
                                    break
                                else:
                                    print("Wrong option selected")
                                    break
                            elif e_wh == 6:
                                print("You can't change that")
                                continue
                            elif e_wh == 7:
                                print("You can't change that")
                                continue
                            elif e_wh == 8:
                                date_new = input("Enter the new Date of Journey (YYYY-MM-DD): ")
                                s3 = "update railway set datefd='{}'where pnr='{}'".format(date_new, pnrno)
                                cursor.execute(s3)

                                print("✅ Edited the ticket's date")
                                stop = input("Want to continue editing? (Y/N)")

                                if stop == "Y":
                                    continue
                                elif stop == "N":
                                    main_area(cached_username[0], cached_time[0])
                                    break
                                else:
                                    print("Wrong option selected")
                                    break
                            elif e_wh == 9:
                                print("You can't change that")
                            elif e_wh == 10:
                                print("You can't change that")
                            else:
                                print("You have choose an incorrect option or that option can not be changed.")
                                continue
                    elif uc4 == 3:
                        main_area(cached_username[0], cached_time[0])
                    else:
                        print("Choose a wrong number.")
                        main_area(cached_username[0], cached_time[0])
                except Exception as err:
                    print(err)
                    managetickets()

def dbcheck():
    # DATABASE CHECK
    database_check_1 = "select * from useraccount"
    try:
        cursor.execute(database_check_1)
    except:
        database_edit_1 = "create table useraccount (fname varchar(100), lname varchar(100), email varchar(100) primary key, password varchar(150), phno varchar(20), gender varchar(50), dob date, age int)"
        cursor.execute(database_edit_1)


    database_check_2 = "select * from railway"
    try:
        cursor.execute(database_check_2)
    except:
        database_edit_2 = "create table railway (pnr varchar(15) primary key, fname varchar(100), lname varchar(100), phno varchar(20), email varchar(100), gender varchar(50), age int, fromf varchar(100), tod varchar(100), datefd date, trainexp varchar(50), status varchar(3))"
        cursor.execute(database_edit_2)

    return True


database_check = dbcheck()
if database_check:
    main()
else:
    print("There was an error and the tables couldn't be created")