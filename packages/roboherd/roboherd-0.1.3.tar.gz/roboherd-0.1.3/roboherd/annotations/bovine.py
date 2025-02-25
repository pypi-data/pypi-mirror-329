"""Test documentation"""

from typing import Annotated
from fast_depends import Depends
from .common import Profile

try:
    from bovine.activitystreams import factories_for_actor_object
    from bovine.activitystreams.activity_factory import (
        ActivityFactory as BovineActivityFactory,
    )
    from bovine.activitystreams.object_factory import (
        ObjectFactory as BovineObjectFactory,
    )

    def get_activity_factory(profile: Profile) -> BovineActivityFactory:
        activity_factory, _ = factories_for_actor_object(profile)
        return activity_factory

    def get_object_factory(profile: Profile) -> BovineObjectFactory:
        _, object_factory = factories_for_actor_object(profile)
        return object_factory

except ImportError:

    class BovineActivityFactory: ...

    class BovineObjectFactory: ...

    def get_activity_factory() -> None:
        raise ImportError("bovine not installed")

    def get_object_factory() -> None:
        raise ImportError("bovine not installed")


ActivityFactory = Annotated[BovineActivityFactory, Depends(get_activity_factory)]
"""The activity factory of type [bovine.activitystreams.activity_factory.ActivityFactory][]"""

ObjectFactory = Annotated[BovineObjectFactory, Depends(get_object_factory)]
"""The object factory of type [bovine.activitystreams.object_factory.ObjectFactory][]"""
