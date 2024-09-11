global repo

defaults = {
    'mikrotik_exporter': {
        'version': '1.2.7',
        'user': 'mktxp',
        'group': 'mktxp',
        'install_dir': '/opt/mktxp',
        'routeros_boards': {
            #'name': {
            #    'hostname': 'switch-office.example.org',
            #    'username': 'mktxp',
            #    'password': 'mktxp_secure_password',
            #},
        },
    },
}

@metadata_reactor
def get_routeros_boards(metadata):
    routeros_boards = {}

    for checked_node in sorted(repo.nodes, key=lambda x: x.name):
        if checked_node.os == "routeros":
            # There is a special configuration for mikrotik_exporter
            if checked_node.metadata.get("mikrotik_exporter", {}).get('router_boards', {}):
                name = list(checked_node.metadata.get("mikrotik_exporter").get('router_boards').keys())[0]
                cfg = checked_node.metadata.get("mikrotik_exporter").get('router_boards')[name]
                routeros_boards[name] = {
                    'hostname': cfg.get('hostname', checked_node.hostname),
                    'username': cfg.get('username', checked_node.username),
                    'password': cfg.get('password', checked_node.password),
                }
            else:
                routeros_boards[checked_node.name] = {
                    'hostname': checked_node.hostname,
                    'username': checked_node.username,
                    'password': checked_node.password,
                }

    return {
        'mikrotik_exporter': {
            'routeros_boards': routeros_boards,
        },
    }
