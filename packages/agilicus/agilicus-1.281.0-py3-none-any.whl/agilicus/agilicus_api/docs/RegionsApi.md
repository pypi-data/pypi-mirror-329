# agilicus_api.RegionsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_cluster**](RegionsApi.md#add_cluster) | **POST** /v1/clusters | Add a Cluster
[**add_point_of_presence**](RegionsApi.md#add_point_of_presence) | **POST** /v1/point_of_presences | Add a point of presence.
[**delete_cluster**](RegionsApi.md#delete_cluster) | **DELETE** /v1/clusters/{cluster_id} | Delete a Cluster
[**delete_point_of_presence**](RegionsApi.md#delete_point_of_presence) | **DELETE** /v1/point_of_presences/{point_of_presence_id} | Delete a point of presence
[**get_cluster**](RegionsApi.md#get_cluster) | **GET** /v1/clusters/{cluster_id} | Get a Cluster
[**get_point_of_presence**](RegionsApi.md#get_point_of_presence) | **GET** /v1/point_of_presences/{point_of_presence_id} | Get a point of presence
[**list_clusters**](RegionsApi.md#list_clusters) | **GET** /v1/clusters | List all Clusters
[**list_point_of_presences**](RegionsApi.md#list_point_of_presences) | **GET** /v1/point_of_presences | List all regions
[**replace_cluster**](RegionsApi.md#replace_cluster) | **PUT** /v1/clusters/{cluster_id} | update a Cluster
[**replace_point_of_presence**](RegionsApi.md#replace_point_of_presence) | **PUT** /v1/point_of_presences/{point_of_presence_id} | update a point of presence


# **add_cluster**
> Cluster add_cluster(cluster)

Add a Cluster

Adds a new Cluster 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.cluster import Cluster
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    cluster = Cluster(
        metadata=MetadataWithId(),
        spec=ClusterSpec(
            name=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
            domain=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
            config=ClusterConfig(
                description="description_example",
                ip_addresses=[
                    "127.0.0.1",
                ],
            ),
        ),
    ) # Cluster | 

    # example passing only required values which don't have defaults set
    try:
        # Add a Cluster
        api_response = api_instance.add_cluster(cluster)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->add_cluster: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster** | [**Cluster**](Cluster.md)|  |

### Return type

[**Cluster**](Cluster.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New Cluster created |  -  |
**400** | The request is invalid |  -  |
**409** | Cluster already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_point_of_presence**
> PointOfPresence add_point_of_presence(point_of_presence)

Add a point of presence.

Adds a new point of presence. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.point_of_presence import PointOfPresence
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence = PointOfPresence(
        metadata=MetadataWithId(),
        spec=PointOfPresenceSpec(
            name=FeatureTagName("north-america"),
            tags=[
                FeatureTagName("north-america"),
            ],
            routing=PointOfPresenceRouting(
                domains=[
                    Domain("domains_example"),
                ],
            ),
            master_cluster_id="master_cluster_id_example",
            cluster_ids=[
                "123",
            ],
        ),
        status=PointOfPresenceStatus(
            master_cluster=Cluster(
                metadata=MetadataWithId(),
                spec=ClusterSpec(
                    name=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                    domain=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                    config=ClusterConfig(
                        description="description_example",
                        ip_addresses=[
                            "127.0.0.1",
                        ],
                    ),
                ),
            ),
            clusters=[
                Cluster(
                    metadata=MetadataWithId(),
                    spec=ClusterSpec(
                        name=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                        domain=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                        config=ClusterConfig(
                            description="description_example",
                            ip_addresses=[
                                "127.0.0.1",
                            ],
                        ),
                    ),
                ),
            ],
        ),
    ) # PointOfPresence | 

    # example passing only required values which don't have defaults set
    try:
        # Add a point of presence.
        api_response = api_instance.add_point_of_presence(point_of_presence)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->add_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence** | [**PointOfPresence**](PointOfPresence.md)|  |

### Return type

[**PointOfPresence**](PointOfPresence.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New region created |  -  |
**400** | The request is invalid |  -  |
**409** | region already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cluster**
> delete_cluster(cluster_id)

Delete a Cluster

Delete a Cluster

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    cluster_id = "aL31kzArc8YSA2" # str | cluster id in path

    # example passing only required values which don't have defaults set
    try:
        # Delete a Cluster
        api_instance.delete_cluster(cluster_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->delete_cluster: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| cluster id in path |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Cluster was deleted |  -  |
**404** | Cluster does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_point_of_presence**
> delete_point_of_presence(point_of_presence_id)

Delete a point of presence

Delete a point of presence

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence_id = "aL31kzArc8YSA2" # str | point of presence id in path

    # example passing only required values which don't have defaults set
    try:
        # Delete a point of presence
        api_instance.delete_point_of_presence(point_of_presence_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->delete_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence_id** | **str**| point of presence id in path |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | PointOfPresence was deleted |  -  |
**404** | PointOfPresence does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cluster**
> Cluster get_cluster(cluster_id)

Get a Cluster

Get a Cluster

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.cluster import Cluster
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    cluster_id = "aL31kzArc8YSA2" # str | cluster id in path

    # example passing only required values which don't have defaults set
    try:
        # Get a Cluster
        api_response = api_instance.get_cluster(cluster_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->get_cluster: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| cluster id in path |

### Return type

[**Cluster**](Cluster.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a Cluster |  -  |
**404** | Cluster does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_point_of_presence**
> PointOfPresence get_point_of_presence(point_of_presence_id)

Get a point of presence

Get a point of presence

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.point_of_presence import PointOfPresence
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence_id = "aL31kzArc8YSA2" # str | point of presence id in path

    # example passing only required values which don't have defaults set
    try:
        # Get a point of presence
        api_response = api_instance.get_point_of_presence(point_of_presence_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->get_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence_id** | **str**| point of presence id in path |

### Return type

[**PointOfPresence**](PointOfPresence.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a PointOfPresence |  -  |
**404** | PointOfPresence does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_clusters**
> ListClusterResponse list_clusters()

List all Clusters

List all Clusters matching the provided query parameters.  

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.list_cluster_response import ListClusterResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    page_at_name = "ca-1" # str | Pagination based query with the name as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_name` field from the list response.  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all Clusters
        api_response = api_instance.list_clusters(limit=limit, page_at_name=page_at_name)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->list_clusters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **page_at_name** | **str**| Pagination based query with the name as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_name&#x60; field from the list response.  | [optional]

### Return type

[**ListClusterResponse**](ListClusterResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query succeeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_point_of_presences**
> ListPointOfPresencesResponse list_point_of_presences()

List all regions

List all regions matching the provided query parameters. Perform keyset pagination by setting the page_at_name parameter to the name for the next page to fetch. Set it to `\"\"` to start from the beginning. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.list_point_of_presences_response import ListPointOfPresencesResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    name = "name-1" # str | Filters based on whether or not the items in the collection have the given name.  (optional)
    page_at_name = "ca-1" # str | Pagination based query with the name as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_name` field from the list response.  (optional)
    includes_all_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to include in the search. Each provided tag must match in order for the item to be returned.  (optional)
    includes_any_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to include in the search. If any provided tag matches then the item is returned.  (optional)
    excludes_all_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to exclude in the search. If all provided tags match, then the item is not returned.  (optional)
    excludes_any_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to exclude in the search. If any provided tag matches, then the item is not returned.  (optional)
    cluster_name = "ca-1" # str | query for specific cluster (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all regions
        api_response = api_instance.list_point_of_presences(limit=limit, name=name, page_at_name=page_at_name, includes_all_tag=includes_all_tag, includes_any_tag=includes_any_tag, excludes_all_tag=excludes_all_tag, excludes_any_tag=excludes_any_tag, cluster_name=cluster_name, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->list_point_of_presences: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **name** | **str**| Filters based on whether or not the items in the collection have the given name.  | [optional]
 **page_at_name** | **str**| Pagination based query with the name as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_name&#x60; field from the list response.  | [optional]
 **includes_all_tag** | **[str]**| A list of case-sensitive tags to include in the search. Each provided tag must match in order for the item to be returned.  | [optional]
 **includes_any_tag** | **[str]**| A list of case-sensitive tags to include in the search. If any provided tag matches then the item is returned.  | [optional]
 **excludes_all_tag** | **[str]**| A list of case-sensitive tags to exclude in the search. If all provided tags match, then the item is not returned.  | [optional]
 **excludes_any_tag** | **[str]**| A list of case-sensitive tags to exclude in the search. If any provided tag matches, then the item is not returned.  | [optional]
 **cluster_name** | **str**| query for specific cluster | [optional]
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**ListPointOfPresencesResponse**](ListPointOfPresencesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query succeeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_cluster**
> Cluster replace_cluster(cluster_id)

update a Cluster

update a Cluster

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.cluster import Cluster
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    cluster_id = "aL31kzArc8YSA2" # str | cluster id in path
    cluster = Cluster(
        metadata=MetadataWithId(),
        spec=ClusterSpec(
            name=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
            domain=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
            config=ClusterConfig(
                description="description_example",
                ip_addresses=[
                    "127.0.0.1",
                ],
            ),
        ),
    ) # Cluster |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # update a Cluster
        api_response = api_instance.replace_cluster(cluster_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->replace_cluster: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # update a Cluster
        api_response = api_instance.replace_cluster(cluster_id, cluster=cluster)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->replace_cluster: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| cluster id in path |
 **cluster** | [**Cluster**](Cluster.md)|  | [optional]

### Return type

[**Cluster**](Cluster.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated Cluster |  -  |
**400** | The request is invalid |  -  |
**404** | Cluster does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_point_of_presence**
> PointOfPresence replace_point_of_presence(point_of_presence_id)

update a point of presence

update a point of presence

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.point_of_presence import PointOfPresence
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence_id = "aL31kzArc8YSA2" # str | point of presence id in path
    point_of_presence = PointOfPresence(
        metadata=MetadataWithId(),
        spec=PointOfPresenceSpec(
            name=FeatureTagName("north-america"),
            tags=[
                FeatureTagName("north-america"),
            ],
            routing=PointOfPresenceRouting(
                domains=[
                    Domain("domains_example"),
                ],
            ),
            master_cluster_id="master_cluster_id_example",
            cluster_ids=[
                "123",
            ],
        ),
        status=PointOfPresenceStatus(
            master_cluster=Cluster(
                metadata=MetadataWithId(),
                spec=ClusterSpec(
                    name=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                    domain=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                    config=ClusterConfig(
                        description="description_example",
                        ip_addresses=[
                            "127.0.0.1",
                        ],
                    ),
                ),
            ),
            clusters=[
                Cluster(
                    metadata=MetadataWithId(),
                    spec=ClusterSpec(
                        name=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                        domain=Domain("uzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyv0.0.Gpul80FcVjSkp5k.L.Dw-v0dZfUofvKERjsmInY9s-EmMH6kw8gsnXv2Z7jRPK5L.A.q.W.M8pb-ziKqEde8fXg9wdpfxa2-zRi2iAxU4NCUavTrirUe4ba7JnjrgEdBCJZ.w.C.t.g-Vnrj9RmauFxv71lRsCE.Y.V.FKGSDRGKUIQh.KhXoEdbZpGptfI4pvLXGuLk-kwwO2jcMEEkIauW5ApNaDi5ackLaR2kw9-zmvqRnM-dar09VaHCQz0TlT4b42Jml4PJXMF.z8G0e5q9Z4WMWovY63Gk6ixTd5NxRU25mQYd6VBLRGkQ5H9-FH2v5iUaMQ6iIJ-7auxDSR-lIz.7w9bP3XhsKpT6YkX2ymMVYtYsFBx8OyxaBZ75cAidDZ6lvrLQxekRdyiJFjhCbEZunVXTqV3VP-DPO.H.i.VhY.t49MeAEDz67NG9dihNlL1YPO1GvRUDnbsR0-SswaNzc7s9ONPZw-HNPtVfykpnotMPK4Aqhv7VjToBNn1oLr"),
                        config=ClusterConfig(
                            description="description_example",
                            ip_addresses=[
                                "127.0.0.1",
                            ],
                        ),
                    ),
                ),
            ],
        ),
    ) # PointOfPresence |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # update a point of presence
        api_response = api_instance.replace_point_of_presence(point_of_presence_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->replace_point_of_presence: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # update a point of presence
        api_response = api_instance.replace_point_of_presence(point_of_presence_id, point_of_presence=point_of_presence)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->replace_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence_id** | **str**| point of presence id in path |
 **point_of_presence** | [**PointOfPresence**](PointOfPresence.md)|  | [optional]

### Return type

[**PointOfPresence**](PointOfPresence.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated PointOfPresence |  -  |
**400** | The request is invalid |  -  |
**404** | PointOfPresence does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

