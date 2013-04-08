from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app, abort
from models.forms import Page, Confirm
from decorators import is_admin

pages = Blueprint("pages", __name__)

@pages.route("/<path:name>")
def show(name):
    page = g.database.engine.get_page(name)
    if page and page.published:
        return render_template("page.jinja.html", page=page, page_name=page.title)
    abort(404)

@pages.route("/list")
@is_admin
def list():
    pages = g.database.engine.get_all_pages()
    return render_template("page_list.jinja.html", pages=pages, page_name="List of all pages.")
    
@pages.route("/new", methods=["GET", "POST"])
@is_admin
def new():
    form = Page()
    if form.validate_on_submit():
        new_page = g.database.models.Page.from_form(form, session['user'])
        g.database.engine.add_page(new_page)
        flash("Saved.")
        return redirect(url_for(".edit", name=new_page.name))
    return render_template("forms.jinja.html", form=form, page_name="Create new page")

@pages.route("/<path:name>/edit", methods=["GET", "POST"])
@is_admin
def edit(name):
    page = g.database.engine.get_page(name)
    if page:
        form = Page(obj=page)
        if form.validate_on_submit():
            edited_page = g.database.models.Page.from_form(form, session['user'])
            g.database.engine.add_page(edited_page)
            flash("Saved.")
        return render_template("forms.jinja.html", form=form, page_name="Editing page '{0}'".format(page.title))
    abort(404)

@pages.route("/<path:name>/delete", methods=["GET", "POST"])
@is_admin
def delete(name):
    form = Confirm()
    if form.validate_on_submit() and form.yes.data == True:
        g.database.engine.delete_page(name)
        flash("Page '{0}' has been deleted".format(name))
        return redirect(url_for(".new"))
    return render_template("forms.jinja.html", form=form)
    
    

