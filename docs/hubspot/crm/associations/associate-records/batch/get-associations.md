> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Retrieve associations

> Batch read associations for objects to specific object type. The 'after' field in a returned paging object  can be added alongside the 'id' to retrieve the next page of associations from that objectId. The 'link' field is deprecated and should be ignored. Note: The 'paging' field will only be present if there are more pages and absent otherwise.

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
  'crm.objects.orders.read',
  'crm.objects.appointments.sensitive.read.v2',
  'crm.objects.contacts.highly_sensitive.read.v2',
  'crm.objects.companies.write',
  'crm.objects.custom.sensitive.read.v2',
  'crm.objects.users.read',
  'crm.objects.users.write',
  'crm.objects.commercepayments.write',
  'crm.objects.invoices.write',
  'crm.objects.contacts.highly_sensitive.write.v2',
  'crm.objects.carts.write',
  'crm.objects.appointments.write',
  'crm.objects.partner-services.read',
  'crm.objects.custom.write',
  'tickets',
  'crm.objects.deals.sensitive.write.v2',
  'crm.objects.deals.highly_sensitive.write.v2',
  'crm.objects.companies.highly_sensitive.write.v2',
  'tickets.sensitive.v2',
  'crm.objects.projects.highly_sensitive.read',
  'crm.objects.appointments.read',
  'crm.objects.appointments.sensitive.write.v2',
  'crm.objects.projects.sensitive.read',
  'crm.objects.projects.write',
  'media_bridge.read',
  'crm.objects.listings.read',
  'crm.objects.courses.write',
  'crm.objects.carts.read',
  'crm.objects.listings.write',
  'crm.objects.custom.read',
  'crm.objects.deals.read',
  'crm.objects.subscriptions.read',
  'crm.objects.companies.sensitive.read.v2',
  'crm.objects.companies.read',
  'crm.objects.custom.sensitive.write.v2',
  'crm.objects.deals.highly_sensitive.read.v2',
  'crm.objects.contacts.sensitive.write.v2',
  'crm.objects.companies.highly_sensitive.read.v2',
  'crm.objects.projects.highly_sensitive.write',
  'crm.objects.partner-services.write',
  'crm.objects.contacts.read',
  'crm.objects.services.write',
  'crm.objects.orders.write',
  'crm.objects.subscriptions.write',
  'crm.objects.commercepayments.read',
  'crm.objects.products.write',
  'crm.objects.custom.highly_sensitive.read.v2',
  'crm.objects.deals.write',
  'crm.objects.invoices.read',
  'e-commerce',
  'tickets.highly_sensitive.v2',
  'crm.objects.quotes.write',
  'crm.objects.leads.read',
  'crm.objects.leads.write',
  'crm.objects.custom.highly_sensitive.write.v2',
  'crm.objects.projects.sensitive.write',
  'crm.objects.deals.sensitive.read.v2',
  'crm.objects.goals.write',
  'crm.objects.companies.sensitive.write.v2',
  'crm.objects.projects.read',
  'crm.objects.contacts.write',
  'crm.objects.goals.read',
  'crm.objects.partner-clients.write',
  'crm.objects.line_items.read',
  'crm.objects.contacts.sensitive.read.v2',
  'crm.objects.line_items.write',
  'crm.objects.products.read',
  'crm.objects.courses.read',
  'crm.objects.quotes.read',
  'crm.objects.partner-clients.read',
  'crm.objects.services.read'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-associations-v2026-09.json POST /crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/read
openapi: 3.0.1
info:
  title: CRM Associations
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
servers:
  - url: https://api.hubapi.com
security: []
tags:
  - name: Advanced
  - name: Basic
  - name: Batch
  - name: Search
paths:
  /crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/read:
    post:
      tags:
        - Batch
      summary: Retrieve associations
      description: >-
        Batch read associations for objects to specific object type. The 'after'
        field in a returned paging object  can be added alongside the 'id' to
        retrieve the next page of associations from that objectId. The 'link'
        field is deprecated and should be ignored. Note: The 'paging' field will
        only be present if there are more pages and absent otherwise.
      operationId: >-
        post-/crm/associations/2026-09/{fromObjectType}/{toObjectType}/batch/read_/crm/associations/2026-09-beta/{fromObjectType}/{toObjectType}/batch/read
      parameters:
        - name: fromObjectType
          in: path
          description: >-
            The type of the source object from which associations are being
            read.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: toObjectType
          in: path
          description: The type of the target object to which associations are being read.
          required: true
          style: simple
          explode: false
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/BatchInputPublicFetchAssociationsBatchRequest
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/BatchResponsePublicAssociationMultiWithLabel
        '207':
          description: multiple statuses
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/BatchResponsePublicAssociationMultiWithLabelWithErrors
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
    BatchInputPublicFetchAssociationsBatchRequest:
      required:
        - inputs
      type: object
      properties:
        inputs:
          type: array
          description: >-
            An array of PublicFetchAssociationsBatchRequest objects, each
            specifying the details for fetching associations for a particular
            object. This property is required.
          items:
            $ref: '#/components/schemas/PublicFetchAssociationsBatchRequest'
    BatchResponsePublicAssociationMultiWithLabel:
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
            The timestamp when the batch processing was completed, in ISO 8601
            format.
          format: date-time
        links:
          type: object
          additionalProperties:
            type: string
          description: An object containing relevant links related to the batch request.
        requestedAt:
          type: string
          description: >-
            The timestamp when the batch request was initially made, in ISO 8601
            format.
          format: date-time
        results:
          type: array
          description: >-
            An array of results from the batch operation, each representing an
            association with labels between objects.
          items:
            $ref: '#/components/schemas/PublicAssociationMultiWithLabel'
        startedAt:
          type: string
          description: The timestamp when the batch processing began, in ISO 8601 format.
          format: date-time
        status:
          type: string
          description: >-
            The status of the batch processing request: "PENDING", "PROCESSING",
            "CANCELED", or "COMPLETE".
          enum:
            - CANCELED
            - COMPLETE
            - PENDING
            - PROCESSING
    BatchResponsePublicAssociationMultiWithLabelWithErrors:
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
            An array of errors that occurred during the batch operation, with
            each error represented by a standard error object.
          items:
            $ref: '#/components/schemas/StandardError'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing additional links related to the batch
            operation, with each link represented as a string.
        numErrors:
          type: integer
          description: >-
            The number of errors that occurred during the batch operation,
            represented as an integer.
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
            An array of results from the batch operation, each item representing
            a public association with labels.
          items:
            $ref: '#/components/schemas/PublicAssociationMultiWithLabel'
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
    PublicFetchAssociationsBatchRequest:
      required:
        - id
      type: object
      properties:
        after:
          type: string
          description: >-
            A paging cursor token used to retrieve the next set of results in a
            paginated response.
        id:
          type: string
          description: >-
            The unique identifier for the object whose associations are being
            fetched.
    PublicAssociationMultiWithLabel:
      required:
        - from
        - to
      type: object
      properties:
        from:
          $ref: '#/components/schemas/PublicObjectId'
        paging:
          $ref: '#/components/schemas/Paging_1'
        to:
          type: array
          description: >-
            An array of objects representing the target objects in the
            association. Each object includes the target object's ID and the
            types of associations, which are specified with labels.
          items:
            $ref: '#/components/schemas/MultiAssociatedObjectWithLabel'
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
          description: The main category of the error.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: Additional context-specific information related to the error.
        errors:
          type: array
          description: The detailed error objects.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        id:
          type: string
          description: A unique ID for the error instance.
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            URLs linking to documentation or resources associated with the
            error.
        message:
          type: string
          description: >-
            A human-readable string describing the error and possible
            remediation steps.
        status:
          type: string
          description: The HTTP status code associated with the error.
        subCategory:
          type: object
          properties: {}
          description: A more specific error category within each main category.
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
    PublicObjectId:
      required:
        - id
      type: object
      properties:
        id:
          type: string
          description: ID of the object
      description: Contains the Id of a Public Object
    Paging_1:
      type: object
      properties:
        next:
          $ref: '#/components/schemas/NextPage'
        prev:
          $ref: '#/components/schemas/PreviousPage'
      description: >-
        Represents the pagination information for navigating through a list of
        results in the API. It provides details on how to access the previous or
        next set of results.
    MultiAssociatedObjectWithLabel:
      required:
        - associationTypes
        - toObjectId
      type: object
      properties:
        associationTypes:
          type: array
          description: >-
            An array of association types with labels, defining the nature of
            the associations between objects. Each item in the array is an
            AssociationSpecWithLabel object.
          items:
            $ref: '#/components/schemas/AssociationSpecWithLabel'
        toObjectId:
          type: string
          description: The unique identifier for the target object in the association.
      description: >-
        Represents an object that is associated with multiple other objects,
        with optional context.
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
    NextPage:
      required:
        - after
      type: object
      properties:
        after:
          type: string
          description: A paging cursor token for retrieving subsequent pages.
        link:
          type: string
          description: A URL that can be used to retrieve the next page results.
      description: >-
        Specifies the paging information needed to retrieve the next set of
        results in a paginated API response
    PreviousPage:
      required:
        - before
      type: object
      properties:
        before:
          type: string
          description: A paging cursor token for retrieving previous pages.
        link:
          type: string
          description: A URL that can be used to retrieve the previous pages' results.
      description: >-
        specifies the paging information needed to retrieve the previous set of
        results in a paginated API response
    AssociationSpecWithLabel:
      required:
        - category
        - typeId
      type: object
      properties:
        category:
          type: string
          description: >-
            The category of the association, such as HUBSPOT_DEFINED,
            USER_DEFINED, or INTEGRATOR_DEFINED.
          enum:
            - HUBSPOT_DEFINED
            - INTEGRATOR_DEFINED
            - USER_DEFINED
            - WORK
        fromObjectTypeId:
          type: string
          description: >-
            A string representing the object type ID from which the association
            originates.
        label:
          type: string
          description: A label describing the association between two objects.
        toObjectTypeId:
          type: string
          description: >-
            A string representing the object type ID to which the association is
            directed.
        typeId:
          type: integer
          description: The unique identifier for the type of association.
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