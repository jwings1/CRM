> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Retrieve errors for a specific import

> Retrieves detailed error records for a specific import operation, enabling you to identify and troubleshoot records that failed during processing.

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
  'crm.import'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-imports-v2026-09.json GET /crm/imports/2026-09/{importId}/errors
openapi: 3.0.1
info:
  title: CRM Imports
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
paths:
  /crm/imports/2026-09/{importId}/errors:
    get:
      tags:
        - Basic
      summary: Retrieve errors for a specific import
      description: >-
        Retrieves detailed error records for a specific import operation,
        enabling you to identify and troubleshoot records that failed during
        processing.
      operationId: >-
        get-/crm/imports/2026-09/{importId}/errors_/crm/imports/v3/{importId}/errors
      parameters:
        - name: importId
          in: path
          description: The unique identifier of the import for which to retrieve errors.
          required: true
          style: simple
          explode: false
          schema:
            type: integer
            format: int64
        - name: after
          in: query
          description: >-
            The paging cursor token of the last successfully read resource will
            be returned as the `paging.next.after` JSON property of a paged
            response containing more results.
          required: false
          style: form
          explode: true
          schema:
            type: string
        - name: includeErrorMessage
          in: query
          description: >-
            A boolean indicating whether to include detailed error messages in
            the response.
          required: false
          style: form
          explode: true
          schema:
            type: boolean
        - name: includeRowData
          in: query
          description: >-
            A boolean indicating whether to include the row data associated with
            each error in the response.
          required: false
          style: form
          explode: true
          schema:
            type: boolean
        - name: limit
          in: query
          description: The maximum number of results to display per page.
          required: false
          style: form
          explode: true
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/CollectionResponsePublicImportErrorForwardPaging
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.import
components:
  schemas:
    CollectionResponsePublicImportErrorForwardPaging:
      required:
        - results
      type: object
      properties:
        paging:
          $ref: '#/components/schemas/ForwardPaging'
        results:
          type: array
          description: >-
            An array of public import errors, each represented by a
            PublicImportError object.
          items:
            $ref: '#/components/schemas/PublicImportError'
    ForwardPaging:
      type: object
      properties:
        next:
          $ref: '#/components/schemas/NextPage'
      description: >-
        Paging information for forward-only pagination. Contains the next page
        reference when more results are available; omitted or empty on the last
        page.
    PublicImportError:
      required:
        - createdAt
        - errorType
        - id
        - sourceData
      type: object
      properties:
        createdAt:
          type: integer
          description: The epoch millisecond timestamp when this error was recorded.
          format: int64
        errorMessage:
          type: string
          description: A human-readable error message.
        errorType:
          type: string
          description: The classification of what went wrong during import processing.
          enum:
            - AMBIGUOUS_ENUMERATION_OPTION
            - ASSOCIATION_LABEL_NOT_FOUND
            - ASSOCIATION_LIMIT_EXCEEDED
            - ASSOCIATION_RECORD_NOT_FOUND
            - COLUMN_TOO_LARGE
            - COULD_NOT_FIND_BUSINESS_UNIT
            - COULD_NOT_FIND_OWNER
            - COULD_NOT_PARSE_DATE
            - COULD_NOT_PARSE_NUMBER
            - COULD_NOT_PARSE_ROW
            - COULD_NOT_PARSE_TERM
            - CREATE_ONLY_IMPORT
            - DUPLICATE_ALTERNATE_ID
            - DUPLICATE_ASSOCIATION_ID
            - DUPLICATE_EVENT
            - DUPLICATE_OBJECT_ID
            - DUPLICATE_RECORD_ID
            - DUPLICATE_ROW_CONTENT
            - DUPLICATE_UNIQUE_CREATION_KEY
            - DUPLICATE_UNIQUE_PROPERTY_VALUE
            - FAILED_TO_CREATE_ASSOCIATION
            - FAILED_TO_FIND_RECORD_FOR_ASSOCIATIONS
            - FAILED_TO_OPT_OUT_CONTACT
            - FAILED_TO_PROCESS_OBJECT_WITH_EMPTY_PROPERTY_VALUES
            - FAILED_VALIDATION
            - FILE_NOT_FOUND
            - GDPR_BLACKLISTED_EMAIL
            - INCORRECT_NUMBER_OF_COLUMNS
            - INVALID_ALTERNATE_ID
            - INVALID_ASSOCIATION_IDENTIFIER
            - INVALID_ASSOCIATION_KEY
            - INVALID_COLUMN_CONFIGURATION
            - INVALID_CUSTOM_PROPERTY_VALIDATION
            - INVALID_DOMAIN
            - INVALID_EMAIL
            - INVALID_ENUM_FILE_ID_OR_URL
            - INVALID_ENUMERATION_OPTION
            - INVALID_EVENT
            - INVALID_EVENT_TIMESTAMP
            - INVALID_FILE_TYPE
            - INVALID_NUMBER_SIZE
            - INVALID_OBJECT_ID
            - INVALID_PROPERTY_VALUE_FORMAT
            - INVALID_RECORD_ID
            - INVALID_REQUIRED_PROPERTY
            - INVALID_SHEET_COUNT
            - INVALID_SPREADSHEET
            - LIMIT_EXCEEDED
            - LINE_ITEM_MULTIPLE_PARENTS_IN_ROW
            - MANY_ERRORS_IN_ROW
            - MISSING_EVENT_DEFINITION
            - MISSING_EVENT_TIMESTAMP
            - MISSING_OBJECT_DEFINITION
            - MISSING_REQUIRED_PROPERTY
            - MULTIPLE_COMPANIES_WITH_THIS_DOMAIN
            - MULTIPLE_OWNERS_FOUND
            - NO_OBJECT_ID_FROM_ASSOCIATION_IDENTIFIER
            - OUTSIDE_VALID_TERM_RANGE
            - OUTSIDE_VALID_TIME_RANGE
            - PORTAL_WIDE_CUSTOM_OBJECT_LIMIT_EXCEEDED
            - PROPERTY_DEFINITION_NOT_FOUND
            - PROPERTY_VALUE_NOT_FOUND
            - ROW_DATA_TOO_LARGE
            - SECONDARY_EMAIL_WRITE_FAILURE
            - UNKNOWN_ASSOCIATION_RECORD_ID
            - UNKNOWN_BAD_REQUEST
            - UNKNOWN_ERROR
            - UPDATE_ONLY_IMPORT
        extraContext:
          type: string
          description: Additional human-readable context about the error.
        id:
          type: string
          description: A unique, stable identifier for this specific error.
        invalidPropertyValue:
          $ref: '#/components/schemas/PropertyValue'
        invalidValue:
          type: string
          description: >-
            The raw string value from the import file that caused the validation
            failure.
        invalidValueToDisplay:
          type: string
          description: >-
            A convenience accessor that returns either the value from
            `invalidPropertyValue` or `invalidValue`, whichever is present
            (preferring the property value).
        knownColumnNumber:
          type: integer
          description: >-
            The zero-based column index in the import file where the error
            occurred
          format: int32
        objectType:
          type: string
          description: The CRM object type affected by this error.
          enum:
            - ABANDONED_CART
            - ACCEPTANCE_TEST
            - AD
            - AD_ACCOUNT
            - AD_CAMPAIGN
            - AD_GROUP
            - AI_FORECAST
            - ALL_PAGES
            - APPROVAL
            - APPROVAL_STEP
            - ATTRIBUTION
            - AUDIENCE
            - AUTOMATION_JOURNEY
            - AUTOMATION_PLATFORM_FLOW
            - AUTOMATION_PLATFORM_FLOW_ACTION
            - BET_ALERT
            - BET_DELIVERABLE_SERVICE
            - BLOG_LISTING_PAGE
            - BLOG_POST
            - CALL
            - CAMPAIGN
            - CAMPAIGN_BUDGET_ITEM
            - CAMPAIGN_SPEND_ITEM
            - CAMPAIGN_STEP
            - CAMPAIGN_TEMPLATE
            - CAMPAIGN_TEMPLATE_STEP
            - CART
            - CASE_STUDY
            - CHATFLOW
            - CLIP
            - CMS_URL
            - COMBO_EVENT_CONFIGURATION
            - COMMERCE_PAYMENT
            - COMMUNICATION
            - COMPANY
            - CONTACT
            - CONTACT_CREATE_ATTRIBUTION
            - CONTENT
            - CONTENT_AUDIT
            - CONTENT_AUDIT_PAGE
            - CONVERSATION
            - CONVERSATION_INBOX
            - CONVERSATION_SESSION
            - CRM_OBJECTS_DUMMY_TYPE
            - CRM_PIPELINES_DUMMY_TYPE
            - CTA
            - CTA_VARIANT
            - DATA_PRIVACY_CONSENT
            - DATA_SYNC_STATE
            - DEAL
            - DEAL_CREATE_ATTRIBUTION
            - DEAL_REGISTRATION
            - DEAL_SPLIT
            - DISCOUNT
            - DISCOUNT_CODE
            - DISCOUNT_TEMPLATE
            - EMAIL
            - ENGAGEMENT
            - EXPORT
            - EXTERNAL_WEB_URL
            - FEE
            - FEEDBACK_SUBMISSION
            - FEEDBACK_SURVEY
            - FILE_MANAGER_FILE
            - FILE_MANAGER_FOLDER
            - FOLDER
            - FORECAST
            - FORM
            - FORM_SUBMISSION_INBOUNDDB
            - GOAL_TARGET
            - GOAL_TARGET_GROUP
            - GOAL_TEMPLATE
            - GSC_PROPERTY
            - HUB
            - IMPORT
            - INVOICE
            - KEYWORD
            - KNOWLEDGE_ARTICLE
            - LANDING_PAGE
            - LEAD
            - LINE_ITEM
            - MARKETING_CALENDAR
            - MARKETING_CAMPAIGN_UTM
            - MARKETING_EMAIL
            - MARKETING_EVENT
            - MARKETING_EVENT_ATTENDANCE
            - MARKETING_SMS
            - MEDIA_BRIDGE
            - MEETING_EVENT
            - MIC
            - NOTE
            - OBJECT_LIST
            - ORDER
            - OWNER
            - PARTNER_ACCOUNT
            - PARTNER_CLIENT
            - PARTNER_CLIENT_REVENUE
            - PARTNER_SERVICE
            - PAYMENT_LINK
            - PAYMENT_SCHEDULE
            - PAYMENT_SCHEDULE_INSTALLMENT
            - PERMISSIONS_TESTING
            - PLAYBOOK
            - PLAYBOOK_QUESTION
            - PLAYBOOK_SUBMISSION
            - PLAYBOOK_SUBMISSION_ANSWER
            - PLAYLIST
            - PLAYLIST_FOLDER
            - PODCAST_EPISODE
            - PORTAL
            - PORTAL_OBJECT_SYNC_MESSAGE
            - POSTAL_MAIL
            - PRIVACY_SCANNER_COOKIE
            - PRODUCT
            - PRODUCT_OR_FOLDER
            - PROPERTY_INFO
            - PROSPECTING_AGENT_CONTACT_ASSIGNMENT
            - PUBLISHING_TASK
            - QUARANTINED_SUBMISSION
            - QUOTA
            - QUOTE
            - QUOTE_FIELD
            - QUOTE_MODULE
            - QUOTE_MODULE_FIELD
            - QUOTE_TEMPLATE
            - RESTORABLE_CRM_OBJECT
            - ROSTER
            - ROSTER_MEMBER
            - SALES_DOCUMENT
            - SALES_TASK
            - SALES_WORKLOAD
            - SALESFORCE_SYNC_ERROR
            - SCHEDULING_PAGE
            - SCHEMAS_BACKEND_TEST
            - SCORE_CONFIGURATION
            - SEQUENCE
            - SEQUENCE_ENROLLMENT
            - SEQUENCE_STEP
            - SEQUENCE_STEP_ENROLLMENT
            - SERVICE
            - SITE_PAGE
            - SNIPPET
            - SOCIAL_BROADCAST
            - SOCIAL_CHANNEL
            - SOCIAL_POST
            - SOCIAL_PROFILE
            - SOX_PROTECTED_DUMMY_TYPE
            - SOX_PROTECTED_TEST_TYPE
            - SUBMISSION_TAG
            - SUBSCRIPTION
            - TASK
            - TASK_TEMPLATE
            - TAX
            - TEMPLATE
            - TICKET
            - UNKNOWN
            - UNSUBSCRIBE
            - USER
            - VIEW
            - VIEW_BLOCK
            - WEB_INTERACTIVE
        objectTypeId:
          type: string
          description: >-
            The modern object type identifier for the CRM object affected by
            this error.
        sourceData:
          $ref: '#/components/schemas/ImportRowCore'
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
    NextPage:
      required:
        - after
      type: object
      properties:
        after:
          type: string
          description: >-
            A string token used as a cursor to fetch the next set of results in
            a paginated response.
        link:
          type: string
          description: A URL string that provides the link to the next page of results.
      description: >-
        Specifies the paging information needed to retrieve the next set of
        results in a paginated API response
    PropertyValue:
      required:
        - dataSensitivity
        - isEncrypted
        - isLargeValue
        - maskedSubstrings
        - name
        - persistenceTimestamp
        - requestId
        - selectedByUser
        - selectedByUserTimestamp
        - source
        - sourceId
        - sourceLabel
        - sourceMetadata
        - sourceUpstreamDeployable
        - sourceVid
        - timestamp
        - unit
        - updatedByUserId
        - useTimestampAsPersistenceTimestamp
        - value
      type: object
      properties:
        dataSensitivity:
          type: string
          description: >-
            A string indicating the sensitivity level of the data. Valid values
            are 'none', 'standard', and 'high'.
          enum:
            - high
            - none
            - standard
        isEncrypted:
          type: boolean
          description: A boolean indicating whether the property value is encrypted.
        isLargeValue:
          type: boolean
          description: Indicates if the value exceeds normal size limits.
        maskedSubstrings:
          $ref: '#/components/schemas/MaskedSubstrings'
        name:
          type: string
          description: The name of the property, represented as a string.
        persistenceTimestamp:
          type: integer
          description: When the value was persisted to database, in epoch milliseconds.
          format: int64
        requestId:
          type: string
          description: >-
            A string identifier for the request associated with the property
            value.
        selectedByUser:
          type: boolean
          description: >-
            A boolean indicating whether the property value was selected by a
            user.
        selectedByUserTimestamp:
          type: integer
          description: >-
            A Unix timestamp in milliseconds indicating when the user selected
            the property value.
          format: int64
        source:
          type: string
          description: >-
            A string indicating the origin of the property value. Valid values
            include various sources such as 'API', 'FORM', 'SALESFORCE', and
            others.
          enum:
            - ACADEMY
            - ACCEPTANCE_TEST
            - ACTIVITY_AUTO_ASSOCIATE
            - ACTIVITY_LOG_REVERT
            - ADS
            - AI_GROUP
            - ANALYTICS
            - API
            - APPROVALS
            - ASSISTS
            - ASSOCIATIONS
            - AUTO_ASSOCIATE_BY_DOMAIN
            - AUTOMATION_JOURNEY
            - AUTOMATION_PLATFORM
            - AVATARS_SERVICE
            - BATCH_UPDATE
            - BCC_TO_CRM
            - BEHAVIORAL_EVENTS
            - BET_ASSIGNMENT
            - BET_CRM_CONNECTOR
            - BIDEN
            - BILLING
            - BOT
            - BREEZE_AGENT
            - CALCULATED
            - CENTRAL_EXCHANGE_RATES
            - CHATSPOT
            - CLONE_OBJECTS
            - COMMUNICATOR
            - COMPANIES
            - COMPANY_FAMILIES
            - COMPANY_INSIGHTS
            - CONNECTED_ACCOUNT
            - CONTACTS
            - CONTACTS_WEB
            - CONTENT_MEMBERSHIP
            - CONVERSATIONAL_ENRICHMENT
            - CONVERSATIONS
            - CRM_PROCESSES_PLATFORM
            - CRM_UI
            - CRM_UI_BULK_ACTION
            - CUSTOMER_AGENT
            - CUSTOMER_PORTAL
            - DATA_ENRICHMENT
            - DATA_QUALITY
            - DATASET
            - DEALS
            - DEFAULT
            - DELETE_OBJECTS
            - DI_WRITE_TO_CRM
            - EMAIL
            - EMAIL_INBOX_IMPORT
            - EMAIL_INTEGRATION
            - ENGAGEMENTS
            - EXTENSION
            - FILE_MANAGER
            - FLYWHEEL_PRODUCT_DATA_SYNC
            - FORECASTING
            - FORM
            - FORWARD_TO_CRM
            - GMAIL_INTEGRATION
            - GOALS
            - HEISENBERG
            - HELP_DESK
            - HELP_DESK_AI
            - IMPORT
            - INTEGRATION
            - INTEGRATIONS_PLATFORM
            - INTEGRATIONS_SYNC
            - INTENT
            - INTERNAL_PROCESSING
            - LEADIN
            - LEGAL_BASIS_REMEDIATION
            - MARKET_SOURCING
            - MARKETPLACE
            - MARKETS
            - MEETINGS
            - MERGE_COMPANIES
            - MERGE_CONTACTS
            - MERGE_OBJECTS
            - MERGE_REVERT_OBJECTS
            - MICROAPPS
            - MIGRATION
            - MOBILE_ANDROID
            - MOBILE_IOS
            - PAYMENTS
            - PIPELINE_SETTINGS
            - PLAYBOOKS
            - PORTAL_OBJECT_SYNC
            - PORTAL_USER_ASSOCIATOR
            - PRESENTATIONS
            - PRIMARY_AUTOMATION
            - PROPERTY_DEFAULT_VALUE
            - PROPERTY_RESTORE
            - PROPERTY_SETTINGS
            - PROSPECTING_AGENT
            - QUOTAS
            - QUOTES
            - RECYCLING_BIN
            - RESTORE_OBJECTS
            - REVENUE_PLATFORM
            - SALES
            - SALES_MESSAGES
            - SALESFORCE
            - SEQUENCES
            - SETTINGS
            - SIDEKICK
            - SIGNALS
            - SLACK_INTEGRATION
            - SMART_DATA_CAPTURE
            - SOCIAL
            - SUCCESS
            - TALLY
            - TASK
            - UNKNOWN
            - WAL_INCREMENTAL
            - WORK_UI
            - WORKFLOW_CONTACT_DELETE_ACTION
            - WORKFLOWS
        sourceId:
          type: string
          description: A string identifier for the source of the property value.
        sourceLabel:
          type: string
          description: A string label describing the source of the property value.
        sourceMetadata:
          type: string
          description: A string containing metadata about the source of the property value.
        sourceUpstreamDeployable:
          type: string
          description: >-
            A string indicating the upstream deployable source of the property
            value.
        sourceVid:
          type: array
          description: >-
            An array of integers representing the source video IDs associated
            with the property value.
          items:
            type: integer
            format: int64
        timestamp:
          type: integer
          description: >-
            A Unix timestamp in milliseconds indicating when the property value
            was recorded.
          format: int64
        unit:
          type: string
          description: A string representing the unit of the property value, if applicable.
        updatedByUserId:
          type: integer
          description: >-
            An integer representing the ID of the user who last updated the
            property value.
          format: int32
        useTimestampAsPersistenceTimestamp:
          type: boolean
          description: >-
            Flag indicating whether to use the timestamp field as the
            persistence timestamp.
        value:
          type: string
          description: The actual value of the property, represented as a string.
      description: >-
        Represents a single custom property of a marketing event, storing its
        name, value, metadata (like source, timestamp, and sensitivity), and
        related audit information for tracking changes.
    ImportRowCore:
      required:
        - additionalRowData
        - containsEncryptedProperties
        - fileId
        - lineNumber
        - rowData
      type: object
      properties:
        additionalRowData:
          type: array
          description: >-
            An array of strings containing any additional data associated with
            this row.
          items:
            type: string
        containsEncryptedProperties:
          type: boolean
          description: Indicates whether this row contains values that were encrypted.
        fileId:
          type: integer
          description: The unique identifier of the uploaded file containing this row.
          format: int64
        lineNumber:
          type: integer
          description: >-
            The 1-indexed line number of this row in the source file. Line
            number 0 is reserved for file-wide errors that don't correspond to a
            specific row.
          format: int32
        pageName:
          type: string
          description: The name of the spreadsheet sheet/page containing this row.
        rowData:
          type: array
          description: An array of strings representing the core data of the row.
          items:
            type: string
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
    MaskedSubstrings:
      required:
        - substrings
      type: object
      properties:
        substrings:
          type: array
          description: >-
            An array of MaskedSubstring objects, each defining a specific
            portion of a string to be masked. This property is required and
            ensures that sensitive data is appropriately obscured.
          items:
            $ref: '#/components/schemas/MaskedSubstring'
    MaskedSubstring:
      required:
        - end
        - start
      type: object
      properties:
        end:
          type: integer
          description: An integer indicating the ending position of the substring.
          format: int32
        start:
          type: integer
          description: An integer indicating the starting position of the substring.
          format: int32
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
            crm.import: ''

````