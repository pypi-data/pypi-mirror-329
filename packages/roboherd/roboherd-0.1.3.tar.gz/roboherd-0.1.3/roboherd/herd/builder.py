from roboherd.cow import RoboCow
from roboherd.examples.moocow import moocow  # noqa


def create_actor_message_for_cow(cow: RoboCow, base_url):
    """
    ```pycon
    >>> create_actor_message_for_cow(moocow, "http://domain.example/")
    {'baseUrl': 'http://domain.example/',
        'preferredUsername': 'moocow',
        'automaticallyAcceptFollowers': True,
        'profile': {'type': 'Service'}}

    ```
    """
    return {
        "baseUrl": base_url,
        "preferredUsername": cow.information.handle,
        "automaticallyAcceptFollowers": cow.auto_follow,
        "profile": {"type": "Service"},
    }
