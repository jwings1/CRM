> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Associate records

> Use the associations API to create, manage, and remove associations between CRM records.

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

<Warning>
  For the previous version, please see the documentation for the [v3 Associations API](/docs/api-reference/latest/crm/associations/associate-records/guide).
</Warning>

<Accordion title="Required Scopes" icon="key">
  <ScopesList
    scopes={[
  'crm.objects.appointments.read',
  'crm.objects.appointments.sensitive.read.v2',
  'crm.objects.appointments.sensitive.write.v2',
  'crm.objects.appointments.write',
  'crm.objects.carts.read',
  'crm.objects.carts.write',
  'crm.objects.commercepayments.read',
  'crm.objects.commercepayments.write',
  'crm.objects.companies.highly_sensitive.read.v2',
  'crm.objects.companies.highly_sensitive.write.v2',
  'crm.objects.companies.read',
  'crm.objects.companies.sensitive.read.v2',
  'crm.objects.companies.sensitive.write.v2',
  'crm.objects.companies.write',
  'crm.objects.contacts.highly_sensitive.read.v2',
  'crm.objects.contacts.highly_sensitive.write.v2',
  'crm.objects.contacts.read',
  'crm.objects.contacts.sensitive.read.v2',
  'crm.objects.contacts.sensitive.write.v2',
  'crm.objects.contacts.write',
  'crm.objects.courses.read',
  'crm.objects.courses.write',
  'crm.objects.custom.highly_sensitive.read.v2',
  'crm.objects.custom.highly_sensitive.write.v2',
  'crm.objects.custom.read',
  'crm.objects.custom.sensitive.read.v2',
  'crm.objects.custom.sensitive.write.v2',
  'crm.objects.custom.write',
  'crm.objects.deals.highly_sensitive.read.v2',
  'crm.objects.deals.highly_sensitive.write.v2',
  'crm.objects.deals.read',
  'crm.objects.deals.sensitive.read.v2',
  'crm.objects.deals.sensitive.write.v2',
  'crm.objects.deals.write',
  'crm.objects.goals.read',
  'crm.objects.goals.write',
  'crm.objects.invoices.read',
  'crm.objects.invoices.write',
  'crm.objects.leads.read',
  'crm.objects.leads.write',
  'crm.objects.line_items.read',
  'crm.objects.line_items.write',
  'crm.objects.listings.read',
  'crm.objects.listings.write',
  'crm.objects.orders.read',
  'crm.objects.orders.write',
  'crm.objects.partner-clients.read',
  'crm.objects.partner-clients.write',
  'crm.objects.partner-services.read',
  'crm.objects.partner-services.write',
  'crm.objects.products.read',
  'crm.objects.products.write',
  'crm.objects.quotes.read',
  'crm.objects.quotes.write',
  'crm.objects.services.read',
  'crm.objects.services.write',
  'crm.objects.subscriptions.read',
  'crm.objects.subscriptions.write',
  'crm.objects.users.read',
  'crm.objects.users.write',
  'e-commerce',
  'media_bridge.read',
  'oauth',
  'tickets',
  'tickets.highly_sensitive.v2',
  'tickets.sensitive.v2'
]}
  />
</Accordion>

Associations represent the relationships between objects and activities in the HubSpot CRM. Record associations can exist between records of different objects (e.g., Contact to Company), as well as within the same object (e.g., Company to Company).

The Associations API includes two sets of endpoints:

* **Association details endpoints**: create, edit, and remove associations between records. In this article, you'll learn more about using the associations details endpoints.
* **[Association schema endpoints](/docs/api-reference/latest/crm/associations/associations-schema/guide)**: view your account's association definitions (also known as types), create and manage custom association labels, and set limits for associations. Learn more about using the [associations schema endpoints](/docs/api-reference/latest/crm/associations/associations-schema/guide).

Learn more about objects, records, properties, and associations APIs in the [Understanding the CRM](/docs/api-reference/latest/crm/understanding-the-crm) guide.

## Associate records

You can associate records with each other unlabeled (i.e. contact and company associated with no descriptor) or with labels (e.g., contact and company associated and the contact is the company's *Decision maker*).

<Warning>
  The number of associations a record can have depends on [the object and your HubSpot subscription.](https://legal.hubspot.com/hubspot-product-and-services-catalog#TechnicalLimits:~:text=CRM%20Record%20Association%20Limits)
</Warning>

### Associate records without a label

You can create a default unlabeled association between two records, or set up unlabeled associations for records in bulk. To set up an individual default association between two records, make a `PUT` request to

`/crm/objects/2026-09/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

In the request URL, include:

* `fromObjectType`**:** the ID of the object you're associating. To find the ID values, refer to this [list of object type IDs,](/docs/api-reference/latest/crm/understanding-the-crm#object-type-ids) or for contacts, companies, deals, tickets, and notes, you can use the object name (e.g., `contact`, `company`).
* `fromObjectId`**:** the ID of the record to associate.
* `toObjectType`**:** the ID of the object you're associating the record to. To find the ID values, refer to this [list of object type IDs,](/docs/api-reference/latest/crm/understanding-the-crm#object-type-ids) or for contacts, companies, deals, tickets, and notes, you can use the object name (e.g., `contact`, `company`).
* `toObjectId`**:** the ID of the record to associate to.

For example, to associate a contact record whose ID is `12345` with a company record whose ID is `67891`, your request URL would be: `/crm/objects/2026-09/contact/12345/associations/default/company/67891`.

To associate records without a label in bulk, make a `POST` request to `/crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/associate/default`. In the request body, include `objectId` values for the records you want to associate. For example:

```json theme={null}
{
  "inputs": [
    {
      "from": {
        "id": "12345"
      },
      "to": {
        "id": "56678"
      }
    },
    {
      "from": {
        "id": "49475850"
      },
      "to": {
        "id": "2049585"
      }
    },
    {
      "from": {
        "id": "304958"
      },
      "to": {
        "id": "204959"
      }
    }
  ]
}
```

### Associate records with a label

You can also associate records with [labels](/docs/api-reference/latest/crm/associations/associations-schema/guide#retrieve-association-labels) for individual record pairs or multiple pairs of records in bulk. For each association, depending on your [association limits](/docs/api-reference/latest/crm/associations/associations-schema/guide#set-and-manage-association-limits), you can include multiple labels.

* To associate two records and set a label to describe the association, make a `PUT` request to `/crm/objects/2026-09/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`. In the request URL, include the `id` values of the two records you're associating.
* To bulk create labeled associations between records of the same objects, make a `POST` request to `/crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/create`. In the request body, include the `id` values of records to associate in addition to the required parameters below.

In the request body, include the following information to indicate the labeled association you want to create:

* `associationCategory`: either `HUBSPOT_DEFINED` (default label) or `USER_DEFINED` (custom label).
* `associationTypeId`: the numerical ID value for the label. If using a default label (e.g., Primary company), refer to this [list of default type IDs.](#association-type-id-values) If you're using a custom label, you'll need to [retrieve the labels](/docs/api-reference/latest/crm/associations/associations-schema/guide#retrieve-association-labels) between those objects.

<Warning>
  For cross-object and paired label relationships, ensure you use the `typeId` that refers to the correct direction. For example, if your `fromObjectType` is `contact` and your `toObjectType` is `company`, the [`typeId`](#contact-to-object) you should use to label that company as primary is `1`.
</Warning>

For example, to associate a contact with a deal using a custom label:

1\. Make a `GET` request to `/crm/associations/2026-09/contact/deal/labels`.

2\. In the response, look at the `typeId` and `category` values for the label. The ID will be a number (e.g., `36`), and the category will always be `USER_DEFINED` for custom labels.

3\. Make a `PUT` request to `/crm/objects/2026-09/contact/{objectId}/associations/deal/{toObjectId}` with the following example request body:

```json theme={null}
[
  {
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 36
  }
]
```

A successful response will include the `id` values of the two associated records along with the `label` for the association. For the example above, the response would look like:

```json theme={null}
{
  "fromObjectTypeId": "0-1",
  "fromObjectId": 29851,
  "toObjectTypeId": "0-3",
  "toObjectId": 21678228008,
  "labels": ["Point of contact"]
}
```

## Retrieve associated records

You can retrieve a record's associations of a specific object type.

* To retrieve an individual record's associations of a specific object, make a `GET` request to `/crm/objects/2026-09/{fromObjectType}/{objectId}/associations/{toObjectType}`. In the request URL, include the record's object as the `fromObjectType` and its record ID as the `objectId`.
* To retrieve a record's associated records of a specific object, make a `POST` request to `/crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/read`. In the request body, include up to 1,000 `id` values of records whose associated records you want to retrieve.

For example, to retrieve all company associations for two contacts, make a `POST` request to `/crm/associations/2026-09/contacts/companies/batch/read`. Your request body would look like the following:

```json theme={null}
{
  "inputs": [
    {
      "id": "33451"
    },
    {
      "id": "29851"
    }
  ]
}
```

For both the basic and batch endpoints, the record ID values will be returned for each associated record, along with information to describe the association between the record, including the `label`, `category`, and `typeId`. For the example batch request above, the response would be:

```json theme={null}
{
  "status": "COMPLETE",
  "results": [
    {
      "from": {
        "id": "33451"
      },
      "to": [
        {
          "toObjectId": 5790939450,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 1,
              "label": "Primary"
            },
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            },
            {
              "category": "USER_DEFINED",
              "typeId": 28,
              "label": "Billing contact"
            }
          ]
        }
      ]
    },
    {
      "from": {
        "id": "29851"
      },
      "to": [
        {
          "toObjectId": 5790939450,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 1,
              "label": "Primary"
            },
            {
              "category": "USER_DEFINED",
              "typeId": 37,
              "label": "Chef"
            },
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            }
          ]
        },
        {
          "toObjectId": 6675245424,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            }
          ]
        },
        {
          "toObjectId": 17705714757,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            },
            {
              "category": "USER_DEFINED",
              "typeId": 30,
              "label": "Decision maker"
            }
          ]
        }
      ]
    }
  ],
  "startedAt": "2024-10-21T20:22:42.152Z",
  "completedAt": "2024-10-21T20:22:42.167Z"
}
```

## Update record association labels

For existing associations, to update the association labels, you can use the basic and batch create endpoints. If an existing labeled association exists between two records, to <u>replace</u> the existing label, only include the new label in the request. If you want to append labels (i.e. add a new label and keep the existing label), include both labels in your request.

For example, if records are already associated with a label with the `typeId` of `30`, to keep that label while adding another label, your request body would look like:

```json theme={null}
[
  {
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 30
  },
  {
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 37
  }
]
```

## Remove record associations

You can delete all associations between records, or delete only associations of specific [types](/docs/api-reference/latest/crm/associations/associate-records) (i.e. default or custom labels). When deleting all associations, the records will <u>not</u> be deleted, but they will no longer be associated with one another. If deleting a specific association type, the records will still be associated, but the specified labels will be removed. However, if you delete the [default unlabeled association type](#associate-records-without-a-label), this will remove all other associations.

### Remove all associations between records

To remove all associations between pairs of records:

* To remove all associations between two records, make a `DELETE` request to `/crm/objects/2026-09/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`.
* To batch remove all associations between record pairs, make a `POST` request to `/crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/archive`. In the request body, include the `id` values of records for which you want to remove all associations. You can include a maximum of 100 unique `from` inputs per batch request (i.e. remove associations originating from 100 different records).

For example, to remove all associations between sets of contacts and companies, your request body would look like:

```json theme={null}
{
  "inputs": [
    {
      "from": {
        "id": "12345"
      },
      "to": [
        {
          "id": "67891"
        }
      ]
    },
    {
      "from": {
        "id": "9876"
      },
      "to": [
        {
          "id": "54321"
        }
      ]
    }
  ]
}
```

### Remove associations with specific labels

To remove record associations with specific association labels, make a `POST` request to `/crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/labels/archive`. In the request body, include an array with `id` values of the associated records and the `associationTypeId` and `category` values of labels to remove. You can include a maximum of 100 inputs per batch request.

For example, to remove a custom label from an association, but keep the unlabeled association, your request body would look like:

```json theme={null}
{
  "inputs": [
    {
      "types": [
        {
          "associationCategory": "USER_DEFINED",
          "associationTypeId": 37
        }
      ],
      "from": {
        "id": "29851"
      },
      "to": {
        "id": "5790939450"
      }
    }
  ]
}
```

If you then retrieve that contact's company associations, now only the unlabeled association type will be returned for the above associated company:

```json theme={null}
{
  "results": [
    {
      "toObjectId": 5790939450,
      "associationTypes": [
        {
          "category": "HUBSPOT_DEFINED",
          "typeId": 279,
          "label": null
        }
      ]
    },
    {
      "toObjectId": 6675245424,
      "associationTypes": [
        {
          "category": "HUBSPOT_DEFINED",
          "typeId": 279,
          "label": null
        }
      ]
    },
    {
      "toObjectId": 17705714757,
      "associationTypes": [
        {
          "category": "HUBSPOT_DEFINED",
          "typeId": 279,
          "label": null
        },
        {
          "category": "USER_DEFINED",
          "typeId": 30,
          "label": "Decision maker"
        }
      ]
    }
  ]
}
```

## Report on high association usage

There are technical [limits to the number of associations a record can have](https://legal.hubspot.com/hubspot-product-and-services-catalog). You can use the associations API to retrieve a report of records that are either approaching or have hit the maximum limit for associations.

To retrieve the report, make a `POST` request to `/crm/associations/2026-09/usage/high-usage-report/{userID}`. The file includes records using 80% or more of their association limit. For example, if a company can be associated with up to 50,000 contacts, the company will be included in the file if it has 40,000 or more associated contacts. The file will be sent to the email of the user whose ID was included in the request URL. Learn how to retrieve user IDs with the [users API](/docs/api-reference/latest/account/settings/user-provisioning/guide).

## Limits

The association API endpoints are subject to the following limits based on your account subscription:

* Daily limits:
  * ***Professional* accounts:** 500,000 requests
  * ***Enterprise* accounts:** 500,000 requests
  * You can purchase an [API limit increase](https://legal.hubspot.com/hubspot-product-and-services-catalog#Addons), you can make a maximum of 1,000,000 requests per day. This maximum will <u>not</u> increase for association API requests if you purchase an additional API limit increase.
* Burst limits:
  * ***Free*** **and *Starter* accounts:** 100 requests per 10 seconds
  * ***Professional*** **and *Enterprise* accounts:** 150 requests per 10 seconds
  * If you purchase the [API limit increase](https://legal.hubspot.com/hubspot-product-and-services-catalog#Addons), you can make a maximum of 200 requests per 10 seconds. This maximum will <u>not</u> increase for association API requests if you purchase an additional API limit increase.

The following limits apply for batch associations API endpoint requests:

* **Batch read associations**: limited to 1,000 inputs per request body.
* **Batch create associations**: limited to 2,000 inputs per request body.

Learn more about API limits in [this article](/docs/developer-tooling/platform/usage-guidelines).

## Association type ID values

The following tables include the HubSpot-defined `associationTypeId` values that specify the type of association. Association types vary depending on the included objects and the direction of the association (e.g., Contact to Company is different from Company to Contact). If you create custom objects or custom association labels, the related association types will have unique `typeId` values that you'll need to [retrieve](/docs/api-reference/latest/crm/associations/associations-schema/guide#retrieve-association-labels) or locate in your [association settings in HubSpot](https://knowledge.hubspot.com/object-settings/create-and-use-association-labels#association-label-api-details).

<Warning>
  Default company association types include an unlabeled association type and a primary association type. If a record has more than one associated company, only one can be the primary company. The other associations can either be unlabeled or have custom association labels.
</Warning>

### Company to object

| TYPE ID | Association type |
| - | - |
| `450` | Company to company |
| `14` | Child to parent company |
| `13` | Parent to child company |
| `280` | Company to contact |
| `2` | Company to primary contact |
| `930` | Company to billing contact |
| `342` | Company to deal |
| `6` | Primary company to deal |
| `340` | Company to ticket |
| `25` | Primary company to ticket |
| `181` | Company to call |
| `185` | Company to email |
| `611` | Company to lead |
| `187` | Company to meeting |
| `189` | Company to note |
| `191` | Company to task |
| `88` | Company to communication (SMS, WhatsApp, or LinkedIn message) |
| `460` | Company to postal mail |
| `180` | Company to invoice |
| `935` | Company to order |
| `510` | Primary company to order |
| `390` | Company to payment |
| `472` | Company to payment link |
| `72` | Company to quote |
| `1335` | Billing company to quote |
| `298` | Company to subscription |
| `909` | Company to appointment |
| `939` | Company to course |
| `885` | Company to listing |
| `793` | Company to service |
| `929` | Company to feedback submission |
| `1237` | Company to project |
| `1387` | Company to marketing event |

### Contact to object

\| TYPE ID | Association type                                              |
\| ------- | ----- ------------------------------------------------------ |
\| `449`   | Contact  to contact                                            |
\| `279`   | Contact  to company                                            |
\| `1`     | Contact  to primary company                              |
\| `931`   | Billing  contact to company                                   |
\| `4`     | Contact  to deal                                               |
\| `15`    | Contact  to ticket                                             |
\| `193`   | Contact  to call                                               |
\| `197`   | Contact to email                                              |
\| `199`   | Contact to meeting                                            |
\| `201`   | Contact to note                                               |
\| `203`   | Contact to task                                               |
\| `82`    | Contact to communication (SMS, WhatsApp, or LinkedIn message) |
\| `454`   | Contact to postal mail                                        |
\| `587`   | Contact to cart                                               |
\| `508`   | Contact to order                                              |
\| `178`   | Contact to invoice                                            |
\| `388`   | Contact to payment                                            |
\| `470`   | Contact to payment link                                       |
\| `296`   | Contact to subscription                                       |
\| `907`   | Contact to appointment                                        |
\| `861`   | Contact to course                                             |
\| `883`   | Contact to listing                                            |
\| `799`   | Contact to service                                            |
\| `97`    | Contact to feedback submission                                |
\| `1243`  | Contact to project                                            |
\| `609`   | Contact to lead                               |
\| `70`    | Contact to quote |
\| `703`   | Signer contact to quote (for e-signatures)  |
\| `1227`  | Billing contact to quote  |
\| `1375`  | Contact to marketing event |

### Deal to object

| TYPE ID | Association type |
| - | - |
| `451` | Deal to deal |
| `3` | Deal to contact |
| `341` | Deal to company |
| `5` | Deal to primary company |
| `27` | Deal to ticket |
| `205` | Deal to call |
| `1038` | Deal to lead |
| `583` | Primary deal to lead |
| `209` | Deal to email |
| `1357` | Deal to goal |
| `211` | Deal to meeting |
| `213` | Deal to note |
| `215` | Deal to task |
| `86` | Deal to communication (SMS, WhatsApp, or LinkedIn message) |
| `458` | Deal to postal mail |
| `313` | Deal to deal split |
| `19` | Deal to line item |
| `1346` | Deal to cart |
| `176` | Deal to invoice |
| `511` | Deal to order |
| `392` | Deal to payment |
| `474` | Deal to payment link |
| `63` | Deal to quote |
| `300` | Deal to subscription |
| `945` | Deal to appointment |
| `863` | Deal to course |
| `887` | Deal to listing |
| `795` | Deal to service |
| `985` | Deal to feedback submission |
| `1239` | Deal to project |
| `1389` | Deal to marketing event |

### Ticket to object

| TYPE ID | Association type |
| - | - |
| `452` | Ticket to ticket |
| `16` | Ticket to contact |
| `339` | Ticket to company |
| `26` | Ticket to primary company |
| `28` | Ticket to deal |
| `219` | Ticket to call |
| `223` | Ticket to email |
| `225` | Ticket to meeting |
| `227` | Ticket to note |
| `229` | Ticket to task |
| `84` | Ticket to communication (SMS, WhatsApp, or LinkedIn message) |
| `456` | Ticket to postal mail |
| `32` | Ticket to thread |
| `278` | Ticket to conversation |
| `526` | Ticket to order |
| `947` | Ticket to appointment |
| `941` | Ticket to course |
| `943` | Ticket to listing |
| `797` | Ticket to service |
| `1122` | Ticket to subscription |
| `1355` | Ticket to payment |
| `99` | Ticket to feedback submission |
| `1241` | Ticket to project |

### Lead to object

| TYPE ID | Association type |
| - | - |
| `608` | Lead to contact |
| `578` | Lead to primary contact |
| `610` | Lead to company |
| `580` | Lead to primary company |
| `1037` | Lead to deal |
| `582` | Lead to primary deal |
| `596` | Lead to call |
| `598` | Lead to email |
| `600` | Lead to meeting |
| `854` | Lead to note |
| `646` | Lead to task |
| `602` | Lead to communication (SMS, WhatsApp, or LinkedIn message) |
| `1162` | Lead to feedback submission |
| `1391` | Lead to marketing event |

### Appointment to object

| TYPE ID | Association type |
| - | - |
| `906` | Appointment to contact |
| `908` | Appointment to company |
| `944` | Appointment to deal |
| `946` | Appointment to ticket |
| `912` | Appointment to call |
| `916` | Appointment to email |
| `918` | Appointment to meeting |
| `920` | Appointment to note |
| `922` | Appointment to task |
| `924` | Appointment to communication (SMS, WhatsApp, or LinkedIn message) |
| `926` | Appointment to postal mail |
| `1325` | Appointment to project |
| `2728` | Appointment to marketing event |

### Goal to object

| TYPE ID | Association type |
| - | - |
| `809` | Goal to campaign |
| `1356` | Goal to deal |
| `333` | Goal to goal target group |

### Course to object

| TYPE ID | Association type |
| - | - |
| `860` | Course to contact |
| `938` | Course to company |
| `862` | Course to deal |
| `940` | Course to ticket |
| `866` | Course to call |
| `870` | Course to email |
| `872` | Course to meeting |
| `874` | Course to note |
| `876` | Course to task |
| `878` | Course to communication (SMS, WhatsApp, or LinkedIn message) |
| `880` | Course to postal mail |
| `1323` | Course to project |
| `2760` | Course to marketing event |

### Listing to object

| TYPE ID | Association type |
| - | - |
| `882` | Listing to contact |
| `884` | Listing to company |
| `886` | Listing to deal |
| `942` | Listing to ticket |
| `890` | Listing to call |
| `894` | Listing to email |
| `896` | Listing to meeting |
| `898` | Listing to note |
| `900` | Listing to task |
| `902` | Listing to communication (SMS, WhatsApp, or LinkedIn message) |
| `904` | Listing to postal mail |
| `1321` | Listing to project |
| `2772` | Listing to marketing event |

### Service to object

| TYPE ID | Association type |
| - | - |
| `798` | Service to contact |
| `792` | Service to company |
| `794` | Service to deal |
| `796` | Service to ticket |
| `840` | Service to call |
| `842` | Service to email |
| `838` | Service to meeting |
| `836` | Service to note |
| `852` | Service to task |
| `846` | Service to communication (SMS, WhatsApp, or LinkedIn message) |
| `848` | Service to postal mail |
| `1245` | Service to project |
| `2782` | Service to marketing event |

### Call to object

| TYPE ID | Association type |
| - | - |
| `913` | Call to appointment |
| `182` | Call to company |
| `194` | Call to contact |
| `206` | Call to deal |
| `1156` | Call to feedback submission |
| `597` | Call to lead |
| `773` | Call to order |
| `867` | Call to course |
| `891` | Call to listing |
| `1258` | Call to project |
| `841` | Call to service |
| `220` | Call to ticket |

### Email to object

| TYPE ID | Association type |
| - | - |
| `917` | Email to appointment |
| `186` | Email to company |
| `198` | Email to contact |
| `871` | Email to course |
| `210` | Email to deal |
| `777` | Email to order |
| `895` | Email to listing |
| `1260` | Email to project |
| `843` | Email to service |
| `224` | Email to ticket |
| `498` | Email to marketing event |

### Feedback submission to object

| TYPE ID | Association type |
| - | - |
| `98` | Feedback submission to contact |
| `928` | Feedback submission to company |
| `984` | Feedback submission to deal |
| `100` | Feedback submission to ticket |
| `1155` | Feedback submission to call |
| `1157` | Feedback submission to cart |
| `1173` | Feedback submission to subscription |
| `1159` | Feedback submission to invoice |
| `1161` | Feedback submission to lead |
| `1167` | Feedback submission to order |
| `1171` | Feedback submission to quote |
| `1169` | Feedback submission to payment |

### Meeting to object

| TYPE ID | Association type |
| - | - |
| `200` | Meeting to contact |
| `188` | Meeting to company |
| `212` | Meeting to deal |
| `226` | Meeting to ticket |
| `601` | Meeting to lead |
| `769` | Meeting to order |
| `919` | Meeting to appointment |
| `873` | Meeting to course |
| `897` | Meeting to listing |
| `839` | Meeting to service |

### Note to object

| TYPE ID | Association type |
| - | - |
| `202` | Note to contact |
| `190` | Note to company |
| `214` | Note to deal |
| `228` | Note to ticket |
| `855` | Note to lead |
| `765` | Note to order |
| `921` | Note to appointment |
| `875` | Note to course |
| `899` | Note to listing |
| `837` | Note to service |
| `1249` | Note to project |
| `260` | Note to marketing event |

### Postal mail to object

| TYPE ID | Association type |
| - | - |
| `453` | Postal mail to contact |
| `459` | Postal mail to company |
| `457` | Postal mail to deal |
| `455` | Postal mail to ticket |
| `927` | Postal mail to appointment |
| `881` | Postal mail to course |
| `905` | Postal mail to listing |
| `788` | Postal mail to order |
| `849` | Postal mail to service |
| `1264` | Postal mail to project |

### Task to object

| TYPE ID | Association type |
| - | - |
| `204` | Task to contact |
| `192` | Task to company |
| `216` | Task to deal |
| `230` | Task to ticket |
| `647` | Task to lead |
| `218` | Task to quote |
| `727` | Task to order |
| `923` | Task to appointment |
| `877` | Task to course |
| `901` | Task to listing |
| `853` | Task to service |
| `1247` | Task to project |
| `262` | Task to marketing event |

### Communication (SMS, WhatsApp, or LinkedIn message) to object

| TYPE ID | Association type |
| - | - |
| `81` | Communication to contact |
| `87` | Communication to company |
| `85` | Communication to deal |
| `83` | Communication to ticket |
| `603` | Communication to lead |
| `785` | Communication to order |
| `925` | Communication to appointment |
| `879` | Communication to course |
| `903` | Communication to listing |
| `847` | Communication to service |
| `1282` | Communication to project |

### Invoice to object

| TYPE ID | Association type |
| - | - |
| `177` | Invoice to contact |
| `179` | Invoice to company |
| `175` | Invoice to deal |
| `407` | Invoice to quote |
| `622` | Invoice to subscription |
| `815` | Invoice to payment link |
| `517` | Invoice to order |
| `986` | Invoice to ticket |
| `409` | Invoice to line item |
| `411` | Invoice to discount |
| `413` | Invoice to fee |
| `415` | Invoice to tax |
| `541` | Invoice to payment |
| `691` | Invoice to payment schedule installment |
| `679` | Invoice to data sync state |
| `1160` | Invoice to feedback submission |

### Payment to object

| TYPE ID | Association type |
| - | - |
| `389` | Payment to company |
| `387` | Payment to contact |
| `391` | Payment to deal |
| `428` | Payment to discount |
| `1326` | Payment to fee |
| `1170` | Payment to feedback submission |
| `542` | Payment to invoice |
| `395` | Payment to line item |
| `524` | Payment to order |
| `476` | Payment to payment link |
| `397` | Payment to quote |
| `393` | Payment to subscription |
| `1354` | Payment to ticket |

### Payment link to object

| TYPE ID | Association type |
| - | - |
| `475` | Payment link to payment |
| `469` | Payment link to contact |
| `471` | Payment link to company |
| `473` | Payment link to deal |
| `682` | Payment link to discount |
| `686` | Payment link to fee |
| `814` | Payment link to invoice |
| `758` | Payment link to line item |
| `477` | Payment link to subscription |
| `684` | Payment link to tax |

### Quote to object

| TYPE ID | Association type |
| - | - |
| `69` | Quote to contact |
| `1226` | Quote to billing contact |
| `71` | Quote to company |
| `1334` | Quote to billing company |
| `64` | Quote to deal |
| `67` | Quote to line item |
| `286` | Quote to quote template |
| `362` | Quote to discount |
| `364` | Quote to fee |
| `366` | Quote to tax |
| `217` | Quote to task |
| `702` | Quote to signer contact (for e-signatures) |
| `733` | Quote to cart |
| `408` | Quote to invoice |
| `731` | Quote to order |
| `398` | Quote to payment |
| `304` | Quote to subscription |
| `1172` | Quote to feedback submission |

### Line item to object

| TYPE ID | Association type |
| - | - |
| `571` | Line item to abandoned cart |
| `591` | Line item to cart |
| `396` | Line item to payment |
| `20` | Line item to deal |
| `368` | Line item to discount |
| `410` | Line item to invoice |
| `514` | Line item to order |
| `759` | Line item to payment link |
| `1345` | Line item to project |
| `68` | Line item to quote |
| `302` | Line item to subscription |
| `565` | Upcoming line item to subscription |

### Order to object

| TYPE ID | Association type |
| - | - |
| `772` | Order to call |
| `593` | Order to cart |
| `507` | Order to contact |
| `784` | Order to communication (SMS, WhatsApp, or LinkedIn message) |
| `934` | Order to company |
| `509` | Order to primary company |
| `512` | Order to deal |
| `519` | Order to discount |
| `521` | Order to discount code |
| `776` | Order to email |
| `1168` | Order to feedback submission |
| `518` | Order to invoice |
| `513` | Order to line item |
| `768` | Order to meeting |
| `764` | Order to note |
| `523` | Order to payment |
| `789` | Order to postal mail |
| `730` | Order to quote |
| `516` | Order to subscription |
| `726` | Order to task |
| `525` | Order to ticket |
| `2538` | Order to marketing event |

### Cart to object

| TYPE ID | Association type |
| - | - |
| `586` | Cart to contact |
| `1347` | Cart to deal |
| `588` | Cart to discount |
| `590` | Cart to line item |
| `592` | Cart to order |
| `732` | Cart to quote |
| `728` | Cart to task |
| `594` | Cart to ticket |
| `1158` | Cart to feedback submission |

### Discount to object

| TYPE ID | Association type |
| - | - |
| `369` | Discount to deal |
| `361` | Discount to quote |
| `412` | Discount to invoice |
| `683` | Discount to payment link |
| `520` | Discount to order |
| `589` | Discount to cart |
| `367` | Discount to line item |

### Fee to object

| TYPE ID | Association type |
| - | - |
| `1327` | Fee to payment |
| `687` | Fee to payment link |
| `363` | Fee to quote |
| `414` | Fee to invoice |

### Subscription to object

| TYPE ID | Association type |
| - | - |
| `295` | Subscription to contact |
| `297` | Subscription to company |
| `299` | Subscription to deal |
| `1121` | Subscription to ticket |
| `623` | Subscription to invoice |
| `301` | Subscription to line item |
| `303` | Subscription to quote |
| `478` | Subscription to payment link |
| `515` | Subscription to order |
| `1174` | Subscription to feedback submission |

### Tax to object

| TYPE ID | Association type |
| - | - |
| `685` | Tax to payment link |
| `365` | Tax to quote |
| `416` | Tax to invoice |

### Project to object

| TYPE ID | Association type |
| - | - |
| `1324` | Project to appointment |
| `1257` | Project to call |
| `1281` | Project to communication (SMS, WhatsApp, or LinkedIn message) |
| `1236` | Project to company |
| `1299` | Project to primary company |
| `1242` | Project to contact |
| `1261` | Project to conversation session |
| `1322` | Project to course |
| `1304` | Project to data sync |
| `1238` | Project to deal |
| `1259` | Project to email |
| `1252` | Project to engagement |
| `1320` | Project to listing |
| `1250` | Project to marketing event |
| `1255` | Project to meeting event |
| `1248` | Project to note |
| `1263` | Project to postal mail |
| `1254` | Project to project |
| `1244` | Project to service |
| `1246` | Project to task |
| `1240` | Project to ticket |
| `1250` | Project to marketing event |

### Marketing event to object

| TYPE ID | Association type |
| - | - |
| `2729` | Marketing event to appointment |
| `1228` | Marketing event to call |
| `492` | Marketing event to campaign |
| `2535` | Marketing event to commerce payment |
| `1234` | Marketing event to communication |
| `1386` | Marketing event to company |
| `1374` | Marketing event to contact |
| `1232` | Marketing event to conversation session |
| `2761` | Marketing event to course |
| `1388` | Marketing event to deal |
| `497` | Marketing event to email |
| `493` | Marketing event to engagement |
| `1390` | Marketing event to lead |
| `2773` | Marketing event to listing |
| `2563` | Marketing event to marketing event |
| `499` | Marketing event to meeting event |
| `259` | Marketing event to note |
| `2537` | Marketing event to order |
| `1251` | Marketing event to project |
| `1231` | Marketing event to publishing task |
| `2783` | Marketing event to service |
| `261` | Marketing event to task |
| `2592` | Marketing event to user |

## v1 associations (legacy)

If you're using the v1 associations API, view the table below for information about IDs to use when associating records.

| Association type | ID |
| - | - |
| Contact to company | 1 |
| Company to contact (default) | 2 |
| Company to contact (all labels) | 280 |
| Deal to contact | 3 |
| Contact to deal | 4 |
| Deal to company | 5 |
| Company to deal | 6 |
| Company to engagement | 7 |
| Engagement to company | 8 |
| Contact to engagement | 9 |
| Engagement to contact | 10 |
| Deal to engagement | 11 |
| Engagement to deal | 12 |
| Parent company to child company | 13 |
| Child company to parent company | 14 |
| Contact to ticket | 15 |
| Ticket to contact | 16 |
| Ticket to engagement | 17 |
| Engagement to ticket | 18 |
| Deal to line item | 19 |
| Line item to deal | 20 |
| Company to ticket | 25 |
| Ticket to company | 26 |
| Deal to ticket | 27 |
| Ticket to deal | 28 |
