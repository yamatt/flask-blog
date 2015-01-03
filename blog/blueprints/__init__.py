from flask.views import View

def loader(app):
    for blueprint in app.config['blueprints']:
        blueprint_module = __import__("blueprints.{blueprint}.blueprint.blueprint".format(blueprint=blueprint['name']))
        app.register_blueprint(blueprint_module, url_prefix=blueprint['root'])

class ObjectMixin(View):
    def get_objects(self, *args, **kwargs):
        raise NotImplementedError()

class TemplateView(View, ObjectMixin):
    def __init__(self, template_name):
        self.template_name = template_name
        
    def dispatch_request(self):
        return render_template(self.template_name, objects=self.get_objects())

class APIView(View, ObjectMixin):
    def dispatch_request(self):
        return self.get_objects()
        
class APITemplateView(TemplateView, APIView):
    def dispatch_request(self):
        if request.is_xhr:
            return super(APIView, self).dispatch_request()
        return super(TemplateView, self).dispatch_request()
    
        

