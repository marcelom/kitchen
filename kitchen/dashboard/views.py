from django.http import HttpResponse
from django.template.loader import render_to_string

from kitchen.dashboard.chef import get_nodes_extended, get_roles, filter_nodes
from kitchen.dashboard import graphs
from kitchen.settings import REPO


def get_data(request):
    filter_env = request.GET.get('env', '')
    filter_roles = request.GET.get('roles','')
    if filter_env or filter_roles:
        nodes = filter_nodes(filter_env, filter_roles, get_nodes_extended())
    else:
        nodes = get_nodes_extended()
    roles = get_roles()
    environments = [] # an 'implicit' set, as environments must be uniquely named
    roles_groups = set()
    for role in roles:
        split = role['name'].split('_')
        if split[0] == REPO['ENV_PREFIX']:
            name = '_'.join(split[1:])
            environments.append({'name': name, 
                                 'count': len([node for node in nodes if node['chef_environment'] == name])})
        else:
            roles_groups.add(split[0])
    return nodes, roles, roles_groups, environments, filter_env


def main(request):
    nodes, roles, roles_groups, environments, filter_env = get_data(request)
    return HttpResponse(render_to_string('main.html',
                                        {'nodes': nodes,
                                         'roles': roles,
                                         'roles_groups': sorted(roles_groups),
                                         'environments': sorted(environments),
                                         'filter_env': filter_env}))


def graph(request):
    nodes, roles, roles_groups, environments, filter_env = get_data(request)
    graphs.generate_node_map(nodes)
    return HttpResponse(render_to_string('graph.html',
                                        {'nodes': nodes,
                                         'roles': roles,
                                         'roles_groups': sorted(roles_groups),
                                         'environments': sorted(environments),
                                         'filter_env': filter_env}))
