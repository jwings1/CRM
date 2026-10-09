> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Properties API

>  The CRM properties endpoints allow you to manage custom properties as well as view default property details for any object.

export const CrmWriteValidationEnforcement = () => <Warning>
        <p>Starting with the GA release of API version <code>/2026-09/</code> on September 8, 2026, HubSpot will enforce admin-configured validation rules on all CRM API write paths. Learn more about this enforcement policy and the changes you may need to make on the <a href="https://developers.hubspot.com/changelog/crm-api-write-validation-enforcement">HubSpot Developer Changelog</a>.</p>

        <p>You can retrieve or manage your validation rules using the <a href="https://developers.hubspot.com/docs/api-reference/latest/crm/property-validations/guide">property validation API</a>, or by reviewing rules via the <a href="https://knowledge.hubspot.com/properties/set-validation-rules-for-properties">property settings page</a> in your HubSpot account.</p>
    </Warning>;

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
  'automation',
  'crm.objects.appointments.read',
  'crm.objects.appointments.sensitive.read.v2',
  'crm.objects.appointments.sensitive.write.v2',
  'crm.objects.appointments.write',
  'crm.objects.carts.read',
  'crm.objects.carts.write',
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
  'crm.objects.feedback_submissions.read',
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
  'crm.objects.marketing_events.read',
  'crm.objects.marketing_events.write',
  'crm.objects.orders.read',
  'crm.objects.orders.write',
  'crm.objects.owners.read',
  'crm.objects.products.write',
  'crm.objects.quotes.read',
  'crm.objects.quotes.write',
  'crm.objects.services.read',
  'crm.objects.services.write',
  'crm.objects.subscriptions.read',
  'crm.objects.subscriptions.write',
  'crm.objects.users.read',
  'crm.objects.users.write',
  'crm.pipelines.orders.read',
  'crm.pipelines.orders.write',
  'crm.schemas.appointments.read',
  'crm.schemas.appointments.write',
  'crm.schemas.carts.read',
  'crm.schemas.carts.write',
  'crm.schemas.commercepayments.read',
  'crm.schemas.commercepayments.write',
  'crm.schemas.companies.read',
  'crm.schemas.companies.write',
  'crm.schemas.contacts.read',
  'crm.schemas.contacts.write',
  'crm.schemas.courses.read',
  'crm.schemas.courses.write',
  'crm.schemas.custom.read',
  'crm.schemas.deals.read',
  'crm.schemas.deals.write',
  'crm.schemas.invoices.read',
  'crm.schemas.invoices.write',
  'crm.schemas.line_items.read',
  'crm.schemas.listings.read',
  'crm.schemas.listings.write',
  'crm.schemas.orders.read',
  'crm.schemas.orders.write',
  'crm.schemas.quotes.read',
  'crm.schemas.quotes.write',
  'crm.schemas.services.read',
  'crm.schemas.services.write',
  'crm.schemas.subscriptions.read',
  'crm.schemas.subscriptions.write',
  'e-commerce',
  'media_bridge.read',
  'tickets',
  'tickets.highly_sensitive.v2',
  'tickets.sensitive.v2',
  'timeline'
]}
  />
</Accordion>

Use properties to store information on records. HubSpot provides a set of default properties for each object, and you can also create and manage your own custom properties either [in HubSpot](https://knowledge.hubspot.com/properties/create-and-edit-properties) or using the properties API.

When creating properties, it’s important to consider how to architect your data. In many cases, creating custom properties for HubSpot's standard objects is the right course of action. However, there may be times when you'll need to create a separate [custom object](/docs/api-reference/latest/crm/objects/custom-objects/guide) with its own set of properties.

## Default properties

Each object has a unique set of default properties. To learn more about default properties for different objects, refer to an object's definition page (e.g, [contacts definition page](/docs/api-reference/latest/crm/objects/contacts/object-definition)).

You can also [retrieve all an object's properties via API](#retrieve-properties).

## Property groups

[Property groups](https://knowledge.hubspot.com/properties/organize-and-export-properties#create-and-edit-property-groups) are used to group related properties into categories. Groups are primarily used to organize properties and know from where they originated. For example, if your integration creates custom properties, a custom property group will make it easy to identify that data.

## Property type and fieldType values

When creating or updating properties, both `type` and `fieldType` values are required. The `type` value determines the type of the property, i.e. a string or a number. The `fieldType` property determines how the property will appear in HubSpot or on a form, i.e. as a plain text field, a dropdown menu, or a date picker.

### Types

In the table below, learn about the available property `type` and corresponding `fieldType` values.

| `type` | Description | Valid `fieldType` values |
| - | - | - |
| `bool` | A field containing binary options (e.g., `Yes` or `No`, `True` or `False`). | `booleancheckbox`, `calculation_equation` |
| `enumeration` | A string representing a set of options, with options separated by a semicolon. | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date` | A value representing a specific day, month, and year. Values must be represented in UTC time and can be formatted as [ISO 8601 strings or EPOCH-timestamps in milliseconds](#add-values-to-date-and-datetime-properties) (i.e. midnight UTC). | `date` |
| `datetime` | A value representing a specific day, month, year, and time of day. Values must be represented in UTC time and can be formatted as [ISO 8601 strings or UNIX-timestamps in milliseconds](#add-values-to-date-and-datetime-properties). | `date` |
| `string` | A plain text string, limited to 65,536 characters. | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number` | A number value containing numeric digits and at most one decimal. | `number`, `calculation_equation` |
| `object_coordinates` | A text value used to reference other HubSpot objects, used only for internal properties. Properties of this type cannot be created or edited, and are not visible in HubSpot. | `text` |
| `json` | A text value stored as formatted JSON, used only for internal properties. Properties of this type cannot be created or edited, and are not visible in HubSpot. | `text` |

### Field types

Valid values for `fieldType` include:

| Fieldtype | Description |
| - | - |
| `booleancheckbox` | An input that will allow users to selected one of either Yes or No. When used in a form, it will be displayed as a single checkbox. Learn how to [add a value to single checkbox properties](#add-values-to-checkbox-type-properties). |
| `calculation_equation` | A custom equation that can calculate values based on other property values and/or associations. Learn how to define [calculation properties](#create-calculation-properties). |
| `checkbox` | A list of checkboxes that will allow a user to select multiple options from a set of options allowed for the property. Learn how to [format values when updating multiple checkbox properties](#add-values-to-checkbox-type-properties). |
| `date` | A date value, displayed as a date picker. |
| `file` | Allows for a file to be uploaded on a record or via a form. Stores a file ID. |
| `html` | A string, rendered as sanitized html, that enables the use of a rich text editor for the property. |
| `number` | A string of numerals or numbers written in decimal or scientific notation. |
| `phonenumber` | A plain text string, displayed as a formatted phone number. |
| `radio` | An input that will allow users to select one of a set of options allowed for the property. When used in a form, this will be displayed as a set of radio buttons. |
| `select` | A dropdown input that will allow users to select one of a set of options allowed for the property. |
| `text` | A plain text string, displayed in a single line text input. |
| `textarea` | A plain text string, displayed as a multi-line text input. |

### Date, number, and text display formats

For `date`, `number`, and `text` field types, add an optional display field to specify how the values should be rendered in HubSpot. Learn more about [how different formatting types are displayed](https://knowledge.hubspot.com/properties/property-field-types-in-hubspot).

| Field Type | Display field | Supported values |
| - | - | - |
| `date` | `dateDisplayHint` | `absolute` (default), `absolute_with_relative`, `time_since`, `time_until` |
| `number` | `numberDisplayHint` | `formatted` (default), `duration`, `percentage`, `unformatted` |
| `text` | `textDisplayHint` | `domain_name` |

<Note>
  **Please note:**  To render a number value as a currency, include the field `showCurrencySymbol` and set the value as `true`.
</Note>

For example, to create a *Discount* property that displays a customer's discount as a percentage, your request body would look like:

```json theme={null}
{
  "groupName": "dealinformation",
  "name": "discount",
  "label": "Discount",
  "type": "number",
  "fieldType": "number",
  "numberDisplayHint": "percentage"
}
```

## Create a property

To create a property, make a `POST` request to `/crm/properties/2026-09/{objectType}`. In your request body, include the following required fields:

* `groupName`: the [property group](https://knowledge.hubspot.com/properties/organize-and-export-properties) the property will be in.
* `name`: the internal name of the property (e.g., favorite\_food).
* `label`: the name of the property as it appears in HubSpot (e.g., Favorite Food).
* `type`: the [type](#property-type-and-fieldtype-values) of property.
* `fieldType`: the [field type](#property-type-and-fieldtype-values) of the property.

For example, to create a contact property called *Favorite Food*, your request would look like:

```json theme={null}
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

### Create unique identifier properties

When a record is created in HubSpot, a unique ID (`hs_object_id`) is automatically generated and should be treated as a string. These IDs are unique only within that object type, so there can be both a contact and company with the same ID. For contacts and companies, there are additional unique identifiers, including a contact's email address (`email`) and a company's domain name (`domain`).

In some cases, you want may to create your own unique identifier property so that you can't enter the same value for multiple records. You can have up to ten unique ID properties per object. To create a property requiring unique values via API:

1. Make a `POST` request to `/crm/properties/2026-09/{objectType}`.
2. In your request body, for the `hasUniqueValue` field, set the value to `true`.

```json theme={null}
{
  "groupName": "dealinformation",
  "name": "system_a_unique",
  "label": "Unique ID for System A",
  "hasUniqueValue": true,
  "type": "string",
  "fieldType": "text"
}
```

Once you've created your unique ID property, you can use it in an API call to retrieve specific records. For example, to retrieve a deal with a value of `abc` for the `system_a_unique` property, your request URL would be: `/crm/objects/2026-09/deals/abc?idProperty=system_a_unique`.

You can then use this unique identifier property value to identify and update specific records in the same way you could use `hs_object_id`, `email` (contacts), or `domain` (companies).

<Note>
  When cloning a record with a unique property value, the value will not be copied to the new record. This is because uniqueness is enforced across all records of that object type, and copying the value would cause a conflict. To set unique property values on cloned records, update the new record after creation.
</Note>

### Create calculation properties

Calculation properties define a property value based on other properties within the same object record. They are defined using a formula, which may include operations like min, max, count, sum, or average. You can use the properties API to read or create calculation properties in your HubSpot account, using a field type of `calculation_equation` and a type of `number`, `bool`, `string`, or `enumeration`.

You can define the property's calculation formula with the `calculationFormula` field. Using `calculationFormula`, you can write your formula with arithmetic operators, comparison operators, logic operators, conditional statements, and other functions.

<Warning>
  Calculation properties created via API <u>cannot</u> be edited within HubSpot. You can only edit these properties via the properties API.
</Warning>

#### Literal syntax

* **String literal**: constant strings can be represented with either single quotes (`'constant'`) or double quotes (`"constant"`).
* **Number literal**: constant numbers can be any real numbers, and can include point notation. `1005` and `1.5589` are both valid constant numbers.
* **Boolean literal**: constant booleans can be `true` or `false`.

#### Property syntax

* **String property variables:** for an identifier string to be interpreted as a string property, it must be wrapped in the `string` function. For example, `string(var1)`will be interpreted as the value for the string property var1.
* **Number property variables**: all identifiers will be interpreted as number property variables. For example, `var1` will be interpreted as the value for the number property var1.
* **Boolean property variables**: for an identifier to be interpreted as a bool property, it must be wrapped in the `bool` function. For example, the identifier `bool(var1)` will be interpreted as the value for the boolean property var1.

<Warning>
  The language used is case sensitive for all types <u>except</u> strings. For example, `If A ThEn B` is exactly the same as `if a then b` but `'a'` is not the same as `'A'`. Spaces, tabs, and new lines will be used for tokenization but will be ignored.
</Warning>

#### Operators

Operators can be used with literal and property values. For arithmetic operators, you can use prefix notation to multiply, and parenthesis can be used to specify the order of operations.

| Operator | Description | Examples |
| - | - | - |
| `+` | Add numbers or strings. | `property1 + 100` |
| `-` | Subtract numbers. | `property1 + 100 - property2` |
| `*` | Multiply numbers. | `10property1` = `10 * property1` |
| `/` | Divide numbers. | `property1 * (100 - property2/(50 - property3))` |
| `<` | Checks if a value is less than another. Supported by number properties or constants. | `a < 100` |
| `>` | Checks if a value is greater than another. Supported by number properties or constants. | `a > 50` |
| `<=` | Checks if a value is less than or equal to another. Supported by number properties or constants. | `a <= b` |
| `>=` | Checks if a value is greater than or equal to another. Supported by number properties or constants. | `b>= c` |
| `=` | Checks if a value is equal to another. Supported by both numbers and strings. | `(a + b - 100c * 150.652) = 150-230b` |
| `equals` | Checks if a value is equal to another. Supported by both numbers and strings. | `a + b - 100.2c * 150 equals 150 - 230` |
| `!=` | Checks if a value is not equal to another. Supported by both numbers and strings. | `string(property1) != 'test_string'` |
| `or` | Checks if either or two values are true. | `a > b or b <= c` |
| `and` | Checks if both values are true. | `bool(a) and bool(c)` |
| `not` | Checks if none of the values are true. | `not (bool(a) and bool(c))` |

#### Functions

The following are supported functions:

| Function | Description | Examples |
| - | - | - |
| `max` | Will have between 2 and 100 input numbers, and will return the maximum number out of all the inputs. | `max(a, b, c, 100)` or `max(a, b)` |
| `min` | Will have between 2 and 100 input numbers, and will return the minimum number of out all the inputs. | `min(a, b, c, 100)` or `min(a, b)` |
| `is_present` | Evaluates whether an expression can be evaluated. | `is_present(bool(a))`= true if the property is boolean, but `is_present(bool(a))` = false if the property is empty or not boolean. |
| `contains` | Has two strings as inputs and will return true if the first input contains the second. | `contains('hello', 'ello')` = `true` while `contains('ello', 'hello')` = false. |
| `concatenate` | Joins a list of strings. The list of inputs can go from 2 up to 100. | `concatenate('a', 'b', string(a), string(b))` |

There are also two parsing functions:

* `number_to_string`: tries to convert the input number expression to a string.
* `string_to_number`: tries to convert the input string expression to a number.

For example, `"Number of cars: " + num_cars` is not a valid property because you can't add a string with a number, but `"Number of cars: " + number_to_string(num_cars)` is.

#### Conditional statements

You can also write your formula with conditional statements using `if`, `elseif`, `endif`, and `else`.

For example, a conditional statement could look like: `if boolean_expression then statement [elseif expression then statement]* [else statement | endif]` where the `[a]` brackets represent that a is optional, the `a|b` represent that either a or b will work, and `*` means 0 or more. `endif` can be used to finish a conditional statement prematurely, ensuring that the parser can identify which `if` the next `elseif` belongs to.

#### Example formulas

The following are examples you can use to help define your own calculation formulas:

```json theme={null}
"calculationFormula": "closed - started"
```

A more advanced example with conditionals:

```json theme={null}
"calculationFormula": "if is_present(hs_latest_sequence_enrolled_date) then
  if is_present(hs_sequences_actively_enrolled_count) an hs_sequences_actively_enrolled_count >= 1 then
    true
  else
    false
else
  ''"
```

## Retrieve properties

You can retrieve information for individual properties or all properties within an object.

* To retrieve an individual property, make a `GET` request to `crm/properties/2026-09/{object}/{propertyName}`. For example, to retrieve the `favorite_food` property, your request URL would be `/crm/properties/2026-09/contacts/favorite_food`.
* To retrieve all properties for an object, make a `GET` request to `/crm/properties/2026-09/{objectType}`.

<Warning>
  When retrieving all properties, by default only non-sensitive properties are returned. To retrieve sensitive data properties, include the `dataSensitivity` query parameter with the value `sensitive`. Learn more about [managing sensitive data via API](/docs/api-reference/latest/crm/properties/sensitive-data#manage-sensitive-data) (BETA, *Enterprise* only).
</Warning>

## Update or clear a property's values

To update a property value for a record, make a `PATCH` request to `crm/objects/2026-09/{objectType}/{recordId}`. In your request body, include the properties and their values in an array. Learn more about updating records via the [object APIs](/docs/api-reference/latest/crm/understanding-the-crm).

The following sections explain how to set or update property values where unique formatting or steps are required.

<Tip>
  Property value updates are stored in a [record's property history](https://knowledge.hubspot.com/records/view-record-property-history). To view historical values via API, [retrieve records](/docs/api-reference/latest/crm/using-object-apis#retrieve-records) with the `propertiesWithHistory` parameter. To track property updates on a record timeline, you can create a property change event [in HubSpot](https://knowledge.hubspot.com/reports/create-a-property-change-event) or use the [events API](/docs/api-reference/legacy/events/define-events/guide).
</Tip>

<CrmWriteValidationEnforcement />

### Add values to date and datetime properties

Time values are represented in ISO 8601 format in responses, but HubSpot APIs will accept either of two formats for date and time values:

* **ISO 8601 formatted strings**: depending on the type of data, these will be one of two different formats:
  * For values that represent a specific date, the complete date format will be used: YYYY-MM-DD (e.g. `2020-02-29`)
  * For values that represent a specific date and time, the complete date plus hours, minutes, seconds, and a decimal fraction of a second format will be used: YYYY-MM-DDThh:mm:ss.sTZD (e.g. `2020-02-29T03:30:17.000Z`). All times are represented in UTC, so the values will always use the UTC designator "Z."
* **UNIX-formatted timestamps in milliseconds**: timestamp values in milliseconds, which are represented in UTC time. For example, the timestamp value `1427997766000` translates to *02 Apr 2015 18:02:46 UTC*, or *April 2nd, 2015, 2:02:46 PM EDT* (Eastern Daylight Saving Time).

There are two types of properties for storing dates (`date` and `datetime`) which also affect how you format values:

* `date` properties store the date, <u>not</u> the time. `date` properties display the date they're set to, regardless of the time zone setting of the account or user. For `date` property values, it is recommended to use the ISO 8601 complete date format. If you use the UNIX timestamp format, you must use an EPOCH millisecond timestamp (i.e. the value must be set to midnight UTC for the date). For example, to represent May 1, 2015 in either format:
  * **IOS 8601**: 2015-05-01
  * **UNIX millisecond timestamp**: 1430438400000
* `datetime` properties store <u>both</u> the date and time. Either timestamp format will be accepted. In HubSpot, `datetime` properties are displayed based on the time zone of the user viewing the record, so the value will be converted to the local time zone of the user.

### Add values to checkbox type properties

When updating values for a record's checkbox type properties, format the values in the following ways:

* **Boolean** **checkbox property**: to display as *Yes*, or checked in HubSpot, your value must be `true`. To display as *No* or not checked in HubSpot, your value must be `false`.
* **Multiple select** **checkbox property**: to add or append values to a multiple checkboxes property, add a semicolon before the first value, and separate the values with semicolons without a space between. If the property has an existing value, the leading semicolon will append the values instead of overwriting the value. For example, a contact has the existing value `DECISION_MAKER` for the `hs_buying_role` property. To add additional values without replacing the existing value, your request would look like this:

```json theme={null}
{
  "properties": {
    "hs_buying_role": ";BUDGET_HOLDER;END_USER"
  }
}
```

### Assign record owners with user properties

When assigning users to CRM records via API, your value must be user's owner `id`, which you can find in your [property settings](https://knowledge.hubspot.com/properties/create-and-edit-properties) or via the [owners API](/docs/api-reference/latest/crm/owners/guide).

For example, to assign a user as owner of a contact, send a `PATCH` request to `crm/objects/2026-09/contacts/{contactId}`, with the body `{ "properties":{ "hubspot_owner_id": "41629779"}}`.

### Clear a property value

You can clear an object property value via the API by setting the property value to an empty string.

For example, to clear the `firstname` from a contact object, send a `PATCH` request to `/crm/objects/2026-09/contacts/{contactId}` with the body `{ "properties": { "firstname": ""}}`.
