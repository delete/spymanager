import json


class User():
    """ SiteImage user model """

    def __init__(self, username, html_page):
        self.username = username
        self._data = self._extract_data_from_html(html_page)

        self.images = self._get_images(self._data)
        self._get_user_informations(self._data)

    def __repr__(self):
        return '{}'.format(self.username)

    def _extract_data_from_html(self, html_content):
        json_text = self._extract_json_data_from_html(html_content)
        # clean text removing these junk strings
        first = '<script type="text/javascript">window._sharedData = '
        last = ';</script>'

        json_text = json_text.replace(first, "")
        json_text = json_text.replace(last, "")

        data = json.loads(json_text)

        try:
            user = data['entry_data']['ProfilePage'][0]['user']
        except KeyError:
            raise UserNotFoundException("{} not found!".format(self.username))

        return user

    def _extract_json_data_from_html(self, html_page):
        json_text = ''
        lines = html_page.split('\n')
        for line in lines:
            if 'window._sharedData =' in line:
                json_text = line
                break
        return json_text

    def _get_images(self, user_data):
        nodes = user_data['media']['nodes']

        images = {}

        for node in nodes:
            images[node['code']] = {
                'display_src': node.get('display_src'),
                'caption': node.get('caption')
            }
        return images

    def _get_user_informations(self, user_data):
        self.id = user_data['id']
        self.name = user_data['full_name']
        # Following back only works if who is requesting is logged
        self.is_following_back = user_data['follows_viewer']
        self.is_private = user_data['follows_viewer']

    def pretty_print(self):
        print('####################')
        print('## {} ##'.format(self.name))
        print('#################### \n\n')
        for image in self.images:
            print(self.images[image]['display_src'])
            print('-----------------------\n')


class UserNotFoundException(Exception):
    pass
