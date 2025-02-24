import re
from pathlib import Path
import json


def resolve_path(ctx, param, value):
    """Convert path string to absolute Path object"""
    return Path(value).resolve()


def ip2name(routers, ip):
    for router in routers:
        if router['ip'] == ip:
            return router['name']
    return ip


def get_priority(routers, ip):
    for router in routers:
        if router['ip'] == ip:
            return router['priority']
    return 10


def parse_bird(config, output):
    routers = []
    connections = []
    networks = []
    current_router = None
    for line in output.splitlines():
        line = line.rstrip()
        if re.match(r'^\trouter (\S+)$', line):
            parts = line.split()
            routers.append(parts[1])
            current_router = parts[1]
        if re.match(r'^\t\t(external|stubnet) (\S+) metric (\d+)$', line):
            parts = line.split()
            networks.append({
                'router': current_router,
                'network': parts[1],
                'metric': parts[3]
            })
        if re.match(r'^\t\trouter (\S+) metric (\d+)$', line):
            parts = line.split()
            connections.append({
                'source': current_router,
                'destination': parts[1],
                'metric': parts[3],
                'priority': get_priority(config['routers'], current_router)
            })
    return routers, connections, networks


def filter_connections(routers, connections, pdostal, ngn):
    """
    Filter connections based on --pdostal and --ngn options

    Parameters:
    * routers: list of routers
    * connections: list of connections
    * pdostal: bool
    * ngn: bool

    Returns:
    * filtered_connections: list of connections
    """
    filtered_connections = []
    for c in connections:
        x_name = ip2name(routers, c['source'])
        y_name = ip2name(routers, c['destination'])
        if not ngn and not pdostal:
            filtered_connections.append(c)
        elif pdostal and x_name.endswith('pdostal.ngn') and y_name.endswith('pdostal.ngn'):
            filtered_connections.append(c)
        elif ngn and x_name.endswith('pot.pdostal.ngn') and not y_name.endswith('pdostal.ngn'):
            filtered_connections.append(c)
        elif ngn and x_name.endswith('pot.pdostal.ngn') and y_name.endswith('tata.pdostal.ngn'):
            filtered_connections.append(c)
        elif ngn and x_name.endswith('tata.pdostal.ngn') and not y_name.endswith('pdostal.ngn'):
            filtered_connections.append(c)
        elif ngn and x_name.endswith('tata.pdostal.ngn') and y_name.endswith('pot.pdostal.ngn'):
            filtered_connections.append(c)
        elif ngn and not x_name.endswith('pdostal.ngn') and not y_name.endswith('pdostal.ngn'):
            filtered_connections.append(c)
    return filtered_connections


def precompute_connections_dict(connections):
    connections_dict = {}
    for c in connections:
        connections_dict[(c['source'], c['destination'])] = c['metric']
        connections_dict[(c['destination'], c['source'])] = c['metric']
    return connections_dict


def is_unique_connection(connection, x_metric, y_metric, used):
    return (x_metric and y_metric
            and (connection['source'], connection['destination']) not in used
            and (connection['destination'], connection['source']) not in used)


def print_markdown_mermaid(routers, unique_routers, sorted_connections, networks):
    print("```mermaid")
    print("flowchart TB")

    for router in unique_routers:
        print(f"    {ip2name(routers, router)}[\"{ip2name(routers, router)}")
        for network in networks:
            if network['router'] == router:
                print(f"    {network['network']}")
        print("    \"]")

    connections_dict = precompute_connections_dict(sorted_connections)

    # Use a set to track used connections
    used = set()

    for c in sorted_connections:
        x_metric = connections_dict.get((c['destination'], c['source']))
        y_metric = connections_dict.get((c['source'], c['destination']))

        if is_unique_connection(c, x_metric, y_metric, used):
            x_name = ip2name(routers, c['source'])
            y_name = ip2name(routers, c['destination'])

            print(f"    {x_name} o-- {x_metric}-{y_metric} --o {y_name}")

            used.add((c['source'], c['destination']))

    print("```")


def print_text_routers(routers, unique_routers, networks):
    print(f"We currently have {len(unique_routers)} routers.\n")
    for router in unique_routers:
        print(f"Router {ip2name(routers, router)} ({router}):")
        for network in networks:
            if network['router'] == router:
                print(f"- {network['network']}")
        print("")


def print_text_routers_diff_ready(routers, unique_routers, networks):
    print(f"We currently have {len(unique_routers)} routers.\n")
    for router in unique_routers:
        print(f"Router {ip2name(routers, router)} ({router}):")
        for network in networks:
            if network['router'] == router:
                print(f"Router {ip2name(routers, router)} publishes {network['network']}.")
        print("")


def print_text_connections_diff_ready(routers, unique_routers, sorted_connections):
    print(f"We currently have {len(sorted_connections)//2} connections.\n")

    connections_dict = precompute_connections_dict(sorted_connections)

    for c in sorted_connections:
        x_metric = connections_dict.get((c['destination'], c['source']))
        y_metric = connections_dict.get((c['source'], c['destination']))

        x_name = ip2name(routers, c['source'])
        y_name = ip2name(routers, c['destination'])

        print(f"Connection {x_name} <--> {y_name} ({x_metric}/{y_metric})")


def print_text_connections(routers, unique_routers, sorted_connections):
    print(f"We currently have {len(sorted_connections)//2} connections.\n")

    connections_dict = precompute_connections_dict(sorted_connections)

    # Use a set to track used connections
    used = set()

    for c in sorted_connections:
        x_metric = connections_dict.get((c['destination'], c['source']))
        y_metric = connections_dict.get((c['source'], c['destination']))

        if is_unique_connection(c, x_metric, y_metric, used):
            x_name = ip2name(routers, c['source'])
            y_name = ip2name(routers, c['destination'])

            print(f"Connection {x_name} <--> {y_name} ({x_metric}/{y_metric})")

            used.add((c['source'], c['destination']))


def print_json(routers, unique_routers, sorted_connections):
    output = {"nodes": [], "links": []}
    for router in unique_routers:
        node = {"id": ip2name(routers, router), "name": ip2name(routers, router)}
        output['nodes'].append(node)
    for connection in sorted_connections:
        output['links'].append({
            "source": ip2name(routers, connection['source']),
            "target": ip2name(routers, connection['destination'])
        })
    print(json.dumps(output))
