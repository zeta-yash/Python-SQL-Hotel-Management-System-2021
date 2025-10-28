from logging import exception
from random import choice
import mysql.connector

print("Please Fill the following details.. TO CONNECT YOUR SQL DATABASE")
hst=input("Host Name:")
usr=input("Enter User:")
pssw=input("Password:")


cn = mysql.connector.connect(
  host=hst, #"localhost"
  user=usr, #"root"
  password=pssw #"root"
)

cur=cn.cursor()

cur.execute("DROP DATABASE if exists HOTEL")
cur.execute("CREATE DATABASE if not exists HOTEL")
cur.execute("USE HOTEL")
#                                                         HH    HH     ======  IIIIII  HHIIIII   HH
#                                                         HHEEEEHH   //     \\   HH    HH===     HH
#                                                         HH    HH    \\____//   HH    HHIIIII   HHIIIII


#EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE((((.........EMPLOYEE.........))))EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
cur.execute("CREATE TABLE  if not exists EmpDet(eID int (3) NOT NULL ,\
             eName varchar (16),\
             eContact varchar(12),\
             eGender varchar (10),\
             eCity varchar (15),\
             eSalary int (4),\
             Password varchar (16),\
             PRIMARY KEY(eID))")

cur.execute("INSERT INTO EmpDet VALUES (100, 'Tony',9695626581, 'Male', 'NewYork', 36000, 1),\
              ('101', 'Steve', '6586321456', 'Male', 'Sydney', '60000', '1'),\
              ('102', 'Wanda', '3625149658', 'Female', 'Sukovia', '35000', '1'),\
              ('103', 'Gamora', '8565231464', 'Female', 'Titan', '30000', '1'),\
              ('104', 'Bruce', '9575632145', 'Male', 'Kokata', '54000', '1')")
#EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE(((((......ROOMS......)))))EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
cur.execute("CREATE TABLE  if not exists Rooms(RoomNo int (3) NOT NULL ,\
             cID int (3) DEFAULT NULL)\
             ")
cur.execute("INSERT INTO Rooms VALUES (101,103),(102,101),(103,104),(104,100),(107,102)")  
cur.execute("INSERT INTO Rooms(RoomNo) VALUES (105),(106),(108),(109),(110)") 

#EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE(((((......CUSTOMER......)))))EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
cur.execute("CREATE TABLE Customer (cID int(3), cName varchar(15), cCity varchar(15), cContact varchar(11))")
cur.execute("INSERT INTO Customer VALUES (100,'Ajay', 'Delhi', 9214569872),(101, 'Kritika', 'Mumbai', 9575632144),\
                                          (102,'Harpreet', 'Delhi', 6585724163),(103, 'Afzal', 'Gurugram', 9565475223),\
                                          (104, 'Arvind', 'Mumbai', 9565854752)")
                                          
#EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE(((((......MENU......)))))EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
cur.execute("CREATE TABLE  if not exists Menu (Code int PRIMARY KEY, Food_Item varchar(17), Price int)")
cur.execute("INSERT INTO Menu VALUES (101, 'SPECIAL THALI', 1500),\
              (102, 'PizzaCombo',1300),\
              (103, 'Ice-Cream', 100),\
              (104, 'Pop Corn', 70),\
              (105, 'Pav Bhaji', 120),\
              (106, 'ColdCoffee', 40),\
              (107, 'Tea & Rusk', 25),\
              (108, 'SunnySideUp', 80),\
              (109, 'Omelette', 120),\
              (110, 'Shampeign', 600)")

cn.commit()
#                                                             //IIII    //HHH\\   ||HH\\     HHEEEE
#                                                            ||        ||     ||  ||    ||   HH==
#                                                             \\IIII    \\HHH//   ||III//    HHEEEE
#===========================================
def SaveChng(): #SAVE CHANGES
  opt=int(input("Press 1 to save changes, 2 to discard:"))
  if opt==1:
    cn.commit()
    print("Changes made successfully.")
  if opt==2:
    cn.rollback()
    print("Changes aborted.")

def showEmp():
  cur.execute("select eID,eName,eContact,eGender,eCity, eSalary FROM EmpDet")
  details=cur.fetchall()
  for i in details:
    print(i)

def AddEmp():
  Add=0
  success=0
  while success!=1 :
    cur.execute("SELECT MAX(eID) FROM EmpDet")
    maxid=cur.fetchall()[0][0]
    newID=int(maxid)+1
    eN=input("Enter Name:")
    eCont=input("Enter Contact:")
    eGen=input("Enter Gender:")
    eCt=input("Enter City:")
    eSal=input("Set Salary:")
    ePass=input("Enter New Password:")
    try:
      cur.execute("INSERT INTO EmpDet VALUES( %s,%s,%s,%s,%s,%s,%s)",(newID,eN,eCont,eGen,eCt,eSal,ePass))
      cn.commit()
      Add=int(input("Enter 1 to Add More and 0 to Exit:"))
      if Add==1:
        success=0
      if Add==0:
        success=1  
      print("{} has been added as Employee.\
              ID: {}  Password:{}".format(eN,newID,ePass))   

    except Exception as e:
      cn.rollback()
      print("An Error Occured..")
      opt=input("Still want to Add? [Y]/[N]:")
      if opt in "Yy1":
        success=0
      else:
        print("You opted for no!!")
        success=1

def RemoveEmp():
  EmpID=100
  cur.execute("SELECT eName FROM EmpDet WHERE eID=%s",(EmpID,))
  delname=cur.fetchall()[0][0]
  cur.execute("DELETE FROM EmpDet WHERE eID= %s",(EmpID,))
  print("{} has been removed successfully.".format(delname))
  showEmp()
  SaveChng()

def ChangePass():
  EmpID=100
  cur.execute("SELECT eName,Password FROM EmpDet WHERE eID=%s",(EmpID,))
  nm_ps=cur.fetchall()
  name=nm_ps[0][0]
  oldpass=nm_ps[0][1]
  print("Hello",name)
  get_oldpass=input("Enter Old Password:")
  if get_oldpass==oldpass:
    newpass=input("Enter new password:")
    cur.execute("UPDATE EmpDet SET Password=%s WHERE eID= %s",(newpass,EmpID))
    print("Password for {} has been changed to {} successfully.".format(name,newpass))
    SaveChng()

  else:
    print("Wrong Password.")
    opt=int(input("Still want to change the password[1:Yes   2:Exit]:"))
    if opt==1:
      ChangePass()
    else:
      pass

def roomleft():
  cur.execute("SELECT COUNT(RoomNo) FROM Rooms WHERE cID=NULL")
  a=cur.fetchall()
  print("There are {} available.".format(a))

def ViewCus():
  print("ID    Customer Name    City    Contact    Room No.")
  print("=================================================================")
  cur.execute("SELECT Customer.cID, Customer.cName, Customer.cCity,\
              Customer.cContact, Rooms.RoomNo FROM Customer,Rooms \
              WHERE Rooms.cID=Customer.cID ORDER BY cID")
  data=cur.fetchall()
  for i in data:
    print(i)

def UpdateCus():
  cid=int(input("Enter Customer ID:"))
  cur.execute("SELECT cName FROM Customer WHERE cID=%s",(cid,))
  name=cur.fetchall()
  print("What do you want to Update, for Customer {} ".format(name[0][0]))
  print("1. Name \n 2.City \n 3.Contact No.")
  a=int(input("Enter your choice:"))
  if a==1:
    new_n=input("Enter New Name:")
    cur.execute("UPDATE Customer SET cName=%s WHERE cID=%s",(new_n,cid))
  if a==2:
    new_c=input("Enter New City:")
    cur.execute("UPDATE Customer SET cCity=%s WHERE cID=%s",(new_c,cid))
  if a==3:
    cont=input("Enter New Contact:")
    cur.execute("UPDATE Customer SET cContact=%s WHERE cID=%s",(cont,cid))
  else:
    print("Give Correct Input.")
    UpdateCus()
  SaveChng()

def menu():
  print("FoodCode \t Food & Bevrages \t\t Price")
  print("=======================================================")
  cur.execute("SELECT Code,Food_Item,Price FROM Menu")
  menu=cur.fetchall()
  for i in menu:
    print(i[0],"\t\t",i[1],"\t\t\t",i[2] )

def UpdateFood():
  menu()
  fdcd=int(input("Enter Food Code:"))
  cur.execute("SELECT Code FROM Menu")
  cdlist=cur.fetchall()
  print(cdlist)
  for i in cdlist:
    if fdcd in i:
      break
    else:
      print("Code Not Matched..")
      UpdateFood()
  print("What do you want to change?? \n 1.Food Name \n 2. Price")
  a=int(input("Enter Your Choice:"))
  if a==1:
    fd=input("New Food Name:")
    cur.execute("UPDATE Menu SET Food_Item = %s WHERE Code= %s",(fd,fdcd))
    print("Success!!")
  if a==2:
    prc=int(input("Enter New Price:"))
    cur.execute("UPDATE Menu SET Price=%s WHERE Code= %s",(prc,fdcd))
    print("")
  SaveChng()
  print("")
  menu()
  print("")

def login():
  global curr_user
  user=int(input("UserID:"))
  pwd=input("Password:")
  cur.execute("SELECT eName,Password FROM EmpDet WHERE eID=%s AND Password=%s",(user,pwd))
  result=cur.fetchall()
  if bool(result)==False:
    print("")
    print("Wrong ID or Password")
    print("")
    login()
  else:
    print("Hello",result[0][0])
    curr_user=result[0][0]

    
#########################################################################################
#########################################################################################
while True:

  print("Welcome to the Hotel Mangement System.")

  login()

  print("Select from following options")

  mng_emp=100


  while mng_emp!=5:
    print("1. Manage Employees \n 2. Rooms Left \n 3.Customer Details \n 4. Update Menu \n 5. Exit")
    mng_emp=int(input("Your Choice:"))


    if mng_emp==1:
      print("1. Show All Employees \n 2. Add Employee \n 3. Remove employee \n 4. Password Change \n 5. Exit")
      a=int(input("Your Choice:"))
      if a==1:
        showEmp()
      if a==2:
        AddEmp()
      if a==3:
        RemoveEmp()
      if a==4:
        ChangePass()
      if a==5:
        pass
      else:
        print("Wrong Option.")


    if mng_emp==2:
      roomleft()


    if mng_emp==3:
      print("1. Veiw All Customer's Details \n 2.Update Details \n 5. Exit")
      c_op=int(input("Your Choice:"))
      if c_op==1:
        ViewCus()
      if c_op==2:
        UpdateCus()
      if c_op ==5:
        pass
      else:
        print("Wrong Option.")

        
    if mng_emp==4:
      UpdateFood()

    if mng_emp==5:
      print(curr_user,"you are exiting..")
      pass
