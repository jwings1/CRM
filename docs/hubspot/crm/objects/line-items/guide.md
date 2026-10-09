> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Line Items API

> In HubSpot, line items represent individual instances of products on a deal, quote, or other object. The line items endpoints allow you to manage and sync this data.

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
  'crm.objects.line_items.read',
  'crm.objects.line_items.write'
]}
  />
</Accordion>

In HubSpot, line items are individual instances of [products](/docs/api-reference/latest/crm/objects/products/guide). When a product is attached to a deal or quote, it becomes a line item. You can also create standalone line items that aren't based on an existing product. The line items endpoints allow you to manage this data and sync it between HubSpot and other systems.

**Example use case:** when creating a set of [quotes](/docs/api-reference/latest/crm/objects/quotes/guide) for sales reps to send to potential buyers, you can use this API to create standalone line items per quote, as well as line items based on existing products.

## Create a line item

To create a line item, make a `POST` request to `/crm/objects/2026-09/line_items`. In the request body, include the line item's details, such as name, quantity, and price. You may also want to include additional data in the request body:

* To create a line item based on an existing product (created through the [products API](/docs/api-reference/latest/crm/objects/products/guide) or [in HubSpot](https://knowledge.hubspot.com/products/create-and-manage-products)), include `hs_product_id` in the request body.
* To include the [tax rate](#retrieve-tax-rates) for your line item, include its ID as the `hs_tax_rate_group_id` within the `properties` field of the request body.
* You can also associate the line item with deals, quotes, invoices, payment links, or subscriptions by including an `associations` array in the request body. For example, the request body below would create a line item named "New standalone line item" that's associated with a deal (ID: `12345`).

```json theme={null}
{
  "properties": {
    "price": 10,
    "quantity": 1,
    "name": "New standalone line item",
    "hs_tax_rate_group_id": "2148420997"
  },
  "associations": [
    {
      "to": {
        "id": 12345
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 20
        }
      ]
    }
  ]
}
```

<Warning>
  **Please note:**

  * Line items belong to one single parent object. If associating objects, line items should be individual to each object. For example, if you're creating a deal and a quote, you should create one set of line items for the deal, and another set for the quote. This will help streamline CRM data across objects and prevent unexpected data loss when needing to modify line items (e.g., deleting a quote will delete the quote's line items, and if those line items are associated with a deal, the deal's line items will also be deleted).
  * The `price` specified within the `properties` field cannot be negative.
</Warning>

### Batch create line items

To create multiple line items in a single request, make a `POST` request to `/crm/objects/2026-09/line_items/batch/create`. In the request body, include an `inputs` array where each entry contains a `properties` object with the line item's details.

The following example creates two line items in a single request:

```json theme={null}
{
  "inputs": [
    {
      "properties": {
        "name": "Line item one",
        "price": "50.00",
        "quantity": "2"
      }
    },
    {
      "properties": {
        "name": "Line item two",
        "price": "75.00",
        "quantity": "1"
      }
    }
  ]
}
```

<Warning>
  Duplicate line item entries are silently merged. If the `inputs` array contains identical entries, the API deduplicates them and returns fewer objects in `results` than were submitted. To prevent this, ensure each input has at least one differentiating property value. For example, give each line item a distinct `name` or custom field value.
</Warning>

### Tiered pricing

Line items support the same tiered pricing model as products. You can create a tiered pricing line item in two ways:

* **Based on an existing product:** include `hs_product_id` in the request body. The tiered pricing properties are inherited from the product.
* **Directly on the line item:** include `hs_pricing_model`, `hs_tier_ranges`, and `hs_tier_prices` in the `properties` object of the request body, using the same format as products.

Learn more about [tiered pricing properties and models](/docs/api-reference/latest/crm/objects/products/guide#tiered-pricing) in the products API guide, including single-currency and multi-currency examples.

<Warning>
  **Please note:** do not set the `price` property when using tiered pricing properties on a line item. The line item price will be set based on the tiered pricing properties instead.
</Warning>

To retrieve all tiered pricing properties for a given line item, make a `GET` request to  `/crm/objects/2026-09/line_item/{lineItemId}?properties=hs_pricing_model,hs_tier_ranges,hs_tier_prices`

The response will include the tiered pricing properties:

```json theme={null}
{
  "id": "53810745416",
  "properties": {
    "createdate": "2026-03-31T19:16:50.063Z",
    "hs_lastmodifieddate": "2026-03-31T19:16:51.187Z",
    "hs_object_id": "53810745416",
    "hs_pricing_model": "graduated",
    "hs_tier_prices": "[{\"index\":0,\"price\":100},{\"index\":1,\"price\":90},{\"index\":2,\"price\":80}]",
    "hs_tier_ranges": "[{\"start\":0,\"end\":99},{\"start\":100,\"end\":199},{\"start\":200}]"
  },
  "createdAt": "2026-03-31T19:16:50.063Z",
  "updatedAt": "2026-03-31T19:16:51.187Z",
  "archived": false
}
```

### Recurring billing

When creating a line item with recurring billing, two properties control billing behavior: `recurringbillingfrequency` and `hs_recurring_billing_period`. These properties configure how frequently the customer is charged and for how long (i.e., how many payments).

* `recurringbillingfrequency`: how often the customer is billed. Valid values are `weekly`, `biweekly`, `monthly`, `quarterly`, `per_six_months`, `annually`, `per_two_years`, `per_three_years`, `per_four_years`, and `per_five_years`.
* `hs_recurring_billing_period`: the total billing duration, in [ISO 8601 duration format](https://docs.oracle.com/javase/8/docs/api/java/time/Period.html) (`PnYnMnD` or `PnW`). Setting this property alongside `recurringbillingfrequency` limits billing to a fixed number of payments. Omit this property to automatically renew billing until canceled.

The table below shows common combinations and their results. Use `PnW` (weeks) format with `weekly` or `biweekly` frequency, and `PnM` or `PnY` (months/years) format with all other frequencies.

| `recurringbillingfrequency` | `hs_recurring_billing_period` | Result |
| - | - | - |
| `weekly` | `P12W` | 12 weekly payments (12 weeks total) |
| `monthly` | `P8M` | 8 monthly payments (8 months total) |
| `quarterly` | `P1Y` | 4 quarterly payments (1 year total) |
| `annually` | `P3Y` | 3 annual payments (3 years total) |
| `monthly` | (not set) | billing renews monthly until canceled |

The following example creates a line item with 8 monthly payments. The period `P8M` represents 8 months, and combined with `monthly` frequency, results in 8 total payments.

```json theme={null}
{
  "properties": {
    "name": "Monthly subscription",
    "price": "99.99",
    "quantity": "1",
    "recurringbillingfrequency": "monthly",
    "hs_recurring_billing_period": "P8M",
    "hs_recurring_billing_start_date": "2025-09-01"
  }
}
```

The following example creates an auto-renewing monthly line item with no fixed end. Because `hs_recurring_billing_period` is omitted, billing continues until the subscription is canceled.

```json theme={null}
{
  "properties": {
    "name": "Monthly subscription",
    "price": "99.99",
    "quantity": "1",
    "recurringbillingfrequency": "monthly",
    "hs_recurring_billing_start_date": "2025-09-01"
  }
}
```

<Note>
  * Setting `hs_recurring_billing_end_date` alone does not create fixed-term billing. Use `hs_recurring_billing_period` to limit a recurring line item to a specific number of payments.
  * The `hs_recurring_billing_terms` property and `hs_recurring_billing_number_of_payments` are both calculated automatically from the period and frequency. You cannot set them directly.
</Note>

## Retrieve a line item

You can retrieve line items individually or in bulk.

* To retrieve a specific line item, make a `GET` request to `/crm/objects/2026-09/line_items/{lineItemId}` where `lineItemId` is the ID of the line item.
* To retrieve all line items, make a `GET` request to `/crm/objects/2026-09/line_items`.

In the request URL, you can include the following parameters:

| Parameter | Description |
| - | - |
| `properties` | A comma-separated list of the properties to be returned in the response. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a line item doesn't have a value, it will be returned as `null`. |
| `propertiesWithHistory` | A comma-separated list of the properties to be returned along with their history of previous values. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a line item doesn't have a value, it will be returned as `null`. |

## Update a line item

To update a line item, make a `PATCH` request to `/crm/objects/2026-09/line_items/{lineItemId}`, where `lineItemId` is the ID of the line item.

In the request body, include the property values that you want to update. You cannot update associations through this method. Instead, use the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide).

For example, your request body might look similar to the following:

```json theme={null}
{
  "properties": {
    "price": 25,
    "quantity": 3,
    "name": "Updated line item"
  }
}
```

## Merge line items

To merge two line item records, make a `POST` request to `/crm/objects/2026-09/line_items/merge`. The remaining record combines activities, associations, and most property values from both records. For example, merge duplicate line items to preserve historical context and consolidate their activity timelines. Learn more about [what happens when you merge HubSpot records](https://knowledge.hubspot.com/records/merge-records#what-happens-when-i-merge-records).

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

## Delete a line item

To delete a line item, make a `DELETE` request to `/crm/objects/2026-09/line_items/{lineItemId}`, where `lineItemId` is the ID of the line item.

## Line item properties

For a full list of default line item properties, see the [Line item object definition](/docs/api-reference/latest/crm/objects/line-items/object-definition#properties). To retrieve all line item properties from your account, including any custom properties, make a `GET` request to `/crm/properties/2026-09/line_items`. Learn more about using the [properties API](/docs/api-reference/latest/crm/properties/guide).

<Note>
  When line items are cloned (for example, when cloning a deal to a quote, or a quote to a new quote), properties with [unique values](/docs/api-reference/latest/crm/properties/guide#create-unique-identifier-properties) (`hasUniqueValue: true`) are not copied to the new line items. This is because uniqueness is enforced across all line items, and copying the value would cause a conflict. To set unique property values on cloned line items, update the line items after creation.
</Note>

## Retrieve tax rates

You can apply a tax rate to individual line items (e.g., a MA Sales tax of 6.25%). Once you [configure your tax rate library](https://knowledge.hubspot.com/payments/set-up-automated-tax-and-tax-rates#add-a-tax-rate-to-the-tax-library) in your HubSpot account, you can then make a `GET` request to `/tax-rates/v1/tax-rates` to fetch all tax rates, or `/tax-rates/v1/tax-rates/{taxRateId}` to fetch a tax rate by its ID. Your app will need to authorize the `tax_rates.read` scope to make this request.

The resulting response will resemble the following:

```json theme={null}
{
  "name": "MA Sales tax 2025",
  "percentageRate": 6.25,
  "label": "Sales Tax",
  "active": true,
  "id": "2148420997",
  "createdAt": "2024-12-12T23:20:39.923Z",
  "updatedAt": "2024-12-12T23:20:39.923Z"
}
```

Each tax rate object will include the following properties:

| Property name | Description |
| - | - |
| `name` | The internal descriptor for the tax rate. |
| `percentageRate` | The value of the tax rate, expressed as a percentage. |
| `label` | The buyer-facing descriptor of the tax rate, shown on the quote, invoice, or other parent objects. |
| `active` | A boolean that denotes whether the tax rate can be applied to a new quote or invoice. You might set this to `false` for a previous year's tax rate that's no longer applicable. |
| `id` | The ID of the tax rate. |
| `createdAt` | An ISO 8601 timestamp denoting when the tax rate was created. |
| `updatedAt` | An ISO 8601 timestamp denoting when the tax rate was last updated. |

Once you have the ID of the tax rate you want to apply, provide that `id` for the `hs_tax_rate_group_id` within the `properties` field when creating a line item. Learn more about creating line items in the [section above](#create-a-line-item).
