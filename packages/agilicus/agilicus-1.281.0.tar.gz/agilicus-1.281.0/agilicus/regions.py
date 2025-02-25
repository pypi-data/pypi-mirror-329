from typing import List

import agilicus

from . import context
from .input_helpers import strip_none
from .input_helpers import add_remove_uniq_list
from .output.table import (
    spec_column,
    format_table,
    metadata_column,
    status_column,
)


def list_point_of_presences(
    ctx, excludes_all_tag, excludes_any_tag, includes_all_tag, includes_any_tag, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    excludes_all_tags = tag_list_to_tag_names(excludes_all_tag)
    excludes_any_tags = tag_list_to_tag_names(excludes_any_tag)
    includes_all_tags = tag_list_to_tag_names(includes_all_tag)
    includes_any_tags = tag_list_to_tag_names(includes_any_tag)

    return apiclient.regions_api.list_point_of_presences(
        excludes_all_tag=excludes_all_tags,
        excludes_any_tag=excludes_any_tags,
        includes_all_tag=includes_all_tags,
        includes_any_tag=includes_any_tags,
        **strip_none(kwargs),
    ).point_of_presences


def add_point_of_presence(ctx, name, tag: List[str], domain=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    tags = []
    if tag:
        tags = tag_list_to_tag_names(tag)

    domains = []
    if domain:
        domains = [agilicus.Domain(d) for d in domain]

    routing = agilicus.PointOfPresenceRouting(domains=domains)
    pop_spec = agilicus.PointOfPresenceSpec(
        name=agilicus.FeatureTagName(name), tags=tags, routing=routing
    )
    pop = agilicus.PointOfPresence(spec=pop_spec)
    return apiclient.regions_api.add_point_of_presence(pop)


def update_point_of_presence(
    ctx,
    pop_id,
    tag: List[str],
    domain=None,
    overwrite_tags=False,
    overwrite_domains=False,
    name=None,
    add_cluster_ids=None,
    remove_cluster_ids=None,
    master_cluster_id=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)

    original = apiclient.regions_api.get_point_of_presence(point_of_presence_id=pop_id)

    tags = []
    if tag:
        tags = tag_list_to_tag_names(tag)

    if not overwrite_tags:
        tags.extend(original.spec.tags)
        tags = tag_list_to_tag_names(list(set(str(tag) for tag in tags)))

    original.spec.tags = tags

    domains = []
    if domain:
        domains = [agilicus.Domain(d) for d in domain]

    if not overwrite_domains:
        to_write = original.spec.routing.domains
        for domain in domains:
            if domain not in to_write:
                to_write.append(domain)
        domains = to_write

    original.spec.routing.domains = domains
    if name is not None:
        original.spec.name = name

    original.spec.cluster_ids = add_remove_uniq_list(
        original.spec.cluster_ids,
        add_cluster_ids,
        remove_cluster_ids,
    )
    if master_cluster_id is not None:
        original.spec.master_cluster_id = master_cluster_id

    return apiclient.regions_api.replace_point_of_presence(
        pop_id,
        point_of_presence=original,
    )


def show_point_of_presence(ctx, pop_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.get_point_of_presence(point_of_presence_id=pop_id)


def delete_point_of_presence(ctx, pop_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.delete_point_of_presence(point_of_presence_id=pop_id)


def format_point_of_presences_as_text(ctx, tags):
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("tags"),
        spec_column("routing.domains", "domains"),
        spec_column("master_cluster_id"),
        status_column("clusters"),
    ]

    return format_table(ctx, tags, columns)


def tag_list_to_tag_names(tags: List[str]) -> List[agilicus.FeatureTagName]:
    return [agilicus.FeatureTagName(tag_name) for tag_name in tags]


def add_cluster(ctx, name, ip_addresses=None, description=None, domain=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    config = agilicus.ClusterConfig()

    if ip_addresses:
        config.ip_addresses = ip_addresses

    if description:
        config.description = description

    spec = agilicus.ClusterSpec(
        name=agilicus.Domain(name),
        config=config,
    )

    if domain:
        spec.domain = agilicus.Domain(domain)

    cluster = agilicus.Cluster(spec=spec)
    return apiclient.regions_api.add_cluster(cluster)


def _update_list(ip_addresses):
    return {k: True for v, k in enumerate(ip_addresses)}


def update_cluster(
    ctx,
    cluster_id,
    name=None,
    domain=None,
    remove_ip_addresses=None,
    add_ip_addresses=None,
    description=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    cluster = apiclient.regions_api.get_cluster(cluster_id)

    config = cluster.spec.config
    if not config:
        cluster.spec.config = agilicus.ClusterConfig()
        config = cluster.spec.config

    config.ip_addresses = add_remove_uniq_list(
        config.ip_addresses,
        add_ip_addresses,
        remove_ip_addresses,
    )

    if description:
        config.description = description

    if name:
        cluster.spec.name = agilicus.Domain(name)

    if domain:
        cluster.spec.domain = agilicus.Domain(domain)

    return apiclient.regions_api.replace_cluster(cluster_id, cluster=cluster)


def delete_cluster(ctx, cluster_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.delete_cluster(cluster_id)


def list_clusters(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    return apiclient.regions_api.list_clusters(
        **strip_none(kwargs),
    ).clusters
