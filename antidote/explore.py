# `world`` id sthe default dependency catalog
from antidote import injectable, world

# By default @injectable creates a Singleton
@injectable
class Service:
    def hello(self):
        print("Hello World")

world[Service]
world[Service].hello()

########################
# -- Specifying the dependency
# always explicit - no guessing
from antidote import inject
from antidote import InjectMe

@inject
def f(service: Service = inject.me()):
    service.hello()


@inject
def f2(service = inject[Service]):
    # Type hints work
    service.hello()

@inject(kwargs=dict(service=Service))
def f3(service:Service):
    service.hello()

@inject
def f4(service: InjectMe[Service]):
    service.hello()


#########################################
# Overriding injection by passing argument
@inject
def of(service: InjectMe[Service]):
    return service

# by default injected service is used
original_service = world[Service]
new_service = Service()

assert new_service is not original_service, "We should have created different instance"
assert of() is original_service, "Injection injects service from `world`"
assert of(new_service) is new_service, "Passing argument overrides injection"

# Overriding injection by using context manager
with world.test.clone() as overrides:
    overrides[Service] = new_service
    assert world[Service] is new_service, "Overriding service is used by `world`"
    assert of() is new_service, "Injection uses overriding service"
assert world[Service] is original_service, "Outside context manager original service is used"

