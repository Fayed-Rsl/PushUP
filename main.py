from sqlite3 import DatabaseError
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database


class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    email = ObjectProperty(None)
    user_id = None

    def submit(self):
        global user_id
        '''function to create an account'''
        if (self.username.text != '' and self.email.text != '' and
            self.email.text.count('@') == 1 and self.email.text.count('.') > 0):
            if self.password != '':
                user = (self.username.text, self.password.text, self.email.text, today)
                user_id = db.insert_user( user )

                self.reset()
                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.username.text = ""
        self.password.text = ""
        self.email.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    user_id = None
    def loginBtn(self):
        global user_id
        if db.check_account( (self.email.text, self.password.text)) == 1:
            MainWindow.current = self.email.text
            user_id = db.get_user_id( (self.email.text,) )
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    '''Main menu window to:
    enter goal - select type of sport'''
    goal = ObjectProperty(None)

    # add des widget pr chaque type d'action

    def logOut(self):
        sm.current = "login"
    
    def goalBtn(self):
        if self.goal.text != '':
            print(self.goal.text, type(self.goal.text))
            db.insert_goal( (user_id, self.goal.text,) )
            self.reset()
            # sm.current = "" # next page 
    
    def reset(self):
        self.goal.text = ""

    # def on_enter(self, *args):
    #     pass
        # if db.check_primary_key( (user_id, today)) == 1:
        #     data = ('', '')
        #     db.update_data( (200, 340, 500, 140, user_id, today) )
        # else:
        #     data = ('', '')
        #     db.insert_data( (user_id, 300, 600, 800, 40, today) )
        #                 self.reset()

class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv") # load the kv file

sm = WindowManager() # screen manager 
db = Database ('database.db') # sql lite database
today = db.get_date()
# db.drop_table('_User')
# db.drop_table('_UserData')
db.drop_table('_UserGoal')
# db.create_user_table()
# db.create_userdata_table()
db.create_user_goal()

# every screen on our application
screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen) # add every screen in the screen manager

sm.current = "login" # the first page to show = login

class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
