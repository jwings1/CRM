> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Search for quotes using specified criteria.

> Execute a search for quotes based on the criteria defined in the request body, such as filters, properties, and sorting options. This endpoint allows for detailed querying of quote records to retrieve specific data sets.

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
  'crm.objects.quotes.read',
  'e-commerce'
]}
    />
  </Accordion>

  <UserLevelAccessCallout />
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-quotes-v2026-09.json POST /crm/objects/2026-09/quotes/search
openapi: 3.0.1
info:
  title: Quotes
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
    Create a contract proposal for a customer who is interested in signing up
    for one of your annual SEO auditing service packages.
  x-hubspot-introduction: >-
    Use the quotes API to create and manage sales quotes for sharing pricing
    information with potential buyers.
servers:
  - url: https://api.hubapi.com
security: []
tags:
  - name: Advanced
  - name: Basic
  - name: Batch
  - name: Search
paths:
  /crm/objects/2026-09/quotes/search:
    post:
      tags:
        - Search
      summary: Search for quotes using specified criteria.
      description: >-
        Execute a search for quotes based on the criteria defined in the request
        body, such as filters, properties, and sorting options. This endpoint
        allows for detailed querying of quote records to retrieve specific data
        sets.
      operationId: >-
        post-/crm/objects/2026-09/quotes/search_/crm/objects/2026-09-beta/{objectType}/search
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PublicObjectSearchRequest'
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/CollectionResponseWithTotalSimplePublicObject
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
    PublicObjectSearchRequest:
      required:
        - after
        - filterGroups
        - limit
        - properties
        - sorts
      type: object
      properties:
        after:
          type: string
          description: >-
            A string representing the paging cursor token to retrieve the next
            set of results.
        filterGroups:
          type: array
          description: >-
            An array of filter groups used to specify the criteria for the
            search. Each filter group contains a set of filters that are
            combined using logical AND.
          items:
            $ref: '#/components/schemas/FilterGroup'
        limit:
          type: integer
          description: An integer specifying the maximum number of results to return.
          format: int32
        properties:
          type: array
          description: >-
            An array of strings specifying the properties to be returned in the
            search results.
          items:
            type: string
        query:
          type: string
          description: >-
            A string representing the search query to be applied across the
            specified properties.
        sorts:
          type: array
          description: >-
            An array of strings indicating the fields and order by which the
            search results should be sorted.
          items:
            type: string
      description: Describes a search request
    CollectionResponseWithTotalSimplePublicObject:
      required:
        - results
        - total
      type: object
      properties:
        paging:
          $ref: '#/components/schemas/Paging'
        results:
          type: array
          description: >-
            An array of SimplePublicObject items, each representing an
            individual CRM object.
          items:
            $ref: '#/components/schemas/SimplePublicObject'
        total:
          type: integer
          description: The number of available results
          format: int32
      description: >-
        Represents a list of simple objects returned from an API request, along
        with the total count of objects available.
    FilterGroup:
      required:
        - filters
      type: object
      properties:
        filters:
          type: array
          description: >-
            An array of filter objects that define the conditions for the
            search. Each filter specifies a property, an operator, and a value
            or range of values to match against.
          items:
            $ref: '#/components/schemas/Filter'
      description: >-
        Represents a group of filters used to query data within HubSpot. This
        component is used to define criteria for filtering records in various
        API endpoints.
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
          description: >-
            A string used for tracing the write operations related to this
            object.
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
            A map of property names to arrays of values with timestamps, showing
            the history of changes for each property.
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
            An array of warnings associated with this object, each containing a
            category, message, and context.
          items:
            $ref: '#/components/schemas/PublicObjectWarning'
      description: A simple public object.
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
    Filter:
      required:
        - operator
        - propertyName
      type: object
      properties:
        highValue:
          type: string
          description: >-
            The upper bound value used for range comparisons in the filter. It
            is a string.
        operator:
          type: string
          description: >-
            The operator used to compare the property with the value(s). Valid
            operators include 'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE', 'BETWEEN',
            'IN', 'NOT_IN', 'HAS_PROPERTY', 'NOT_HAS_PROPERTY',
            'CONTAINS_TOKEN', and 'NOT_CONTAINS_TOKEN'.
          enum:
            - BETWEEN
            - CONTAINS_TOKEN
            - EQ
            - GT
            - GTE
            - HAS_PROPERTY
            - IN
            - LT
            - LTE
            - NEQ
            - NOT_CONTAINS_TOKEN
            - NOT_HAS_PROPERTY
            - NOT_IN
        propertyName:
          type: string
          description: >-
            The name of the property on which the filter is applied. It is a
            string.
        value:
          type: string
          description: The value used for comparison in the filter. It is a string.
        values:
          type: array
          description: >-
            An array of values used for comparison in the filter. Each value is
            a string.
          items:
            type: string
      description: >-
        Defines a single condition for searching CRM objects, specifying the
        property to filter on, the operator to use (such as equals, greater
        than, or contains), and the value(s) to compare against. 
    NextPage:
      required:
        - after
      type: object
      properties:
        after:
          type: string
          description: >-
            A string token used to identify the starting point for the next page
            of results.
        link:
          type: string
          description: >-
            A URL string that provides a direct link to access the next page of
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
            A string representing the cursor token used to access the previous
            page of results.
        link:
          type: string
          description: A string containing the URL link to the previous page of results.
      description: >-
        specifies the paging information needed to retrieve the previous set of
        results in a paginated API response
    ValueWithTimestamp:
      required:
        - sourceType
        - timestamp
        - value
      type: object
      properties:
        sourceId:
          type: string
          description: A string identifier for the specific source that provided the value.
        sourceLabel:
          type: string
          description: A string label that describes the source of the value.
        sourceType:
          type: string
          description: >-
            A string specifying the type of source from which the value was
            obtained.
        timestamp:
          type: string
          description: A date-time string indicating when the value was recorded.
          format: date-time
        updatedByUserId:
          type: integer
          description: >-
            An integer representing the ID of the user who last updated the
            value.
          format: int32
        value:
          type: string
          description: >-
            A string representing the value of the property at the specified
            timestamp.
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
            An object providing additional context for the warning, with
            properties that are strings.
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