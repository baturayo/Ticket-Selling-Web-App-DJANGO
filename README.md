# Ticket Selling Web App in DJANGO
## Online Activity Ticket Manager
Each user first register to the system by a unique username. <br />
• Users will login to the system with their own password in order to use the system.<br />
• There will be several activities such as theatre, cinema, concert and so on.<br />
• The registered user can search the activities according to different search criteria.<br />
o Activities between two given days (e.g., see activities between 10.08.2009 and 20.08.2009)<br />
o Activities according to their type (e.g., cinema, theatre)<br />
o Activities according to their city (e.g., activities in Istanbul)<br />
o Activities according to their showroom (e.g., Cemil Topuzlu AcikhavaSahnesi) o And combinations of these above search<br /> conditions (e.g. search for a particular<br />
activity in a given city, which holds in specified dates)<br />
• Note that the user can select these conditions together, or separately. For instance, the<br />
user can specify the date and activity type or she can specify date, activity type and<br />
city. There may be a number of combinations.<br />
• The user can make reservation to a specific activity by specifying the number of<br />
tickets to be issued.<br />
• The user can update his/her reservation by only changing the number of tickets to be<br />
issued.<br />
• The user can cancel his reservation (s).<br />
• The user can list or view his all reservation information.<br />

## Detailed Report About Database Design

Firstly, we recognized a need of complex database to create a setting to run online activity ticket manager. There will be many entities and complex relationships between them to run this system smoothly.
<br />
Before determining entities and their relations, we wanted to fully understand the needs of our implementation. Most basic functionality for a user is being able to sign up to the system using a unique email address. That’s why the first entity we identified was the User entity. Also, our design must include Activity entity which includes the possible activities that a user may make reservation. Using these relations each user will be able to make reservations, cancel reservations and view reservations. Additionally, there will be several activity types for an activity such as cinema, theater, concert and sports. So, we need an Activity Type entity to restrict the types of the Activities. Since each activity occurs in a specific place, we need a Showroom entity to restrict possible places for an activity with the ones in our database. Also, cities of the showrooms are also known. We created City entity to restrict showrooms to be in cities which in our database. Finally, we concluded that we need an entity consist of Reservations which can be only made by registered users in our system to specific activity registered in the system. 
<br />
The properties of User entity are email, password, name and surname that have domains varchar(20), varchar(20), varchar(20), varchar(20) respectively which all are not null. Furthermore the properties of Activity entity are ID, Name, Type, Showroom ID, Date and Number of Tickets left that have domains numeric(5,0), varchar(20), varchar(20), numeric(5,0), date, numeric(5,0) respectively which all are not null. Similarly, the properties of Reservations entity consists of ID, User, Activity ID and Number of People that reservation made for that all have domains numeric(5,0), varchar(20), numeric(5,0), numeric(2,0) respectively which all are not null. Moreover, the properties of Showrooms entity are ID, Name, City and Capacity that have domains numeric(5,0), varchar(20), varchar(20), numeric(5,0) respectively which all are not null. The last 2 entity in our proposed model are Activity Types and Cities which have properties Type and City respectively that both have domain varchar(20) and are not null. Note that underlined properties are the ones which are primary keys in their corresponding entities. 
<br />

<br />



###Violation of the 2 NF:<br />

Functional dependency on Showroom table when initially constructed would be: <br />
Showroom (ID, City, Name, Capacity) with dependencies: <br />

ID -> City, Name, Capacity <br />
City, Name -> ID Capacity <br />

Here exists a partial dependency on the primary key which is violating the 2NF relation, as well as the 3NF. Table can be converted to 2NF by dividing this table into 2 sub tables with functional dependencies given as follows: 
<br />
First: ShowroomMain (ID, name, capacity)<br />
ID -> name, capacity <br />
name, capacity -> ID <br />
<br />
Second: ShowroomCapacity (Name, City, Capacity)<br />
Name,City -> Capacity <br />
<br />
With the new set-up the table would be in both 2NF form. E-R diagram showing the relations and properties is shown below. 
As it can be seen from E-R diagram, our base relations are Showrooms, Activity, User, Types, Cities and Reservations.
<br />
Functional Dependency diagrams are as follows: <br />

User (email, password, name, surname)<br />
email -> password name surname<br />

Reservations (ID, email, ActivityID, # of people) <br />
ID -> email, activityID, # of people<br />

ShowroomMain (ID, Name, Surname)<br />
ID -> Name, Surname <br />
Name Surname -> ID <br />

Activity (ID, name, date, ticketleft, price, type, ReservationID )<br />
ID -> name, date, ticketleft, price, type, ReservationID<br />

As there is no repeating data, partial dependecy and transivity in the database, it is in 3 Normal Form. <br />

In our database model we designed our foreign key(s) is City from table Cities for ShowroomMain, City from table Cities for ShowroomCapacity, Type and ID from tables Types and ShowroomMain respectively for Activity, Email and ID from tables User and Activity respectively for Reservations.
<br />
Deletion Integrity Rules: Before we delete a tuple from User table, we have to make sure that there are no current tuples in Reservations table with that User Email. Otherwise, we may face some users in Reservations table that does not exist in our system. Similarly, before deleting a tuple from Activity table we have to make sure that this activity does not exist in Reservations. Before deleting a tuple from Types, we have to ensure that tuple does not exist in Activity table. Before deleting a tuple from Showroom, we have to make sure that Showroom does not currently in use by an Activity. Additionally, we have to delete the Showroom from both ShowroomMain and ShowroomCapacity tables to provide consistency in our database system. Before deleting a tuple from Cities we have to make sure that city is not currently in use by our Showroom tables. 
<br />
Users Views: We identified two user views for our implementation. First of them is for searching activities. When a user search an activity, instead of seeing Activity table, user will see Name, Date, TicketLeft, Price and Type from Activity table and City, Name  of the Showroom. Similarly, if user wants to see his/her reservations, instead of seeing the whole Reservations table, he/she will see Name, Date, Price attirbutes from Activity table, City and Name from ShowroomMain table, NumberOfPeople from Reservations table. 
<br />
###Data Definition Language Statements:<br />

For creating our database we run the following SQL statement on MySQL.<br />

CREATE TABLE User<br />
(<br />
  Email VARCHAR(20) NOT NULL,<br />
  Password VARCHAR(20) NOT NULL,<br />
  Name VARCHAR(20) NOT NULL,<br />
  Surname VARCHAR(20) NOT NULL,<br />
  PRIMARY KEY (Email)<br />
);<br />
<br />
CREATE TABLE Types<br />
(<br />
  Type VARCHAR(20) NOT NULL,<br />
  PRIMARY KEY (Type)<br />
);<br />
<br />
CREATE TABLE Cities<br />
(<br />
  City VARCHAR(20) NOT NULL,<br />
  PRIMARY KEY (City)<br />
);<br />
<br />
CREATE TABLE ShowroomMain<br />
(<br />
  ID NUMERIC(5, 2) NOT NULL,<br />
  Name VARCHAR(20) NOT NULL,<br />
  City VARCHAR(20) NOT NULL,<br />
  PRIMARY KEY (ID),<br />
  FOREIGN KEY (City) REFERENCES Cities(City)<br />
);<br />
<br />
CREATE TABLE ShowroomCapacity<br />
(<br />
  Name VARCHAR(20) NOT NULL,<br />
  Capacity NUMERIC(5, 2) NOT NULL,<br />
  City VARCHAR(20) NOT NULL,<br />
  PRIMARY KEY (Name, City),<br />
  FOREIGN KEY (City) REFERENCES Cities(City)<br />
);<br />
<br />
CREATE TABLE Activity<br />
(<br />
  ID NUMERIC(5, 2) NOT NULL,<br />
  Name VARCHAR(20) NOT NULL,<br />
  Date DATE NOT NULL,<br />
  TicketsLeft NUMERIC(5, 2) NOT NULL,<br />
  Type VARCHAR(20) NOT NULL,<br />
  ID NUMERIC(5, 2) NOT NULL,<br />
  PRIMARY KEY (ID),<br />
  FOREIGN KEY (Type) REFERENCES Types(Type),<br />
  FOREIGN KEY (ID) REFERENCES ShowroomMain(ID)<br />
);<br />
<br />
CREATE TABLE Reservations<br />
(<br />
  ID NUMERIC(5, 2) NOT NULL,<br />
  NumberOfPeople NUMERIC(2, 0) NOT NULL,<br />
  Email VARCHAR(20) NOT NULL,<br />
  ID NUMERIC(5, 2) NOT NULL,<br />
  FOREIGN KEY (Email) REFERENCES User(Email),<br />
  FOREIGN KEY (ID) REFERENCES Activity(ID)<br />
);<br />
For the two views that we described previously, we generated two DDL statements as follows: <br />
CREATE VIEW rezs AS <br />
(SELECT Name, Date, Price, SName, City, NumberOfPeople <br />
FROM ((ACTIVITY NATURAL JOIN SHOWROOM) <br />
NATURAL JOIN RESERVATIONS));<br />
<br />
CREATE VIEW search AS <br />
(SELECT Name, Date, TicketLeft, SName, City, Capacity <br />
FROM (ACTIVITY NATURAL JOIN SHOWROOM));<br />
<br />


###Data Manipulation Language Diagrams:
<br />
Django, web framework written in Python, is used to connect MySQL Database and Web Page. Below, two DML examples are given from our implementation to register a user and to check whether they enter the correct user email and password.
<br />
 def insertUser(email, name, surname, password):<br />
   with connection.cursor() as cursor:<br />
       cursor.execute( <br />
           "INSERT INTO TicketDb.user values (%s,%s,%s,%s)" % ( <br />
               "'{}'".format(email), "'{}'".format(name), "'{}'".format(surname), "'{}'".format(password)))<br />
<br />
def loginCheck(email, password):<br />
   cursor = connection.cursor()<br />
   query = ("Select email, Password from TicketDb.user where email= %s and Password = %s" % (<br />
       "'{}'".format(email), "'{}'".format(password)))<br />
   cursor.execute(query)<br />
<br />
   for (email, password) in cursor:<br />
       if email != "" and password != "":<br />
           return True<br />
       else:<br />
           return False<br />
   cursor.close()<br />
<br />
Below there are 2 other DML commands for viewing reservations of a given user and for doing a search among the activities. 
<br />
SELECT * FROM rezs;<br />
SELECT * FROM search;<br />
<br />
Currently in our design for the implementation we are not planning to implement User account, Showroom, Activity, City, Type deletion system. That is why we did not write deletion statements for these tables. However, to make user be able to cancel a reservation, we have to write a delete command which is:
<br />
DELETE FROM RESERVATION WHERE <br />
EMAIL = ‘User Email’ AND <br />
ACTIVITYID = ‘Activity ID of the Activity that desired to be canceled’<br />
<br />
Each time new tickets is bought from a user we need to update TicketsLeft at our Activity table. Also, we need to update Reservations when a user increases or decreases the number of tickets bought.
<br />
UPDATE Activity  <br />
SET ticketleft = ticketleft - x   (x is the number of tickets bought)<br />
WHERE ActivityID = ‘the ID of the activity which will be updated’<br />

<br />
UPDATE RESERVATION<br />
SET NumberOfPeople = NumberOfPeople + x (where x is the input from user)<br />
WHERE ActivityID = ‘the ID of the activity which will be updated’ AND<br />
Email = ‘Email address of the user logged in’<br />
<br />
Note that, when an update in Reservations table happens, we also need to update the Acitivty table because the amount of people joining to an activity is directly connected with number of tickets left. TicketsLeft in the Activity table will increase by x if NumberOfPeople in Reservations table decrease by x. Similarly, if TicketsLeft decrease by x, NumberOfPeople will increase by x.
<br />
