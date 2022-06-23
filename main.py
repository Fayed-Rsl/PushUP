# from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database

from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker


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
    def loginBtn(self):
        global user_id
        if db.check_account( (self.email.text, self.password.text)) == 1:
            SetupGoalWindow.current = self.email.text
            user_id = db.get_user_id( (self.email.text,) )
            self.reset()

            # check if the user already have a goal, if yes skip this page
            if db.check_user_goal( (user_id,)) == 1:
                sm.current = "login"
            
            else:
                sm.current = "setupgoal"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class SetupGoalWindow(Screen):
    '''Window to enter a goal and the time to achieve the goal'''
    push_up = ObjectProperty(None)
    push_up_time = ObjectProperty(None)
    pull_up = ObjectProperty(None)
    pull_up_time = ObjectProperty(None)
    abdo = ObjectProperty(None)
    abdo_time = ObjectProperty(None)
    squat = ObjectProperty(None)
    squat_time = ObjectProperty(None)

    def logOut(self):
        sm.current = "login"
    
    def goalBtn(self):
        if (self.push_up.text != '' and self.push_up_time.text != '' and
        self.pull_up.text != '' and self.pull_up_time.text != '' and
        self.abdo.text != '' and self.abdo_time.text != '' and
        self.squat.text != '' and self.squat_time.text != ''):

            goal_value = (user_id, self.push_up.text, self.push_up_time.text,
            self.pull_up.text, self.pull_up_time.text, self.abdo.text, self.abdo_time.text,
            self.squat.text, self.squat_time.text)
            db.insert_goal(goal_value)
            self.reset()
            # sm.current = "" # next page 
 
	# Click OK
    def on_save_push_up(self, instance, value, date_range):
        self.push_up_time.text = str(value)

    def on_save_pull_up(self, instance, value, date_range):
        self.pull_up_time.text = str(value)

    def on_save_abdo(self, instance, value, date_range):
        self.abdo_time.text = str(value)

    def on_save_squat(self, instance, value, date_range):
        self.squat_time.text = str(value)


    # Click Cancel
    def on_cancel_push_up(self, instance, value):
        self.push_up_time.text = "Goal End"

    def on_cancel_pull_up(self, instance, value):
        self.pull_up_time.text = "Goal End"

    def on_cancel_abdo(self, instance, value):
        self.abdo_time.text = "Goal End"

    def on_cancel_squat(self, instance, value):
        self.squat_time.text = "Goal End"

    def show_date_push_up(self):
        date_dialog = MDDatePicker(min_year=2022)
        date_dialog.bind(on_save=self.on_save_push_up, on_cancel=self.on_cancel_push_up)
        date_dialog.open()

    def show_date_pull_up(self):
        date_dialog = MDDatePicker(min_year=2022)
        date_dialog.bind(on_save=self.on_save_pull_up, on_cancel=self.on_cancel_pull_up)
        date_dialog.open()

    def show_date_abdo(self):
        date_dialog = MDDatePicker(min_year=2022)
        date_dialog.bind(on_save=self.on_save_abdo, on_cancel=self.on_cancel_abdo)
        date_dialog.open()

    def show_date_squat(self):
        date_dialog = MDDatePicker(min_year=2022)
        date_dialog.bind(on_save=self.on_save_squat, on_cancel=self.on_cancel_squat)
        date_dialog.open()


    def reset(self):
        self.push_up.text = ""

        # if db.check_primary_key( (user_id, today)) == 1:
        #     data = ('', '')
        #     db.update_data( (200, 340, 500, 140, user_id, today) )
        # else:
        #     data = ('', '')
        #     db.insert_data( (user_id, 300, 600, 800, 40, today) )
        #                 self.reset()


class InsertDataWindow(Screen):
    '''Window to insert data'''
    pass


class SeeDataWindow(Screen):
    '''Window to see our personal data and all users data'''
    pass


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
user_id = None

# db.drop_table('_User')
# db.drop_table('_UserData')
# db.drop_table('_UserGoal')
# db.create_user_table()
# db.create_userdata_table()
# db.create_user_goal()

# every screen on our application
screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),SetupGoalWindow(name="setupgoal")]
for screen in screens:
    sm.add_widget(screen) # add every screen in the screen manager

sm.current = "login" # the first page to show = login

class MyMainApp(MDApp):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
