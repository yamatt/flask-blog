from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app
from models.forms import Page
from decorators import is_admin

pages = Blueprint("pages", __name__)

@pages.route("/<path:name>")
def archive(name):
    posts = g.database.engine.get_page(name)
    return render_template("page.jinja.html", posts=posts)
	
@pages.route("/new", methods=["GET", "POST"])
@is_admin
def new():
    form = Page()
    if form.validate_on_submit():
        new_page = g.database.models.Page.from_form(form, session['user'])
        g.database.engine.add_page(new_page)
        flash("Saved.")
        return redirect(url_for(".edit", name=new_page.name))
    return render_template("forms.jinja.html", form=form)

@pages.route("/<path:name>/edit", methods=["GET", "POST"])
@is_admin
def edit(name):
	page = g.database.engine.get_page(name)
	form = Page(obj=page)
	if form.validate_on_submit():
		edited_page = g.database.models.Page.from_form(form, session['user'])
		g.database.engine.add_page(edited_page)
		flash("Saved.")
	return render_template("forms.jinja.html", form=form)

@pages.route("/<path:name>/delete", methods=["GET", "POST"])
@is_admin
def delete(identifier):
    pass
	
	

