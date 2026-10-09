> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Retrieve a company

> Retrieve a company by its ID (`companyId`) or by a unique property (`idProperty`). You can specify what is returned using the `properties` query parameter.

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
  'crm.objects.companies.read'
]}
    />
  </Accordion>

  <UserLevelAccessCallout />
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-companies-v2026-09.json GET /crm/objects/2026-09/companies/{companyId}
openapi: 3.0.1
info:
  title: Companies
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
    When a new customer signs up on your website with their business email
    address, create a company record to represent the relationship between the
    customer and the company they work for. A sales rep can later use this
    company record for outreach to find other potential sales opportunities. 
  x-hubspot-introduction: >-
    Use the companies API to create and manage CRM records that represent the
    companies and organizations that interact with your business.
servers:
  - url: https://api.hubapi.com
security: []
tags:
  - name: Advanced
  - name: Basic
  - name: Batch
  - name: Search
paths:
  /crm/objects/2026-09/companies/{companyId}:
    get:
      tags:
        - Basic
      summary: Retrieve a company
      description: >-
        Retrieve a company by its ID (`companyId`) or by a unique property
        (`idProperty`). You can specify what is returned using the `properties`
        query parameter.
      operationId: >-
        get-/crm/objects/2026-09/companies/{companyId}_/crm/objects/2026-09-beta/{objectType}/{objectId}
      parameters:
        - name: companyId
          in: path
          required: true
          schema:
            pattern: .+
            type: string
        - name: archived
          in: query
          description: Whether to return only results that have been archived.
          required: false
          style: form
          explode: true
          schema:
            type: boolean
            default: false
        - name: associations
          in: query
          description: >-
            A comma separated list of object types to retrieve associated IDs
            for. If any of the specified associations do not exist, they will be
            ignored.
          required: false
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
        - name: idProperty
          in: query
          description: The name of a property whose values are unique for this object type
          required: false
          style: form
          explode: true
          schema:
            type: string
        - name: properties
          in: query
          description: >-
            A comma separated list of the properties to be returned in the
            response. If any of the specified properties are not present on the
            requested object(s), they will be ignored.
          required: false
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
        - name: propertiesWithHistory
          in: query
          description: >-
            A comma separated list of the properties to be returned along with
            their history of previous values. If any of the specified properties
            are not present on the requested object(s), they will be ignored.
          required: false
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SimplePublicObjectWithAssociations'
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
    SimplePublicObjectWithAssociations:
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
        associations:
          type: object
          additionalProperties:
            $ref: '#/components/schemas/CollectionResponseAssociatedId'
          description: >-
            A map of associated object types to their associated IDs, detailing
            the relationships this object has with others.
        createdAt:
          type: string
          description: The date and time when this object was created, in ISO 8601 format.
          format: date-time
        id:
          type: string
          description: The unique identifier for this object.
        objectWriteTraceId:
          type: string
          description: >-
            A string identifier used for tracing write operations on this
            object.
        properties:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of property names to their current values, represented as
            strings.
        propertiesWithHistory:
          type: object
          additionalProperties:
            type: array
            items:
              $ref: '#/components/schemas/ValueWithTimestamp'
          description: >-
            A map of property names to their historical values, each including a
            timestamp and source information.
        updatedAt:
          type: string
          description: >-
            The date and time when this object was last updated, in ISO 8601
            format.
          format: date-time
        url:
          type: string
          description: The URL link to access this object.
        warnings:
          type: array
          description: >-
            An array of warnings related to this object, each containing a
            category, message, and context.
          items:
            $ref: '#/components/schemas/PublicObjectWarning'
      description: >-
        Represents a CRM object along with its properties, timestamps, and a set
        of associated object IDs grouped by association type.
    CollectionResponseAssociatedId:
      required:
        - results
      type: object
      properties:
        paging:
          $ref: '#/components/schemas/Paging'
        results:
          type: array
          description: >-
            An array of associated IDs, each represented by an 'AssociatedId'
            object. This property is required.
          items:
            $ref: '#/components/schemas/AssociatedId'
      description: >-
        Represents a collection of associated IDs returned by an API request,
        including pagination details for navigating through the results.
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
            A label providing additional context about the source. It is a
            string.
        sourceType:
          type: string
          description: >-
            The type of source from which the value was obtained. It is a string
            and is required.
        timestamp:
          type: string
          description: The date and time when the value was recorded, in ISO 8601 format.
          format: date-time
        updatedByUserId:
          type: integer
          description: The ID of the user who last updated the value. It is an integer.
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
            string properties.
        message:
          type: string
          description: A string containing the warning message.
      description: >-
        Represents a warning message related to a public object in HubSpot,
        providing details about the nature and context of the warning.
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
    Paging:
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
    AssociatedId:
      required:
        - id
        - type
      type: object
      properties:
        id:
          type: string
          description: The unique identifier for the association. It is a string.
        type:
          type: string
          description: The type of the association, represented as a string.
          example: deal_to_contact
      description: Contains the id and type of an association
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
          description: >-
            A string token used as a cursor to retrieve the next page of
            results.
        link:
          type: string
          description: >-
            A string URL that provides a direct link to the next page of
            results.
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
          description: >-
            A string token that indicates the position before the current page
            in the paginated results.
        link:
          type: string
          description: >-
            A string URL that provides a direct link to the previous page of
            results.
      description: >-
        specifies the paging information needed to retrieve the previous set of
        results in a paginated API response
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