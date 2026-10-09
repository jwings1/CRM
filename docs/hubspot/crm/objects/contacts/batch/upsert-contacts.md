> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Upsert contacts

> Upsert a batch of contacts. The `inputs` array can contain a `properties` object to define property values for each record.

export const UserLevelAccessCallout = () => <div className="px-5 py-3.5 gap-3 flex flex-row">
    <div>
      <Icon icon="user" size={16} />
    </div>
    <div>
      Supports <a href="/docs/apps/developer-platform/build-apps/authentication/user-level-apps">user-level access</a>.
    </div>
  </div>;

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

export const SupportedProducts = ({marketing, sales, service, cms, data, commerce, crm, marketingLevel, salesLevel, serviceLevel, cmsLevel, dataLevel, commerceLevel, crmLevel}) => {
  const translations = {
    description: "Requires one of the following products or higher.",
    productNames: {
      marketing: "Marketing Hub",
      sales: "Sales Hub",
      service: "Service Hub",
      cms: "Content Hub",
      data: "Data Hub",
      commerce: "Revenue Hub",
      crm: "Smart CRM"
    },
    tiers: {
      free: "Free",
      starter: "Starter",
      professional: "Professional",
      enterprise: "Enterprise"
    }
  };
  const translateTier = tier => {
    if (!tier) return '';
    const lowerTier = tier.toLowerCase();
    return translations.tiers[lowerTier] || tier;
  };
  const products = [{
    name: marketing ? translations.productNames.marketing : '',
    level: translateTier(marketingLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/MarketingHub.svg",
    alt: "Marketing Hub"
  }, {
    name: sales ? translations.productNames.sales : '',
    level: translateTier(salesLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/SalesHub.svg",
    alt: "Sales Hub"
  }, {
    name: service ? translations.productNames.service : '',
    level: translateTier(serviceLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/ServiceHub.svg",
    alt: "Service Hub"
  }, {
    name: cms ? translations.productNames.cms : '',
    level: translateTier(cmsLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/ContentHub.svg",
    alt: "Content Hub"
  }, {
    name: data ? translations.productNames.data : '',
    level: translateTier(dataLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/DataHub.svg",
    alt: "Data Hub"
  }, {
    name: commerce ? translations.productNames.commerce : '',
    level: translateTier(commerceLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base/subscription_key_icons/commerce_icon.svg",
    alt: "Revenue Hub"
  }, {
    name: crm ? translations.productNames.crm : '',
    level: translateTier(crmLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/SmartCRM.svg",
    alt: "Smart CRM"
  }].filter(product => product.name && product.level);
  if (products.length === 0) return null;
  return <div>
      <div className="text-sm mb-2">{translations.description}</div>
      <div className={`grid ${products.length === 1 ? 'grid-cols-1' : 'grid-cols-2'} gap-1.5`}>
        {products.map((product, index) => <div key={index} style={{
    display: 'flex',
    alignItems: 'center'
  }}>
            <img src={product.icon} alt={product.alt} className="w-3.5 h-3.5 mr-1.5 mt-2.5 mb-2.5 flex-shrink-0 align-middle" />
            <span className="font-medium mr-1 text-sm">{product.name} -</span>
            <span className="text-sm">{product.level}</span>
          </div>)}
      </div>
    </div>;
};

<AccordionGroup>
  <Accordion title="Supported products" defaultOpen="true" icon="cubes">
    <SupportedProducts marketing={true} sales={true} service={true} cms={true} marketingLevel="FREE" salesLevel="FREE" serviceLevel="FREE" cmsLevel="FREE" />
  </Accordion>

  <Accordion title="Required Scopes" icon="key">
    <ScopesList
      scopes={[
  'crm.objects.contacts.write'
]}
    />
  </Accordion>

  <UserLevelAccessCallout />
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-contacts-v2026-09.json POST /crm/objects/2026-09/contacts/batch/upsert
openapi: 3.0.1
info:
  title: Contacts
  description: Basepom for all HubSpot Projects
  version: 2026-09
  x-hubspot-product-tier-requirements:
    marketing: FREE
    sales: FREE
    service: FREE
    cms: FREE
    commerce: FREE
    crmHub: FREE
    dataHub: FREE
  x-hubspot-api-use-case: >-
    Retrieve a contact by ID to bring that contact data into your external
    system.
  x-hubspot-introduction: Use the contacts API to create and manage contacts.
servers:
  - url: https://api.hubapi.com
security: []
tags:
  - name: Advanced
  - name: Basic
  - name: Batch
  - name: Search
paths:
  /crm/objects/2026-09/contacts/batch/upsert:
    post:
      tags:
        - Batch
      summary: Create or update a batch of contacts
      description: >-
        Upsert a batch of contacts. The `inputs` array can contain a
        `properties` object to define property values for each record.
      operationId: >-
        post-/crm/objects/2026-09/contacts/batch/upsert_/crm/objects/2026-09-beta/{objectType}/batch/upsert
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/BatchInputSimplePublicObjectBatchInputUpsert
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BatchResponseSimplePublicUpsertObject'
        '207':
          description: multiple statuses
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/BatchResponseSimplePublicUpsertObjectWithErrors
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.objects.deals.read
        - oauth2:
            - crm.objects.subscriptions.read
        - oauth2:
            - crm.objects.services.read
        - oauth2:
            - crm.objects.tickets.sensitive.read
        - oauth2:
            - crm.objects.orders.read
        - oauth2:
            - crm.objects.listings.write
        - oauth2:
            - crm.objects.custom.read
        - oauth2:
            - crm.objects.companies.write
        - oauth2:
            - crm.objects.tasks.read
        - oauth2:
            - crm.objects.custom.sensitive.write.v2
        - oauth2:
            - crm.objects.custom.highly_sensitive.write.v2
        - oauth2:
            - crm.objects.companies.read
        - oauth2:
            - crm.objects.contacts.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.appointments.sensitive.read.v2
        - oauth2:
            - crm.objects.tickets.highly_sensitive.read
        - oauth2:
            - crm.objects.companies.sensitive.read.v2
        - oauth2:
            - crm.objects.tickets.sensitive.write
        - oauth2:
            - media_bridge.read
        - oauth2:
            - crm.objects.deals.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.contacts.highly_sensitive.write.v2
        - oauth2:
            - crm.objects.companies.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.commercepayments.write
        - oauth2:
            - crm.objects.invoices.write
        - oauth2:
            - crm.objects.contacts.sensitive.write.v2
        - oauth2:
            - crm.objects.users.write
        - oauth2:
            - crm.objects.calls.read
        - oauth2:
            - crm.objects.meetings.read
        - oauth2:
            - crm.objects.custom.sensitive.read.v2
        - oauth2:
            - crm.objects.users.read
        - oauth2:
            - crm.objects.partner-services.read
        - oauth2:
            - crm.objects.orders.write
        - oauth2:
            - crm.objects.partner-services.write
        - oauth2:
            - crm.objects.appointments.write
        - oauth2:
            - crm.objects.projects.highly_sensitive.write
        - oauth2:
            - crm.objects.carts.write
        - oauth2:
            - crm.objects.tickets.highly_sensitive.write
        - oauth2:
            - crm.objects.commercepayments.read
        - oauth2:
            - crm.objects.products.write
        - oauth2:
            - crm.objects.feedback_submissions.read
        - oauth2:
            - crm.objects.services.write
        - oauth2:
            - crm.objects.subscriptions.write
        - oauth2:
            - crm.objects.deals.sensitive.write.v2
        - oauth2:
            - crm.objects.contacts.read
        - oauth2:
            - crm.objects.appointments.sensitive.write.v2
        - oauth2:
            - crm.objects.invoices.read
        - oauth2:
            - crm.objects.projects.highly_sensitive.read
        - oauth2:
            - tickets.sensitive.v2
        - oauth2:
            - crm.objects.custom.write
        - oauth2:
            - crm.objects.deals.write
        - oauth2:
            - e-commerce
        - oauth2:
            - crm.objects.appointments.read
        - oauth2:
            - crm.objects.companies.sensitive.write.v2
        - oauth2:
            - crm.objects.projects.read
        - oauth2:
            - crm.objects.custom.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.deals.highly_sensitive.write.v2
        - oauth2:
            - crm.objects.companies.highly_sensitive.write.v2
        - oauth2:
            - crm.objects.goals.write
        - oauth2:
            - crm.objects.line_items.write
        - oauth2:
            - crm.objects.projects.sensitive.read
        - oauth2:
            - crm.objects.contacts.write
        - oauth2:
            - crm.objects.goals.read
        - oauth2:
            - crm.objects.line_items.read
        - oauth2:
            - crm.objects.partner-clients.write
        - oauth2:
            - crm.objects.projects.write
        - oauth2:
            - crm.objects.projects.sensitive.write
        - oauth2:
            - crm.objects.deals.sensitive.read.v2
        - oauth2:
            - crm.objects.quotes.write
        - oauth2:
            - tickets.highly_sensitive.v2
        - oauth2:
            - crm.objects.leads.read
        - oauth2:
            - crm.objects.leads.write
        - oauth2:
            - crm.objects.carts.read
        - oauth2:
            - crm.objects.emails.read
        - oauth2:
            - crm.objects.quotes.read
        - oauth2:
            - crm.objects.courses.write
        - oauth2:
            - crm.objects.partner-clients.read
        - oauth2:
            - crm.objects.notes.read
        - oauth2:
            - crm.objects.courses.read
        - oauth2:
            - crm.objects.listings.read
        - oauth2:
            - crm.objects.contacts.sensitive.read.v2
        - oauth2:
            - crm.objects.products.read
components:
  schemas:
    BatchInputSimplePublicObjectBatchInputUpsert:
      required:
        - inputs
      type: object
      properties:
        inputs:
          type: array
          description: >-
            An array of SimplePublicObjectBatchInputUpsert objects, each
            containing the properties and identifiers needed for the upsert
            operation.
          items:
            $ref: '#/components/schemas/SimplePublicObjectBatchInputUpsert'
      description: >-
        Represents a batch input operation for upserting simple public objects
        in HubSpot. This component is used to process multiple upsert operations
        in a single request, improving efficiency and performance.
    BatchResponseSimplePublicUpsertObject:
      required:
        - completedAt
        - results
        - startedAt
        - status
      type: object
      properties:
        completedAt:
          type: string
          description: >-
            The date and time when the batch operation was completed, in ISO
            8601 format.
          format: date-time
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of link names to associated URIs, providing additional
            information or actions related to the batch operation.
        requestedAt:
          type: string
          description: >-
            The date and time when the batch operation was requested, in ISO
            8601 format.
          format: date-time
        results:
          type: array
          description: >-
            An array of objects representing the results of the upsert
            operation. Each object is a SimplePublicUpsertObject.
          items:
            $ref: '#/components/schemas/SimplePublicUpsertObject'
        startedAt:
          type: string
          description: >-
            The date and time when the batch operation started, in ISO 8601
            format.
          format: date-time
        status:
          type: string
          description: >-
            The current status of the batch operation. Valid values include
            'PENDING', 'PROCESSING', 'CANCELED', and 'COMPLETE'.
          enum:
            - CANCELED
            - COMPLETE
            - PENDING
            - PROCESSING
      description: >-
        Represents the result of a batch upsert operation, including the
        operation’s status, timestamps, and a list of successfully created or
        updated objects.
    BatchResponseSimplePublicUpsertObjectWithErrors:
      required:
        - completedAt
        - results
        - startedAt
        - status
      type: object
      properties:
        completedAt:
          type: string
          description: >-
            The date and time when the batch operation was completed, in ISO
            8601 format.
          format: date-time
        errors:
          type: array
          description: >-
            An array of errors encountered during the batch operation, each
            represented as a StandardError.
          items:
            $ref: '#/components/schemas/StandardError'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of link names to associated URIs that provide additional
            information or resources related to the batch operation.
        numErrors:
          type: integer
          description: The total number of errors encountered during the batch operation.
          format: int32
        requestedAt:
          type: string
          description: >-
            The date and time when the batch operation was requested, in ISO
            8601 format.
          format: date-time
        results:
          type: array
          description: >-
            An array containing the results of the upsert operation, each
            represented as a SimplePublicUpsertObject.
          items:
            $ref: '#/components/schemas/SimplePublicUpsertObject'
        startedAt:
          type: string
          description: >-
            The date and time when the batch operation started, in ISO 8601
            format.
          format: date-time
        status:
          type: string
          description: >-
            The current status of the batch operation. Valid values include
            'PENDING', 'PROCESSING', 'CANCELED', and 'COMPLETE'.
          enum:
            - CANCELED
            - COMPLETE
            - PENDING
            - PROCESSING
      description: >-
        Represents the response from a batch upsert operation, including the
        status, timestamps, successfully processed objects, and any errors that
        occurred during processing.
    SimplePublicObjectBatchInputUpsert:
      required:
        - id
        - properties
      type: object
      properties:
        id:
          type: string
          description: A string representing the unique identifier for the CRM object.
        idProperty:
          type: string
          description: The name of a property whose values are unique for this object
        objectWriteTraceId:
          type: string
          description: >-
            A string used to trace the write operation for debugging or logging
            purposes.
        properties:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing key-value pairs representing the properties of
            the CRM object. Each key is a property name, and each value is the
            property's value.
      description: >-
        Represents an object used in batch upsert operations, containing an
        object’s unique identifier, its properties, and optionally the unique
        property name and a write trace ID.
    SimplePublicUpsertObject:
      required:
        - archived
        - createdAt
        - id
        - new
        - properties
        - updatedAt
      type: object
      properties:
        archived:
          type: boolean
          description: A boolean indicating whether the object is archived.
        archivedAt:
          type: string
          description: The date and time when this object was archived, in ISO 8601 format.
          format: date-time
        createdAt:
          type: string
          description: The date and time when this object was created, in ISO 8601 format.
          format: date-time
        id:
          type: string
          description: The unique identifier for this object.
        new:
          type: boolean
          description: A boolean indicating whether this object is newly created.
        objectWriteTraceId:
          type: string
          description: An identifier for tracing the creation request.
        properties:
          type: object
          additionalProperties:
            type: string
          description: A map of property names to their current values for the object.
        propertiesWithHistory:
          type: object
          additionalProperties:
            type: array
            items:
              $ref: '#/components/schemas/ValueWithTimestamp'
          description: >-
            A map of property names to arrays of their historical values, each
            with a timestamp.
        updatedAt:
          type: string
          description: >-
            The date and time when this object was last updated, in ISO 8601
            format.
          format: date-time
        url:
          type: string
          description: The URL of the object.
        warnings:
          type: array
          description: >-
            An array of warnings related to the object, each containing a
            category, message, and context.
          items:
            $ref: '#/components/schemas/PublicObjectWarning'
      description: >-
        Represents a CRM object that has either been created or updated
        (upserted)
    StandardError:
      required:
        - category
        - context
        - errors
        - links
        - message
        - status
      type: object
      properties:
        category:
          type: string
          description: A string that categorizes the error.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: >-
            An object containing additional context about the error, with string
            arrays as values.
        errors:
          type: array
          description: >-
            An array of ErrorDetail objects that provide further information
            about the error.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        id:
          type: string
          description: A string representing a unique identifier for the error.
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object mapping link names to associated URIs that contain
            documentation or recommended remediation steps for the error.
        message:
          type: string
          description: A string containing a human-readable message describing the error.
        status:
          type: string
          description: A string indicating the status of the error.
        subCategory:
          type: object
          properties: {}
          description: An object providing more specific categorization of the error.
      description: >-
        Represents a standard error response in the HubSpot API, providing
        detailed information about an error that occurred during an API request.
    Error:
      required:
        - category
        - correlationId
        - message
      type: object
      properties:
        category:
          type: string
          description: The error category
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: Context about the error condition
          example: >-
            {invalidPropertyName=[propertyValue], missingScopes=[scope1,
            scope2]}
        correlationId:
          type: string
          description: >-
            A unique identifier for the request. Include this value with any
            error reports or support tickets
          format: uuid
          example: aeb5f871-7f07-4993-9211-075dc63e7cbf
        errors:
          type: array
          description: further information about the error
          items:
            $ref: '#/components/schemas/ErrorDetail'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of link names to associated URIs containing documentation
            about the error or recommended remediation steps
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate
          example: An error occurred
        subCategory:
          type: string
          description: >-
            A specific category that contains more specific detail about the
            error
      description: >-
        Represents an error response returned by the API when an operation
        fails. This component is used in various endpoints to provide detailed
        information about the error encountered.
      example:
        message: Invalid input (details will vary based on the error)
        correlationId: aeb5f871-7f07-4993-9211-075dc63e7cbf
        category: VALIDATION_ERROR
        links:
          knowledge-base: https://www.hubspot.com/products/service/knowledge-base
    ValueWithTimestamp:
      required:
        - sourceType
        - timestamp
        - value
      type: object
      properties:
        sourceId:
          type: string
          description: A string identifier for the specific source of the value.
        sourceLabel:
          type: string
          description: A string label that provides a human-readable name for the source.
        sourceType:
          type: string
          description: >-
            A string indicating the type of source from which the value
            originated.
        timestamp:
          type: string
          description: The date and time when the value was recorded, in ISO 8601 format.
          format: date-time
        updatedByUserId:
          type: integer
          description: >-
            An integer representing the ID of the user who last updated the
            value.
          format: int32
        value:
          type: string
          description: The actual value being recorded. It is a string.
      description: Property model that includes timestamp.
    PublicObjectWarning:
      required:
        - category
        - context
        - message
      type: object
      properties:
        category:
          type: string
          description: A string representing the category of the warning.
        context:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object providing additional context for the warning, with string
            values for each context key.
        message:
          type: string
          description: A string containing the warning message.
      description: >-
        Represents a warning message related to a public object in HubSpot,
        providing details about the nature and context of the warning.
    ErrorDetail:
      required:
        - message
      type: object
      properties:
        code:
          type: string
          description: The status code associated with the error detail
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: Context about the error condition
          example: '{missingScopes=[scope1, scope2]}'
        in:
          type: string
          description: The name of the field or parameter in which the error was found.
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate
        subCategory:
          type: string
          description: >-
            A specific category that contains more specific detail about the
            error
      description: >-
        Represents detailed information about an error that occurred in the API.
        This component is used to provide additional context and specifics about
        errors, typically as part of an error response.
  responses:
    Error:
      description: An error occurred.
      content:
        '*/*':
          schema:
            $ref: '#/components/schemas/Error'
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://app.hubspot.com/oauth/authorize
          tokenUrl: https://api.hubapi.com/oauth/v1/token
          scopes:
            crm.objects.appointments.read: ''
            crm.objects.appointments.sensitive.read.v2: ''
            crm.objects.appointments.sensitive.write.v2: ''
            crm.objects.appointments.write: ''
            crm.objects.calls.read: ''
            crm.objects.carts.read: ''
            crm.objects.carts.write: ''
            crm.objects.commercepayments.read: ''
            crm.objects.commercepayments.write: ''
            crm.objects.companies.highly_sensitive.read.v2: ''
            crm.objects.companies.highly_sensitive.write.v2: ''
            crm.objects.companies.read: ''
            crm.objects.companies.sensitive.read.v2: ''
            crm.objects.companies.sensitive.write.v2: ''
            crm.objects.companies.write: ''
            crm.objects.contacts.highly_sensitive.read.v2: ''
            crm.objects.contacts.highly_sensitive.write.v2: ''
            crm.objects.contacts.read: ''
            crm.objects.contacts.sensitive.read.v2: ''
            crm.objects.contacts.sensitive.write.v2: ''
            crm.objects.contacts.write: ''
            crm.objects.courses.read: ''
            crm.objects.courses.write: ''
            crm.objects.custom.highly_sensitive.read.v2: ''
            crm.objects.custom.highly_sensitive.write.v2: ''
            crm.objects.custom.read: ''
            crm.objects.custom.sensitive.read.v2: ''
            crm.objects.custom.sensitive.write.v2: ''
            crm.objects.custom.write: ''
            crm.objects.deals.highly_sensitive.read.v2: ''
            crm.objects.deals.highly_sensitive.write.v2: ''
            crm.objects.deals.read: ''
            crm.objects.deals.sensitive.read.v2: ''
            crm.objects.deals.sensitive.write.v2: ''
            crm.objects.deals.write: ''
            crm.objects.emails.read: ''
            crm.objects.feedback_submissions.read: ''
            crm.objects.goals.read: ''
            crm.objects.goals.write: ''
            crm.objects.invoices.read: ''
            crm.objects.invoices.write: ''
            crm.objects.leads.read: ''
            crm.objects.leads.write: ''
            crm.objects.line_items.read: ''
            crm.objects.line_items.write: ''
            crm.objects.listings.read: ''
            crm.objects.listings.write: ''
            crm.objects.meetings.read: ''
            crm.objects.notes.read: ''
            crm.objects.orders.read: ''
            crm.objects.orders.write: ''
            crm.objects.partner-clients.read: ''
            crm.objects.partner-clients.write: ''
            crm.objects.partner-services.read: ''
            crm.objects.partner-services.write: ''
            crm.objects.products.read: ''
            crm.objects.products.write: ''
            crm.objects.projects.highly_sensitive.read: ''
            crm.objects.projects.highly_sensitive.write: ''
            crm.objects.projects.read: ''
            crm.objects.projects.sensitive.read: ''
            crm.objects.projects.sensitive.write: ''
            crm.objects.projects.write: ''
            crm.objects.quotes.read: ''
            crm.objects.quotes.write: ''
            crm.objects.services.read: ''
            crm.objects.services.write: ''
            crm.objects.subscriptions.read: ''
            crm.objects.subscriptions.write: ''
            crm.objects.tasks.read: ''
            crm.objects.tickets.highly_sensitive.read: ''
            crm.objects.tickets.highly_sensitive.write: ''
            crm.objects.tickets.sensitive.read: ''
            crm.objects.tickets.sensitive.write: ''
            crm.objects.users.read: ''
            crm.objects.users.write: ''
            e-commerce: ''
            media_bridge.read: ''
            tickets.highly_sensitive.v2: ''
            tickets.sensitive.v2: ''

````