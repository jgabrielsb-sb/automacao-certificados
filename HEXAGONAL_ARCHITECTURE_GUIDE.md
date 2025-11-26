# Hexagonal Architecture: Where to Create Objects

## Overview

In hexagonal architecture (ports and adapters), object creation should follow a clear hierarchy to maintain separation of concerns and testability.

## Current Structure Analysis

Your current architecture has:
- ✅ **Ports (Interfaces)** - `core/interfaces/`
- ✅ **Adapters** - `adapters/`
- ✅ **Application Layer** - `application/`
- ✅ **Factories** - `application/workflow/factories/`
- ⚠️ **Composition Root** - Currently in `main.py` (should be separated)

## Where to Create Objects

### 1. **Composition Root** (Recommended Location)

Create a dedicated module for object composition. This is where all dependencies are wired together.

**Location:** `src/automacao_certificados/composition/` or `src/automacao_certificados/di/`

**Purpose:**
- Create all infrastructure objects (HTTP clients, webdriver, etc.)
- Wire adapters to ports
- Compose use cases with their dependencies
- Create application-level services

**Example Structure:**
```
composition/
  __init__.py
  container.py          # Main DI container
  infrastructure.py      # Infrastructure setup (webdriver, HTTP clients)
  adapters.py           # Adapter creation
  use_cases.py          # Use case composition
```

### 2. **Factories** (Keep Current Pattern)

**Location:** `application/workflow/factories/`

**Purpose:**
- Create complex workflows with their dependencies
- Encapsulate workflow-specific object creation
- ✅ **You're already doing this correctly!**

**What factories should do:**
- Create workflows with all their dependencies
- Use infrastructure objects passed in or created internally
- Return fully configured workflows

### 3. **Infrastructure Providers** (New - Recommended)

**Location:** `infra/providers/` or `composition/infrastructure.py`

**Purpose:**
- Create and manage infrastructure objects
- HTTP clients
- WebDriver instances
- External service clients (Groq, etc.)

**Why separate:**
- Infrastructure objects are often singletons or need special lifecycle management
- Easier to mock in tests
- Clear separation of infrastructure concerns

### 4. **Main Entry Point** (Keep Simple)

**Location:** `main.py`

**Purpose:**
- Only call the composition root
- Start the application
- Handle application lifecycle (scheduling, etc.)

**Should NOT:**
- ❌ Create adapters directly
- ❌ Wire dependencies
- ❌ Know about infrastructure details

## Recommended Structure

```
src/automacao_certificados/
├── composition/              # NEW: Composition Root
│   ├── __init__.py
│   ├── container.py         # Main DI container
│   ├── infrastructure.py    # Infrastructure providers
│   └── use_cases.py         # Use case factory
│
├── main.py                  # Entry point (simplified)
│
├── selenium_automations/
│   ├── application/
│   │   └── workflow/
│   │       └── factories/   # Keep: Workflow factories
│   │
│   ├── adapters/            # Adapters (no object creation)
│   ├── core/                # Ports/interfaces (no object creation)
│   └── infra/               # Infrastructure (providers only)
│
└── config/                  # Configuration
```

## Implementation Example

### 1. Infrastructure Provider

```python
# composition/infrastructure.py

from automacao_certificados.selenium_automations.adapters.http import HttpxClient
from automacao_certificados.selenium_automations.infra.webdriver import get_global_webdriver
from automacao_certificados.config import settings
from groq import Groq

class InfrastructureProvider:
    """Provides infrastructure objects (singletons or shared instances)."""
    
    def __init__(self):
        self._http_client = None
        self._webdriver = None
        self._groq_client = None
    
    @property
    def http_client(self):
        """Get or create HTTP client (singleton)."""
        if self._http_client is None:
            self._http_client = HttpxClient()
        return self._http_client
    
    @property
    def webdriver(self):
        """Get or create webdriver (singleton)."""
        if self._webdriver is None:
            self._webdriver = get_global_webdriver()
        return self._webdriver
    
    @property
    def groq_client(self):
        """Get or create Groq client (singleton)."""
        if self._groq_client is None:
            self._groq_client = Groq(api_key=settings.groq_api_key)
        return self._groq_client
```

### 2. Adapter Factory

```python
# composition/adapters.py

from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.infra.api_requester import (
    PPEAPIRequester,
    CertificadoAPIRequester,
    ReceitaAPIRequester,
)
from automacao_certificados.config import settings
from .infrastructure import InfrastructureProvider

class AdapterFactory:
    """Creates adapter instances."""
    
    def __init__(self, infrastructure: InfrastructureProvider):
        self.infrastructure = infrastructure
    
    def create_ppe_api_requester(self) -> PPEAPIRequester:
        return PPEAPIRequester(
            http=self.infrastructure.http_client,
            api_key=settings.ppe_api_key
        )
    
    def create_certificado_api_requester(self) -> CertificadoAPIRequester:
        return CertificadoAPIRequester(
            base_url=settings.base_certificado_api_url,
            http=self.infrastructure.http_client
        )
    
    def create_receita_api_requester(self) -> ReceitaAPIRequester:
        return ReceitaAPIRequester(
            http=self.infrastructure.http_client
        )
    
    def create_receita_api_municipio_getter(self) -> ReceitaAPIMunicipioGetter:
        return ReceitaAPIMunicipioGetter(
            api_requester=self.create_receita_api_requester()
        )
```

### 3. Use Case Factory

```python
# composition/use_cases.py

from automacao_certificados.selenium_automations.application.use_cases.download_certificates import DownloadCertificatesUseCase
from automacao_certificados.selenium_automations.application.workflow.workflow_selector import WorkflowSelector
from .adapters import AdapterFactory

class UseCaseFactory:
    """Creates use case instances."""
    
    def __init__(self, adapter_factory: AdapterFactory):
        self.adapter_factory = adapter_factory
    
    def create_download_certificates_use_case(self) -> DownloadCertificatesUseCase:
        return DownloadCertificatesUseCase(
            ppe_api_requester=self.adapter_factory.create_ppe_api_requester(),
            workflow_selector=WorkflowSelector(
                municipio_api_requester=self.adapter_factory.create_receita_api_municipio_getter()
            )
        )
```

### 4. Main Container

```python
# composition/container.py

from .infrastructure import InfrastructureProvider
from .adapters import AdapterFactory
from .use_cases import UseCaseFactory

class Container:
    """Main dependency injection container."""
    
    def __init__(self):
        self.infrastructure = InfrastructureProvider()
        self.adapter_factory = AdapterFactory(self.infrastructure)
        self.use_case_factory = UseCaseFactory(self.adapter_factory)
    
    def get_download_certificates_use_case(self):
        return self.use_case_factory.create_download_certificates_use_case()
```

### 5. Simplified Main

```python
# main.py

from automacao_certificados.composition.container import Container
from automacao_certificados.selenium_automations.adapters.report_generator import DownloadCertificatesReportGenerator
from automacao_certificados.config import settings

from datetime import datetime
from pathlib import Path
import schedule
import time

# Create container (composition root)
container = Container()

# Get use case from container
use_case = container.get_download_certificates_use_case()

# Create report generator
generator = DownloadCertificatesReportGenerator(
    save_path=Path("data/certificates_report"),
)

def run():
    certificates = use_case.run()
    file_path = generator.run(certificates, date=datetime.now())
    print(f"Report generated at {file_path}")

schedule.every().day.at(settings.run_cron_time).do(run)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
```

## Factory Pattern for Workflows

Your workflow factories are correct! They should:
- ✅ Create workflows with dependencies
- ✅ Use infrastructure objects (can receive them as parameters)
- ✅ Encapsulate workflow-specific creation logic

**Optional Improvement:** Pass infrastructure to factories instead of creating inside:

```python
class FGTSWorkflowFactory(WorkflowFactory):
    def __init__(self, infrastructure: InfrastructureProvider):
        self.infrastructure = infrastructure
    
    def get_workflow(self) -> Workflow:
        driver = self.infrastructure.webdriver
        http_client = self.infrastructure.http_client
        # ... rest of creation
```

## Benefits of This Structure

1. **Single Responsibility** - Each module has one clear purpose
2. **Testability** - Easy to mock infrastructure and adapters
3. **Maintainability** - All object creation in one place
4. **Flexibility** - Easy to swap implementations
5. **Clear Dependencies** - Dependency graph is explicit

## Rules of Thumb

### ✅ DO:
- Create objects in the composition root
- Use factories for complex objects (workflows)
- Pass dependencies through constructors
- Keep main.py simple

### ❌ DON'T:
- Create adapters in use cases
- Create infrastructure in adapters
- Create objects in core/ports
- Mix business logic with object creation

## Testing Benefits

With this structure, testing becomes easier:

```python
# In tests, you can create a test container
class TestContainer(Container):
    def __init__(self):
        # Override with test doubles
        self.infrastructure = MockInfrastructureProvider()
        # ...
```

This keeps your architecture clean and maintainable!

