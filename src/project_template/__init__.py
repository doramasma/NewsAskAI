#TODO: Update to the project name
from project_template.services.hello_world_service import HelloWorldService

def main() -> None:
    print("Hello world!!!")
    service = HelloWorldService()
    print(service.say_hello())