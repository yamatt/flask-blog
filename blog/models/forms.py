from flask.ext.wtf import Form, TextField, TextAreaField, HiddenField, PasswordField, BooleanField, SubmitField, validators, FileField

class Form(Form):
    mimetype=""

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
    content = TextAreaField("Content", [validators.Required()], description="What you want to convey.")

class Page(Comment):
    name = TextField("Name", [validators.Required()], description="The path the page  will be accessable from.")
    title = TextField("Title", [validators.Required()], description="The heading of the page.")
    published = BooleanField("Publish?", default=False, description="Tick to make this post publically accessible.")
    
class Post(Comment):
    submit_name = "Save"
    id_val = HiddenField("id_val")
    title = TextField("Title", [validators.Required()], description="The heading of the blog post.")
    published = BooleanField("Publish?", default=False, description="Tick to make this post publically accessible.")

class Confirm(Form):
    yes = SubmitField("Yes")
    no = SubmitField("No")
    
class Upload(Form):
    submit_name = "Upload"
    mimetype="multipart/form-data"
    upload = FileField(u'File', description=u"The file you wish to upload.")
    filename = TextField(u"New filename:", description="If you wish to rename this file type it here otherwise leave it blank.")
    
