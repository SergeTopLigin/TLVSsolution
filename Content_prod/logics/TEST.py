from modules.gh_push import gh_push
import os
mod_name = os.path.basename(__file__)[:-3]
gh_push(str(mod_name), 'answers', 'test.txt', 'rename:NEWtest')
gh_push(str(mod_name), 'answers', 'test.json', 'rename:NEWtest')