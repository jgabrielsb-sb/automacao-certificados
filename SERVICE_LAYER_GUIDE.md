# Service Layer in Hexagonal Architecture

## Overview

The **Service Layer** in hexagonal architecture represents **reusable business logic** that can be shared across multiple use cases or workflows. Services encapsulate domain operations that don't fit into a single use case.

## What Services Should Stand For

### 1. **Reusable Business Logic**
Services contain business logic that is:
- Used by multiple use cases or workflows
- Not specific to a single use case
- Domain-focused (not infrastructure)

### 2. **Orchestration of Multiple Adapters**
Services coordinate multiple adapters to accomplish a business operation:
- Combine multiple API calls
- Handle complex business rules
- Manage transactions or multi-step operations

### 3. **Domain Operations**
Services represent domain concepts and operations:
- Business rules validation
- Complex calculations
- Data transformations with business logic
- Cross-cutting concerns

## Service Layer vs Other Layers

### Services vs Use Cases

| **Use Cases** | **Services** |
|--------------|--------------|
| Represent a **single user/business action** | Represent **reusable business operations** |
| Orchestrate workflows and services | Encapsulate specific business logic |
| Entry point for application features | Called by use cases or workflows |
| Example: `DownloadCertificatesUseCase` | Example: `DocumentRegistrationService` |

**Example:**
```python
# Use Case - Orchestrates the full process
class DownloadCertificatesUseCase:
    def run(self):
        certificates = self.get_certificates()
        for cert in certificates:
            workflow = self.workflow_selector.get_workflow(...)
            result = workflow.run(cert.cnpj)
            # Uses service for registration
            self.registration_service.register(result)

# Service - Reusable business logic
class DocumentRegistrationService:
    def register(self, document):
        # Complex business logic for registration
        # Used by multiple use cases/workflows
        pass
```

### Services vs Adapters

| **Adapters** | **Services** |
|--------------|--------------|
| Implement **ports (interfaces)** | Implement **business logic** |
| Connect to **external systems** | Work with **domain models** |
| Handle **technical concerns** | Handle **business concerns** |
| Example: `CertificadoAPIRequester` | Example: `CertificadoAPIService` |

**Key Difference:**
- **Adapters** = "How to call the API" (technical)
- **Services** = "What business rules apply when registering" (business)

### Services vs Workflows

| **Workflows** | **Services** |
|--------------|--------------|
| Represent a **complete process** | Represent **reusable operations** |
| Sequence of steps for a specific goal | Single or related operations |
| Example: `Workflow` (download + persist) | Example: `DocumentValidationService` |

## When to Create a Service

Create a service when you have:

1. **Reusable Business Logic**
   - Logic used by multiple use cases
   - Logic used by multiple workflows
   - Domain operations that are independent

2. **Complex Business Rules**
   - Multi-step operations with business rules
   - Validation logic
   - Business calculations

3. **Orchestration of Multiple Adapters**
   - Need to call multiple APIs in a specific way
   - Transaction-like operations
   - Complex data transformations

4. **Domain Concepts**
   - Operations that represent domain concepts
   - Business operations that are meaningful on their own

## When NOT to Create a Service

Don't create a service for:

1. **Simple Adapter Calls**
   - Direct API calls → Use adapters directly
   - Simple CRUD → Use adapters directly

2. **Use Case-Specific Logic**
   - Logic only used in one use case → Keep in use case
   - Workflow-specific logic → Keep in workflow

3. **Infrastructure Concerns**
   - HTTP calls → Use adapters
   - Database access → Use adapters
   - File operations → Use adapters

## Example: CertificadoAPIService

Based on your architecture, here's what `CertificadoAPIService` should do:

### ❌ What it should NOT do:
```python
# This is adapter territory - just making API calls
class CertificadoAPIService:
    def register_supplier(self, supplier):
        return self.api_requester.register_supplier(supplier)
```

### ✅ What it SHOULD do:
```python
class CertificadoAPIService:
    """
    Service for managing document registration in Certificado API.
    
    This service encapsulates the business logic for registering documents,
    including checking if suppliers exist, handling document types, and
    managing the complete registration process.
    """
    
    def __init__(self, api_requester: CertificadoAPIRequester):
        self.api_requester = api_requester
    
    def register_document(
        self, 
        document: DocumentExtracted
    ) -> DocumentResponse:
        """
        Register a document with business logic.
        
        This method:
        1. Checks if supplier exists (business rule)
        2. Creates supplier if needed (business rule)
        3. Gets/validates document type (business rule)
        4. Registers document (business operation)
        
        This is business logic, not just an API call!
        """
        # Business logic: Check if supplier exists
        supplier = self._get_or_create_supplier(document.supplier.cnpj)
        
        # Business logic: Get document type
        document_type = self._get_document_type(document.document_type)
        
        # Business operation: Register document
        return self.api_requester.register_document(
            DocumentCreate(
                supplier_id=supplier.id,
                document_type_id=document_type.id,
                identifier=document.identifier,
                expiration_date=document.expiration_date
            )
        )
    
    def _get_or_create_supplier(self, cnpj: str) -> SupplierResponse:
        """Business logic: Get existing or create new supplier."""
        try:
            return self.api_requester.get_supplier(
                SupplierFilter(cnpj=cnpj)
            )[0]
        except NotFoundError:
            return self.api_requester.register_supplier(
                SupplierCreate(cnpj=cnpj)
            )
    
    def _get_document_type(self, name: str) -> DocumentTypeResponse:
        """Business logic: Get document type."""
        return self.api_requester.get_document_type(
            DocumentTypeFilter(name=name)
        )[0]
```

## Service Structure in Your Architecture

```
application/
├── services/              ← Services (reusable business logic)
│   ├── api/
│   │   └── certificado_api_service.py
│   ├── validation/
│   │   └── document_validation_service.py
│   └── transformation/
│       └── document_transformation_service.py
│
├── use_cases/            ← Use cases (orchestrate workflows/services)
│   └── download_certificates.py
│
└── workflow/             ← Workflows (complete processes)
    └── workflow.py
```

## Real-World Examples

### Example 1: Document Registration Service
```python
class DocumentRegistrationService:
    """
    Service for registering documents with business rules.
    
    This service handles the complete business process of registering
    a document, including validation, supplier management, and registration.
    """
    
    def register_document(self, document: DocumentExtracted):
        # 1. Validate document (business rule)
        self._validate_document(document)
        
        # 2. Get or create supplier (business logic)
        supplier = self._ensure_supplier_exists(document.supplier)
        
        # 3. Register document (business operation)
        return self.api_requester.register_document(...)
```

### Example 2: Document Validation Service
```python
class DocumentValidationService:
    """
    Service for validating documents according to business rules.
    """
    
    def validate(self, document: DocumentExtracted) -> ValidationResult:
        """Validate document against business rules."""
        errors = []
        
        # Business rule: CNPJ must be valid
        if not self._is_valid_cnpj(document.supplier.cnpj):
            errors.append("Invalid CNPJ")
        
        # Business rule: Expiration date must be in future
        if document.expiration_date < date.today():
            errors.append("Document expired")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

### Example 3: Certificate Processing Service
```python
class CertificateProcessingService:
    """
    Service for processing certificates with business logic.
    """
    
    def process_certificate(
        self, 
        certificate: CertificateToDownload
    ) -> ProcessedCertificate:
        """Process certificate with business rules."""
        # Business logic: Determine processing strategy
        strategy = self._determine_strategy(certificate)
        
        # Business logic: Apply processing rules
        processed = strategy.process(certificate)
        
        # Business logic: Validate result
        self._validate_processed(processed)
        
        return processed
```

## Best Practices

### ✅ DO:
1. **Keep services focused** - One service, one responsibility
2. **Use domain language** - Services should speak business language
3. **Make them reusable** - Services should be usable by multiple use cases
4. **Keep business logic** - Services contain business rules, not technical details
5. **Depend on adapters** - Services use adapters, not the other way around

### ❌ DON'T:
1. **Don't mix concerns** - Services shouldn't handle infrastructure
2. **Don't duplicate use case logic** - If only one use case uses it, keep it there
3. **Don't create thin wrappers** - Services should add value, not just wrap adapters
4. **Don't depend on use cases** - Services are used by use cases, not vice versa

## Summary

**Services in hexagonal architecture should:**

1. **Encapsulate reusable business logic**
2. **Orchestrate multiple adapters for business operations**
3. **Implement domain operations and business rules**
4. **Be independent and reusable across use cases/workflows**

**Services are NOT:**
- Simple adapter wrappers
- Use case-specific logic
- Infrastructure code
- Thin facades over adapters

The key is: **Services add business value** by encapsulating meaningful business operations that can be reused across your application.

