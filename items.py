global node

user = node.metadata.get('mikrotik_exporter').get('user')
group = node.metadata.get('mikrotik_exporter').get('group')
install_dir = node.metadata.get('mikrotik_exporter').get('install_dir')

pkg_apt = {
    'python3-pip': {
        'installed': True,
        'tags': [
            'mktxp_prepare_venv'
        ]
    },
    'python3-venv': {
        'installed': True,
        'tags': [
            'mktxp_prepare_venv',
        ]
    }
}

users = {
    user: {
        'home': install_dir,
        'shell': '/bin/nologin',
        'tags': [
            'mktxp_prepare_venv'
        ]
    },
}

svc_systemd = {
    'mktxp.service': {
        'running': True,
        'enabled': True,
        'needs': [
            f'pkg_pip:{install_dir}/mktxp',
            'file:/etc/systemd/system/mktxp.service',
            'file:/etc/mktxp/mktxp.conf',
            'file:/etc/mktxp/_mktxp.conf',
        ]
    }
}

directories = {
    install_dir: {
        'owner': user,
        'group': group,
        'needs': [
            f'user:{user}',
        ],
        'tags': [
            'mktxp_prepare_venv'
        ],
    },
}

actions = {
    'create_venv': {
        'command': f'python3 -m venv {install_dir}',
        'needs': [
            f'directory:{install_dir}',
            f'user:{user}',
            'pkg_apt:',
        ],
        'triggers': [
            'action:chown_venv',
        ],
        'unless': f'test -f {install_dir}/bin/pip',
        'tags': [
            'mktxp_prepare_venv'
        ]
    },
    'chown_venv': {
        'command': f'chown -R {user}:{group} {install_dir}',
        'triggered': True,
        'tags': [
            'mktxp_prepare_venv'
        ],
    },
}

pkg_pip = {
    f"{install_dir}/mktxp": {
        'installed': True,
        'version': node.metadata.get('mikrotik_exporter', {}).get('version'),
        'needs': [
            'tag:mktxp_prepare_venv',
        ],
    }
}

files = {
    '/etc/systemd/system/mktxp.service': {
        'source': 'etc/systemd/system/mktxp.service.j2',
        'content_type': 'jinja2',
        'context': {
            'user': user,
            'install_dir': install_dir,
        },
        'triggers': [
            'svc_systemd:mktxp.service:restart',
        ],
    },
    '/etc/mktxp/mktxp.conf': {
        'source': 'etc/mktxp/mktxp.conf.j2',
        'content_type': 'jinja2',
        'context': {
            'routeros_boards': node.metadata.get('mikrotik_exporter', {}).get('routeros_boards'),
        },
        'owner': user,
        'group': group,
        'triggers': [
            'svc_systemd:mktxp.service:restart',
        ],
    },
    '/etc/mktxp/_mktxp.conf': {
        'source': 'etc/mktxp/_mktxp.conf.j2',
        'content_type': 'jinja2',
        'owner': user,
        'group': group,
        'triggers': [
            'svc_systemd:mktxp.service:restart',
        ],
    },
}
