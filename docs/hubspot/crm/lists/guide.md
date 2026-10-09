> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 174d5e58-cbbd-4c54-9991-14434f734813
---

# Segments API

> Retrieve, create, and manage segments (lists).

export const ScopesList = ({scopes = [], description = "This API requires one of the following scopes:"}) => {
  if (!scopes || scopes.length === 0) {
    return null;
  }
  const sortedScopes = scopes.sort((a, b) => a.localeCompare(b));
  return <div>
      <div className="text-sm mb-2">{description}</div>
      <div>
        {sortedScopes.map((scope, index) => <div key={index}>
            <code>
              <span className="text-xs">{scope}</span>
            </code>
          </div>)}
      </div>
    </div>;
};

<Accordion title="Required Scopes" icon="key">
  <ScopesList
    scopes={[
 'cms.membership.access_groups.write',
 'crm.lists.read',
 'crm.lists.write'
]}
  />
</Accordion>

Use the Segments (Lists) API to create and manage segments. For example, create a segment of good-fit leads to send a marketing email or group high-priority deals.

Learn more about using [segments](https://knowledge.hubspot.com/segments/create-active-or-static-lists) in HubSpot.

## What’s new in 2026-09

In the `2026-09` version of the Segments (Lists) API, a new search endpoint (`/crm/lists/2026-09/all`) was added that sorts results by segment ID in ascending order. Pagination for this endpoint uses a cursor (`after`), so you can page through all segments by making additional calls with the cursor.

Learn more about [reading segments](#retrieve-all-segments).

## Create segments

To create a segment, make a `POST` request to `/crm/lists/2026-09/`.

In the request body, you must include the following fields: `name`, `objectTypeId`, and `processingType`. The `filterBranch` parameter is optional, and can be included to create branching logic for `DYNAMIC` and `SNAPSHOT` type segments. Learn more about [configuring segment filters and branches](/docs/api-reference/latest/crm/lists/filters/guide).

### Processing types

There are three `processingType` values for segments: `MANUAL`, `DYNAMIC`, and `SNAPSHOT`.

* `MANUAL`: records can only be added to or removed from the segment via manual actions by the user or API call. There is no segment processing or segment membership management done in the background by HubSpot's systems. This type of segment is helpful for when you need a set group of records that won't change unless manually updated.
* `DYNAMIC`: [filters](/docs/api-reference/latest/crm/lists/filters/guide) are used to determine which records become segment members. This type of segment is processed in the background by HubSpot to ensure that the segment only contains records that match the filters. Whenever a record changes, it is reevaluated against the filters and is either added or removed. This type of segment is helpful for when you want to keep a running group that you expect to change over time.
* `SNAPSHOT`: [filters](/docs/api-reference/latest/crm/lists/filters/guide) are specified at the time of segment creation. After initial processing is completed, records can only be added to or removed from the segment by manual actions. This type of segment is helpful for when you want to create a group of records based on specific criteria, but don't want that segment to change automatically after initial processing.

### Example

For example, the following request body would create a new static segment of contacts:

```json theme={null}
{
  "name": "My static segment",
  "objectTypeId": "0-1",
  "processingType": "MANUAL"
}
```

Once created, a `listId` (the ILS list ID) will be generated. This ID is used for future updates and modifications. The following is an example response with the ILS list ID highlighted:

```json highlight={3} theme={null}
{
  "list": {
    "listId": "611",
    "listVersion": 1,
    "createdAt": "2026-02-02T16:13:48.146Z",
    "updatedAt": "2026-02-02T16:13:48.146Z",
    "filtersUpdatedAt": "2026-02-02T16:13:48.146Z",
    "processingStatus": "COMPLETE",
    "createdById": "9586504",
    "updatedById": "9586504",
    "processingType": "MANUAL",
    "objectTypeId": "0-1",
    "name": "My static segment",
    "listPermissions": {
      "teamsWithEditAccess": [],
      "usersWithEditAccess": []
    },
    "membershipSettings": {
      "membershipTeamId": null,
      "includeUnassigned": null
    }
  }
}
```

## Retrieve segments

Depending on your use case, there are multiple ways to retrieve segments. A segment can be retrieved by its name and object or by its ILS list ID. When retrieving segments, include a query parameter of `includeFilters=true` to return [segment filter definitions](/docs/api-reference/latest/crm/lists/filters/guide) in the response.

### Retrieve all segments

To read all segments, sorted by ID, make a `POST` request to `/crm/lists/2026-09/all`.

To retrieve all segments, add an empty request body. To retrieve specific segments, you can include the following optional filters.

| Filter | Type | Description |
| - | - | - |
| `objectTypeId` | String | The CRM object for which to return segments. You can find a full list of object type IDs [here](/docs/api-reference/latest/crm/understanding-the-crm#object-type-ids). |
| `processingTypes` | Array | The types of segment to view: `MANUAL`, `DYNAMIC`, or `SNAPSHOT`. |
| `count` | Number | Set the number of results per page. By default, 20 segments are returned per page, but you can request up to 500 per page. |
| `additionalProperties` | Array | Other segment properties to return for each segment in the response. |
| `after` | String | In subsequent requests, include the `after` value returned in the response to retrieve the next page of results. |

Segments are returned in ascending ID order. By default, the following properties are returned for each segment if there are values:

| Field | Description |
| - | - |
| `listId` | The segment's ILS ID. |
| `listVersion` | The current version of the segment. |
| `createdAt` | The date and time the segment was created. |
| `updatedAt` | The date and time of the latest update to the segment. |
| `filtersUpdatedAt` | The date and time of the latest update to the segment's filters. |
| `processingStatus` | The segment's processing status: `COMPLETE`, `PAUSED`, or `PROCESSING`. |
| `createdById` | The ID of the user that created the segment. |
| `updatedById` | The ID of the user that last updated the segment. |
| `processingType` | The type of segment: `MANUAL`, `DYNAMIC`, or `SNAPSHOT`. |
| `objectTypeId` | The ID of the type of the object in the segment. |
| `name` | The name of the segment. |
| `additionalProperties` | An object with additional segment metadata. Includes `hs_list_size` and `hs_list_reference_count` by default, and will include other properties if there are values, including: `hs_folder_name`, `hs_last_record_added_at`, and `hs_last_record_removed_at`. You can request other specific properties by including `additionalProperties` in your request. |

For example, to retrieve active contact segments (five per page) with their descriptions, your request body would look like:

```json theme={null}
{
  "processingTypes": ["DYNAMIC"],
  "objectTypeId": "0-1",
  "count": 5,
  "additionalProperties": ["hs_description"]
}
```

Your response would look like:

```json expandable theme={null}
{
  "results": [
    {
      "listId": "53",
      "listVersion": 2,
      "createdAt": "2020-01-09T20:47:03.539Z",
      "updatedAt": "2020-12-24T02:47:16.212Z",
      "filtersUpdatedAt": "2020-01-09T20:47:03.539Z",
      "processingStatus": "COMPLETE",
      "createdById": "9586504",
      "processingType": "DYNAMIC",
      "objectTypeId": "0-1",
      "name": "Tech Companies",
      "additionalProperties": {
        "hs_description": "Good-fit tech companies",
        "hs_list_reference_count": "0",
        "hs_last_record_added_at": "1740405014244",
        "hs_last_record_removed_at": "1769941583344",
        "hs_list_size": "68"
      }
    },
    {
      "listId": "55",
      "listVersion": 2,
      "createdAt": "2020-01-15T15:10:16.823Z",
      "updatedAt": "2020-12-24T02:47:16.212Z",
      "filtersUpdatedAt": "2020-01-15T15:10:16.823Z",
      "processingStatus": "COMPLETE",
      "createdById": "9586504",
      "processingType": "DYNAMIC",
      "objectTypeId": "0-1",
      "name": "MQLs",
      "additionalProperties": {
        "hs_list_reference_count": "0",
        "hs_last_record_added_at": "1726766929847",
        "hs_last_record_removed_at": "1732133659385",
        "hs_list_size": "24"
      }
    },
    {
      "listId": "57",
      "listVersion": 2,
      "createdAt": "2020-01-15T15:12:45.348Z",
      "updatedAt": "2020-12-24T02:47:16.212Z",
      "filtersUpdatedAt": "2020-01-15T15:12:45.348Z",
      "processingStatus": "COMPLETE",
      "createdById": "9586504",
      "processingType": "DYNAMIC",
      "objectTypeId": "0-1",
      "name": "Customers",
      "additionalProperties": {
        "hs_list_reference_count": "1",
        "hs_last_record_added_at": "1744036843676",
        "hs_last_record_removed_at": "1777623926634",
        "hs_list_size": "0"
      }
    },
    {
      "listId": "58",
      "listVersion": 2,
      "createdAt": "2020-01-15T15:14:13.180Z",
      "updatedAt": "2020-12-24T02:47:16.212Z",
      "filtersUpdatedAt": "2020-01-15T15:14:13.180Z",
      "processingStatus": "COMPLETE",
      "createdById": "9586504",
      "processingType": "DYNAMIC",
      "objectTypeId": "0-1",
      "name": "Sales Job Titles",
      "additionalProperties": {
        "hs_list_reference_count": "0",
        "hs_last_record_removed_at": "1671038817928",
        "hs_list_size": "0"
      }
    },
    {
      "listId": "59",
      "listVersion": 1,
      "createdAt": "2025-02-10T17:12:18.294Z",
      "updatedAt": "2025-02-10T17:12:18.294Z",
      "filtersUpdatedAt": "2025-02-10T17:12:18.294Z",
      "processingStatus": "COMPLETE",
      "createdById": "9586504",
      "updatedById": "9586504",
      "processingType": "DYNAMIC",
      "objectTypeId": "0-1",
      "name": "Recent marketing email opens",
      "additionalProperties": {
        "hs_description": "Contacts with recent marketing email opens (last 30 days)",
        "hs_list_reference_count": "0",
        "hs_list_size": "0"
      }
    }
  ],
  "paging": {
    "next": {
      "after": "eyJsaXN0SWQiOiI1OSIsIm9iamVjdFR5cGVJZCI6IjAtMSIsInByb2Nlc3NpbmdUeXBlcyI6WyJEWU5BTUlDIl19"
    }
  }
}
```

To request the next page of results, using the `after` string, your request body would look like:

```json theme={null}
{
  "processingTypes": ["DYNAMIC"],
  "objectTypeId": "0-1",
  "count": 5,
  "after": "eyJsaXN0SWQiOiI1OSIsIm9iamVjdFR5cGVJZCI6IjAtMSIsInByb2Nlc3NpbmdUeXBlcyI6WyJEWU5BTUlDIl19",
  "additionalProperties": ["hs_description"]
}
```

You may run into the following validation errors when using the `/crm/lists/2026-09/all` endpoint.

| Status | Validation error subcategory | Description |
| - | - | - |
| `400` | `INVALID_CURSOR` | This occurs when the `after` token is malformed or invalid, or if the `objectTypeId` or `processingTypes` filters changed between pages. Verify you're using the correct `after` value from the response and the same filters from your previous request body. |
| `400` | `INVALID_PROCESSING_TYPE` | This occurs when one or more values in the `processingTypes` filter do not match a known processing type. Use one of the supported `processingTypes` options in your filter: `MANUAL`, `DYNAMIC`, or `SNAPSHOT`. |

### Retrieve by segment name

To retrieve a segment by name, make a `GET` request to `/crm/lists/2026-09/object-type-id/{objectTypeId}/name/{listName}`. The `objectTypeId` is the ID that corresponds to the type of object stored by the segment. See the [full list of object type IDs](/docs/api-reference/latest/crm/understanding-the-crm#object-type-ids).

For example, to retrieve the contact segment [created above](#create-segments), make a `GET` request to `/crm/lists/2026-09/object-type-id/0-1/name/My%20static%20segment`.

### Retrieve by ILS list ID

A segment's ILS ID is returned in the `listId` field when a new segment is created. To find an existing segment's ILS ID, you can either:

* Navigate to the segments tool in HubSpot. Hover over the **segment**, then click **Details**. Learn more about [viewing segments](https://knowledge.hubspot.com/segments/edit-or-delete-lists#preview-segment-details-and-filters).
* [Search for a segment](#retrieve-by-searching-segment-details) by other criteria, then view the `listId` in the response.

To retrieve segments by ILS ID:

* To retrieve an individual segment by ILS list ID, make a `GET` request to `/crm/lists/2026-09/{listId}`.
* To retrieve multiple segments by ILS list ID, make a `GET` request to `/crm/lists/2026-09` and include a `listIds` query parameter for each segment. For example: `/crm/lists/2026-09?listIds=940&listIds=938`.

### Retrieve by searching segment details

You can search for segments by other criteria by making a `POST` request to `/crm/lists/2026-09/search`.

In the request body, specify the criteria that you want to search by.

* To search for segments that contain specific words in their name, include the `query` field.
* To search for segments of a specific processing type, include a `processingTypes` array with each of the processing types you want to search by.
* To search for segments of a specific object, include the `objectTypeId` field, with the [type ID value](/docs/api-reference/latest/crm/understanding-the-crm#object-type-ids) for the object (e.g., `0-1` for contacts).

For example, to search for contact static segments that contain "HubSpot" in the name, your request body would look like:

```json theme={null}
{
  "query": "HubSpot",
  "processingTypes": ["MANUAL"],
  "objectTypeId": "0-1"
}
```

## Update segments

### Update segment names

To update a segment's name, make a `PUT` request to `/crm/lists/2026-09/{listId}/update-list-name` with the `listName` query parameter. If the segment with the provided ILS list ID exists, then its name will be updated to the provided `listName`. The `listName` must be unique within the account.

You can also include a query parameter of `includeFilters=true` to return segment filter definitions in the response.

For example, to change a segment's name (with the ILS ID `612`) to "January Event Contacts Segment" and return filters, the request URL would be: `/crm/lists/2026-09/612/update-list-name?listName=January%20Event%20Contacts%20Segment&includeFilters=true`. Expand the section below to review an example of the expected response.

<Expandable title="Example response">
  ```json theme={null}
  {
    "updatedList": {
      "listId": "612",
      "listVersion": 1,
      "createdAt": "2026-02-02T16:34:48.872Z",
      "updatedAt": "2026-02-02T16:34:48.872Z",
      "filtersUpdatedAt": "2026-02-02T16:34:48.872Z",
      "processingStatus": "COMPLETE",
      "createdById": "9586504",
      "updatedById": "9586504",
      "processingType": "DYNAMIC",
      "objectTypeId": "0-1",
      "name": "January Event Contacts Segment",
      "filterBranch": {
        "filterBranches": [
          {
            "filterBranches": [],
            "filters": [
              {
                "property": "email",
                "operation": {
                  "operator": "IS_KNOWN",
                  "includeObjectsWithNoValueSet": false,
                  "operationType": "ALL_PROPERTY"
                },
                "filterType": "PROPERTY"
              },
              {
                "property": "hs_content_membership_email_confirmed",
                "operation": {
                  "operator": "IS_BETWEEN",
                  "includeObjectsWithNoValueSet": false,
                  "lowerBoundEndpointBehavior": "INCLUSIVE",
                  "upperBoundEndpointBehavior": "INCLUSIVE",
                  "propertyParser": "UPDATED_AT",
                  "lowerBoundTimePoint": {
                    "timezoneSource": "CUSTOM",
                    "zoneId": "US/Eastern",
                    "indexReference": {
                      "referenceType": "TODAY"
                    },
                    "offset": {
                      "days": -15
                    },
                    "timeType": "INDEXED"
                  },
                  "upperBoundTimePoint": {
                    "timezoneSource": "CUSTOM",
                    "zoneId": "US/Eastern",
                    "indexReference": {
                      "referenceType": "NOW"
                    },
                    "timeType": "INDEXED"
                  },
                  "type": "TIME_RANGED",
                  "operationType": "TIME_RANGED"
                },
                "filterType": "PROPERTY"
              }
            ],
            "filterBranchType": "AND",
            "filterBranchOperator": "AND"
          }
        ],
        "filters": [],
        "filterBranchType": "OR",
        "filterBranchOperator": "OR"
      },
      "listPermissions": {
        "teamsWithEditAccess": [],
        "usersWithEditAccess": []
      },
      "membershipSettings": {
        "membershipTeamId": null,
        "includeUnassigned": true
      }
    }
  }
  ```
</Expandable>

### Update segment filters

To update a `DYNAMIC` segment's [filter branches](/docs/api-reference/latest/crm/lists/filters/guide), make a `PUT` request to `/crm/lists/2026-09/{listId}/update-list-filters`. In the request body, include the updated filter branch definition. This definition will replace the existing definition, so include any filters you want to keep from the previous definition. Once the filter branch is updated, the segment will begin processing its new memberships.

For example, your segment includes a filter based on contact's *Likelihood to close* (`hs_predictivecontactscore_v2`) that you want to keep. To add filters to include contacts with a value for `email` who also opted into certain email subscriptions, your request body would look like:

```json theme={null}
{
  "filterBranch": {
    "filterBranchType": "OR",
    "filterBranches": [
      {
        "filterBranchType": "AND",
        "filters": [
          {
            "filterType": "PROPERTY",
            "operation": {
              "operationType": "NUMBER",
              "operator": "IS_GREATER_THAN_OR_EQUAL_TO",
              "value": 12
            },
            "property": "hs_predictivecontactscore_v2"
          },
          {
            "filterType": "PROPERTY",
            "operation": {
              "operationType": "ALL_PROPERTY",
              "operator": "IS_KNOWN"
            },
            "property": "email"
          },
          {
            "acceptedStatuses": [
              "OPT_IN"
            ],
            "filterType": "EMAIL_SUBSCRIPTION",
            "subscriptionIds": [
              "81537745",
              "321981152"
            ]
          }
        ]
      }
    ]
  }
}
```

## Delete and restore a segment

To delete a segment, make a `DELETE` request to `/crm/lists/2026-09/{listId}`.

Once deleted, segments can be restored within 90 days of deletion by making a `PUT` request to `/crm/lists/2026-09/{listId}/restore`. Segments deleted more than 90 days ago <u>cannot</u> be restored.

## Manage segment membership

To view and manage records included in a segment, you can use the `/memberships/` endpoints below. Segment membership endpoints that update memberships can only be used on `MANUAL` or `SNAPSHOT` segment processing types.

`DYNAMIC` segments will add and remove records based on the filter criteria set. You <u>cannot</u> use segment membership endpoints to update your segment. Instead, [edit the segment's filters](#update-segment-filters) or [edit the record](/docs/api-reference/latest/crm/using-object-apis) you want to add or remove.

### Retrieve records with segment memberships

To retrieve records with segment memberships, you'll need to make two calls: one to retrieve the records, then another to retrieve their segment memberships.

First, make a [search request to the objects API](/docs/api-reference/latest/crm/using-object-apis#retrieve-records-based-on-criteria) with the object for which you want to search records (e.g.,`0-1` for contacts). You can add [filters](/docs/api-reference/latest/crm/search-the-crm#filter-search-results) to specify the records you want.

* To retrieve recently created records, filter by `createdate`.
* To retrieve recently updated records, filter by `lastmodifieddate`.

You can add properties to retrieve more details about the records as needed.

For example, to search for contacts edited after May 31, 2025:

```json theme={null}
{
  "properties": [
    "firstname",
    "lastname",
    "email",
    "hs_object_id",
    "createdate",
    "lastmodifieddate"
  ],
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "lastmodifieddate",
          "operator": "GT",
          "value": "2025-05-31"
        }
      ]
    }
  ]
}
```

Next, use the object endpoint to retrieve the membership details for the records individually or in bulk. From your search request, use record `id` values to retrieve segment membership details.

To retrieve an individual record's memberships, make a `GET` request to `/crm/lists/2026-09/records/{objectTypeId}/{recordId}/memberships`. For example, to retrieve an individual contact's memberships, your request URL would look like `/crm/lists/2026-09/records/0-1/1234567/memberships`.

Your response will look like:

```json theme={null}
{
  "results": [
    {
      "listId": "76",
      "listVersion": 1,
      "isPublicList": true,
      "firstAddedTimestamp": "2025-07-28T13:42:08.595Z",
      "lastAddedTimestamp": "2025-07-28T13:42:08.595Z"
    },
    {
      "listId": "78",
      "listVersion": 1,
      "isPublicList": true,
      "firstAddedTimestamp": "2025-07-28T13:42:08.595Z",
      "lastAddedTimestamp": "2025-07-28T13:42:08.595Z"
    },
    {
      "listId": "493",
      "listVersion": 1,
      "isPublicList": false,
      "firstAddedTimestamp": "2024-07-23T19:40:36.192Z",
      "lastAddedTimestamp": "2024-07-23T19:40:36.192Z"
    },
    {
      "listId": "541",
      "listVersion": 1,
      "isPublicList": true,
      "firstAddedTimestamp": "2025-04-21T14:01:43.475Z",
      "lastAddedTimestamp": "2025-04-21T14:01:43.475Z"
    },
    {
      "listId": "492",
      "listVersion": 1,
      "isPublicList": false,
      "firstAddedTimestamp": "2024-07-23T19:36:11.890Z",
      "lastAddedTimestamp": "2024-07-23T19:36:11.890Z"
    }
  ]
}
```

To retrieve multiple records' memberships, make a `POST` request to `/crm/lists/2026-09/records/memberships/batch/read`. In the request, include the `objectTypeId` value of the object for which you're retrieving records (e.g., `0-1` for contacts) and the `id` values for the records.

For example, to retrieve memberships for contacts `12345` and `101112`, your request would look like:

```json theme={null}
{
  "inputs": [
    {
      "objectTypeId": "0-1",
      "recordId": "12345"
    },
    {
      "objectTypeId": "0-1",
      "recordId": "101112"
    }
  ]
}
```

### View records in an existing segment

To view all records in an existing segment, make a `GET` request to `/crm/lists/2026-09/{listId}/memberships`. This returns all members of a segment ordered by `recordId`.

### Add records to an existing segment

To add records to an existing segment, make a `PUT` request to `/crm/lists/2026-09/{listId}/memberships/add` with a list of record IDs in the request body.

For example, your request body would look like:

```json theme={null}
[
  "55555",
  "69876",
  "487888",
  "46999874"
]
```

### Remove records from an existing segment

To remove all records from an existing segment, make a `DELETE` request to `/crm/lists/2026-09/{listId}/memberships`. This will <u>not</u> delete the segment from your account, but the segment will contain no records.

To remove specific records from an existing segment, make a `PUT` request to `/crm/lists/2026-09/{listId}/memberships/remove` with a list of record IDs in the request body.

For example, your request body would look like:

```json theme={null}
[
  "12345",
  "55986",
  "489756"
]
```

### Add and remove records in the same request

To both add records to and remove records from a segment at the same time, make a `PUT` request to `/crm/lists/2026-09/{listId}/memberships/add-and-remove`. In the request body, include the `recordIdsToAdd` and `recordIdsToRemove` fields with the IDs of records to add and remove.

For example, your request body would look like:

```json theme={null}
{
  "recordIdsToAdd": [
    "123",
    "456",
    "789"
  ],
  "recordIdsToRemove": [
    "654",
    "5555"
  ]
}
```

### Add records from one segment to another

To add all records from one segment to another segment, make a `PUT` request to `/crm/lists/2026-09/{listId}/memberships/add-from/{sourceListId}`. The `listId` is the segment to add the records to and the `sourceListId` is the segment to retrieve records from. You can move a limit of 100,000 records at a time.

### Retrieve members by join order

To retrieve members of a segment ordered by when they joined, make a `GET` request to `/crm/lists/2026-09/{listId}/memberships/join-order`.

You can include the following optional query parameters to control pagination:

| Parameter | Type | Description |
| - | - | - |
| `after` | String | A cursor token returned in the previous response to retrieve the next page of results. |
| `before` | String | A cursor token to retrieve results before a specific point. |
| `limit` | Number | The maximum number of results to return per page. Defaults to 100. |

## Convert segments from active to static

You can [convert existing active segments into static segments](https://knowledge.hubspot.com/segments/change-list-type) by scheduling the conversion for a specific date or based on inactivity. You can use the segments endpoints to schedule conversions, retrieve scheduled or past conversions, and delete scheduled conversions.

### Schedule or update a segment conversion

To schedule a conversion or update an existing scheduled conversion, make a `PUT` request to `/crm/lists/2026-09/{listId}/schedule-conversion`.

In the request body, include one of the following `conversionType` values and the type's related fields:

* `CONVERSION_DATE`: schedules the conversion for a specific date. Include `year`, `month`, and `day` fields to specify the desired date. This date must be in the future.
* `INACTIVITY`: schedules the conversion if the segment hasn't been active for a set amount of time, based on when the last record was added or removed. Include the `timeUnit` field to specify the unit of time (`DAY`, `WEEK`, or `MONTH`) and the `offset` field to specify the amount of time after which the segment is considered inactive. Only one `timeUnit` can be specified and the `offset` value must be positive.

For example, to schedule an active segment to be converted to a static segment on January 31, 2025, your request would look like the following:

<Tabs>
  <Tab title="JSON">
    ```json theme={null}
    {
      "conversionType": "CONVERSION_DATE",
      "year": 2025,
      "month": 1,
      "day": 31
    }
    ```
  </Tab>
</Tabs>

To schedule an active segment to be converted to a static segment after five days of inactivity, your request would look like the following:

<Tabs>
  <Tab title="JSON">
    ```json theme={null}
    {
      "conversionType": "INACTIVITY",
      "timeUnit": "DAY",
      "offset": 5
    }
    ```
  </Tab>
</Tabs>

### Retrieve a segment conversion

To retrieve information about a segment's conversion, make a `GET` request to `/crm/lists/2026-09/{listId}/schedule-conversion`. The response will include the `requestedConversionTime` object with the `conversionType` and the relevant fields for that type. If the segment was already converted, the `convertedAt` field will be returned with the timestamp of the conversion.

For example, for a segment that completed a conversion, your response would look similar to the following:

```json theme={null}
{
  "listId": "35",
  "requestedConversionTime": {
    "conversionType": "CONVERSION_DATE",
    "year": 2025,
    "month": 1,
    "day": 1
  },
  "convertedAt": "2025-01-01T05:20:34.002Z"
}
```

### Delete a scheduled segment conversion

To delete a conversion, make a `DELETE` request to `/crm/lists/2026-09/{listId}/schedule-conversion`. If the conversion does not exist, a 404 will be returned.

## Manage segment folders

Segments can be organized into folders to help you manage large numbers of segments in your account. You can retrieve, create, rename, move, and delete folders using the `/folders` endpoints.

### Retrieve folders

To retrieve your folder structure, make a `GET` request to `/crm/lists/2026-09/folders`.

By default, this returns the root folder. To navigate into a specific folder, include the `folderId` query parameter. The response includes the following fields for the folder:

| Field | Type | Description |
| - | - | - |
| `id` | String | The unique identifier of the folder. |
| `name` | String | The name of the folder. |
| `parentFolderId` | String | The ID of the parent folder. |
| `childNodes` | Array | IDs of child folders nested within this folder. |
| `childLists` | Array | IDs of segments directly within this folder. |
| `createdAt` | String | The date and time the folder was created. |
| `updatedAt` | String | The date and time the folder was last updated. |
| `updatedContentsAt` | String | The date and time the folder's contents were last updated. |

### Create a folder

To create a folder, make a `POST` request to `/crm/lists/2026-09/folders`. In the request body, include the `name` for the new folder. To nest the folder inside an existing folder, include the `parentFolderId` of the parent.

For example, to create a folder called "Marketing segments" at the root level, your request body would look like:

```json theme={null}
{
  "name": "Marketing segments"
}
```

To create a subfolder inside an existing folder with ID `42`, your request body would look like:

```json theme={null}
{
  "name": "Q3 campaigns",
  "parentFolderId": "42"
}
```

### Move a segment to a folder

To move a segment into a folder, make a `PUT` request to `/crm/lists/2026-09/folders/move-list`. In the request body, include the `listId` of the segment to move and the `newFolderId` of the destination folder.

For example, to move segment `611` into folder `42`, your request body would look like:

```json theme={null}
{
  "listId": "611",
  "newFolderId": "42"
}
```

### Rename a folder

To rename a folder, make a `PUT` request to `/crm/lists/2026-09/folders/{folderId}/rename` and include the `newFolderName` query parameter with the new name.

For example, to rename folder `42` to "Q4 campaigns", the request URL would be: `/crm/lists/2026-09/folders/42/rename?newFolderName=Q4%20campaigns`.

### Move a folder

To move a folder into a different parent folder, make a `PUT` request to `/crm/lists/2026-09/folders/{folderId}/move/{newParentFolderId}`, where `folderId` is the folder to move and `newParentFolderId` is the destination parent folder.

### Delete a folder

To delete a folder, make a `DELETE` request to `/crm/lists/2026-09/folders/{folderId}`.

## Translate legacy list IDs

If you have existing integrations that use legacy list IDs, you can use the `/idmapping` endpoints to retrieve the corresponding current ILS list IDs.

### Translate a single legacy ID

To retrieve the current ILS list ID for a single legacy list, make a `GET` request to `/crm/lists/2026-09/idmapping` with the `legacyListId` query parameter.

For example: `/crm/lists/2026-09/idmapping?legacyListId=123`.

The response returns both the `legacyListId` and the corresponding `listId`.

### Translate multiple legacy IDs

To translate multiple legacy list IDs in a single request, make a `POST` request to `/crm/lists/2026-09/idmapping` with an array of legacy list IDs in the request body.

For example, to translate three legacy IDs, your request body would look like:

```json theme={null}
[
  "123",
  "456",
  "789"
]
```

The response includes:

* `legacyListIdsToIdsMapping`: an array of objects, each containing the `legacyListId` and its corresponding current `listId`.
* `missingLegacyListIds`: an array of any legacy IDs that could not be found.

## Retrieve segment size and edit history

To retrieve the historical size data and edit timestamps for a segment over a date range, make a `GET` request to `/crm/lists/2026-09/{listId}/size-and-edits-history/between`.

Include the following required query parameters:

| Parameter | Type | Description |
| - | - | - |
| `startDate` | String | The start of the date range, formatted as an ISO 8601 date-time string (e.g., `2025-01-01T00:00:00Z`). |
| `endDate` | String | The end of the date range, formatted as an ISO 8601 date-time string (e.g., `2025-06-30T23:59:59Z`). |

The response includes:

* `sizeHistory`: an array of data points showing the segment's size over time within the requested range.
* `editHistory`: an array of timestamps indicating when the segment was edited within the requested range.
