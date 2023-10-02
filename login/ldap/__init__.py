from flask import current_app, flash
from ldap3 import Server, Connection, SAFE_SYNC, SIMPLE
from ldap3.core.exceptions import LDAPException

_ldap_server = current_app.config['LDAP_SERVER']
_ldap_port = current_app.config['LDAP_PORT']

_base_dn = current_app.config['BASE_DN']
_service_ou = current_app.config['SERVICE_OU']
_service_password = current_app.config['SERVICE_PASSWORD']
service_username = current_app.config['SERVICE_ACCOUNT']
_server = Server(_ldap_server,_ldap_port)
_user_ou = current_app.config['USER_OU']

def _get_id(connection: Connection, search_base, search_filter):
  status, _, response, _ = connection.search(search_base,search_filter,attributes=['uidNumber'])
  print('load status: {}'.format(status))
  print('response: {}'.format(response))
  if status:
    return response[0]['attributes']['uidNumber']
  return None

def _build_connection(user_dn,password):
  return Connection(_server, authentication=SIMPLE,
      user=user_dn,
      password=password,
      auto_bind=True,
      client_strategy=SAFE_SYNC)

def service_get_id( search_filter):
  bind_dn='cn={},{},{}'.format(service_username,_service_ou,_base_dn)
  try:
    print('Attempting to connect: {}'.format(bind_dn))
    c = _build_connection(bind_dn,_service_password)
    return _get_id(c,'ou=users,dc=example,dc=org', search_filter)
  except LDAPException as e:
    flash('Couldn\'t connect to _server')
    print('SA LDAP error: {}'.format(e))
    return None

def login(username, password):
  user_dn='cn={},{},{}'.format(username,_user_ou,_base_dn)
  try:
    print('Attempting to connect: {}'.format(user_dn))
    c = _build_connection(user_dn,password)
    id = _get_id(c,'{},dc=example,dc=org'.format(_user_ou),'(cn={})'.format(username))
    return id
  except LDAPException as e:
    print('LDAP error: {}'.format(e))
    return None