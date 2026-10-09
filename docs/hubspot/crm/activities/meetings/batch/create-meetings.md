> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create meetings

> Create a batch of meetings. The `inputs` array can contain a `properties` object to define property values for the record, along with an `associations` array to define relationships with other object records.

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
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-meetings-v2026-09.json POST /crm/objects/2026-09/meetings/batch/create
openapi: 3.0.1
info:
  title: Meetings
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
    If you're using a different service outside of HubSpot to schedule your
    meetings, or if you want to supplement the built-in tracking of the HubSpot
    meetings tool, you can use this API to help keep track of how your meetings
    went with prospects and customers in the HubSpot CRM.
  x-hubspot-introduction: >-
    The meetings engagements API allows you to log and manage meetings on the
    corresponding CRM records, such as contacts or companies. You can include
    notes from the meeting and its outcome, along with other important data from
    the meeting to share with the rest of your team.
servers:
  - url: https://api.hubapi.com
security: []
tags:
  - name: Advanced
  - name: Basic
  - name: Batch
  - name: Search
paths:
  /crm/objects/2026-09/meetings/batch/create:
    post:
      tags:
        - Batch
      summary: Create a batch of meetings
      description: >-
        Create a batch of meetings. The `inputs` array can contain a
        `properties` object to define property values for the record, along with
        an `associations` array to define relationships with other object
        records.
      operationId: >-
        post-/crm/objects/2026-09/meetings/batch/create_/crm/objects/2026-09-beta/{objectType}/batch/create
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/BatchInputSimplePublicObjectBatchInputForCreate
        required: true
      responses:
        '201':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BatchResponseSimplePublicObject'
        '207':
          description: multiple statuses
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BatchResponseSimplePublicObjectWithErrors'
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
    BatchInputSimplePublicObjectBatchInputForCreate:
      required:
        - inputs
      type: object
      properties:
        inputs:
          type: array
          description: >-
            An array of SimplePublicObjectBatchInputForCreate objects, each
            containing the properties and associations needed to create a single
            CRM object.
          items:
            $ref: '#/components/schemas/SimplePublicObjectBatchInputForCreate'
      description: >-
        Represents a batch input for creating multiple simple public objects in
        a single request. This component is used to streamline the process of
        adding new objects to a HubSpot account by allowing multiple entries to
        be created at once.
    BatchResponseSimplePublicObject:
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
            A map of link names to associated URIs for additional information
            related to the batch operation.
        requestedAt:
          type: string
          description: >-
            The date and time when the batch operation was requested, in ISO
            8601 format.
          format: date-time
        results:
          type: array
          description: >-
            An array of SimplePublicObject items representing the results of the
            batch operation.
          items:
            $ref: '#/components/schemas/SimplePublicObject'
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
      description: A public object batch response object
    BatchResponseSimplePublicObjectWithErrors:
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
            An array of StandardError items detailing any errors that occurred
            during the batch operation.
          items:
            $ref: '#/components/schemas/StandardError'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of link names to associated URIs, providing additional
            information or actions related to the batch operation.
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
            An array of SimplePublicObject items representing the successful
            results of the batch operation.
          items:
            $ref: '#/components/schemas/SimplePublicObject'
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
        Represents the result of a batch operation on CRM objects, including the
        processing status, batch results, timestamps, and a list of any errors
        encountered during the operation.
    SimplePublicObjectBatchInputForCreate:
      required:
        - associations
        - properties
      type: object
      properties:
        associations:
          type: array
          description: >-
            An array of associations for the CRM objects, where each association
            links the object to another object. Each item in the array is a
            'PublicAssociationsForObject' object.
          items:
            $ref: '#/components/schemas/PublicAssociationsForObject'
        objectWriteTraceId:
          type: string
          description: >-
            A string used to trace the write operations for the objects being
            created. This is optional and can be used for debugging or tracking
            purposes.
        properties:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing key-value pairs representing the properties of
            the CRM objects to be created. Each key is a property name, and each
            value is the property's value.
      description: >-
        An input object that contains a collection of objects to be created
        together in a batch.
    SimplePublicObject:
      required:
        - archived
        - createdAt
        - id
        - properties
        - updatedAt
      type: object
      properties:
        archived:
          type: boolean
          description: A boolean indicating whether this object is archived.
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
          description: The unique identifier for this object, represented as a string.
        objectWriteTraceId:
          type: string
          description: A string used to trace the write operations for this object.
        properties:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of property names to their values, where each value is a
            string.
        propertiesWithHistory:
          type: object
          additionalProperties:
            type: array
            items:
              $ref: '#/components/schemas/ValueWithTimestamp'
          description: >-
            A map of property names to arrays of historical values, each
            containing a value and its associated timestamp.
        updatedAt:
          type: string
          description: >-
            The date and time when this object was last updated, in ISO 8601
            format.
          format: date-time
        url:
          type: string
          description: A string representing the URL of this object.
        warnings:
          type: array
          description: >-
            An array of warnings related to this object, each containing a
            category, message, and context.
          items:
            $ref: '#/components/schemas/PublicObjectWarning'
      description: A simple public object.
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
          description: A string representing the category of the error.
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
            An array of ErrorDetail objects providing further information about
            the error.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        id:
          type: string
          description: A string representing the unique identifier for this error.
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object mapping link names to associated URIs containing
            documentation about the error or recommended remediation steps.
        message:
          type: string
          description: A string containing a human-readable message describing the error.
        status:
          type: string
          description: A string indicating the status of the error.
        subCategory:
          type: object
          properties: {}
          description: An object providing additional categorization of the error.
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
    PublicAssociationsForObject:
      required:
        - to
        - types
      type: object
      properties:
        to:
          $ref: '#/components/schemas/PublicObjectId'
        types:
          type: array
          description: >-
            An array of association specifications, each defining the category
            and type of association between the objects.
          items:
            $ref: '#/components/schemas/AssociationSpec'
      description: >-
        Represents the associations for a specific object in HubSpot, detailing
        the types of associations and the related objects involved.
    ValueWithTimestamp:
      required:
        - sourceType
        - timestamp
        - value
      type: object
      properties:
        sourceId:
          type: string
          description: >-
            The identifier of the source from which the value was obtained. It
            is a string.
        sourceLabel:
          type: string
          description: >-
            A label describing the source from which the value was obtained. It
            is a string.
        sourceType:
          type: string
          description: >-
            The type of source from which the value was obtained. It is a
            string.
        timestamp:
          type: string
          description: The date and time when the value was recorded, in ISO 8601 format.
          format: date-time
        updatedByUserId:
          type: integer
          description: The ID of the user who updated the value. It is an integer.
          format: int32
        value:
          type: string
          description: The value associated with the timestamp. It is a string.
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
          description: A string indicating the category of the warning.
        context:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object providing additional context about the warning, with
            properties as key-value pairs where both keys and values are
            strings.
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
    PublicObjectId:
      required:
        - id
      type: object
      properties:
        id:
          type: string
          description: A string representing the unique identifier for the CRM object.
      description: Contains the Id of a Public Object
    AssociationSpec:
      required:
        - associationCategory
        - associationTypeId
      type: object
      properties:
        associationCategory:
          type: string
          description: >-
            A string indicating the category of the association. Valid values
            include 'HUBSPOT_DEFINED', 'USER_DEFINED', 'INTEGRATOR_DEFINED', and
            'WORK'.
          enum:
            - HUBSPOT_DEFINED
            - INTEGRATOR_DEFINED
            - USER_DEFINED
            - WORK
        associationTypeId:
          type: integer
          description: >-
            An integer representing the unique identifier for the type of
            association.
          format: int32
      description: >-
        Defines the type, direction, and details of the relationship between two
        CRM objects.
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