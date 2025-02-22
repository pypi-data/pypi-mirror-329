from absl import app, flags, logging
import os
import requests
from jwt import JWT
import re


FLAGS = flags.FLAGS

PREFIX = 'UNIFI_RECONNECT'

flags.DEFINE_string('url', os.getenv(f'{PREFIX}_URL', None), 'Base url including http(s) to CloudKey endpoint. Do not include /network/')
flags.DEFINE_string('site', os.getenv(f'{PREFIX}_SITE', 'default'), 'Site id')
flags.DEFINE_string('username', os.getenv(f'{PREFIX}_USERNAME', None), 'Local username')
flags.DEFINE_string('password', os.getenv(f'{PREFIX}_PASSWORD', None), 'Local password')
flags.DEFINE_string('mac', os.getenv(f'{PREFIX}_MAC', None), 'Client MAC address to reconnect')


def not_null(value):
    return value is not None


flags.register_validator('username',
                         not_null,
                         message='username must be set',
                         flag_values=FLAGS)
flags.register_validator('password',
                         not_null,
                         message='password must be set',
                         flag_values=FLAGS)
flags.register_validator('url',
                         not_null,
                         message='url must be set',
                         flag_values=FLAGS)
flags.register_validator('mac',
                         not_null,
                         message='mac must be set',
                         flag_values=FLAGS)


def format_mac(mac: str) -> str:
    mac = re.sub('[.:-]', '', mac).lower()  # remove delimiters and convert to lower case
    mac = ''.join(mac.split())  # remove whitespaces
    assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)
    assert mac.isalnum()  # should only contain letters and numbers
    # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
    mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])
    return mac


def main(argv):
    del argv


    login_data = {'username' : FLAGS.username, 'password' : FLAGS.password}
    with requests.Session() as session:
        r = session.post(FLAGS.url + '/api/auth/login', json=login_data)
        token = session.cookies.get("TOKEN")
        if not token:
            logging.fatal(f'Valid token could not be fetched, {r.text}')

        jwt_instance = JWT()
        jwt_payload = jwt_instance.decode(token, key=None, do_verify=False, algorithms=None, do_time_check=False)

        headers = {'x-csrf-token': jwt_payload['csrfToken']}
        device_data = {
                'cmd': 'kick-sta',
                'mac': format_mac(FLAGS.mac)
                }
        endpoint = f'{FLAGS.url}/proxy/network/api/s/{FLAGS.site}/cmd/stamgr'
        logging.debug(endpoint)
        response = session.post(endpoint, json=device_data, headers=headers)
        print(response.json())



# script endpoint installed by package
def run():
    app.run(main)


if __name__ == '__main__':
    run()


