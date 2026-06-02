##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

import setuptools


REQUIRES = [
    'Werkzeug == 3.1.6',
    'connexion[swagger-ui] == 2.15.1',
    'certifi >= 2024.07.04',
    'python-dateutil >= 2.8.2',
    'setuptools >= 21.0.0',
    'transitions == 0.6.4',
    'pypubsub == 4.0.3',
    'rwlock == 0.0.7',
    'autologging >= 1.3.2',
    'PyYAML >= 6.0',
    'urllib3 >= 2.6.3',
    'six >= 1.16.0',
    'gevent == 26.4.0',
    'bottle >= 0.12.25',
    'flask == 3.1.3',
    'csvvalidator >= 1.2',
    'bson == 0.5.10'
]

version_args = {"version": "1.3.0"}

setuptools.setup(
    name='mistk',
    packages=setuptools.find_packages() + ['conf'],
    package_data={'conf': ['*.ini', 'log_config.json']},
    include_package_data=True,
    install_requires=REQUIRES,
    **version_args)
