> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 0748af12-c8bf-468c-883b-0c31a14f92e6
---

# Retrieve stage

> Retrieve details of a specific stage within a pipeline for a given object type in HubSpot. This endpoint is useful for accessing information about a particular stage, such as its label, display order, and metadata, which can be used for managing or analyzing pipeline stages.

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
  'crm.objects.owners.read',
  'crm.objects.deals.read',
  'crm.objects.subscriptions.read',
  'crm.objects.services.read',
  'crm.objects.tickets.sensitive.read',
  'crm.objects.listings.write',
  'crm.objects.custom.read',
  'crm.schemas.tickets.read',
  'crm.objects.custom.sensitive.write.v2',
  'crm.objects.tasks.read',
  'crm.objects.custom.highly_sensitive.write.v2',
  'crm.schemas.quotes.read',
  'crm.objects.companies.read',
  'crm.objects.tickets.highly_sensitive.read',
  'crm.objects.companies.sensitive.read.v2',
  'media_bridge.read',
  'crm.objects.deals.highly_sensitive.read.v2',
  'crm.objects.companies.highly_sensitive.read.v2',
  'crm.objects.contacts.sensitive.write.v2',
  'crm.objects.calls.read',
  'crm.objects.meetings.read',
  'crm.schemas.services.read',
  'crm.schemas.line_items.read',
  'crm.schemas.subscriptions.read',
  'crm.objects.projects.highly_sensitive.write',
  'crm.schemas.companies.read',
  'crm.objects.feedback_submissions.read',
  'crm.objects.products.write',
  'crm.objects.services.write',
  'crm.objects.subscriptions.write',
  'crm.schemas.calls.read',
  'crm.schemas.meetings.read',
  'crm.objects.contacts.read',
  'crm.objects.invoices.read',
  'crm.schemas.orders.read',
  'crm.schemas.emails.read',
  'crm.schemas.deals.read',
  'crm.objects.deals.write',
  'e-commerce',
  'crm.schemas.notes.read',
  'crm.objects.projects.read',
  'crm.objects.companies.sensitive.write.v2',
  'crm.objects.custom.highly_sensitive.read.v2',
  'crm.objects.goals.write',
  'crm.objects.line_items.write',
  'crm.objects.contacts.write',
  'crm.objects.goals.read',
  'crm.objects.line_items.read',
  'crm.objects.deals.sensitive.read.v2',
  'crm.objects.projects.sensitive.write',
  'crm.objects.quotes.write',
  'tickets.highly_sensitive.v2',
  'crm.schemas.contacts.read',
  'crm.objects.leads.read',
  'crm.objects.leads.write',
  'crm.schemas.tasks.read',
  'crm.objects.emails.read',
  'crm.schemas.invoices.read',
  'crm.objects.quotes.read',
  'crm.objects.notes.read',
  'crm.objects.courses.read',
  'timeline',
  'crm.pipelines.orders.read',
  'crm.objects.marketing_events.read',
  'crm.objects.contacts.sensitive.read.v2',
  'crm.schemas.projects.read',
  'crm.objects.orders.read',
  'automation',
  'crm.objects.companies.write',
  'crm.schemas.carts.read',
  'cpq.quotes.write',
  'crm.schemas.listings.read',
  'crm.objects.contacts.highly_sensitive.read.v2',
  'crm.objects.appointments.sensitive.read.v2',
  'crm.objects.contacts.highly_sensitive.write.v2',
  'crm.objects.commercepayments.write',
  'crm.objects.invoices.write',
  'crm.objects.custom.sensitive.read.v2',
  'crm.objects.users.read',
  'crm.objects.appointments.write',
  'tickets',
  'crm.objects.deals.sensitive.write.v2',
  'cpq.quotes.read',
  'crm.objects.appointments.sensitive.write.v2',
  'crm.objects.projects.highly_sensitive.read',
  'crm.schemas.appointments.read',
  'tickets.sensitive.v2',
  'crm.objects.custom.write',
  'crm.objects.appointments.read',
  'crm.schemas.courses.read',
  'crm.objects.deals.highly_sensitive.write.v2',
  'crm.objects.companies.highly_sensitive.write.v2',
  'crm.objects.projects.sensitive.read',
  'crm.objects.projects.write',
  'crm.objects.marketing_events.write',
  'crm.schemas.custom.read',
  'crm.objects.carts.read',
  'crm.objects.courses.write',
  'crm.schemas.commercepayments.read',
  'crm.objects.listings.read'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-pipelines-v2026-09.json GET /crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}
openapi: 3.0.1
info:
  title: CRM Pipelines
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
  - name: Basic
paths:
  /crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}:
    get:
      tags:
        - Basic
      summary: Retrieve stage
      description: >-
        Retrieve details of a specific stage within a pipeline for a given
        object type in HubSpot. This endpoint is useful for accessing
        information about a particular stage, such as its label, display order,
        and metadata, which can be used for managing or analyzing pipeline
        stages.
      operationId: get-/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}
      parameters:
        - name: objectType
          in: path
          description: The type of object for which the pipeline stage is being retrieved.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: pipelineId
          in: path
          description: The unique identifier of the pipeline that contains the stage.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: stageId
          in: path
          description: The unique identifier of the stage to retrieve within the pipeline.
          required: true
          style: simple
          explode: false
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PipelineStage'
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.objects.owners.read
        - oauth2:
            - crm.objects.deals.read
        - oauth2:
            - crm.objects.subscriptions.read
        - oauth2:
            - crm.objects.services.read
        - oauth2:
            - crm.objects.tickets.sensitive.read
        - oauth2:
            - crm.objects.listings.write
        - oauth2:
            - crm.objects.custom.read
        - oauth2:
            - crm.objects.tasks.read
        - oauth2:
            - crm.objects.custom.sensitive.write.v2
        - oauth2:
            - crm.objects.custom.highly_sensitive.write.v2
        - oauth2:
            - crm.schemas.quotes.read
        - oauth2:
            - crm.objects.companies.read
        - oauth2:
            - crm.objects.tickets.highly_sensitive.read
        - oauth2:
            - crm.objects.companies.sensitive.read.v2
        - oauth2:
            - media_bridge.read
        - oauth2:
            - crm.objects.deals.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.companies.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.contacts.sensitive.write.v2
        - oauth2:
            - crm.objects.calls.read
        - oauth2:
            - crm.objects.meetings.read
        - oauth2:
            - crm.schemas.services.read
        - oauth2:
            - crm.schemas.line_items.read
        - oauth2:
            - crm.schemas.subscriptions.read
        - oauth2:
            - crm.objects.projects.highly_sensitive.write
        - oauth2:
            - crm.schemas.companies.read
        - oauth2:
            - crm.objects.products.write
        - oauth2:
            - crm.objects.feedback_submissions.read
        - oauth2:
            - crm.objects.services.write
        - oauth2:
            - crm.objects.subscriptions.write
        - oauth2:
            - crm.schemas.calls.read
        - oauth2:
            - crm.schemas.meetings.read
        - oauth2:
            - crm.objects.contacts.read
        - oauth2:
            - crm.objects.invoices.read
        - oauth2:
            - crm.schemas.orders.read
        - oauth2:
            - crm.schemas.emails.read
        - oauth2:
            - crm.schemas.deals.read
        - oauth2:
            - crm.objects.deals.write
        - oauth2:
            - e-commerce
        - oauth2:
            - crm.schemas.notes.read
        - oauth2:
            - crm.objects.companies.sensitive.write.v2
        - oauth2:
            - crm.objects.projects.read
        - oauth2:
            - crm.objects.custom.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.goals.write
        - oauth2:
            - crm.objects.line_items.write
        - oauth2:
            - crm.objects.contacts.write
        - oauth2:
            - crm.objects.goals.read
        - oauth2:
            - crm.objects.line_items.read
        - oauth2:
            - crm.objects.projects.sensitive.write
        - oauth2:
            - crm.objects.deals.sensitive.read.v2
        - oauth2:
            - crm.objects.quotes.write
        - oauth2:
            - tickets.highly_sensitive.v2
        - oauth2:
            - crm.schemas.contacts.read
        - oauth2:
            - crm.objects.leads.read
        - oauth2:
            - crm.objects.leads.write
        - oauth2:
            - crm.schemas.tasks.read
        - oauth2:
            - crm.objects.emails.read
        - oauth2:
            - crm.schemas.invoices.read
        - oauth2:
            - crm.objects.quotes.read
        - oauth2:
            - crm.objects.notes.read
        - oauth2:
            - crm.objects.courses.read
        - oauth2:
            - crm.objects.marketing_events.read
        - oauth2:
            - crm.pipelines.orders.read
        - oauth2:
            - crm.objects.contacts.sensitive.read.v2
        - oauth2:
            - crm.schemas.projects.read
        - oauth2:
            - crm.objects.orders.read
        - oauth2:
            - automation
        - oauth2:
            - crm.objects.companies.write
        - oauth2:
            - crm.schemas.carts.read
        - oauth2:
            - cpq.quotes.write
        - oauth2:
            - crm.schemas.listings.read
        - oauth2:
            - crm.objects.contacts.highly_sensitive.read.v2
        - oauth2:
            - crm.objects.appointments.sensitive.read.v2
        - oauth2:
            - crm.objects.contacts.highly_sensitive.write.v2
        - oauth2:
            - crm.objects.commercepayments.write
        - oauth2:
            - crm.objects.invoices.write
        - oauth2:
            - crm.objects.custom.sensitive.read.v2
        - oauth2:
            - crm.objects.users.read
        - oauth2:
            - crm.objects.appointments.write
        - oauth2:
            - crm.objects.deals.sensitive.write.v2
        - oauth2:
            - cpq.quotes.read
        - oauth2:
            - crm.objects.appointments.sensitive.write.v2
        - oauth2:
            - crm.objects.projects.highly_sensitive.read
        - oauth2:
            - crm.schemas.appointments.read
        - oauth2:
            - tickets.sensitive.v2
        - oauth2:
            - crm.objects.custom.write
        - oauth2:
            - crm.objects.appointments.read
        - oauth2:
            - crm.schemas.courses.read
        - oauth2:
            - crm.objects.deals.highly_sensitive.write.v2
        - oauth2:
            - crm.objects.companies.highly_sensitive.write.v2
        - oauth2:
            - crm.objects.projects.sensitive.read
        - oauth2:
            - crm.pipelines.approval.read
        - oauth2:
            - crm.objects.marketing_events.write
        - oauth2:
            - crm.objects.projects.write
        - oauth2:
            - crm.schemas.custom.read
        - oauth2:
            - crm.objects.carts.read
        - oauth2:
            - crm.objects.courses.write
        - oauth2:
            - crm.schemas.commercepayments.read
        - oauth2:
            - crm.objects.listings.read
components:
  schemas:
    PipelineStage:
      required:
        - archived
        - createdAt
        - displayOrder
        - id
        - label
        - metadata
        - updatedAt
        - writePermissions
      type: object
      properties:
        archived:
          type: boolean
          description: A boolean indicating whether the stage is archived.
        archivedAt:
          type: string
          description: The date and time when the stage was archived, in ISO 8601 format.
          format: date-time
        createdAt:
          type: string
          description: The date and time when the stage was created, in ISO 8601 format.
          format: date-time
        displayOrder:
          type: integer
          description: >-
            An integer indicating the position of this stage within the
            pipeline, determining its order relative to other stages.
          format: int32
        id:
          type: string
          description: A unique string identifier for the pipeline stage.
        label:
          type: string
          description: The name or title of the pipeline stage, represented as a string.
        metadata:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing additional metadata for the stage, with string
            values for each property.
        updatedAt:
          type: string
          description: >-
            The date and time when the stage was last updated, in ISO 8601
            format.
          format: date-time
        writePermissions:
          type: string
          description: >-
            A string indicating the write permissions for the stage. Valid
            values include 'CRM_PERMISSIONS_ENFORCEMENT', 'READ_ONLY', and
            'INTERNAL_ONLY'.
          enum:
            - CRM_PERMISSIONS_ENFORCEMENT
            - INTERNAL_ONLY
            - READ_ONLY
    Error:
      required:
        - category
        - correlationId
        - message
      type: object
      properties:
        category:
          type: string
          description: The error category.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: >-
            Context about the error condition, represented as an object with
            additional properties.
          example: >-
            {invalidPropertyName=[propertyValue], missingScopes=[scope1,
            scope2]}
        correlationId:
          type: string
          description: >-
            A unique identifier for the request. Include this value with any
            error reports or support tickets.
          format: uuid
          example: aeb5f871-7f07-4993-9211-075dc63e7cbf
        errors:
          type: array
          description: >-
            Further information about the error, represented as an array of
            ErrorDetail objects.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of link names to associated URIs containing documentation
            about the error or recommended remediation steps.
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate.
          example: An error occurred
        subCategory:
          type: string
          description: >-
            A specific category that contains more specific detail about the
            error.
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
          description: The status code associated with the error detail.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: >-
            Context about the error condition, represented as an object with
            additional properties that are arrays of strings.
          example: '{missingScopes=[scope1, scope2]}'
        in:
          type: string
          description: The name of the field or parameter in which the error was found.
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate.
        subCategory:
          type: string
          description: >-
            A specific category that contains more specific detail about the
            error.
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
            automation: ''
            cpq.quotes.read: ''
            cpq.quotes.write: ''
            crm.objects.appointments.read: ''
            crm.objects.appointments.sensitive.read.v2: ''
            crm.objects.appointments.sensitive.write.v2: ''
            crm.objects.appointments.write: ''
            crm.objects.calls.read: ''
            crm.objects.carts.read: ''
            crm.objects.carts.write: ''
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
            crm.objects.marketing_events.read: ''
            crm.objects.marketing_events.write: ''
            crm.objects.meetings.read: ''
            crm.objects.notes.read: ''
            crm.objects.orders.read: ''
            crm.objects.orders.write: ''
            crm.objects.owners.read: ''
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
            crm.pipelines.approval.read: ''
            crm.pipelines.orders.read: ''
            crm.pipelines.orders.write: ''
            crm.schemas.appointments.read: ''
            crm.schemas.appointments.write: ''
            crm.schemas.calls.read: ''
            crm.schemas.calls.write: ''
            crm.schemas.carts.read: ''
            crm.schemas.carts.write: ''
            crm.schemas.commercepayments.read: ''
            crm.schemas.commercepayments.write: ''
            crm.schemas.companies.read: ''
            crm.schemas.companies.write: ''
            crm.schemas.contacts.read: ''
            crm.schemas.contacts.write: ''
            crm.schemas.courses.read: ''
            crm.schemas.courses.write: ''
            crm.schemas.custom.read: ''
            crm.schemas.custom.write: ''
            crm.schemas.deals.read: ''
            crm.schemas.deals.write: ''
            crm.schemas.emails.read: ''
            crm.schemas.emails.write: ''
            crm.schemas.invoices.read: ''
            crm.schemas.invoices.write: ''
            crm.schemas.line_items.read: ''
            crm.schemas.listings.read: ''
            crm.schemas.listings.write: ''
            crm.schemas.meetings.read: ''
            crm.schemas.meetings.write: ''
            crm.schemas.notes.read: ''
            crm.schemas.notes.write: ''
            crm.schemas.orders.read: ''
            crm.schemas.orders.write: ''
            crm.schemas.projects.read: ''
            crm.schemas.quotes.read: ''
            crm.schemas.quotes.write: ''
            crm.schemas.services.read: ''
            crm.schemas.services.write: ''
            crm.schemas.subscriptions.read: ''
            crm.schemas.subscriptions.write: ''
            crm.schemas.tasks.read: ''
            crm.schemas.tasks.write: ''
            e-commerce: ''
            media_bridge.read: ''
            tickets.highly_sensitive.v2: ''
            tickets.sensitive.v2: ''

````