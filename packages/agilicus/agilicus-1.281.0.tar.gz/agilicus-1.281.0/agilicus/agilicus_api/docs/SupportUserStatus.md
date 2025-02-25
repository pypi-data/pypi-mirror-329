# SupportUserStatus

The current status of the support user.  The associating_user field contains the user object corresponding to this support user which associates to, controls permissions for and puts an expiry on the actual user who will be providing support. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The id of the User corresponding to the email in SupportUserSpec to which this support user record applies.  | [optional] 
**associating_user** | [**UserIdentity**](UserIdentity.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


