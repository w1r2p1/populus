import itertools
from collections import OrderedDict

from populus.utils.contracts import (
    get_shallow_dependency_graph,
    get_contract_deploy_order,
    get_recursive_contract_dependencies,
)


def get_deploy_order(contracts_to_deploy, compiled_contracts):
    # Extract and dependencies that exist due to library linking.
    dependency_graph = get_shallow_dependency_graph(compiled_contracts)

    # Compute the full set of dependencies needed to deploy the desired
    # contracts.
    all_deploy_dependencies = set(itertools.chain.from_iterable(
        get_recursive_contract_dependencies(contract_name, dependency_graph)
        for contract_name in contracts_to_deploy
    ))
    all_contracts_to_deploy = all_deploy_dependencies.union(contracts_to_deploy)

    # Now compute the order that the contracts should be deployed based on
    # their dependencies.
    deploy_order = [
        (contract_name, compiled_contracts[contract_name])
        for contract_name
        in get_contract_deploy_order(dependency_graph)
        if contract_name in all_contracts_to_deploy
    ]
    return OrderedDict(deploy_order)
