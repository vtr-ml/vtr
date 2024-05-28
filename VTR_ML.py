import streamlit as st
import streamlit_authenticator as stauth
import streamlit as st 
import mysql.connector
import mysql
from firebase_admin import credentials
from firebase_admin import auth
from streamlit_option_menu import option_menu
from PIL import Image



st.set_page_config(page_title="My Streamlit App", page_icon="🌟", layout="wide", initial_sidebar_state="expanded")


    



import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Password@123",
  database="new_db"
)
mycursor = mydb.cursor()

def create_usertable():
	mycursor.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password VARCHAR 20)')
    


def add_userdata(new_user,new_password):
	mycursor.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(new_user,new_password))
	mydb.commit()

def login_user(new_user,new_password):
	mycursor.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(new_user,new_password))
	data = mycursor.fetchall()
	return data


def view_all_users():
	mycursor.execute('SELECT * FROM userstable')
	data = mycursor.fetchall()
	return data
mydb.commit()


def main():
    menu = ['Home', "Login", "Signup", "About VTR"]
    choice = st.sidebar.selectbox(":violet[**VTR Main Menu**]", menu)

    if choice == "Home":
        st.title(":violet[**VTR Machine Learning**]")

    elif choice =="Login":
        st.subheader("Login")

        username = st.text_input("User Name")
        password = st.text_input("Password", type = 'password')
        if st.button("Login"):
            if password =='12345':
                st.success("Welcome {}".format(username))

                task = st.selectbox ("Task",["Add Post", "Analysis","Profiles"])
                if task == "Add Post":
                    st.subheader("Add Your Post")

                elif task == "Analysis":
                    st.subheader("Analysis")
                elif task =="Profiles":
                    st.subheader("User Profiles")
            else:
                st.warning("Incorrect User Name or Password")
            
                                         

            


    #elif choice == "SignUp":
       # st.subheader("Create New Account")
        #new_user = st.text_input("Username")
        #new_password = st.text_input("Password",type='password')
        #retype_password = st.text_input("Re-Enter Password",type='password')
        #if st.button("Signup"):
        #    if new_password == retype_password:
          #      create_usertable()
         #       add_userdata(new_user,make_hashes(new_password))
         #       st.success("You have successfully created a valid Account")
         #       st.info("Go to Login Menu to login")
        #    else:
       #          st.warning ("Password mismatch, please re-enter the correct password")
                 
            

if __name__== '__main__':
    main()



