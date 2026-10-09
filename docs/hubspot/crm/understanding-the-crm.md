> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Understanding the CRM APIs

> HubSpot's CRM is a system for managing customer relationships and data. Learn about objects and the related CRM APIs.

The foundation of your HubSpot account is a database of your business relationships and processes, called the CRM (Customer Relationship Management). To manage this data, HubSpot accounts include objects, which represent types of relationships or processes. Individual instances of objects, called records, represent the individual entities under each object type (e.g., John Smith is a contact). To store data in each record, you'll use properties (e.g., the email property) and to represent the relationships between individual entities, you can associate records with one another (e.g., associate John Smith with a company Smith & Co.). Records can also store information about interactions through associated engagements/activities, such as emails, calls, and meetings.

In this article, learn about objects, records, properties, associations, pipelines, schemas, and searching the CRM. To learn more about managing your CRM database from within HubSpot, check out [HubSpot's Knowledge Base](https://knowledge.hubspot.com/get-started/manage-your-crm-database).

## Object APIs

You use the object APIs to create and manage an object's records. For supported objects, you can use object endpoints and replace the `{objectTypeId}` in the request URL with the desired object. For example, to create contacts, you'd make a `POST` request to `crm/objects/2026-09/0-1` and to create courses, you'd make a `POST` request to `crm/objects/2026-09/0-410`.

Refer to [this article](/docs/api-reference/latest/crm/using-object-apis) for more information about using the object endpoints for various objects.

### Object type IDs

When using CRM and other APIs, you'll need to use the `objectTypeId` field, which is a unique numerical value assigned to each object. For example, to retrieve records, you'd make a `GET` request to `/crm/objects/2026-09/{objectTypeId}`, or when creating a property for an object, you'd make a `POST` request to `/crm/properties/2026-09/{objectTypeId}`.

Expand the section below to view objects and their object type ID values.

<Accordion title="Object type ID values">
  | Object | Type ID | Description |
  | - | - | - |
  | Appointments | `0-421` | Represent encounters or services scheduled for an individual. View the [appointments API](/docs/api-reference/latest/crm/objects/appointments/guide) |
  | Calls | `0-48` | A type of activity that represents phone call interactions associated with your records. View the [calls API](/docs/api-reference/latest/crm/activities/calls/guide) |
  | Carts | `0-142` | Stores data related to ecommerce purchases in HubSpot. View the [carts API](/docs/api-reference/latest/crm/objects/carts/guide) |
  | Communications | `0-18` | A type of activity that represents SMS, LinkedIn, and WhatsApp message interactions associated with your records. View the [communications API](/docs/api-reference/latest/crm/objects/communications/guide) |
  | Companies | `0-2` | Stores information about a business or organization. View the [companies API](/docs/api-reference/latest/crm/objects/companies/guide) |
  | Contacts | `0-1` | Stores information about an individual person. View the [contacts API](/docs/api-reference/latest/crm/objects/contacts/guide) |
  | Courses | `0-410` | Represent structured programs or series of lessons, trainings, or educational modules. View the [courses API](/docs/api-reference/latest/crm/objects/courses/guide) |
  | Custom objects | `2-XXX` | Stores data that doesn't fit in with existing objects. To find the `objectTypeId` for a custom object, make a `GET` request to `/crm-object-schemas/2026-09/schemas`. View the [objects API](/docs/api-reference/latest/crm/using-object-apis) |
  | Deals | `0-3` | Represent sales opportunities and transactions, tracked through pipeline stages. View the [deals API](/docs/api-reference/latest/crm/objects/deals/guide) |
  | Discounts | `0-84` | Associated with quotes as part of their pricing details. View the [discounts API](/docs/api-reference/latest/crm/objects/discounts/guide) |
  | Emails | `0-49` | A type of activity that represents one-to-one email interactions associated with your records. View the [email API](/docs/api-reference/latest/crm/activities/emails/guide) |
  | Feedback submissions | `0-19` | Stores information submitted to a feedback survey. Feedback submissions are associated with contact records. View the [feedback submissions API](/docs/api-reference/latest/crm/objects/feedback-submissions/guide) |
  | Fees | `0-85` | Associated with quotes as part of their pricing details. View the [fees API](/docs/api-reference/latest/crm/objects/fees/guide) |
  | Goals | `0-74` | Represent targets for HubSpot users. View the [goals API](/docs/api-reference/latest/crm/objects/goals/guide) |
  | Invoices | `0-53` | Represent the invoices sent for sales transactions. View the [invoices API](/docs/api-reference/latest/crm/objects/invoices/guide) |
  | Leads | `0-136` | Represent potential customers who have shown interest in your products or services. View the [leads API](/docs/api-reference/latest/crm/objects/leads/guide) |
  | Line items | `0-8` | Represent individual products and services sold in a deal. Line items can be created from existing products in your product library, or can be created standalone. View the [line items API](/docs/api-reference/latest/crm/objects/line-items/guide) |
  | Listings | `0-420` | Represent properties or units to be bought, sold, or rented. View the [listings API](/docs/api-reference/latest/crm/objects/listings/guide) |
  | Marketing events | `0-54` | Represent events related to your marketing efforts, specifically including events from connected integrations. You can specify whether or not a contact attended, registered for, or cancelled attending a marketing event. View the [marketing events API](/docs/api-reference/latest/marketing/marketing-events/guide) |
  | Meetings | `0-47` | A type of activity that represents meeting interactions associated with your records. View the [meetings API](/docs/api-reference/latest/crm/activities/meetings/guide) |
  | Notes | `0-46` | A type of activity that represents notes associated with your records. View the [notes API](/docs/api-reference/latest/crm/activities/notes/guide) |
  | Orders | `0-123` | Represent ecommerce purchases in HubSpot. View the [orders API](/docs/api-reference/latest/crm/objects/orders/guide) |
  | Payments | `0-101` | The payments made by buyers through invoices, payment links, and quotes. View the [payments API](/docs/api-reference/latest/crm/objects/commerce-payments/guide) |
  | Postal mail | `0-116` | A type of activity that represents physical mail interactions associated with your records. View the [postal mail API](/docs/api-reference/latest/crm/activities/postal-mail/guide) |
  | Products | `0-7` | Represent goods or services for sale. Products can't be associated with other objects, but you can create line items based on products and associate those with deals and quotes. View the [products API](/docs/api-reference/latest/crm/objects/products/guide) |
  | Projects | `0-970` | Centralized tasks to help your team manage work. View the [projects API](/docs/api-reference/latest/crm/objects/projects/guide) |
  | Quotes | `0-14` | Represent pricing information shared with potential buyers. View the [quotes API](/docs/api-reference/latest/crm/objects/quotes/guide) |
  | Services | `0-162` | Represent intangible offerings provided to customers. Examples include onboarding and consulting, repairs and maintenance, and personal care. View the [services API](/docs/api-reference/latest/crm/objects/services/guide) |
  | Subscriptions | `0-69` | Represent recurring payments scheduled through payment links and quotes. View the [subscriptions API](/docs/api-reference/latest/crm/objects/commerce-subscriptions/guide) |
  | Tasks | `0-27` | A type of activity that represents to-dos associated with your records. View the [tasks API](/docs/api-reference/latest/crm/activities/tasks/guide) |
  | Taxes | `0-86` | Associated with quotes as part of their pricing details. View the [taxes API](/docs/api-reference/latest/crm/objects/taxes/guide) |
  | Tickets | `0-5` | Represent customer requests for help or support, tracked through pipeline statuses. View the [tickets API](/docs/api-reference/latest/crm/objects/tickets/guide) |
  | Users | `0-115` | Represent the users in your HubSpot account. Users cannot be associated with other objects, but can be retrieved and updated via API. View the [user details API](/docs/api-reference/latest/crm/objects/users/guide) |
</Accordion>

You can always use the numerical type ID value, but for contacts, companies, deals, tickets, or notes, in some cases you can also use the object's fully qualified name (FQN). For example:

* When starting an import with the [imports API](/docs/api-reference/latest/crm/imports/guide), the `columnObjectTypeId` specifies which object the data in your file belongs to. To import data for contacts, your value for `columnObjectTypeId` could be `contact` or `0-1`.
* When using the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide), the `fromObjectType` and `toObjectType` values specify the objects and the direction of the association. To view association types for contacts to companies, your `GET` request could be to `crm/associations/2026-09/contact/company/labels` or `crm/associations/2026-09/0-1/0-2/labels`.

### Unique identifiers and record IDs

A unique identifier is a value that differentiates one record in the CRM from another, even if they have otherwise identical information. For example, a database might have records for two people named John Smith. To avoid accidentally sending money to the wrong John Smith, each record is assigned a number as their *Record ID*.

When a record is created in HubSpot, its *Record ID* (`hs_object_id`) is automatically generated and should be treated as a string. Record IDs are unique within an object, so there can be both a contact and company with the same ID. For contacts and companies, there are additional unique identifiers, including a contact's `email` and a company's `domain` name. You can also [create custom unique identifier properties](/docs/api-reference/latest/crm/pipelines/guide#create-unique-identifier-properties).

In the CRM APIs, you'll use unique identifier values to identify and manage specific records. You can always use a record's `hs_object_id` value, but can also use custom unique identifier properties for certain endpoints, specified by the `idProperty` parameter. For example, to edit a contact, you could make a `PATCH` request to `/crm/objects/2026-09/0-1/{contactId}` or `/crm/objects/2026-09/0-1/{contactEmail}?idProperty=email`. Learn more about how HubSpot handles deduplication in the [Knowledge Base](https://knowledge.hubspot.com/records/deduplication-of-records).

## Associations API

In HubSpot, you can show how objects are related to one another by associating their records. For example, you can associate multiple contacts with a company, and then associate the company and relevant contacts with a deal. You can use the associations API to manage which association types are supported between objects and to associate individual records within objects.

The Associations API includes two sets of endpoints:

* [**Association details endpoints**](/docs/api-reference/latest/crm/associations/associate-records/guide): create, edit, and remove associations between records. For example, associate a contact record with a company record.
* [**Association schema endpoints**](/docs/api-reference/latest/crm/associations/associations-schema/guide): view and manage your account's association definitions (also known as types or labels) and set limits for associations. For example, create a custom *Decision Maker* association type to associate a contact record and a company record while labelling the contact as that company's *Decision Maker*.

When using the [associations API endpoints](/docs/api-reference/latest/crm/associations/associate-records/guide), you can substitute objects for `{toObjectTypeId}` and `{fromObjectTypeId}` in the request URLs and request bodies.

Before associating records across objects, to understand which objects can be associated to one another, you can [retrieve association types](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-labels). If you have access to a HubSpot account, you can also review your account's unique object relationships by navigating to [the data model tool.](https://knowledge.hubspot.com/data-management/use-the-data-model-builder)

Learn more about object relationships and managing associations in the associations API guides:

* [Association details guide](/docs/api-reference/latest/crm/associations/associate-records/guide)
* [Association schemas guide](/docs/api-reference/latest/crm/associations/associations-schema/guide)

## Properties API

Information about records are stored in fields called properties. HubSpot provides a set of default properties for each object. In addition to each object's default properties, you can store custom data by [creating custom properties](https://knowledge.hubspot.com/properties/create-and-edit-properties).

When using the properties API, you can substitute objects in the endpoints to create and manage an object's properties. For example, `/crm/properties/2026-09/0-1` for contact properties or `/crm/properties/2026-09/0-5` for ticket properties.

Learn more about using the properties API in [this article](/docs/api-reference/latest/crm/properties/guide).

## Schemas API

Each object in HubSpot is defined by a schema, which is a set of configuration details that define what the object is (i.e. its name and ID), the data that it can store (i.e. properties), and its relationships with other objects (i.e. associations).

The schemas API can be used to [create custom objects](/docs/api-reference/latest/crm/objects/custom-objects/guide), which includes setting up schema details such as display properties, searchable properties, unlabeled associations, and properties required to create records. Learn more about [custom objects in HubSpot](https://knowledge.hubspot.com/object-settings/create-custom-objects).

The schemas API can also be used to [retrieve schema details](/docs/api-reference/latest/crm/objects/custom-objects/guide) for custom objects, which will return those high-level object details. However, to manage an object's properties and association types, you'll use the [properties](#properties-api) and [associations](#associations-api) APIs.

## Search API

To filter and sort records and activities based on their properties and associations, you can use the search API. When using the search endpoints, substitute the `{objectTypeId}` value for the object within which you want to search. For example, to search calls, you'd make a POST request to `/crm/objects/2026-09/0-48/search`.

Learn more about using the CRM search API in [this article](/docs/api-reference/latest/crm/search-the-crm).

## Pipelines API

In HubSpot, you can use pipelines to track records through stages in your processes. For example, you can track deals through sales processes or tickets through support statuses. Using the pipelines API, you can create, retrieve, edit, and delete pipelines and pipeline stages.

Learn which objects have pipelines and how to use the pipelines API in [this article](/docs/api-reference/latest/crm/pipelines/guide).
