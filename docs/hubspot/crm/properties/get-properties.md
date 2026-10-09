> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Read all properties

> Read all existing properties for the specified object type and HubSpot account.

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
  'crm.schemas.projects.read',
  'crm.schemas.listings.read',
  'crm.objects.contacts.highly_sensitive.read.v2',
  'crm.schemas.carts.read',
  'automation',
  'crm.objects.companies.write',
  'crm.objects.custom.sensitive.read.v2',
  'crm.objects.users.read',
  'crm.objects.commercepayments.write',
  'crm.objects.invoices.write',
  'crm.objects.contacts.highly_sensitive.write.v2',
  'crm.objects.appointments.write',
  'crm.objects.custom.write',
  'tickets',
  'crm.objects.deals.sensitive.write.v2',
  'crm.schemas.appointments.read',
  'crm.objects.deals.highly_sensitive.write.v2',
  'crm.objects.companies.highly_sensitive.write.v2',
  'tickets.sensitive.v2',
  'crm.objects.projects.highly_sensitive.read',
  'crm.objects.appointments.read',
  'crm.schemas.courses.read',
  'crm.objects.appointments.sensitive.write.v2',
  'crm.objects.projects.sensitive.read',
  'crm.schemas.custom.read',
  'crm.objects.projects.write',
  'crm.objects.marketing_events.write',
  'media_bridge.read',
  'crm.schemas.commercepayments.read',
  'crm.objects.listings.read',
  'crm.objects.courses.write',
  'crm.objects.carts.read',
  'crm.objects.listings.write',
  'crm.objects.custom.read',
  'crm.objects.deals.read',
  'crm.objects.subscriptions.read',
  'crm.objects.owners.read',
  'crm.objects.companies.sensitive.read.v2',
  'crm.schemas.quotes.read',
  'crm.objects.companies.read',
  'crm.objects.custom.sensitive.write.v2',
  'crm.schemas.services.read',
  'crm.objects.deals.highly_sensitive.read.v2',
  'crm.objects.contacts.sensitive.write.v2',
  'crm.objects.companies.highly_sensitive.read.v2',
  'crm.schemas.subscriptions.read',
  'crm.objects.projects.highly_sensitive.write',
  'crm.schemas.companies.read',
  'crm.schemas.line_items.read',
  'crm.objects.contacts.read',
  'crm.objects.services.write',
  'crm.objects.subscriptions.write',
  'crm.objects.products.write',
  'crm.objects.feedback_submissions.read',
  'crm.objects.custom.highly_sensitive.read.v2',
  'crm.objects.deals.write',
  'crm.objects.invoices.read',
  'e-commerce',
  'crm.schemas.deals.read',
  'crm.schemas.orders.read',
  'crm.schemas.contacts.read',
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
  'crm.objects.line_items.read',
  'crm.objects.contacts.sensitive.read.v2',
  'crm.objects.line_items.write',
  'crm.objects.courses.read',
  'timeline',
  'crm.pipelines.orders.read',
  'crm.schemas.invoices.read',
  'crm.objects.quotes.read',
  'crm.objects.services.read',
  'crm.objects.marketing_events.read'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-properties-v2026-09.json GET /crm/properties/2026-09/{objectType}
openapi: 3.0.1
info:
  title: Properties
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
    Create a set of custom multi-select properties for storing contract data on
    company records.
  x-hubspot-introduction: >-
    Use the properties API to store information in fields on individual contact
    records. You can use this API to manage existing default and custom
    properties, create new custom properties, and more.
servers:
  - url: https://api.hubapi.com
security: []
tags:
  - name: Basic
  - name: Batch
paths:
  /crm/properties/2026-09/{objectType}:
    get:
      tags:
        - Basic
      summary: Read all properties
      description: >-
        Read all existing properties for the specified object type and HubSpot
        account.
      operationId: >-
        get-/crm/properties/2026-09/{objectType}_/crm/properties/2025-09/{objectType}
      parameters:
        - name: objectType
          in: path
          description: >-
            The type of CRM object for which properties are being retrieved,
            such as 'contacts', 'companies', etc.
          required: true
          style: simple
          explode: false
          schema:
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
        - name: dataSensitivity
          in: query
          description: >-
            Filter properties based on data sensitivity level. Valid values are
            'non_sensitive', 'sensitive', and 'highly_sensitive'. Defaults to
            'non_sensitive'.
          required: false
          style: form
          explode: true
          schema:
            type: string
            default: non_sensitive
            enum:
              - highly_sensitive
              - non_sensitive
              - sensitive
        - name: locale
          in: query
          description: >-
            Specify the locale to retrieve properties in a particular language
            or regional format.
          required: false
          style: form
          explode: true
          schema:
            type: string
        - name: properties
          in: query
          description: A comma-separated list of property names to include in the response.
          required: false
          style: form
          explode: true
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CollectionResponsePropertyNoPaging'
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
    CollectionResponsePropertyNoPaging:
      required:
        - results
      type: object
      properties:
        results:
          type: array
          description: >-
            An array of Property objects, each representing a specific property
            associated with the object type. This array contains the details of
            each property such as name, label, type, and other metadata.
          items:
            $ref: '#/components/schemas/Property'
    Property:
      required:
        - description
        - fieldType
        - groupName
        - label
        - name
        - options
        - type
      type: object
      properties:
        archived:
          type: boolean
          description: Whether or not the property is archived.
        archivedAt:
          type: string
          description: When the property was archived.
          format: date-time
        calculated:
          type: boolean
          description: >-
            For default properties, true indicates that the property is
            calculated by a HubSpot process. It has no effect for custom
            properties.
        calculationFormula:
          type: string
          description: Represents a formula that is used to compute a calculated property.
        createdAt:
          type: string
          description: The timestamp when the property was created, in ISO 8601 format.
          format: date-time
        createdUserId:
          type: string
          description: >-
            The internal user ID of the user who created the property in
            HubSpot. This field may not exist if the property was created
            outside of HubSpot.
        currencyPropertyName:
          type: string
          description: >-
            The name of the currency property associated with this property, if
            applicable.
        dataSensitivity:
          type: string
          description: >-
            The sensitivity level of the data. Valid values include
            'non_sensitive', 'sensitive', and 'highly_sensitive'.
          enum:
            - highly_sensitive
            - non_sensitive
            - sensitive
        dateDisplayHint:
          type: string
          description: >-
            Indicates how date values should be displayed, with options such as
            'absolute', 'absolute_with_relative', 'time_since', or 'time_until'.
          enum:
            - absolute
            - absolute_with_relative
            - time_since
            - time_until
        description:
          type: string
          description: >-
            A description of the property that will be shown as help text in
            HubSpot.
        displayOrder:
          type: integer
          description: >-
            Properties are shown in order, starting with the lowest positive
            integer value.
          format: int32
        externalOptions:
          type: boolean
          description: >-
            For default properties, true indicates that the options are stored
            externally to the property settings.
        fieldType:
          type: string
          description: Controls how the property appears in HubSpot.
        formField:
          type: boolean
          description: Whether or not the property can be used in a HubSpot form.
        groupName:
          type: string
          description: The name of the property group the property belongs to.
        hasUniqueValue:
          type: boolean
          description: >-
            Whether or not the property's value must be unique. Once set, this
            can't be changed.
        hidden:
          type: boolean
          description: >-
            Whether or not the property will be hidden from the HubSpot UI. It's
            recommended this be set to false for custom properties.
          example: false
        hubspotDefined:
          type: boolean
          description: This will be true for default object properties built into HubSpot.
        label:
          type: string
          description: A human-readable property label that will be shown in HubSpot.
        modificationMetadata:
          $ref: '#/components/schemas/PropertyModificationMetadata'
        name:
          type: string
          description: >-
            The internal property name, which must be used when referencing the
            property via the API.
        numberDisplayHint:
          type: string
          description: >-
            A hint for displaying number properties. Valid values include
            'unformatted', 'formatted', 'currency', 'percentage', 'duration',
            and 'probability'.
          enum:
            - currency
            - duration
            - formatted
            - percentage
            - probability
            - unformatted
        options:
          type: array
          description: >-
            A list of valid options for the property. This field is required for
            enumerated properties, but will be empty for other property types.
          items:
            $ref: '#/components/schemas/Option'
        referencedObjectType:
          type: string
          description: >-
            If this property is related to other object(s), they'll be listed
            here.
        sensitiveDataCategories:
          type: array
          description: >-
            An array of categories indicating the sensitivity of the data
            contained in the property.
          items:
            type: string
        showCurrencySymbol:
          type: boolean
          description: >-
            Whether or not the property will display the currency symbol set in
            the account settings.
        textDisplayHint:
          type: string
          description: >-
            A hint for displaying text properties. Valid values include
            'unformatted_single_line', 'multi_line', 'email', 'phone_number',
            'domain_name', 'ip_address', 'physical_address', and 'postal_code'.
          enum:
            - domain_name
            - email
            - ip_address
            - multi_line
            - phone_number
            - physical_address
            - postal_code
            - unformatted_single_line
        type:
          type: string
          description: The property data type.
        updatedAt:
          type: string
          description: >-
            The timestamp when the property was last updated, in ISO 8601
            format.
          format: date-time
        updatedUserId:
          type: string
          description: >-
            The internal user ID of the user who updated the property in
            HubSpot. This field may not exist if the property was updated
            outside of HubSpot.
      description: A HubSpot property
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
    PropertyModificationMetadata:
      required:
        - archivable
        - readOnlyDefinition
        - readOnlyValue
      type: object
      properties:
        archivable:
          type: boolean
          description: Specifies whether the property can be archived.
        readOnlyDefinition:
          type: boolean
          description: >-
            Indicates whether the property's definition is read-only and cannot
            be modified.
        readOnlyOptions:
          type: boolean
          description: >-
            Indicates whether the property's options are read-only and cannot be
            modified.
        readOnlyValue:
          type: boolean
          description: >-
            Indicates whether the property's value is read-only and cannot be
            modified.
    Option:
      required:
        - hidden
        - label
        - value
      type: object
      properties:
        description:
          type: string
          description: A description of the option.
        displayOrder:
          type: integer
          description: >-
            Options are displayed in order starting with the lowest positive
            integer value. Values of -1 will cause the option to be displayed
            after any positive values.
          format: int32
        hidden:
          type: boolean
          description: Hidden options will not be displayed in HubSpot.
        label:
          type: string
          description: A human-readable option label that will be shown in HubSpot.
        value:
          type: string
          description: >-
            The internal value of the option, which must be used when setting
            the property value through the API.
      description: A HubSpot property option
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