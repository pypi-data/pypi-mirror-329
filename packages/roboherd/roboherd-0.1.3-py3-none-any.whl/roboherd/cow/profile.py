from urllib.parse import urlparse
from bovine.activitystreams.utils import as_list

from .types import Information


def profile_part_needs_update(information: Information, profile: dict) -> bool:
    if information.name != profile.get("name"):
        return True

    if information.description != profile.get("summary"):
        return True

    if information.type != profile.get("type"):
        return True

    return False


def key_index_from_attachment(attachments: list[dict], key: str) -> int | None:
    for idx, attachment in enumerate(attachments):
        if attachment is None:
            continue
        if attachment.get("type") == "PropertyValue" and attachment.get("name") == key:
            return idx
    return None


def determine_action_for_key_and_value(
    attachments: list[dict], key: str, value: str
) -> dict | None:
    idx = key_index_from_attachment(attachments, key)
    if idx is None:
        if value:
            return {
                "action": "update_property_value",
                "key": key,
                "value": value,
            }
        return None

    if value is None:
        return {
            "action": "remove_property_value",
            "key": key,
        }
    current_value = attachments[idx].get("value")
    if value != current_value:
        return {
            "action": "update_property_value",
            "key": key,
            "value": value,
        }

    return None


def determine_actions(information: Information, profile: dict) -> list[dict] | None:
    attachments = as_list(profile.get("attachment", []))
    meta_information = information.meta_information

    actions = [
        determine_action_for_key_and_value(
            attachments, "Author", meta_information.author
        ),
        determine_action_for_key_and_value(
            attachments, "Source", meta_information.source
        ),
        determine_action_for_key_and_value(
            attachments, "Frequency", information.frequency
        ),
    ]

    if information.handle and profile.get("preferredUsername") is None:
        actions.append(
            {
                "action": "add_identifier",
                "identifier": "acct:"
                + information.handle
                + "@"
                + urlparse(profile.get("id")).netloc,
                "primary": True,
            }
        )

    actions = list(filter(lambda x: x, actions))

    if len(actions) == 0:
        return None
    return actions


def determine_profile_update(information: Information, profile: dict) -> dict:
    """Returns the update for the profile"""

    update = {"actor": profile.get("id")}

    if profile_part_needs_update(information, profile):
        update["profile"] = {
            "type": information.type,
            "name": information.name,
            "summary": information.description,
        }

    actions = determine_actions(information, profile)

    if actions:
        update["actions"] = actions

    if len(update) == 1:
        return None

    return update
