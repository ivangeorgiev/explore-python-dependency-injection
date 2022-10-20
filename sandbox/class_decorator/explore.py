
def model_decorator(*args, **kwargs):
    def wrapper(cls):
        print(f"Wrapping {cls}")
        class Decorator(cls):
            def save(self):
                print("To save...")
                return super().save()
                
        return Decorator
    return wrapper

@model_decorator()
class Model:
    def save(self):
        print(f"SAVING {self}")

    def load(self, id):
        print(f"LOADING: {id}")

m = Model()
m.save()
m.load("Hi")
