from flask.ext.wtf import Form, TextField, TextAreaField, HiddenField, PasswordField, BooleanField, validators

class User(Form):
    username = TextField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.Required()])
    
class Login(User):
    submit_name = "Login"
    remember = BooleanField("Remember me", default=False)

class Register(User):
    submit_name = "Register"
    email = TextField('Email Address', [validators.Required()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
class Post(Form):
    submit_name = "Save"
    id_val = HiddenField("id_val")
    title = TextField("Title", [validators.Required()])
    content = TextAreaField("Content", [validators.Required()])
    published = BooleanField("Publish?", default=False)
    
class Comment(Form):
    submit_name = "Submit"
    content = TextAreaField("Content", [validators.Required()])
