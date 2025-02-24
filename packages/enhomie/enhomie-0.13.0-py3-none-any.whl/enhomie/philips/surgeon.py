"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.types import DictStrAny
from encommon.types import getate
from encommon.types import setate



def surgeon(  # noqa: CFQ001, CFQ004
    fetch: DictStrAny,
    event: DictStrAny,
) -> bool:
    """
    Process the stream event updating the origin dictionary.

    :param fetch: Dictionary from the origin to be updated.
    :param event: Event from the stream for updating fetch.
    :returns: Boolean indicating whether or not was changed.
    """

    updated = False


    def _update_state() -> bool:

        _type = item['type']

        types = [
            'grouped_light',
            'light']

        if _type not in types:
            return False

        _update('on/on')

        return True


    def _update_color() -> bool:

        _type = item['type']

        types = [
            'grouped_light',
            'light']

        if _type not in types:
            return False

        _update('color/xy')

        return True


    def _update_level() -> bool:

        _type = item['type']

        types = [
            'grouped_light',
            'light']

        if _type not in types:
            return False

        _update(
            'dimming/brightness')

        return True


    def _update_scene() -> bool:

        _type = item['type']

        if _type != 'scene':
            return False

        _update('status/active')

        return True


    def _update_button() -> bool:

        _type = item['type']

        if _type != 'button':
            return False

        _update(
            'button/button_'
            'report/updated')

        _update(
            'button/button_'
            'report/event')

        _update(
            'button/last_event')

        return True


    def _update_contact() -> bool:

        _type = item['type']

        if _type != 'contact':
            return False

        _update(
            'contact_report'
            '/changed')

        _update(
            'contact_report'
            '/state')

        return True


    def _update_motion() -> bool:

        _type = item['type']

        if _type != 'motion':
            return False

        _update(
            'motion/motion')

        _update(
            'motion/motion_'
            'report/changed')

        _update(
            'motion/motion_'
            'report/event')

        _update(
            'motion/motion_valid')

        return True


    def _update(
        target: str,
    ) -> None:

        value = getate(event, target)

        if value is None:
            return None

        setate(item, target, value)


    unique = event['id']

    for item in fetch['data']:

        _unique = item['id']

        if unique != _unique:
            continue

        if _update_state():
            updated = True

        if _update_color():
            updated = True

        if _update_level():
            updated = True

        if _update_scene():
            updated = True

        if _update_button():
            updated = True

        if _update_contact():
            updated = True

        if _update_motion():
            updated = True


    return updated
