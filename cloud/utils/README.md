# utils

# Background

Postman workflow is too slow.  Jenkins jobs aren't extensive and aren't generic.  A list of curl commands would work except I'm regularly change target domains from `.cloud`, `.st`, `.sh`, `.dev`.

This was built out of my own needs to allow me to query API of target domains quickly, precisely, and repeatedly.

# Usage

![](https://github.com/SpencerWoo/cloud-dev-projects/blob/master/utils/assets/api.gif)

0. Configure [authentication](_settings.py#L19-L20)

1. Set [FUNCTION](_settings.py#L7) and [ARGS](_settings.py#L8) accordingly

2. Run main.py with Python 3.6+ - `python3 main.py`

3. View output in console or `output.json`

# Docs

View 
	at `/docs`

Generate 
	with `pdoc --html _api`

# Future

The use-case of this repository is for running `GET` API queries locally with your own credentials.  


Any API query that modifies data should be ran via jenkins jobs and _not_ with local commands/requests.  Additionally these queries use your permissions while the jenkins job user currently has `TEAM`.
