content = 'test'

import os
mod_name = os.path.basename(__file__)[:-3]
from modules.gh_push import gh_push
gh_push(str(mod_name), 'sub_results', 'standings.txt', content)
