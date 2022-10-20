import inject

"""@inject.autoparams returns a decorator which automatically
 injects arguments into a function that uses type annotations.
 This is supported only in Python >= 3.5."""

class Database:
    def save(self, item):
        print("SAVING:", item)

@inject.autoparams()
def reload_data(db:Database):
    print("Reloading...")
    assert isinstance(db, Database)

def write(user, db:Database):
    db.save(user)

reload_data()
writer = inject.autoparams()(write)
writer("Johnny")

@inject.params(db=Database)
def persist(user, db:Database):
    db.save(user)
persist("Ivan")
persister = inject.params(db=Database)(persist)
persister("Jill")

