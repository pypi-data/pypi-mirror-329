""" Utility functions for model module."""


def arrange_locals(locals_dict: dict, exclude_keys: list = None, filter_none: bool = True) -> dict:
    """
    Arrange the locals dictionary to exclude specified keys and optionally filter None values.

    :param locals_dict: Dictionary of locals.
    :param exclude_keys: List of keys to exclude (default: empty list).
    :param filter_none: Boolean indicating whether to filter out None values (default: True).
    :return: Dictionary of arranged locals.
    """
    exclude_keys = exclude_keys or []

    return {k: v for k, v in locals_dict.items()
            if k != 'self' and k not in exclude_keys and (v is not None or not filter_none)}


def pop_keys_from_dict(original_dict: dict, keep_keys: list) -> tuple[dict, dict]:
    """
    Pop all keys from the list that exist in the dictionary using dictionary comprehension.

    :param original_dict: The dictionary from which keys will be popped.
    :param keep_keys: A list of keys to pop from the dictionary.

    :returns: A tuple containing the original dict without the popped keys and a new dict containing the popped keys
    and their values.
    """
    popped_items = {key: original_dict.pop(key) for key in keep_keys if key in original_dict}
    return original_dict, popped_items


__all__ = ['arrange_locals', 'pop_keys_from_dict']
