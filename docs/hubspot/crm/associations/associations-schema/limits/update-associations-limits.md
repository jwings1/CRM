> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Update association limits

> Batch update association limits that have been configured between two object types.

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
  'crm.objects.deals.read',
  'crm.objects.subscriptions.read',
  'crm.objects.services.read',
  'crm.objects.tickets.sensitive.read',
  'crm.objects.orders.read',
  'crm.objects.listings.write',
  'crm.objects.custom.read',
  'crm.objects.companies.write',
  'crm.objects.tasks.read',
  'crm.objects.custom.sensitive.write.v2',
  'crm.objects.custom.highly_sensitive.write.v2',
  'crm.objects.companies.read',
  'crm.objects.contacts.highly_sensitive.read.v2',
  'crm.objects.appointments.sensitive.read.v2',
  'crm.objects.tickets.highly_sensitive.read',
  'crm.objects.companies.sensitive.read.v2',
  'crm.objects.tickets.sensitive.write',
  'media_bridge.read',
  'crm.objects.deals.highly_sensitive.read.v2',
  'crm.objects.contacts.highly_sensitive.write.v2',
  'crm.objects.companies.highly_sensitive.read.v2',
  'crm.objects.commercepayments.write',
  'crm.objects.invoices.write',
  'crm.objects.contacts.sensitive.write.v2',
  'crm.objects.users.write',
  'crm.objects.calls.read',
  'crm.objects.meetings.read',
  'crm.objects.custom.sensitive.read.v2',
  'crm.objects.users.read',
  'crm.objects.partner-services.read',
  'crm.objects.orders.write',
  'crm.objects.partner-services.write',
  'crm.objects.appointments.write',
  'crm.objects.projects.highly_sensitive.write',
  'crm.objects.carts.write',
  'crm.objects.tickets.highly_sensitive.write',
  'crm.objects.commercepayments.read',
  'crm.objects.products.write',
  'crm.objects.services.write',
  'crm.objects.subscriptions.write',
  'crm.objects.deals.sensitive.write.v2',
  'crm.objects.contacts.read',
  'crm.objects.appointments.sensitive.write.v2',
  'crm.objects.invoices.read',
  'crm.objects.projects.highly_sensitive.read',
  'tickets.sensitive.v2',
  'crm.objects.custom.write',
  'crm.objects.deals.write',
  'e-commerce',
  'crm.objects.appointments.read',
  'crm.objects.companies.sensitive.write.v2',
  'crm.objects.projects.read',
  'crm.objects.deals.highly_sensitive.write.v2',
  'crm.objects.custom.highly_sensitive.read.v2',
  'crm.objects.companies.highly_sensitive.write.v2',
  'crm.objects.goals.write',
  'crm.objects.line_items.write',
  'crm.objects.projects.sensitive.read',
  'crm.objects.contacts.write',
  'crm.objects.goals.read',
  'crm.objects.line_items.read',
  'crm.objects.partner-clients.write',
  'crm.objects.projects.write',
  'crm.objects.deals.sensitive.read.v2',
  'crm.objects.projects.sensitive.write',
  'crm.objects.quotes.write',
  'tickets.highly_sensitive.v2',
  'crm.objects.leads.read',
  'crm.objects.leads.write',
  'crm.objects.carts.read',
  'crm.objects.emails.read',
  'crm.objects.quotes.read',
  'crm.objects.courses.write',
  'crm.objects.partner-clients.read',
  'crm.objects.notes.read',
  'crm.objects.courses.read',
  'crm.objects.listings.read',
  'crm.objects.contacts.sensitive.read.v2',
  'crm.objects.products.read'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-associations-schema-v2026-09.json POST /crm/associations/2026-09/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update
openapi: 3.0.1
info:
  title: CRM Associations Schema
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
  - name: Labels
  - name: Limits
paths:
  /crm/associations/2026-09/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update:
    post:
      tags:
        - Limits
      summary: Update association limits
      description: >-
        Batch update association limits that have been configured between two
        object types.
      operationId: >-
        post-/crm/associations/2026-09/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update_batchUpdate
      parameters:
        - name: fromObjectType
          in: path
          description: The type of the source object in the association.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: toObjectType
          in: path
          description: The type of the target object in the association.
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
                #/components/schemas/BatchInputPublicAssociationDefinitionConfigurationUpdateRequest
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/BatchResponsePublicAssociationDefinitionConfigurationUpdateResult
        '207':
          description: multiple statuses
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/BatchResponsePublicAssociationDefinitionConfigurationUpdateResultWithErrors
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
    BatchInputPublicAssociationDefinitionConfigurationUpdateRequest:
      required:
        - inputs
      type: object
      properties:
        inputs:
          type: array
          description: >-
            An array of PublicAssociationDefinitionConfigurationUpdateRequest
            objects. Each object in the array specifies the configuration
            details to be updated.
          items:
            $ref: >-
              #/components/schemas/PublicAssociationDefinitionConfigurationUpdateRequest
    BatchResponsePublicAssociationDefinitionConfigurationUpdateResult:
      required:
        - completedAt
        - results
        - startedAt
        - status
      type: object
      properties:
        completedAt:
          type: string
          description: The date and time when the batch update operation was completed.
          format: date-time
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            URLs linking to documentation or resources associated with the batch
            update operation.
        requestedAt:
          type: string
          description: The date and time when the batch update operation was requested.
          format: date-time
        results:
          type: array
          description: >-
            An array of results from the batch update operation. Each item in
            the array is a PublicAssociationDefinitionConfigurationUpdateResult
            object.
          items:
            $ref: >-
              #/components/schemas/PublicAssociationDefinitionConfigurationUpdateResult
        startedAt:
          type: string
          description: The date and time when the batch update operation started.
          format: date-time
        status:
          type: string
          description: >-
            The current status of the batch update operation, which can be
            CANCELED, COMPLETE, PENDING, or PROCESSING.
          enum:
            - CANCELED
            - COMPLETE
            - PENDING
            - PROCESSING
    BatchResponsePublicAssociationDefinitionConfigurationUpdateResultWithErrors:
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
            detailing a specific issue that occurred.
          items:
            $ref: '#/components/schemas/StandardError'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of link names to associated URIs, providing additional
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
            An array of results from the batch operation, each representing an
            update result for a public association definition configuration.
          items:
            $ref: >-
              #/components/schemas/PublicAssociationDefinitionConfigurationUpdateResult
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
    PublicAssociationDefinitionConfigurationUpdateRequest:
      required:
        - category
        - maxToObjectIds
        - typeId
      type: object
      properties:
        category:
          type: string
          description: >-
            Specifies the category of the association, which can be
            HUBSPOT_DEFINED, INTEGRATOR_DEFINED, or USER_DEFINED.
          enum:
            - HUBSPOT_DEFINED
            - INTEGRATOR_DEFINED
            - USER_DEFINED
            - WORK
        maxToObjectIds:
          type: integer
          description: >-
            Defines the maximum number of target object IDs that can be
            associated.
          format: int32
        typeId:
          type: integer
          description: A unique identifier for the association type.
          format: int32
    PublicAssociationDefinitionConfigurationUpdateResult:
      required:
        - category
        - typeId
      type: object
      properties:
        category:
          type: string
          description: >-
            The category of the association, which can be HUBSPOT_DEFINED,
            INTEGRATOR_DEFINED, or USER_DEFINED.
          enum:
            - HUBSPOT_DEFINED
            - INTEGRATOR_DEFINED
            - USER_DEFINED
            - WORK
        typeId:
          type: integer
          description: >-
            An integer value used to uniquely identify a specific association
            type within its Association Category.
          format: int32
        userEnforcedMaxToObjectIds:
          type: integer
          description: >-
            The maximum number of object IDs that a user can enforce for
            associations.
          format: int32
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
            An object containing additional context about the error condition,
            with each key mapping to an array of strings.
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
            An object mapping link names to associated URIs that contain
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
          description: An object providing more specific details about the error category.
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