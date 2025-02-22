"""
zenith base module.

This is the principal module of the zenith project.
Here you put your main classes and objects.

Be creative! Do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""

# example constant variable
NAME = "zenith"


def get_greeting(name: str = "World") -> str:
    """
    Returns a greeting message.

    :param name: Name to greet.
    :return: Greeting message.
    """
    return f"Hello, {name}!"
