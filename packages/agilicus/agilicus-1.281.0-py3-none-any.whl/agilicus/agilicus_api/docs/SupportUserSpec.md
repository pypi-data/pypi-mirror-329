# SupportUserSpec

Configuration containing properties associated with a user that is allowed to provide support to the organisation. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_id** | **str** | Unique identifier | 
**email** | [**Email**](Email.md) |  | 
**expiry** | **datetime** | The support user time in UTC. Defaults to support user created time + 24h | 
**read_only** | **bool** | Whether or not this support user is allowed to make modifications in this organisation  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


