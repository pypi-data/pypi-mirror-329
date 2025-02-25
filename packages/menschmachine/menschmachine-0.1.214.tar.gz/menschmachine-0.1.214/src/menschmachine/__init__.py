import json
from json import JSONDecodeError

from menschmachine.llm.proxy import ApiProxy
from menschmachine.log import get_logger


def get_fix_json_prompt(json_str):
    return f'''The following json cannot be parsed using json.loads() on python. 
    Return an answer that is directly parsable with json.loads(). Pay especially attention to string quoting problems.
    If you don't know how to return a parseable json string, return an empty array.
    IMPORTANT: only respond with the json, no explanations or anything else. If the json is already valid, just echo it.
```json
{json_str}
```
'''


def _normalize_json(json_str):
    json_str = json_str.strip()
    first_index_of_square_bracket = json_str.find('[')
    first_index_of_curly_bracket = json_str.find('{')

    if first_index_of_square_bracket > -1 and (
            first_index_of_curly_bracket == -1 or first_index_of_square_bracket < first_index_of_curly_bracket):
        json_start = first_index_of_square_bracket
        json_end = json_str.rfind(']')
    elif first_index_of_curly_bracket > -1:
        json_start = first_index_of_curly_bracket
        json_end = json_str.rfind('}')
    else:
        json_start = -1
        json_end = -1

    if json_start > -1 and json_end > -1:
        return json_str[json_start:json_end + 1]
    else:
        return json_str


def to_json(json_str: str, fallback_value=None) -> object:
    try:
        return json.loads(_normalize_json(json_str))
    except JSONDecodeError:
        return _fix_json(json_str, fallback_value)


def _fix_json(json_str: str, fallback_value=None) -> object:
    get_logger().debug(f"Fixing {json_str}")
    prompt = get_fix_json_prompt(json_str)
    fixed_json = ApiProxy().ask(prompt, model="haiku").message
    try:
        return json.loads(_normalize_json(fixed_json))
    except JSONDecodeError:
        get_logger().exception(
            f"Fixed json - could not be parsed: {_normalize_json(fixed_json)}")
        return fallback_value


class MM(object):
    @staticmethod
    def json(json_str: str):
        return to_json(json_str)


if __name__ == "__main__":
    print(MM.json("Here is the json: {'x': 1, 'y': 2}"))
