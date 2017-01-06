from __future__ import print_function
from django.db import connection
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *

filterEventsQuery = ''
userEmail = ''


# Create views here.


def login(request):
    global filterEventsQuery, userEmail
    filterEventsQuery = ''
    userEmail = ''
    form = LogInForm(request.POST or None)
    context = {
        "form": form,
        "title": ""
    }
    if form.is_valid():
        if loginCheck(form.clean_email(), form.clean_password()):
            global userEmail
            userEmail = form.clean_email()
            if userEmail != '':
                return HttpResponseRedirect('/browse/')
            else:
                context = {
                    "form": form,
                    "title": "PLEASE LOG IN FIRST!"
                }
        else:
            context = {
                "form": form,
                "title": "WRONG USER NAME OR PASSWORD!"
            }
    return render(request, "registration/login.html", context)


def signup(request):
    global filterEventsQuery, userEmail
    filterEventsQuery = ''
    userEmail = ''
    form = SignUpForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        try:
            insertUser(form.clean_email(), form.clean_password(), form.clean_name(), form.clean_surname())
        except IntegrityError:
            context = {
                "warning": "Use Different Email, the Email that you typed has been registered already!",
                "form": form
            }
            return render(request, "signup/signup.html", context)
    return render(request, "signup/signup.html", context)


def browse(request):
    # User must log in before browsing
    if userEmail == '':
        return HttpResponseRedirect('/')
    else:
        global filterEventsQuery
        filterEventsQuery = ''
        event_form = EventForm(request.POST)
        city_form = CityForm(request.POST)
        showroom_form = ShowroomForm(request.POST)

        context = {
            "welcome": "Welcome | %s" % userEmail,
            "categories": event_form,
            "cities": city_form,
            "showrooms": showroom_form
        }

        event_input = request.POST.get('Categories')
        city_input = request.POST.get('Cities')
        showroom_input = request.POST.get('Showrooms')
        dateBegin_input = request.POST.get('DateBegin')
        dateEnd_input = request.POST.get('DateEnd')

        if request.POST:
            global filterEventsQuery
            filterEventsQuery = filterEvents(event_input, dateBegin_input, dateEnd_input, showroom_input, city_input)
            return HttpResponseRedirect('/events/')
        return render(request, "mainPage/main.html", context)


def events(request):
    if filterEventsQuery != "":
        cursor = connection.cursor()
        cursor.execute(filterEventsQuery)
        query_results = cursor.fetchall()
        eventIDs = []
        ticketCapacities = []

        for tupples in query_results:
            eventID = str(tupples[6])
            ticketLeft = str(tupples[2])
            eventIDs.append(eventID)
            ticketCapacities.append(ticketLeft)
        context = {
            "query_results": query_results,
        }
        cursor.close()
        counter = -1
        for eventID in eventIDs:
            counter += 1
            ticketReserved = request.POST.get(eventID)
            if ticketReserved is not None:
                if len(str(ticketReserved)) > 0:  # To grab only typed inputs at events page also ticketReserved should be less then ticketLeft
                    try:
                        if float(ticketCapacities[counter]) >= float(ticketReserved):
                            makeReservation(ticketReserved, userEmail, eventID)
                            return HttpResponseRedirect('/events/')
                        else:
                            context = {
                                "query_results": query_results,
                                "warning": "You cannot buy more tickets than capacity! Please type a number which is below ticket left amount!"
                            }
                            return render(request, "events/event.html", context)
                    except ValueError:
                        context = {
                            "query_results": query_results,
                            "warning": "Do not write chars other than numbers!",
                        }
                        return render(request, "events/event.html", context)
        return render(request, "events/event.html", context)
    else:
        return HttpResponseRedirect('/browse/')


def myReservations(request):
    cursor = connection.cursor()
    cursor.execute(reservationListQuery(userEmail))
    query_results_main = cursor.fetchall()
    reservationIDs = []

    for tupples in query_results_main:
        resID = str(tupples[4])
        reservationIDs.append(resID)

    context = {
        "query_results": query_results_main,
        "email": userEmail
    }
    cursor.close()

    for resID in reservationIDs:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TicketDb.Reservations where ID = %s;" % resID)
        query_results = cursor.fetchall()
        deletedReservation = []
        cursor.close()

        for element in query_results:
            deletedReservation.append(str(element[1]))
            deletedReservation.append(str(element[3]))
        ticketPurchased = deletedReservation[0]
        eventID = deletedReservation[1]

        # To delete partial reservation
        if request.POST.get("partialButton%s" % resID):
            try:
                if float(deletedReservation[0]) > float(request.POST.get("partialInput%s" % resID)):
                    deletePartialReservation(resID, float(request.POST.get("partialInput%s" % resID)), eventID)
                    return HttpResponseRedirect('/myreservations/')

                elif float(deletedReservation[0]) == float(request.POST.get("partialInput%s" % resID)):
                    deleteReservation(resID, ticketPurchased, eventID)
                    return HttpResponseRedirect('/myreservations/')

                elif float(deletedReservation[0]) < float(request.POST.get("partialInput%s" % resID)):
                    context = {
                        "query_results": query_results_main,
                        "email": userEmail,
                        "warning": "You cannot cancel more reservations than you reserved!"
                    }
                    return render(request, "reservations/myreservations.html", context)
            except ValueError:
                context = {
                    "query_results": query_results_main,
                    "email": userEmail,
                    "warning": "Do not write chars other than numbers!"
                }
                return render(request, "reservations/myreservations.html", context)
        # To delete all reservation
        elif request.POST.get(resID):
            deleteReservation(resID, ticketPurchased, eventID)
            return HttpResponseRedirect('/myreservations/')

    return render(request, "reservations/myreservations.html", context)


def insertUser(email, password, name, surname):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO TicketDb.User values (%s,%s,%s,%s)" % (
                "'{}'".format(email), "'{}'".format(password), "'{}'".format(name), "'{}'".format(surname)))
        cursor.close()


def loginCheck(email, password):
    cursor = connection.cursor()

    query = "Select Email, Password from TicketDb.User where Email= %s and Password = %s" % (
        "'{}'".format(email), "'{}'".format(password))
    print (query)
    cursor.execute(query)

    for (email, password) in cursor:
        if email != "" and password != "":
            return True
        else:
            return False
    cursor.close()


def filterEvents(event, begin_date, end_date, showroom, city):
    if event == 'All Events' or event == '':
        event = '.*'  # It means take all the possible chars in regular expression
    if showroom == 'All Showrooms' or showroom == '':
        showroom = '.*'  # It means take all the possible chars in regular expression
    if city == 'All Cities' or city == '':
        city = '.*'  # It means take all the possible chars in regular expression
    if begin_date == '':
        begin_date = '01-01'  # It means take all the possible chars in regular expression
    if end_date == '':
        end_date = '12-31'  # It means take all the possible chars in regular expression
    query = ("""Select
        Date,
        Activity.Name,
        TicketsLeft,
        Type,
        Showroom.Name As Showroom,
        City,
        ActivityID
     from
    (SELECT
        ID as ActivityID,
        Name,
        Date,
        TicketsLeft,
        Type,
        ShowroomID
        FROM TicketDb.Activity
    Where Type REGEXP '%s' and Date between '2017-%s' and '2017-%s') as activity
    join
    (Select *
    From ShowroomMain Where Name REGEXP '%s' and City REGEXP '%s') as showroom
    on activity.ShowroomID = showroom.ID
    order by Date
    """
             % (event, begin_date, end_date, showroom, city))
    return query


def reservationListQuery(email):
    query = (
                """Select
                Date,
                Name,
                Type,
                reservations.TicketAmount,
                reservations.ID
            FROM
                (SELECT NumberOfPeople as TicketAmount,
                Email,
                ActivityID,
                ID
                FROM TicketDb.Reservations
                WHERE Email = '%s') as reservations
                join
                (select * From TicketDb.Activity) as activity
                on reservations.ActivityID = activity.ID"""
            ) % email
    return query


def makeReservation(howManyReservations, email, eventID):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO TicketDb.Reservations (NumberOfPeople,Email,ActivityID) values " +
            "('%s','%s','%s');" % (howManyReservations, email, eventID))
        cursor.execute(
            "UPDATE TicketDb.Activity SET TicketsLeft = TicketsLeft - %s WHERE ID = %s "
            % (howManyReservations, eventID))
        cursor.close()


def deleteReservation(resID, ticketPurchased, eventID):
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM TicketDb.Reservations WHERE ID = %s; "
            % resID)
        cursor.execute(
            "UPDATE TicketDb.Activity SET TicketsLeft = TicketsLeft + %s WHERE ID = %s "
            % (ticketPurchased, eventID))
        cursor.close()
    pass


def deletePartialReservation(resID, deletedTickets, eventID):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE TicketDb.Reservations SET NumberOfPeople = NumberOfPeople - %s WHERE ID = %s "
            % (deletedTickets, resID))
        cursor.execute(
            "UPDATE TicketDb.Activity SET TicketsLeft = TicketsLeft + %s WHERE ID = %s "
            % (deletedTickets, eventID))
        cursor.close()
        print("UPDATE TicketDb.Reservations SET NumberOfPeople = NumberOfPeople - %s WHERE ID = %s "
              % (deletedTickets, resID))
        print("UPDATE TicketDb.Activity SET TicketsLeft = TicketsLeft + %s WHERE ID = %s "
              % (deletedTickets, eventID))
    pass
