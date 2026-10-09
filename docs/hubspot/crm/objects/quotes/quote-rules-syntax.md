> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Quote rules syntax

> Reference information for writing quote validation rules using the quote rules DSL.

The quote rules domain-specific language (DSL) provides a structured way to [define rule conditions for quotes](https://knowledge.hubspot.com/quotes/configure-quote-rules). The DSL uses SQL-like syntax, with constructs such as `FROM`, `WHERE`, `EXISTS`, and aggregate functions such as `COUNT`, `SUM`, `MIN`, and `MAX`.

Instead of writing raw JSON, you use expressions to evaluate line items, quote properties, and related CRM data. Each rule expression describes a violation condition, which is a rule that evaluates to true when the condition is met. You can define logic such as product requirements, incompatibilities, pricing thresholds, and validation rules. For example, you can require certain products to be sold together, prevent incompatible products from being added to the same quote, or enforce quantity limits.

## Prerequisites

Before using the DSL, it's recommended that you:

* Have familiarity working with CRM objects and their properties (e.g., line items, quotes, deals).
* Understand logical operators such as `AND`, `OR`, and `NOT`.
* Know the property names available in your CRM, which you can find either in the account's property settings or via the [properties API](/docs/api-reference/latest/crm/properties/guide).

Also keep in mind the following:

* Property references must follow strict syntax and validation rules.
* Some calculations (e.g., arithmetic inside aggregate functions) are not supported.
* Invalid property names or syntax will return parser errors.

## Best practices

* Use square brackets for all property references to distinguish them from other value types (e.g., `[quantity]` is a property while `"quantity"` is a string literal).
* Use explicit scope prefixes (e.g., `line_item.`, `quote.`) when referencing properties outside a `WHERE` clause.
* Add parentheses to clarify evaluation order in complex expressions.
* Validate property names against your CRM before writing rules to ensure the properties exist.
* Test rules with sample data to verify that rules work as expected, and use a [sandbox environment](https://knowledge.hubspot.com/account-management/deploy-sandbox-changes-to-production) when possible.

## Syntax overview

The DSL supports the following syntax:

* **Boolean logic:** `AND`, `OR`, `NOT`
* **Quantifiers:** `EXISTS`, `ALL_MATCH`, `NONE_MATCH`
* **Comparisons:** `=`, `!=`, `>`, `<`, `>=`, `<=`, `CONTAINS`, `STARTS_WITH`
* **Group expressions:** `SOLD_TOGETHER`, `INCOMPATIBLE`, `ALL_SAME`
* **Aggregates:** `COUNT`, `SUM`, `MIN`, `MAX`
* **Property references:** bracket notation (e.g., `[property_name]`)
* **Arithmetic operations:** `+`, `-`, `*`, `/`

## Property references

The DSL validates all property references against CRM data. All property references must be wrapped in square brackets.

* Outside a `WHERE` clause, use `object.property` dot notation to scope the property to a specific object. For example, `[quote.hs_quote_amount]` describes the quote property `hs_quote_amount`.
* Inside a `WHERE` clause, properties inherit their scope from the clause object. For example, the clause `FROM line_items WHERE [hs_product_id] = ...` references the line item property `hs_product_id`.

Note that you cannot scope a property to a different object type inside a `WHERE` clause. For example, the following rule is invalid because `product.` is a different object scope than `line_items`:

```sql wrap theme={null}
EXISTS FROM line_items WHERE [hs_product_id] = "15493657257" AND [product.price] / [quantity] != 150
```

Some common examples of property references include:

```sql wrap theme={null}
[line_item.property]
[quote.property]
[deal.property]
[company.property]
[recipient_contact.property]
[billing_contact.property]
[billing_company.property]
[payment_schedule.property]
[quote_template.property]
[contract.property]
[current_user.property]
```

You can reference both HubSpot default properties and custom properties. Custom properties follow the same dot notation scope rules as standard properties (e.g., `[quote.my_custom_property]`). Custom property names must:

* Start with a letter.
* Contain only letters, numbers, or underscores.
* Include a valid object scope.

<Note>
  The rule editor renders human-readable labels for recognized properties and objects rather than their internal names. For example, `[hs_product_id]` displays as `Product` and `line_item` displays as `Line item`. If the value doesn't match a recognized property or object, the editor renders the raw syntax instead.

  <Frame>
    <img src="https://developers.hubspot.com/hubfs/Knowledge_Base_2023-24-25/KB-quotes/quote-rule-editor-syntax-rendered-labels.png" alt="Rule editor showing [Product] label instead of [hs_product_id] internal property name" />
  </Frame>
</Note>

### Line item properties

Standard line item property references include:

| Property | Description |
| - | - |
| `hs_product_id` | Product identifier |
| `name` | Product name |
| `quantity` | Item quantity |
| `hs_sku` | Stock keeping unit |
| `description` | Product description |
| `hs_discount_percentage` | Discount percentage |
| `price` | List price before discounts |
| `amount` | Total after discounts |

<Note>
  To check the net unit price after discounts, use `[amount] / [quantity]` rather than `[price]`. For example, to enforce that a product must sell at \$300, use `[amount] / [quantity] != 300`, not `[price] != 300`.
</Note>

### Quote properties

Standard quote property references include:

| Property | Description |
| - | - |
| `quote.hs_title` | Quote title |
| `quote.hs_status` | Quote status |
| `quote.hs_expiration_date` | Expiration date |
| `quote.hs_currency` | Currency code |
| `quote.hs_language` | Language code |

<Warning>
  **Please note:** quote-level discount properties are not available in the DSL.
</Warning>

## Basic expressions

### Existence checks

Use quantifiers to check whether line items matching a condition exist.

```sql wrap theme={null}
# "enterprise" product exists
EXISTS FROM line_item WHERE [hs_product_id] = "enterprise"

# Filter out all non-inventory products
NONE_MATCH FROM line_item WHERE [hs_product_type] = "non-inventory"

# All taxable items
ALL_MATCH FROM line_item WHERE [taxable] = "true"
```

### Comparisons

Use comparison operators to evaluate property values. When referencing line item properties outside a `WHERE` clause, use an explicit scope prefix.

```sql wrap theme={null}
# Simple comparison (requires explicit scope outside WHERE)
[line_item.quantity] > 5

# Quote-level comparison
[quote.hs_currency] = "USD"

# String operations
[line_item.name] CONTAINS "Enterprise"
[line_item.hs_sku] STARTS_WITH "ENT-"
```

## Group expressions

Group expressions simplify common multi-product validation patterns.

### SOLD\_TOGETHER

Requires all products in a group to be present if any one of them is present. This expression is shorthand for the more verbose `(EXISTS ... OR EXISTS ...) AND NOT (EXISTS ... AND EXISTS ...)` pattern.

```sql wrap theme={null}
SOLD_TOGETHER FROM line_item WHERE [hs_product_id] IN ("A", "B", "C")
```

* **Pass:** none or all products are present.
* **Violation:** only some products are present.

### INCOMPATIBLE

Ensures that only one product from a group is present. This expression is shorthand for the more verbose `EXISTS ... OR EXISTS ...` pattern.

```sql wrap theme={null}
INCOMPATIBLE FROM line_item WHERE [hs_product_id] IN ("STARTER", "PRO", "ENTERPRISE")
```

* **Pass:** zero or one product present.
* **Violation:** multiple products present.

### ALL\_SAME

Ensures all line items share the same value for a given property. An optional `WHERE` clause filters items before checking uniformity.

```sql wrap theme={null}
# All items must share the same thread type
ALL_SAME [threadType] FROM line_item

# Only check fittings
ALL_SAME [threadType] FROM line_item WHERE [category] = "fitting"
```

* **Pass:** all values match, or no items exist.
* **Violation:** multiple different values detected.

## Compound expressions

### Boolean operators

Use `AND`, `OR`, and `NOT` to combine multiple conditions.

```sql wrap theme={null}
# AND: both conditions must be true
EXISTS FROM line_item WHERE [type] = "valve" AND EXISTS FROM line_item WHERE [type] = "controller"

# OR: at least one condition must be true
[quote.hs_status] = "pending" OR [quote.hs_status] = "draft"

# NOT: negates the expression
NOT EXISTS FROM line_item WHERE [hs_product_id] = "support"
```

### Nested logic

Use parentheses to group conditions and clarify evaluation order in complex expressions.

```sql wrap theme={null}
(EXISTS FROM line_item WHERE [tier] = "enterprise" OR EXISTS FROM line_item WHERE [tier] = "premium")
AND NOT EXISTS FROM line_item WHERE [support_plan] = "none"
```

## Aggregate expressions

### COUNT

Count the number of line items, optionally filtered by a condition.

```sql wrap theme={null}
# Count all items
COUNT FROM line_item > 10

# Count with filter
COUNT FROM line_item WHERE [type] = "addon" <= 3
```

### SUM

Sum a numeric property across line items, optionally filtered by a condition.

```sql wrap theme={null}
# Sum a property
SUM([quantity]) FROM line_item > 100

# Sum with a filter
SUM([price]) FROM line_item WHERE [category] = "hardware" < 10000
```

### MIN and MAX

Check the minimum or maximum value of a property across line items.

```sql wrap theme={null}
# Check minimum discount
MIN([hs_discount_percentage]) FROM line_item >= 5

# Check maximum quantity
MAX([quantity]) FROM line_item <= 50
```

## Arithmetic

Use arithmetic operators to perform calculations across aggregate expressions.

```sql wrap theme={null}
# At least 5 valves per controller
COUNT FROM line_item WHERE [type] = "valve" >= COUNT FROM line_item WHERE [type] = "controller" * 5
```

<Note>
  Arithmetic inside aggregate functions (e.g., `SUM([quantity] * [price])`) is not supported. Use separate aggregates and compare them instead.
</Note>

## Common examples

### Required products

The following rule validates that an Enterprise tier product cannot be added to a quote without also including a support plan.

```sql wrap theme={null}
EXISTS FROM line_item WHERE [hs_product_id] = "enterprise"
AND NOT EXISTS FROM line_item WHERE [hs_product_id] = "support"
```

### Incompatible products

The following rule validates that legacy and modern platform products cannot coexist on the same quote.

```sql wrap theme={null}
INCOMPATIBLE FROM line_item WHERE [platform] IN ("legacy", "modern")
```

### Bundle validation

The following rule validates that if any item from a bundle is added, all items in the bundle must be included.

```sql wrap theme={null}
SOLD_TOGETHER FROM line_item WHERE [bundle_id] IN ("starter", "starter-support")
```

### Quantity limits

The following rule enforces a maximum of five Enterprise licenses per quote.

```sql wrap theme={null}
SUM([quantity]) FROM line_item WHERE [hs_sku] = "ENT-LICENSE" > 5
```

### Approval thresholds

The following rules check for conditions that would require manual approval: discounts over 20% and quotes with a total amount over \$100,000.

```sql wrap theme={null}
[line_item.hs_discount_percentage] > 20

[quote.hs_quote_amount] > 100000
```

## Error handling

The parser returns descriptive error messages that indicate the position of the issue and suggest corrections. For example:

```text wrap theme={null}
Property references must be wrapped in brackets.
Use '[line_item.property]' instead of 'line_item.property'
         ^
Position: 15
```

Common causes of parser errors include:

* Missing brackets around property references.
* Using an invalid or misspelled property name.
* Referencing a line item property without an explicit scope outside a `WHERE` clause.
* Using unsupported arithmetic inside aggregate functions.
