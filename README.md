Overview:
This project is for CMPT789. The program is about to avoid the password cracker, based on dictionary attack.
After the user enters a password, the program will match the password with each entry in the dictionary to check whether the password has been cracked. 

Environment delpoyment:
Download MongoDB Compass and Studio 3T
Create connection name: CMPT789-Project
Create 3 local collections:
Password-list1, hashedPassword-list1, userInfo
Import the given collections
Deploy the MongoDB environment:
pip install pymongo
brew services start mongodb
check MongoDB status:
brew services list

Admin username:RobbieQu
Admin password:301469193
Regular username: Catherine/Mohsen
Regular password: Cai/789789


Variables list:
1. client: local MongoDB url: mongodb://localhost:27017/
2. userInfo: MongoDB collection stores user credential
3. password_list: The password collection.
4. role: user's role (login as admin or user)
5. input_user_name: user input password used for credential
6. input_user_password: user input password used for creential
7. password: password retrieved from DB
8. input_password: password used input used for check the dictionary
9. hashed_password: hashed password by SHA256
10. choice: user input to determine working mode:
1, search: Perform MongoDB query to determine whether the password is already in the DB or not. This mode can be used by both admin and user.
2, add: Add new password into DB. This mode can only be used by admin. When login as user, this method will not display.
3，Check log: Only available for admin, it will display the activities log.
11. hashed_password_list: The hashed password collection.
12. event_log: The .txt file to store log event.

Logic design:
1. The program will ask to input:1. Existing user. 2. Exit.
If the input is 1, the program will ask the user input username(input_user_name) and password(input_password) at first, then the program will retrieve based on the information input in the MongoDB collection 'userInfo' and check the credential of users. If the input username and password is matching in the collection, then determine the user's role is admin or user based on the collection's element 'role'. If the inputted username or password is not exist, return error msg and ask whether to create a new user.

2. After verify the credential and the role is being determined:
1, If the role is admin, it can choose the mode from search and add. Input 1 for search, 2 for add or 3 to check log, 4 to exit program or 5 create new user. 
2, If the role is user, it can only input 1 for search or 2 to exit program.
In search mode, if the password is existing in password_list or it hashed password (hashed_password) is existing in the hashed_password_list, return password existing msg. If not existing, return password is not being used or safe. Then the plain password will be add into password_list and it hashed password will be add into hashed_password_list.
In add mode, the admin can add the password into password_list and it hashed password will be add into hashed_password_list directly.
In log mode, it will retrieve the log file to display all of the activities.
In create new user mode, create user with given username and password and set the role to 'user'.

Function design:
1. check_user_credential: This function will be used to check user's input username and password from MongoDB collection userInfo. The field name in the object is 'Password' and 'Username'. If the input and field is matching, then pass the credential, and the role is be determined by the field 'Role'. If the input and field is not matching, the return error.
2. create_user: This function will be used to create new user. It will asked for input the username and password, then it will create new Object in userInfo will the username and password, and the role will be set to 'user'.
3. search_password: This function will be used to search the password in the password collections(password_list and hashed_password_list). This function need to perform MongoDB query to search for specific password.
4. add_password: This function can only be used my admin user. It will add the password into the password collections in plaintext or sha256, plaintext will be add into collection password_list, hashed_password will be add into collection hashed_password_list. This will need to perform MongoDB query to create new object in the specific collection.
5. convert_to_hash: This function is used to convert plain password to sha256.
6. log_event: This function will be used to record the activities into, it will record: time, who, event and result.
7. follow_log_file: This function will be used to output the log at real time.
