from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app
from blueprints import APITemplateView

blueprint = Blueprint("frontpage", __name__)

class FrontpageView(APITemplateView):
    def get_objects(self, *args, **kwargs):
        return g.database.engine.get_published_posts()
        
blueprint.add_url_rule('/', view_func=FrontpageView.as_view('frontpage', template_name='frontpage.jinja.html'))
