content = 'changed'

import os
mod_name = os.path.basename(__file__)[:-3]
from modules.gh_push import gh_push
gh_push(str(mod_name), 'content_commits', 'standings.txt', content)
