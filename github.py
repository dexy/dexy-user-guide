import requests
import json

api = "https://api.github.com"
repo_owner = "dexy"
repo_name = "dexy"


def get_request(path, params=None):
    if not params:
        params = {}

    r = requests.get("%s%s" % (api, path), params=params)
    return r.json()

args = { 'owner' : repo_owner, 'name' : repo_name }
path = "/repos/%(owner)s/%(name)s/issues" % args

issues = {}

raw_json_data = get_request(path, {'state' : 'open' })
issues.update(dict((issue['number'], issue) for issue in raw_json_data))

raw_json_data = get_request(path, {'state' : 'closed' })
issues.update(dict((issue['number'], issue) for issue in raw_json_data))

with open("issues.json", "wb") as f:
    json.dump(issues, f)
