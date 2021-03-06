from keystoneclient.v2_0 import Client as keystone_client
from oslo.config import cfg

import sys

cli_opts = [
    cfg.StrOpt('username', default='',
               help='set username'),
    cfg.StrOpt('password', default='',
               help='set password'),
    cfg.StrOpt('tenant', default='',
               help='set tenant'),
]

CONF = cfg.CONF
CONF.import_opt('os_admin_username', 'savanna.main')
CONF.import_opt('os_admin_password', 'savanna.main')
CONF.import_opt('os_admin_tenant_name', 'savanna.main')
CONF.register_cli_opts(cli_opts)


def main():
    CONF(sys.argv[1:], project='get_auth_token')

    user = CONF.username or CONF.os_admin_username
    password = CONF.password or CONF.os_admin_password
    tenant = CONF.tenant or CONF.os_admin_tenant_name

    protocol = CONF.os_auth_protocol
    host = CONF.os_auth_host
    port = CONF.os_auth_port

    auth_url = "%s://%s:%s/v2.0/" % (protocol, host, port)

    print "User: %s" % user
    print "Password: %s" % password
    print "Tenant: %s" % tenant
    print "Auth URL: %s" % auth_url

    keystone = keystone_client(
        username=user,
        password=password,
        tenant_name=tenant,
        auth_url=auth_url
    )

    result = keystone.authenticate()

    print "Auth succeed: %s" % result
    print "Auth token: %s" % keystone.auth_token
    print "Tenant [%s] id: %s" % (tenant, keystone.tenant_id)


if __name__ == "__main__":
    main()
