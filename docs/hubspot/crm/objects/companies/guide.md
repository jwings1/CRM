> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Companies API

> Company records store data about businesses. The companies endpoints allow you to manage this data and sync it between HubSpot and other systems. 

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
  'crm.objects.companies.read',
  'crm.objects.companies.write'
]}
  />
</Accordion>

In HubSpot, companies store information about the organizations that interact with your business. The companies endpoints allow you to create and manage company records, as well as sync company data between HubSpot and other systems.

Learn more about objects, records, properties, and associations APIs in the [Understanding the CRM](/docs/api-reference/latest/crm/understanding-the-crm) guide. For more general information about objects and records in HubSpot, [learn how to manage your CRM database](https://knowledge.hubspot.com/get-started/manage-your-crm-database).

## Create companies

To create new companies, make a `POST` request to `/crm/objects/2026-09/companies`.

In your request, include your company data in a properties object. You can also add an associations object to associate your new company with existing records (e.g., contacts, deals), or activities (e.g., meetings, notes).

### Properties

Company details are stored in company properties. There are [default HubSpot company properties](https://knowledge.hubspot.com/properties/hubspot-crm-default-company-properties), but you can also [create custom properties](https://knowledge.hubspot.com/properties/create-and-edit-properties).

When creating a new company, you should include <u>at least one</u> of the following properties in your request: `name` or `domain`. It is recommended to always include `domain`, because domain names are the [primary unique identifier](https://knowledge.hubspot.com/records/deduplication-of-records#automatic-deduplication-in-hubspot) to avoid duplicate companies in HubSpot. If a company has [multiple domains](https://knowledge.hubspot.com/records/add-multiple-domain-names-to-a-company-record), you can add them through the API by using the `hs_additional_domains` field with semicolons separating each domain. For example: `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`.

To view all available properties, you can retrieve a list of your account's company properties by making a `GET` request to `/crm/properties/2026-09/companies`. Learn more about the [properties API](/docs/api-reference/latest/crm/properties/guide).

<Warning>
  **Please note:**

  If you've included `lifecyclestage` in your request, values must refer to the lifecycle stage's internal name. The internal names of default stages are text values, and do not change even if you edit the stage's [label](https://knowledge.hubspot.com/properties/create-and-edit-properties#:~:text=the%20properties%20settings.-,Label/Name%3A,-enter%20a%20unique)(e.g., `subscriber` or `marketingqualifiedlead`). The internal names of [custom stages](https://knowledge.hubspot.com/object-settings/create-and-customize-lifecycle-stages) are numeric values. You can find a stage's internal ID in your [lifecycle stage settings,](https://knowledge.hubspot.com/object-settings/create-and-customize-lifecycle-stages#:~:text=To%20edit%20a%20lifecycle%20stage%2C%20hover%20over%20the%20stage%20and%20click%20Edit.%20In%20the%20right%20panel%2C%20edit%20the%20Stage%20name%2C%20then%20click%20Edit%20lifecycle%20stage%20to%20confirm.%20Click%20the%20code%20codcode%20icon%20to%20view%20the%20stage%27s%20internal%20ID%2C%20which%20is%20used%20by%20integrations%20and%20APIs.) or by retrieving the lifecycle stage property via API.
</Warning>

For example, to create a new company, your request may look similar to the following:

```json theme={null}
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524"
  }
}
```

### Associations

When creating a new company, you can also associate the company with [existing records](https://knowledge.hubspot.com/records/associate-records) or [activities](https://knowledge.hubspot.com/records/associate-activities-with-records) in an associations object. For example, to associate a new company with an existing contact and email, your request would look like the following:

```json theme={null}
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524"
  },
  "associations": [
    {
      "to": {
        "id": 101
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 280
        }
      ]
    },
    {
      "to": {
        "id": 556677
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 185
        }
      ]
    }
  ]
}
```

In the associations object, you should include the following:

| Parameter | Description |
| - | - |
| `to` | The record or activity you want to associate with the company, specified by its unique `id` value. |
| `types` | The type of the association between the company and the record/activity. Include the `associationCategory`and `associationTypeId`. Default association type IDs are listed [here](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values), or you can retrieve the value for custom association types (i.e. labels) via the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-types). |

## Retrieve companies

You can retrieve companies individually or in batches.

* To retrieve an individual company, make a `GET` request to `/crm/objects/2026-09/companies/{companyId}`.
* To request a list of all companies, make a `GET` request to `/crm/objects/2026-09/companies`.

For these endpoints, you can include the following query parameters in the request URL:

| Parameter | Description |
| - | - |
| `properties` | A comma separated list of the properties to be returned in the response. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a company doesn't have a value, it will be returned as `null`. |
| `propertiesWithHistory` | A comma separated list of the current and historical properties to be returned in the response. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a company doesn't have a value, it will be returned as `null`. |
| `associations` | A comma separated list of objects to retrieve associated IDs for. Any specified associations that don't exist will not be returned in the response. Learn more about the [associations API.](/docs/api-reference/latest/crm/associations/associate-records/guide) |

* To retrieve a batch of specific companies by record ID or a [custom unique identifier property](/docs/api-reference/latest/crm/properties/guide#create-unique-identifier-properties), make a `POST` request to `crm/objects/2026-09/companies/batch/read`. The batch endpoint <u>cannot</u> retrieve associations. Learn how to batch read associations with the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide).

For the batch read endpoint, you can also use the optional `idProperty` parameter to retrieve companies by a custom [unique identifier property](/docs/api-reference/latest/crm/properties/guide#create-unique-identifier-properties). By default, the `id` values in the request refer to the record ID (`hs_object_id`), so the `idProperty` parameter is not required when retrieving by record ID. To use a custom unique value property to retrieve companies, you must include the `idProperty` parameter.

For example, to retrieve a batch of companies, your request could look like either of the following:

<Tabs>
  <Tab title="Email identifier">
    ```json theme={null}
    {
      "properties": ["name", "domain"],
      "inputs": [
        {
          "id": "56789"
        },
        {
          "id": "23456"
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Unique identifier">
    ```json theme={null}
    {
      "properties": ["name", "domain"],
      "idProperty": "uniquepropertyexample",
      "inputs": [
        {
          "id": "abc"
        },
        {
          "id": "def"
        }
      ]
    }
    ```
  </Tab>
</Tabs>

To retrieve companies with current and historical values for a property, your request could look like:

```json theme={null}
{
  "propertiesWithHistory": ["name"],
  "inputs": [
    {
      "id": "56789"
    },
    {
      "id": "23456"
    }
  ]
}
```

## Update companies

You can update companies individually or in batches. For existing companies, the company's record ID is a unique value that you can use to update the company via API.

To update an individual company by its company ID, make a `PATCH` request to `/crm/objects/2026-09/companies/{companyId}`, and include the data you want to update.

<Warning>
  **Please note:**

  If updating the `lifecyclestage` property, you can only set the value <u>forward</u> in the stage order. To set the lifecycle stage backward, you'll first need to clear the record's existing lifecycle stage value. The value can be [cleared manually](https://knowledge.hubspot.com/records/update-a-property-value-for-a-record), or may be automatically cleared via a [workflow](https://knowledge.hubspot.com/records/change-record-lifecycle-stages-in-bulk) or an integration that syncs contact data.
</Warning>

### Associate existing companies with records and activities

To associate a company with other CRM records or an activity, make a `PUT` request to `/crm/objects/2026-09/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

<Info>
  To retrieve the `associationTypeId` value, refer to [this list](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values) of default values, or make a `GET` request to `/crm/associations/2026-09/{fromObjectType}/{toObjectType}/labels`.
</Info>

Learn more about associating records with the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide).

### Remove an association

To remove an association between a company and a record or activity, make a `DELETE` request to the following URL: `/crm/objects/2026-09/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

## Merge companies

To merge two company records, make a `POST` request to `/crm/objects/2026-09/companies/merge`. The remaining record combines activities, associations, and most property values from both records. For example, merge duplicate companies to preserve historical context and consolidate their activity timelines. Learn more about [what happens when you merge HubSpot records](https://knowledge.hubspot.com/records/merge-records#what-happens-when-i-merge-records).

Include the following in your request body:

| Field | Description |
| - | - |
| `objectIdToMerge` | The record ID to merge with the primary record. |
| `primaryObjectId` | The record ID of the primary record, which is the record that will remain after the merge. |

For example, to merge the record `45678` into the record `12345`, your request would look like:

```json theme={null}
{
  "objectIdToMerge": "45678",
  "primaryObjectId": "12345"
}
```

In a successful merge response, the `id` is the record ID of the merged record.

<Warning>
  **Please note:** if an account is enrolled in the [*Primary ID Preservation for Merged Records* public beta](https://app.hubspot.com/l/product-updates/?rollout=318895), the primary (i.e., the remaining record after a merge) record's Record ID value (`primaryObjectId`) is preserved instead of generating a new one. Once enrolled, this behavior applies to all merges, including [in HubSpot](https://knowledge.hubspot.com/records/merge-records) and all versions of the API.
</Warning>

## Pin an activity on a company record

You can pin an activity on a company record via API by including the `hs_pinned_engagement_id` field in your request. In the field, include the `id` of the activity to pin, which can be retrieved via the [engagements APIs](/docs/api-reference/latest/overview). You can pin one activity per record, and the activity must already be associated with the company prior to pinning.

To set or update a company's pinned activity, your request could look like:

```json theme={null}
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

You can also create a company, associate it with an existing activity, and pin the activity in the same request. For example:

```json theme={null}
{
  "properties": {
    "domain": "example.com",
    "name": "Example Company",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": {
        "id": 123456789
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 189
        }
      ]
    }
  ]
}
```

## Delete companies

You can delete companies individually or in batches, which will add the company to the recycling bin in HubSpot. You can later [restore the company within HubSpot](https://knowledge.hubspot.com/records/restore-deleted-records).

To delete an individual company by its ID, make a `DELETE` request to `/crm/objects/2026-09/companies/{companyId}`.

Learn more about batch deleting companies in the [reference documentation](/docs/api-reference/latest/crm/objects/companies/batch/delete-companies).
