from pydantic import BaseModel

class Conci(BaseModel):
    def hello_world(self):
        print("Hello, World!")

conci = Conci()
conci.hello_world()