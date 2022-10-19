import pinject

class MyApp:
    def __init__(self, db_service: 'DbService'):
        self.db = db_service


class DbService:
    ...

obj_graph = pinject.new_object_graph(classes=[MyApp])
app = obj_graph.provide(MyApp)
assert isinstance(app.db, DbService)

# ======= Binding Spec ===============

class DatabaseService:
    ...

class MyBindingSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind('db_service', to_class=DatabaseService)

obj_graph = pinject.new_object_graph(binding_specs=[MyBindingSpec()])
app:MyApp = obj_graph.provide(MyApp)
assert isinstance(app.db, DatabaseService)

# -- can bind to an instance
class MyBindingSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind('db_service', to_instance="I am database")

obj_graph = pinject.new_object_graph(binding_specs=[MyBindingSpec()])
app:MyApp = obj_graph.provide(MyApp)
assert app.db == "I am database"

app1 = obj_graph.provide(MyApp)
assert app1 is not app, "Provide creates new instance"


#################### Provider Methods

class BindingSpecWithProvider(pinject.BindingSpec):
    def provide_db_service(self, db_name, wow='-'):
        """Methods previxed by `provide_` are provider methods
        
        When provider method is called arguments are injected.

        `wow` argument cannot be injected as there is no binding for it,
        As it has default value defined, the default is used.
        """
        return f"here is your database ({wow}): {db_name}"

    def provide_db_name(self):
        return "mydb"

obj_graph = pinject.new_object_graph(binding_specs=[BindingSpecWithProvider()])
app:MyApp = obj_graph.provide(MyApp)
assert app.db == "here is your database (-): mydb", "The return value from provider method is used"


class InjectedClass:
    ...

class MyApp:
    def __init__(self, injected_class: InjectedClass):
        self.injected_class = injected_class

obj_graph = pinject.new_object_graph()
app1 = obj_graph.provide(MyApp)
app2 = obj_graph.provide(MyApp)
assert app1.injected_class is app2.injected_class, "By default injected dependency are cached (singleton)"