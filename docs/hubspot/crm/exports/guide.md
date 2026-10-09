> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Exports API

> Learn how to use the Exports API to export records in views or lists from your HubSpot account.

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
  'crm.export'
]}
  />
</Accordion>

Use the exports API to export records and property data from your HubSpot account, retrieve a URL to download an export file, or see the status of an export. Within HubSpot, you can also [export records](https://knowledge.hubspot.com/import-and-export/export-records) or [view a log of past exports in your account.](https://knowledge.hubspot.com/import-and-export/view-a-log-of-your-users-exports-in-your-account)

<Warning>
  When using an [OAuth](/docs/apps/developer-platform/build-apps/authentication/oauth/working-with-oauth) access token to authenticate requests to the exports API, the user installing the app must be a [Super Admin](https://knowledge.hubspot.com/user-management/hubspot-user-permissions-guide#super-admin) to grant the `crm.export` [scope](/docs/apps/developer-platform/build-apps/authentication/scopes).
</Warning>

## Start an export

To start an export, make a `POST` request to `/crm/exports/2026-09/export/async`. Your request body should specify information such as the file format, the object and properties you want to export, and the type of export you're completing (e.g., exporting an object view or a list). You can also filter the property data to be exported based on specific operators.

For both view and list exports, you can include the following fields in your request:

| Parameter | Description |
| - | - |
| `exportType` | The type of export, either `VIEW` (exports a view from an object index page) or `LIST` (exports a list). |
| `format` | The file format. Options include `XLSX`, `CSV`, or `XLS`. |
| `exportName` | The name of the export. |
| `language` | The language of the export file. Options include `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`. Learn more about [supported languages.](https://knowledge.hubspot.com/help-and-resources/hubspot-language-offerings) |
| `objectType` | The name or ID of the object you're exporting. For standard objects, you can use the object's name (e.g., `CONTACT`), but for custom objects, you must use the `objectTypeId` value. You can retrieve this value by making a `GET` request to `/crm-object-schemas/2026-09/schemas`. |
| `associatedObjectType` | The names or IDs of associated objects to include in the export. You can export up to four associated objects per request. For associated objects, the export will contain the associated record IDs of that object. If you export only one associated object or set the `includePrimaryDisplayPropertyForAssociatedObjects` field to `true`, the records' primary display property values will also be exported (e.g., `name` for companies). |
| `objectProperties` | A list of the properties you want included in your export. By default, property names and values are shown as the human-readable labels, but you can request internal names and values using the `exportInternalValuesOptions` parameter. |
| `includePrimaryDisplayPropertyForAssociatedObjects` | Include this field with the value `true` to export the primary display property values for all associated records (e.g., `name` for companies). If you're only exporting one associated object (indicated by the `associatedObjectType` field), this is set to `true` by default. If you're exporting more than one associated object, the value is set to `false` by default. |
| `includeLabeledAssociations` | Include this field with the value `true` to export [association labels](/docs/api-reference/latest/crm/associations/associations-schema/guide) to describe the relationship between associated records. |
| `exportInternalValuesOptions` | Include this array to export the internal values for property names and/or property values. In the array, include `NAMES` to export internal names of properties (shown as column headers) and/or `VALUES` to export internal property values (e.g., numerical values for custom pipeline stages or timestamps instead of human-readable dates). |
| `overrideAssociatedObjectsPerDefinitionPerRowLimit` | Include this field with the value `true` to override the default 1,000 association per row [limit](#limits). |

### Export a view

If you're exporting an [index page view](https://knowledge.hubspot.com/records/view-and-filter-records), your `exportType` value should be `VIEW`, and you can include the following field to filter and sort the records you're exporting:

| Parameter | Description |
| - | - |
| `publicCrmSearchRequest` | Indicates which data should be exported based on certain property values and search queries. You can include the following within the object:<br />`filterGroups`: the properties and property values to filter records by. Each group of `filters` is independent, which means separate groups follow OR logic. Criteria within one `filters` group follows AND logic. <br />`sorts`: the sort order of a property's values, either ascending, `ASC`, or descending, `DESC`.<br />`query`: a string to search the records' values for. |

For example, to export a filtered view of contacts and their associated company records, with the internal values of property names and values, your request would look like the following:

```json theme={null}
{
  "exportType": "VIEW",
  "exportName": "All contacts",
  "format": "xlsx",
  "language": "EN",
  "objectType": "CONTACT",
  "exportInternalValuesOptions": ["NAMES", "VALUES"],
  "objectProperties": ["email", "firstname", "lastname"],
  "associatedObjectType": "COMPANY",
  "publicCrmSearchRequest": {
    "filterGroups": [
      {
        "filters": [
          {
            "value": "is_borg",
            "operator": "NEQ",
            "property": "state"
          },
          {
            "value": "captain@federation.space",
            "operator": "EQ",
            "property": "email"
          }
        ]
      },
      {
        "filters": [
          {
            "value": "is_borg",
            "operator": "NEQ",
            "property": "state"
          },
          {
            "value": "lucas",
            "operator": "EQ",
            "property": "firstname"
          },
          {
            "value": "picard",
            "operator": "EQ",
            "property": "lastname"
          }
        ]
      }
    ],
    "sorts": [
      {
        "propertyName": "email",
        "order": "ASC"
      }
    ]
  }
}
```

### Export a list

If you're exporting a [list](https://knowledge.hubspot.com/segments/create-active-or-static-lists), your `exportType` value should be `LIST`, but you also need to specify the list you're exporting with the following field:

| Parameter | Description |
| - | - |
| `listId` | The [ILS List ID](https://knowledge.hubspot.com/segments/troubleshoot-lists#ils-list) of the list to export. You can find the ILS List ID value via the list details in HubSpot. Navigate to **Contacts** > **Lists**, hover over the **list** in the table, then click **Details**. In the right panel, click **Copy** **List ID** next to the ILS List ID value. Contact lists have two different ID values, but you <u>must</u> use the ILS List ID value in your request. |

For example, to export a list with the contacts' emails, your request may look like the following:

```json theme={null}
{
  "exportType": "LIST",
  "listId": 1234567,
  "exportName": "Marketing email contacts",
  "format": "xlsx",
  "language": "EN",
  "objectType": "CONTACT",
  "objectProperties": ["email"]
}
```

## Retrieve exports

When you successfully complete an export, the export's name, the export's `id`, and the number of records exported will be returned in the response. To retrieve an export from your HubSpot account, make a `GET` request to `/crm/exports/2026-09/export/async/tasks/{taskId}/status`.

When retrieving exports, the `status` of the export will also be returned. Possible statuses include `COMPLETE`, `PENDING`, `PROCESSING`, or `CANCELED`. For exports with a `COMPLETE` status, a URL is returned that you can use to download the exported file. The download URL will expire five minutes after the completed request. Once expired, you can perform another `GET` request to generate a new unique URL.

<Warning>
  Prior to expiration, an export's download URL can be accessed without any additional authorization. To protect your data, proceed with caution when sharing a URL or integrating with HubSpot via this API.
</Warning>

For example, the output for your request may be:

```json theme={null}
{
  "id": "123456",
  "exportName": "test-public-export",
  "exportType": "VIEW",
  "objectType": "0-1",
  "objectProperties": ["hs_object_id", "email", "firstname", "lastname", "createdate", "lastmodifieddate"],
  "createdAt": "2025-10-03T20:04:27.428Z",
  "updatedAt": "2025-10-03T20:04:28.192Z",
  "exportState": "DONE",
  "recordCount": 2
}
```

## Limits

The following limits apply:

* You can complete up to thirty exports within a rolling 24 hour window, and one export at a time. Additional exports will be queued until the previous export is completed.
* If you're completing a large export, you may receive multiple files delivered in a zip file. This will occur for CSV or XLSX files with more than 1,000,000 rows and XLS files with more than 65,535 rows. CSV files are also automatically zipped if the file is greater than 2MB, even if the file has less than 1,000,000 rows.
* By default, the number of associations per row is limited to 1,000 associations. If you want to override this limit, include the `overrideAssociatedObjectsPerDefinitionPerRowLimit` field with the value `true`.
