from flask.ext.wtf import Form, TextField, TextAreaField BooleanField, validators

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

class Item(Form):
    content = TextAreaField("Content", [validators.Required()])

class Post(Item):
    submit_name = "Save"
    title = TextField("Content", [validators.Required()])
    published = BooleanField("Publish?", default=False)
    
class Comment(Item):
    submit_name = "Submit"
    pass
