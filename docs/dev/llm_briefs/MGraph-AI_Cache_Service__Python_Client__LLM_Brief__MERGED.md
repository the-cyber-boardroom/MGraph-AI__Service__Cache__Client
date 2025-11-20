# MGraph-AI Cache Service - Python Client LLM Brief

**Document Version:** 2.0 (Merged)  
**Cache Service Version:** v0.6.0+  
**Python Client Version:** v0.10.1  
**Last Updated:** 2025-01-20

---

## Overview

The MGraph-AI Cache Service is a production-ready, serverless caching system designed for intelligent content-addressable storage with multiple caching strategies. It's built for AWS Lambda deployment with S3 backing but supports multiple storage backends (S3, SQLite, Local Disk, In-Memory, ZIP) through a Memory-FS abstraction layer.

### Key Features

- **Multiple Storage Strategies**: Direct, temporal, temporal_latest, temporal_versioned, and key-based storage
- **Content-Addressable Storage**: Automatic deduplication via SHA-256 hashing
- **Hierarchical Data Organization**: Attach child data files to cache entries
- **Custom File Naming**: Control storage paths and file identifiers (v0.10.1+)
- **Selective JSON Hashing**: Hash specific fields within JSON objects (v0.10.1+)
- **Namespace Isolation**: Multi-tenant support with isolated namespaces
- **Binary, JSON, and String Support**: Store any data type
- **ZIP Archive Management**: Batch operations on compressed content
- **Ephemeral Testing**: In-memory mode for local development
- **Type Safety**: Built with OSBot-Utils Type_Safe framework for runtime validation

---

## Installation

```bash
pip install mgraph_ai_service_cache_client
```

**Dependencies:**
- `osbot_utils` - Type-safe utilities and Type_Safe framework
- `osbot_fast_api` - FastAPI client infrastructure
- `requests` - HTTP client library

---

## Quick Start

### Basic Configuration

The client requires three environment variables:

```bash
# API Key Authentication
export AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME="X-API-Key"
export AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE="your-api-key-here"

# Service Endpoint
export URL__TARGET_SERVER__CACHE_SERVICE="https://cache.dev.mgraph.ai"
```

### Initialize the Client

```python
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config
from osbot_utils.utils.Env import get_env

# Option 1: Direct configuration
config = Service__Fast_API__Client__Config(
    base_url       = "https://cache.dev.mgraph.ai",
    api_key        = "your-api-key-here",
    api_key_header = "X-API-Key"
)
client = Service__Fast_API__Client(config=config)

# Option 2: From environment variables
base_url  = get_env('URL__TARGET_SERVER__CACHE_SERVICE')
key_name  = get_env('AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME')
key_value = get_env('AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE')

config = Service__Fast_API__Client__Config(
    base_url       = base_url,
    api_key        = key_value,
    api_key_header = key_name
)
client = Service__Fast_API__Client(config=config)

# Verify connection
health = client.info().health()
print(health)  # {'status': 'ok'}
```

---

## Real-World Examples

### Example 1: Web Content Caching System (Production Pattern)

This example shows a real-world pattern from a web proxy service that caches URL transformations.

```python
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy import Enum__Cache__Store__Strategy
from osbot_utils.helpers.cache.Cache__Hash__Generator import Cache__Hash__Generator
from urllib.parse import urlparse
import re

class WebContentCache:
    """Real-world web content caching with hierarchical organization"""
    
    def __init__(self, base_url: str, api_key: str, namespace: str = "web-cache"):
        config = Service__Fast_API__Client__Config(
            base_url       = base_url,
            api_key        = api_key,
            api_key_header = "X-API-Key"
        )
        self.client = Service__Fast_API__Client(config=config)
        self.namespace = namespace
    
    def url_to_cache_key(self, target_url: str) -> str:
        """Convert URL to hierarchical cache key"""
        parsed = urlparse(target_url)
        domain = parsed.netloc
        path   = parsed.path.strip('/')
        
        if not path:
            path = "index"
        
        # Sanitize path for use in cache key
        path = re.sub(r'[^a-zA-Z0-9\-_/]', '-', path)
        path = re.sub(r'-+', '-', path)
        
        # Create hierarchical structure: sites/domain/pages/path
        cache_key = f"sites/{domain}/pages/{path}"
        return cache_key
    
    def get_or_create_page_entry(self, target_url: str) -> dict:
        """Get existing page entry or create new one"""
        cache_key  = self.url_to_cache_key(target_url)
        cache_hash = Cache__Hash__Generator().from_string(cache_key)
        
        # Try to retrieve existing page entry
        try:
            result = self.client.retrieve().retrieve__hash__cache_hash(
                cache_hash = cache_hash,
                namespace  = self.namespace
            )
            return result.get('metadata', {})
        except:
            # Create new page entry
            parsed     = urlparse(target_url)
            page_entry = {
                "url"          : target_url,
                "cache_key"    : cache_key,
                "domain"       : parsed.netloc,
                "path"         : parsed.path,
                "access_count" : 1
            }
            
            # Store with selective JSON hashing (only hash by cache_key)
            result = self.client.store().store__json__cache_key(
                namespace       = self.namespace,
                strategy        = Enum__Cache__Store__Strategy.KEY_BASED,
                cache_key       = cache_key,
                body            = page_entry,
                file_id         = "page-entry",
                json_field_path = "cache_key"  # Only hash this field
            )
            
            return {
                "cache_id"   : result['cache_id'],
                "cache_hash" : cache_hash,
                **page_entry
            }
    
    def store_html_transformation(self, target_url: str, html_content: str, metadata: dict) -> str:
        """Store HTML transformation as child data"""
        page_entry = self.get_or_create_page_entry(target_url)
        cache_id   = page_entry['cache_id']
        
        # Store HTML content as child data
        self.client.data_store().data__store_string__with__id_and_key(
            cache_id     = cache_id,
            namespace    = self.namespace,
            data_key     = "transformations/html",
            data_file_id = "content",
            body         = html_content
        )
        
        # Store metadata separately
        self.client.data_store().data__store_json__with__id_and_key(
            cache_id     = cache_id,
            namespace    = self.namespace,
            data_key     = "transformations/html/metadata",
            data_file_id = "info",
            body         = metadata
        )
        
        return cache_id
    
    def get_cached_html(self, target_url: str) -> str:
        """Retrieve cached HTML transformation"""
        page_entry = self.get_or_create_page_entry(target_url)
        cache_id   = page_entry['cache_id']
        
        # Retrieve HTML content
        html = self.client.data().retrieve().data__string__with__id_and_key(
            cache_id     = cache_id,
            namespace    = self.namespace,
            data_key     = "transformations/html",
            data_file_id = "content"
        )
        
        return html

# Usage
cache = WebContentCache(
    base_url  = "https://cache.dev.mgraph.ai",
    api_key   = "your-api-key",
    namespace = "web-proxy"
)

# Store transformation
cache_id = cache.store_html_transformation(
    target_url   = "https://example.com/docs/api",
    html_content = "<html><body>API Docs</body></html>",
    metadata     = {"status_code": 200, "content_type": "text/html"}
)

# Retrieve cached content
html = cache.get_cached_html("https://example.com/docs/api")
print(html)

# Hierarchical structure created:
# namespace/data/key-based/sites/example.com/pages/docs-api/page-entry.json
# namespace/data/{cache_id}/data/transformations/html/content.txt
# namespace/data/{cache_id}/data/transformations/html/metadata/info.json
```

### Example 2: Configuration Management with Version History

```python
class ConfigManager:
    """Manage application configuration with full version history"""
    
    def __init__(self, client: Service__Fast_API__Client, namespace: str = "configs"):
        self.client = client
        self.namespace = namespace
    
    def store_config(self, app_name: str, config_data: dict) -> str:
        """Store configuration with automatic versioning"""
        result = self.client.store().store__json__cache_key(
            namespace  = self.namespace,
            strategy   = Enum__Cache__Store__Strategy.TEMPORAL_VERSIONED,
            cache_key  = f"apps/{app_name}/settings",
            body       = config_data,
            file_id    = f"{app_name}-config"
        )
        return result['cache_id']
    
    def get_latest_config(self, app_name: str) -> dict:
        """Get current configuration"""
        # With TEMPORAL_VERSIONED, all versions are stored
        # In practice, you'd maintain a "latest" pointer or use timestamps
        cache_key = f"apps/{app_name}/settings"
        # Implementation would track latest version
        pass

# Usage
config_mgr = ConfigManager(client)

# Store version 1
v1_id = config_mgr.store_config("api-server", {
    "port": 8000,
    "debug": True,
    "features": ["auth", "cache"]
})

# Store version 2 (new entry created)
v2_id = config_mgr.store_config("api-server", {
    "port": 8000,
    "debug": False,  # Changed
    "features": ["auth", "cache", "monitoring"]  # Added
})

# Both versions are preserved and accessible
```

### Example 3: Simple Cache-Aside Pattern

```python
def get_user_data(user_id: str) -> dict:
    """Simple cache-aside pattern"""
    cache_id = f"user-{user_id}"
    
    # Try cache first
    try:
        user_data = client.retrieve().retrieve__cache_id__json(
            cache_id  = cache_id,
            namespace = "users"
        )
        return user_data
    except:
        # Cache miss - fetch from database
        user_data = database.get_user(user_id)
        
        # Store in cache
        client.store().store__json(
            strategy  = Enum__Cache__Store__Strategy.DIRECT,
            namespace = "users",
            body      = user_data
        )
        
        return user_data
```

### Example 4: Deduplication with Content Hashing

```python
def store_document(document_content: str) -> dict:
    """Store document with automatic deduplication"""
    result = client.store().store__string(
        strategy  = Enum__Cache__Store__Strategy.DIRECT,
        namespace = "documents",
        body      = document_content
    )
    
    # Same content = same hash
    # If this content was already stored, it reuses the same entry
    return {
        "cache_id"   : result['cache_id'],
        "cache_hash" : result['cache_hash'],
        "is_new"     : result.get('created', True)
    }

# Store identical documents
doc1 = store_document("Important document content")
doc2 = store_document("Important document content")  # Same content

# Both return same cache_hash - only stored once
assert doc1['cache_hash'] == doc2['cache_hash']
```

### Example 5: Time-Series Event Logging

```python
def log_event(event_type: str, event_data: dict):
    """Store time-series events"""
    client.store().store__json(
        strategy  = Enum__Cache__Store__Strategy.TEMPORAL,
        namespace = "events",
        body      = {
            "event_type" : event_type,
            "timestamp"  : time.time(),
            "data"       : event_data
        }
    )

# Each call creates a new timestamped entry
log_event("user_login", {"user_id": "123", "ip": "192.168.1.1"})
log_event("user_login", {"user_id": "456", "ip": "192.168.1.2"})

# Structure: namespace/data/temporal/2024/01/20/15/30/{cache_id}.json
```

### Example 6: Selective Field Hashing for User Deduplication

```python
def store_user_profile(user_data: dict) -> str:
    """Store user profile, deduplicate by email only"""
    result = client.store().store__json__cache_key(
        namespace       = "users",
        strategy        = Enum__Cache__Store__Strategy.DIRECT,
        cache_key       = "profiles",
        body            = {
            "user_id"    : user_data['id'],
            "email"      : user_data['email'],
            "name"       : user_data['name'],
            "created_at" : user_data['created_at'],
            "last_login" : user_data['last_login']
        },
        json_field_path = "email"  # Only hash email for deduplication
    )
    return result['cache_id']

# Users with same email get same cache_hash
# Even if other fields (name, last_login) differ
user1 = store_user_profile({
    "id": "123",
    "email": "john@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01",
    "last_login": "2024-01-20"
})

user2 = store_user_profile({
    "id": "123",
    "email": "john@example.com",
    "name": "John D.",  # Different name
    "created_at": "2024-01-01",
    "last_login": "2024-01-21"  # Different login time
})

# Same cache_hash because email matches
```

---

## Core Concepts

### Content-Addressable Storage

Unlike traditional key-value caches, the service uses **content hashing** to identify cached items. This means:

- **Deduplication**: Identical content automatically shares the same storage
- **Integrity**: Content hash proves data hasn't been corrupted
- **Versioning**: Same content at different times maintains history
- **Efficient Updates**: Only changed content creates new entries

```python
# Same content = same hash, automatic deduplication
result1 = client.store().store__json(
    strategy="temporal_latest",
    namespace="configs",
    body={"timeout": 30, "retries": 3}
)

result2 = client.store().store__json(
    strategy="temporal_latest",
    namespace="configs",
    body={"timeout": 30, "retries": 3}  # Identical content
)

# result1['cache_hash'] == result2['cache_hash']
# Only one copy stored, both requests reference same data
```

### Hierarchical Data Organization

The service supports **child data files** - lightweight data stored under cache entries without creating separate cache entries. This enables organizing related data hierarchically:

```python
# Store main document
doc_result = client.store().store__json(
    strategy="temporal_latest",
    namespace="documents",
    body=main_document
)

doc_id = doc_result["cache_id"]

# Attach analysis results as child data
client.data_store().data__store_json__with__id_and_key(
    cache_id=doc_id,
    namespace="documents",
    data_key="analysis/sentiment",
    data_file_id="v1",
    body={"score": 0.85, "sentiment": "positive"}
)

# Hierarchical structure:
# document (main cache entry)
# └── data/
#     └── analysis/
#         └── sentiment/
#             └── v1.json
```

### Namespace Isolation

Namespaces provide complete data isolation - perfect for multi-tenant applications or separating environments:

```python
# Production data
client.store().store__json(
    strategy="temporal_latest",
    namespace="production",
    body=prod_data
)

# Development data (completely isolated)
client.store().store__json(
    strategy="temporal_latest",
    namespace="development",
    body=dev_data
)

# Each namespace has separate:
# - Storage paths
# - TTL settings
# - Access patterns
# - No cross-namespace retrieval possible
```

### Why Use This Cache Service?

**Intelligent Storage**: Content-based addressing means automatic deduplication and integrity verification

**Flexible Strategies**: Choose the right storage pattern for your use case - simple caching, versioning, or time-series

**Hierarchical Organization**: Organize related data with child files instead of flat key-value pairs

**Production Ready**: Designed for AWS Lambda with S3, but supports multiple backends for development and testing

**Type Safety**: Built with OSBot-Utils Type_Safe framework (see next section) for runtime validation and security

**Multiple Data Types**: Native support for JSON (structured), String (text), and Binary (files) data

**Immutable by Design**: Cache entries are immutable - modifications create new versions maintaining data provenance

---

## Why Type_Safe? The Power of Runtime Type Validation

This client library is built using **OSBot-Utils Type_Safe**, a runtime type checking framework that provides security, reliability, and developer productivity benefits that go far beyond Python's standard type hints.

### The Problem with Standard Python Types

Python's built-in type hints are **ignored at runtime** - they're just documentation:

```python
# Standard Python - type hints are suggestions only
def process_user(user_id: str, age: int) -> dict:
    return {"id": user_id, "age": age}

# These ALL succeed at runtime - no validation!
process_user(123, "not-a-number")           # Wrong types
process_user("'; DROP TABLE users; --", -5)  # SQL injection + negative age
process_user("A" * 1000000, 999999)         # Memory attack + unrealistic age
```

**Result**: Type hints don't prevent bugs, security vulnerabilities, or data corruption.

### Type_Safe's Solution: Continuous Runtime Validation

Type_Safe validates **every operation** - not just at boundaries, but continuously throughout your program:

```python
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.numerical.safe_int.Safe_UInt import Safe_UInt

# Type_Safe validates on assignment
class CacheConfig(Type_Safe):
    namespace : Safe_Str__Id      # Only alphanumeric + underscore + hyphen
    timeout   : Safe_UInt         # Only positive integers

config = CacheConfig()
config.namespace = "production"   # ✓ Valid - unchanged
config.namespace = "prod@ction"   # ✓ Sanitized - becomes "prod_ction" (@ replaced with _)
config.namespace = "prod!@#uct"   # ✓ Sanitized - becomes "prod___uct" (all invalid chars replaced)
config.timeout = 30               # ✓ Valid
config.timeout = -5               # ✗ ValueError - negative not allowed
config.timeout = "invalid"        # ✗ TypeError - must be int
```

### Security Benefits

Type_Safe's domain-specific types prevent entire categories of security vulnerabilities through **automatic sanitization** and **validation**:

```python
# ✗ DANGEROUS - Raw primitives enable attacks
class User(Type_Safe):
    username : str     # Can contain SQL injection, XSS
    email    : str     # No validation
    age      : int     # Can be negative, overflow
    balance  : float   # Floating point errors in money

# ✓ SECURE - Domain types prevent attacks
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Username import Safe_Str__Username
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Email import Safe_Str__Email
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Money import Safe_Float__Money

class User(Type_Safe):
    username : Safe_Str__Username   # Sanitized, 32 char limit
    email    : Safe_Str__Email      # Email validation (strict)
    age      : Safe_UInt            # 0-65535 range enforced  
    balance  : Safe_Float__Money    # Exact decimal arithmetic

# Automatic SANITIZATION for most Safe_Str types
user = User()
user.username = "admin'; DROP TABLE users; --"  # ✓ Sanitized to "admin__DROP_TABLE_users___"
user.username = "user@name!123"                  # ✓ Sanitized to "user_name_123"

# STRICT VALIDATION for types that need it (like emails)
user.email = "not-an-email"                      # ✗ ValueError - must contain @
user.email = "user@example.com"                  # ✓ Valid email format

# Numeric bounds validation
user.age = -5                                    # ✗ ValueError - negative not allowed
user.age = 25                                    # ✓ Valid
user.balance = "999999999999.99"                # ✓ Converts safely with exact precision
```

**Two modes of protection:**

1. **Sanitization** (default for most Safe_Str types): Invalid characters are replaced, making the string safe
   - `Safe_Str__Username`: Removes/replaces special characters
   - `Safe_Str__Id`: Replaces invalid chars with underscores
   - `Safe_Str__File__Path`: Sanitizes path traversal attempts

2. **Strict Validation** (for types where sanitization doesn't make sense): Raises ValueError if input is invalid
   - `Safe_Str__Email`: Must contain @ and valid format
   - `Safe_Str__Url`: Must be valid URL format
   - `Safe_Str__IP_Address`: Must be valid IP address

### Real-World Impact: Preventing Common Vulnerabilities

#### Path Traversal Prevention
```python
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path

class FileConfig(Type_Safe):
    file_path : Safe_Str__File__Path

config = FileConfig()
config.file_path = "../../../etc/passwd"     # ✓ Sanitized - path traversal removed
config.file_path = "data/files/report.pdf"   # ✓ Valid path
```

#### Injection Attack Prevention
```python
# SQL Injection
username = Safe_Str__Username()
username = "admin'; DROP TABLE users; --"
# Result: "admin__DROP_TABLE_users___" - SQL injection neutralized

# XSS Prevention
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Html_Safe import Safe_Str__Html_Safe

user_input = Safe_Str__Html_Safe()
user_input = "<script>alert('XSS')</script>"
# Result: Sanitized string safe for HTML rendering
```

#### Range and Overflow Prevention
```python
from osbot_utils.type_safe.primitives.domains.numerical.safe_int.Safe_Int import Safe_Int

# Prevent integer overflow
age = Safe_UInt()
age = 999999999999999999  # ✗ ValueError - exceeds safe range

# Prevent negative values where inappropriate
quantity = Safe_UInt()
quantity = -10  # ✗ ValueError - negative not allowed
```

### Type_Safe in the Cache Client

The cache client uses Type_Safe throughout:

```python
# All these parameters are validated at runtime
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy import Enum__Cache__Store__Strategy

result = client.store().store__json(
    strategy=Enum__Cache__Store__Strategy.TEMPORAL_LATEST,  # Enum validation
    namespace="my-app",                                       # Safe_Str__Id validation
    body={"data": "value"}                                   # JSON validation
)

# Invalid inputs are caught immediately:
result = client.store().store__json(
    strategy="invalid_strategy",    # ✗ ValueError - not a valid enum
    namespace="my@invalid!name",    # ✓ Sanitized to "my_invalid_name"
    body=None                       # ✗ ValueError - body cannot be None
)
```

### Performance Considerations

Type_Safe validation adds minimal overhead:
- **Validation Time**: Microseconds per operation
- **Memory**: Negligible - types are reused
- **Production Ready**: Used in high-performance production systems

The security and reliability benefits far outweigh the minimal performance cost.

---

## Storage Strategies

The service supports five storage strategies for different use cases:

### 1. **DIRECT** - Immutable Single Version

Simple hash-based storage.

```python
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy import Enum__Cache__Store__Strategy

result = client.store().store__string(
    strategy="direct",
    namespace="my-app",
    body="Hello, World!"
)

cache_id = result['cache_id']  # e.g., "a1b2c3d4-e5f6-..."
```

**Best For:**
- Static content (documentation, assets)
- Immutable data records
- Simple key-value caching without versioning

**Structure:**
```
namespace/data/direct/a1/b2/a1b2c3d4-e5f6-7890.json
```

### 2. **TEMPORAL** - Time-Based Versions

Time-organized storage.

```python
result = client.store().store__json(
    strategy="temporal",
    namespace="analytics",
    body={"event": "user_login", "timestamp": 1234567890}
)
```

**Best For:**
- Event logs
- Time-series data
- Historical records
- Audit logs

**Structure:**
```
namespace/data/temporal/2024/01/20/15/30/cache_id.json
```

### 3. **TEMPORAL_LATEST** - Keep Most Recent

Latest pointer with history.

```python
result = client.store().store__json__cache_key(
    strategy="temporal_latest",
    namespace="config",
    cache_key="app/settings",
    body={"theme": "dark", "version": 2}
)
```

**Best For:**
- Application configuration
- Feature flags
- User preferences
- Frequently updated content where you need both history and quick access to latest

**Behavior:**
- Overwrites previous version
- Maintains single latest entry per cache_key

### 4. **TEMPORAL_VERSIONED** - Full Version History

Complete version history with rollback capability.

```python
# Store version 1
result_v1 = client.store().store__string__cache_key(
    strategy="temporal_versioned",
    namespace="docs",
    cache_key="api/readme",
    body="API Documentation v1"
)

# Store version 2 (creates new entry)
result_v2 = client.store().store__string__cache_key(
    strategy="temporal_versioned",
    namespace="docs",
    cache_key="api/readme",
    body="API Documentation v2"
)

# Both versions accessible by their cache_ids
```

**Best For:**
- Document versioning
- Audit trails
- Change tracking
- Critical data requiring complete audit trail

**Structure:**
```
namespace/data/temporal_versioned/api/readme/2024-01-20T15:30:00_cache_id.json
namespace/data/temporal_versioned/api/readme/2024-01-20T16:45:00_cache_id.json
```

### 5. **KEY_BASED** - Semantic Paths

Semantic path-based storage.

```python
result = client.store().store__binary__cache_key(
    strategy="key_based",
    namespace="assets",
    cache_key="images/logo",
    body=logo_bytes,
    file_id="company-logo-2024"  # ✨ NEW: Custom file identifier
)
```

**Best For:**
- Asset management
- Organized file structure
- Human-readable paths

**Structure:**
```
namespace/data/key-based/images/logo/company-logo-2024.bin
```

---

## Core Operations

### Store Data

#### String Data
```python
result = client.store().store__string(
    strategy="direct",
    namespace="content",
    body="This is text content"
)
```

#### JSON Data
```python
result = client.store().store__json(
    strategy="direct",
    namespace="data",
    body={"user_id": 123, "action": "login"}
)
```

#### Binary Data
```python
with open("image.png", "rb") as f:
    result = client.store().store__binary(
        strategy="direct",
        namespace="files",
        body=f.read()
    )
```

### Retrieve Data

#### By Cache ID
```python
# Retrieve string
text = client.retrieve().retrieve__cache_id__string(
    cache_id="a1b2c3d4-e5f6-7890",
    namespace="content"
)

# Retrieve JSON
data = client.retrieve().retrieve__cache_id__json(
    cache_id="a1b2c3d4-e5f6-7890",
    namespace="data"
)

# Retrieve binary
bytes_data = client.retrieve().retrieve__cache_id__binary(
    cache_id="a1b2c3d4-e5f6-7890",
    namespace="files"
)
```

#### By Content Hash
```python
# Retrieve by hash (any matching entry)
data = client.retrieve().retrieve__hash__cache_hash(
    cache_hash="abc123def456",
    namespace="data"
)
```

**Note**: Hash-based retrieval has known issues in some client versions (see Known Limitations). Use ID-based retrieval when possible.

---

## ✨ NEW: Advanced Features (v0.10.1+)

### Custom File Identifiers

Control the filename used in storage (available with `cache_key`):

```python
result = client.store().store__string__cache_key(
    strategy="key_based",
    namespace="reports",
    cache_key="monthly/sales",
    body="Sales Report Q4 2024",
    file_id="2024-Q4-sales-report"  # ✨ Custom filename
)

# Creates: reports/data/key-based/monthly/sales/2024-Q4-sales-report.json
```

**Benefits:**
- Human-readable file paths
- Consistent naming conventions
- Easier debugging and inspection
- Better organization in storage

**Works with all data types:**
```python
# JSON with custom file_id
client.store().store__json__cache_key(
    strategy="key_based",
    namespace="config",
    cache_key="app/settings",
    body={"theme": "dark"},
    file_id="app-settings-v2"
)

# Binary with custom file_id
client.store().store__binary__cache_key(
    strategy="key_based",
    namespace="assets",
    cache_key="images/hero",
    body=image_bytes,
    file_id="hero-image-2024"
)
```

### Selective JSON Field Hashing

Hash only specific fields within JSON objects to enable partial matching:

```python
result = client.store().store__json__cache_key(
    strategy="direct",
    namespace="users",
    cache_key="profiles",
    body={
        "user_id": 123,
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": "2024-01-20T10:30:00Z"
    },
    json_field_path="user_id,name"  # ✨ Only hash these fields
)

# Hash is computed from: {"user_id": 123, "name": "John Doe"}
# Allows finding users by ID+name even if email/timestamp changed
```

**Use Cases:**
- Deduplication by specific fields
- Version matching on key attributes
- Ignoring volatile fields (timestamps, counters)
- Content similarity detection

**Examples:**

```python
# Configuration versioning (ignore timestamps)
config = {
    "database": {"host": "localhost", "port": 5432},
    "cache": {"ttl": 3600, "size": 1000},
    "updated_at": "2024-01-20T10:30:00Z"
}

result = client.store().store__json__cache_key(
    strategy="temporal_latest",
    namespace="config",
    cache_key="db/primary",
    body=config,
    json_field_path="database,cache"  # Ignore updated_at
)

# User deduplication (by email only)
user = {
    "id": 123,
    "email": "user@example.com",
    "name": "John Doe",
    "last_login": "2024-01-20T10:30:00Z"
}

result = client.store().store__json__cache_key(
    strategy="direct",
    namespace="users",
    cache_key="active",
    body=user,
    json_field_path="email"  # Deduplicate by email only
)
```

### Namespace Management (v0.10.1+)

```python
# List all namespaces
namespaces = client.namespaces().list()
print(f"Found {len(namespaces)} namespaces: {namespaces}")

# Get namespace statistics
stats = client.namespace().stats("production")
# Returns: {
#     "namespace": "production",
#     "total_files": 1234,
#     "total_size_bytes": 45678901,
#     "file_types": {"json": 800, "bin": 400, "txt": 34}
# }

# Get all file hashes in namespace
hashes = client.namespace().file_hashes("production")

# Get all file IDs in namespace
file_ids = client.namespace().file_ids("production")
```

### Enhanced Admin Operations (v0.10.1+)

```python
# Recursive folder listing
folders = client.admin_storage().folders(
    path="production/data",
    recursive=True,
    return_full_path=True
)

# List all files recursively
all_files = client.admin_storage().files__in__path(
    path="production",
    recursive=True,
    return_full_path=True
)

# Get complete folder tree
tree = client.admin_storage().files__all__path("production/data/temporal")
```

### Three Client Execution Modes (v0.10.1+)

```python
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Requests import (
    Enum__Client__Mode
)

# Mode 1: REMOTE - Production mode (HTTP/HTTPS)
client = Service__Fast_API__Client(config=config)  # Default mode

# Mode 2: IN_MEMORY - FastAPI TestClient (no network)
from fastapi.testclient import TestClient
from mgraph_ai_service_cache.fast_api.Service__Fast_API import Cache_Service__Fast_API

service = Cache_Service__Fast_API().setup()
client = Service__Fast_API__Client(config=config)
client._requests._app = service.app
client._requests._mode = Enum__Client__Mode.IN_MEMORY

# Mode 3: LOCAL_SERVER - Local HTTP server for debugging
from osbot_utils.helpers.test.Local__Fast_API__Server import Local__Fast_API__Server

server = Local__Fast_API__Server(service.app).start()
client = Service__Fast_API__Client(
    config=Service__Fast_API__Client__Config(
        base_url=server.url,
        verify_ssl=False
    )
)
```

---

## Hierarchical Data Operations

### Store Child Data

```python
# Parent entry
doc = client.store().store__json(
    strategy="direct",
    namespace="documents",
    body={"title": "Report", "author": "Jane"}
)

# Child data - basic (auto-generated ID)
client.data_store().data__store_json(
    cache_id=doc['cache_id'],
    namespace="documents",
    body={"summary": "Executive summary..."}
)

# Child data - with custom ID
client.data_store().data__store_json__with__id(
    cache_id=doc['cache_id'],
    namespace="documents",
    data_file_id="metadata",
    body={"created": "2024-01-20", "version": 1}
)

# Child data - with key and ID (hierarchical)
client.data_store().data__store_string__with__id_and_key(
    cache_id=doc['cache_id'],
    namespace="documents",
    data_key="analysis/sentiment",
    data_file_id="v1",
    body="Positive sentiment detected"
)
```

### Retrieve Child Data

```python
# Retrieve by ID
metadata = client.data().retrieve().data__json__with__id(
    cache_id=doc['cache_id'],
    namespace="documents",
    data_file_id="metadata"
)

# Retrieve by key and ID
sentiment = client.data().retrieve().data__string__with__id(
    cache_id=doc['cache_id'],
    namespace="documents",
    data_key="analysis/sentiment",
    data_file_id="v1"
)
```

### Delete Child Data

```python
# Delete single child data file
client.data().delete().delete__data__file(
    cache_id=doc['cache_id'],
    namespace="documents",
    data_file_id="metadata"
)

# Delete all child data
client.data().delete().delete__all__data__files(
    cache_id=doc['cache_id'],
    namespace="documents"
)
```

---

## Metadata and References

### Retrieve Metadata

```python
# Get cache entry metadata
metadata = client.retrieve().retrieve__cache_id__metadata(
    cache_id=cache_id,
    namespace="documents"
)

# Returns:
# {
#     "cache_id": "...",
#     "cache_hash": "...",
#     "created_at": "2024-01-20T10:30:00Z",
#     "size_bytes": 1024,
#     "data_type": "json"
# }
```

### Retrieve Configuration

```python
# Get cache entry configuration
config = client.retrieve().retrieve__cache_id__config(
    cache_id=cache_id,
    namespace="documents"
)

# Returns:
# {
#     "strategy": "direct",
#     "namespace": "documents",
#     "cache_key": "...",
#     "file_id": "...",
#     "storage_path": "..."
# }
```

---

## Admin Operations

### Storage Administration

```python
# Get bucket name
bucket = client.admin_storage().bucket_name()

# Check if file exists
exists = client.admin_storage().file__exists(
    path="namespace/data/direct/a1/b2/file.json"
)

# Read file as JSON
data = client.admin_storage().file__json(
    path="namespace/data/direct/a1/b2/file.json"
)

# Read file as bytes
bytes_data = client.admin_storage().file__bytes(
    path="namespace/data/direct/a1/b2/file.bin"
)

# Delete file
client.admin_storage().file__delete(
    path="namespace/data/direct/a1/b2/file.json"
)
```

### File and Folder Listing

```python
# List files in path (non-recursive)
files = client.admin_storage().files__in__path(
    path="namespace/data/direct",
    return_full_path=False,
    recursive=False
)

# List files recursively
all_files = client.admin_storage().files__in__path(
    path="namespace/data",
    return_full_path=True,
    recursive=True
)

# Get complete folder tree
tree = client.admin_storage().files__all__path(
    path="namespace/data/temporal"
)

# List folders
folders = client.admin_storage().folders(
    path="namespace/data",
    return_full_path=False,
    recursive=False
)
```

---

## System Operations

### Health and Status

```python
# Health check
health = client.info().health()
# Returns: {'status': 'ok'}

# Detailed status
status = client.info().status()
# Returns: {
#     'status': 'operational',
#     'storage_mode': 's3',
#     'version': 'v0.6.0'
# }

# Get version info
versions = client.info().versions()
# Returns: {
#     'service': 'v0.6.0',
#     'api': 'v1.0',
#     'client_compatible': ['v0.10.1', 'v0.10.0']
# }
```

---

## Testing and Development

### Ephemeral Testing with In-Memory Mode

```python
from osbot_utils.utils.Env import set_env
from mgraph_ai_service_cache_client.helpers.Test__Helpers__Cache__Fast_API import (
    get__cache_service__fast_api_server
)

def test_cache_operations():
    # Setup ephemeral service
    set_env('CACHE__SERVICE__STORAGE_MODE', 'memory')
    test_objs = get__cache_service__fast_api_server()
    
    # Create client pointing to test server
    client = Service__Fast_API__Client(
        config=Service__Fast_API__Client__Config(
            base_url=test_objs.server_url,
            verify_ssl=False
        )
    )
    
    # Test normally
    result = client.store().store__string(
        strategy="direct",
        namespace="test",
        body="test data"
    )
    
    assert result['cache_id'] is not None
    
    # Retrieve
    data = client.retrieve().retrieve__cache_id__string(
        cache_id=result['cache_id'],
        namespace="test"
    )
    
    assert data == "test data"
```

### Testing with TestClient

```python
from fastapi.testclient import TestClient
from mgraph_ai_service_cache.fast_api.Service__Fast_API import Cache_Service__Fast_API

# Create service
service = Cache_Service__Fast_API().setup()

# Configure client for in-memory testing
config = Service__Fast_API__Client__Config()
client = Service__Fast_API__Client(config=config)
client._requests._app = service.app
client._requests._setup_mode()

# Now client uses TestClient instead of HTTP
result = client.store().store__json(
    strategy="direct",
    namespace="test",
    body={"test": "data"}
)
```

### Custom Request Handler

```python
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Requests import (
    Service__Fast_API__Client__Requests
)

# Direct request execution
requests = Service__Fast_API__Client__Requests(config=config)

result = requests.execute(
    method="POST",
    path="/default/temporal_latest/store/json",
    body={"key": "value"},
    headers={"Custom-Header": "value"}
)

print(f"Status: {result.status_code}")
print(f"Response: {result.json}")
```

---

## Best Practices

### 1. Reuse Client Instance

```python
# Create once, use many times
client = Service__Fast_API__Client(config=config)

# Reuse for multiple operations
for item in items:
    client.store().store__json(
        strategy="temporal_latest",
        namespace="items",
        body=item
    )
```

### 2. Choose the Right Strategy

```python
# Static content
client.store().store__json(
    strategy="direct",
    namespace="static",
    body=configuration_data
)

# Frequently updated, need latest
client.store().store__json(
    strategy="temporal_latest",
    namespace="current",
    body=data
)

# Need complete version history
client.store().store__json(
    strategy="temporal_versioned",
    namespace="audit",
    body=data
)

# Time-series data
client.store().store__json(
    strategy="temporal",
    namespace="events",
    body=event_data
)

# Organized file structure
client.store().store__binary__cache_key(
    strategy="key_based",
    namespace="assets",
    cache_key="images/logos",
    body=image_bytes,
    file_id="company-logo"
)
```

### 3. Use Type-Safe Enums

```python
# Good: Type-safe
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy import Enum__Cache__Store__Strategy

client.store().store__json(
    strategy=Enum__Cache__Store__Strategy.TEMPORAL_LATEST,
    namespace="data",
    body=data
)

# Avoid: String literals (not type-checked)
client.store().store__json(
    strategy="temporal_latest",  # Works but not type-checked
    namespace="data",
    body=data
)
```

### 4. Organize Child Data Logically

```python
# Good: Clear hierarchy
client.data_store().data__store_json__with__id_and_key(
    cache_id=cache_id,
    namespace="docs",
    data_key="analysis/sentiment",     # Clear path
    data_file_id="v1",                  # Version identifier
    body=sentiment_data
)

# Avoid: Flat structure
client.data_store().data__store_json__with__id(
    cache_id=cache_id,
    namespace="docs",
    data_file_id="sentiment-data",  # No organization
    body=sentiment_data
)
```

### 5. Handle Cache Misses Gracefully

```python
def get_cached_or_compute(client, cache_id, namespace, compute_fn):
    """Try cache first, compute if not found"""
    try:
        result = client.retrieve().retrieve__cache_id__json(
            cache_id=cache_id,
            namespace=namespace
        )
        return result
    except Exception as e:
        # Cache miss, compute and store
        computed = compute_fn()
        client.store().store__json(
            strategy="temporal_latest",
            namespace=namespace,
            body=computed
        )
        return computed
```

### 6. Use Namespaces for Isolation

```python
# Separate environments
result_dev = client.store().store__string(
    strategy="direct",
    namespace="dev",
    body="Development data"
)

result_prod = client.store().store__string(
    strategy="direct",
    namespace="prod",
    body="Production data"
)

# Multi-tenant isolation
for tenant in tenants:
    client.store().store__json(
        strategy="direct",
        namespace=f"tenant_{tenant.id}",
        body=tenant.data
    )
```

### 7. Leverage Content Hashing for Deduplication

```python
# Store once, retrieve many times
result1 = client.store().store__json(
    strategy="direct",
    namespace="data",
    body={"value": 42}
)

# Same content = same hash
result2 = client.store().store__json(
    strategy="direct",
    namespace="data",
    body={"value": 42}
)

# Only stored once!
assert result1['cache_hash'] == result2['cache_hash']

# Retrieve by hash from any entry
data = client.retrieve().retrieve__hash__cache_hash(
    cache_hash=result1['cache_hash'],
    namespace="data"
)
```

### 8. Use Custom File IDs for Readability

```python
# Instead of:
# assets/data/key-based/logos/a1b2c3d4-e5f6-7890.bin

# Use:
client.store().store__binary__cache_key(
    strategy="key_based",
    namespace="assets",
    cache_key="logos",
    body=logo_bytes,
    file_id="company-logo-primary"
)
# Creates: assets/data/key-based/logos/company-logo-primary.bin
```

### 9. Organize with Hierarchical Data

```python
# Parent: Project metadata
project = client.store().store__json(
    strategy="direct",
    namespace="projects",
    body={"name": "Project X", "status": "active"}
)

# Children: Related files
client.data_store().data__store_string__with__id_and_key(
    cache_id=project['cache_id'],
    namespace="projects",
    data_key="docs",
    data_file_id="readme",
    body="# Project X Documentation"
)

client.data_store().data__store_json__with__id_and_key(
    cache_id=project['cache_id'],
    namespace="projects",
    data_key="config",
    data_file_id="settings",
    body={"debug": True, "log_level": "INFO"}
)
```

---

## Performance Considerations

### Caching Strategy

1. **Content Deduplication**: Identical content stored once
2. **Hash-Based Retrieval**: Fast lookups by content hash
3. **S3 Backed**: Scalable, durable storage
4. **In-Memory Mode**: Zero latency for testing

### Optimization Tips

```python
# 1. Batch related operations
results = []
for item in items:
    result = client.store().store__json(
        strategy="direct",
        namespace="batch",
        body=item
    )
    results.append(result)

# 2. Use appropriate strategies
# DIRECT for static content (faster, simpler)
# TEMPORAL_VERSIONED only when history needed

# 3. Leverage hash-based deduplication
# Store: O(1) if content exists
# Retrieve by hash: Fast lookups

# 4. Use child data for related content
# Avoid multiple parent entries
# Group related files under single cache_id

# 5. Use selective JSON hashing
# Ignore volatile fields (timestamps)
# Deduplicate by key attributes only
```

---

## Testing and Development

The client supports three execution modes for different testing and development scenarios:

1. **REMOTE**: Production mode - HTTP/HTTPS calls to deployed service
2. **IN_MEMORY**: FastAPI TestClient - Same process, no network
3. **LOCAL_SERVER**: Fast_API_Server - Local HTTP server for debugging

### Mode 1: REMOTE (Production)

Standard mode for connecting to a deployed service:

```python
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config

# Configure for remote service
config = Service__Fast_API__Client__Config(
    base_url       = "https://cache.dev.mgraph.ai",
    api_key        = "your-api-key",
    api_key_header = "X-API-Key"
)

client = Service__Fast_API__Client(config=config)

# Client uses requests.Session for HTTP calls
# Mode: Enum__Client__Mode.REMOTE (default)
result = client.store().store__json(
    strategy  = "direct",
    namespace = "production",
    body      = {"key": "value"}
)
```

### Mode 2: IN_MEMORY (Fast Unit Testing)

Use FastAPI's TestClient for instant, in-memory testing without network calls:

```python
from fastapi.testclient import TestClient
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API import Cache_Service__Fast_API
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config

# Create cache service with in-memory storage
service = Cache_Service__Fast_API().setup()

# Create client and configure for in-memory mode
config = Service__Fast_API__Client__Config()
client = Service__Fast_API__Client(config=config)

# Inject the FastAPI app directly
client._requests._app = service.app
client._requests._setup_mode()

# Client now uses TestClient - no network, instant responses
# Mode: Enum__Client__Mode.IN_MEMORY
result = client.store().store__json(
    strategy  = "direct",
    namespace = "test",
    body      = {"test": "data"}
)

# Retrieve immediately
data = client.retrieve().retrieve__cache_id__json(
    cache_id  = result['cache_id'],
    namespace = "test"
)

assert data == {"test": "data"}
```

### Mode 3: LOCAL_SERVER (Integration Testing)

Run a local HTTP server for integration testing with real HTTP calls:

```python
from osbot_fast_api.utils.Fast_API_Server import Fast_API_Server
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API import Cache_Service__Fast_API
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config

# Create and start local server
service     = Cache_Service__Fast_API().setup()
server      = Fast_API_Server(app=service.app)
server_url  = server.start()

# Create client pointing to local server
config = Service__Fast_API__Client__Config(
    base_url   = server_url,
    verify_ssl = False
)
client = Service__Fast_API__Client(config=config)

# Client makes real HTTP calls to local server
# Mode: Enum__Client__Mode.REMOTE (but to localhost)
try:
    result = client.store().store__json(
        strategy  = "direct",
        namespace = "test",
        body      = {"integration": "test"}
    )
    
    # Test with real HTTP
    data = client.retrieve().retrieve__cache_id__json(
        cache_id  = result['cache_id'],
        namespace = "test"
    )
    
    assert data == {"integration": "test"}
finally:
    server.stop()
```

### Complete Test Infrastructure Pattern (Production-Ready)

This pattern from a real-world proxy service shows complete test infrastructure:

```python
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API import Cache_Service__Fast_API
from mgraph_ai_service_cache.service.cache.Cache__Config import Cache__Config
from mgraph_ai_service_cache.service.cache.Cache__Service import Cache__Service
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Storage_Mode import Enum__Cache__Storage_Mode
from osbot_fast_api.utils.Fast_API_Server import Fast_API_Server
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config import Serverless__Fast_API__Config

class TestCacheInfrastructure:
    """Complete test infrastructure for cache service"""
    
    def __init__(self):
        self.cache_service       = None
        self.cache_client        = None
        self.fast_api_server     = None
        self.server_url          = None
        self.setup_completed     = False
    
    def setup(self):
        """Initialize complete test environment"""
        if self.setup_completed:
            return self
        
        # Step 1: Setup in-memory cache backend
        cache_config     = Cache__Config(storage_mode=Enum__Cache__Storage_Mode.MEMORY)
        serverless_config = Serverless__Fast_API__Config(enable_api_key=False)
        
        self.cache_service = Cache_Service__Fast_API(
            config        = serverless_config,
            cache_service = Cache__Service(cache_config=cache_config)
        )
        self.cache_service.setup()
        
        # Step 2: Setup Fast API server
        self.fast_api_server = Fast_API_Server(app=self.cache_service.app())
        self.server_url      = self.fast_api_server.url().rstrip("/")
        
        # Step 3: Setup cache client
        client_config    = Service__Fast_API__Client__Config(base_url=self.server_url)
        self.cache_client = Service__Fast_API__Client(config=client_config)
        
        self.setup_completed = True
        return self
    
    def start_server(self):
        """Start the Fast API server"""
        if not self.fast_api_server.running:
            self.fast_api_server.start()
            return True
        return False
    
    def stop_server(self):
        """Stop the Fast API server"""
        if self.fast_api_server.running:
            self.fast_api_server.stop()
            return True
        return False
    
    def add_test_data(self):
        """Populate cache with test data"""
        self.start_server()
        
        test_urls = [
            "https://example.com/",
            "https://docs.example.com/api",
            "https://docs.example.com/api/about.html"
        ]
        
        for url in test_urls:
            # Store different transformations for each URL
            self.cache_client.store().store__string__cache_key(
                namespace  = "test-cache",
                strategy   = "key_based",
                cache_key  = f"sites/{url}",
                body       = f"<html><body><h1>Content for {url}</h1></body></html>",
                file_id    = "html-content"
            )
        
        return self

# Usage in tests
def test_cache_operations():
    """Example test using complete infrastructure"""
    # Setup
    test_infra = TestCacheInfrastructure().setup()
    test_infra.start_server()
    
    try:
        client = test_infra.cache_client
        
        # Test store
        result = client.store().store__json(
            strategy  = "direct",
            namespace = "test",
            body      = {"test": "data"}
        )
        
        assert result['cache_id'] is not None
        
        # Test retrieve
        data = client.retrieve().retrieve__cache_id__json(
            cache_id  = result['cache_id'],
            namespace = "test"
        )
        
        assert data == {"test": "data"}
        
        print("✓ All tests passed")
        
    finally:
        test_infra.stop_server()

# Run test
test_cache_operations()
```

### Choosing the Right Mode

**Use IN_MEMORY when:**
- Running unit tests (fastest)
- Testing client logic without network
- CI/CD pipelines (speed critical)
- No need for HTTP layer testing

**Use LOCAL_SERVER when:**
- Integration testing
- Testing HTTP behavior
- Debugging network issues
- Testing with real HTTP clients

**Use REMOTE when:**
- Production deployment
- End-to-end testing
- Load testing
- Real-world scenarios

### Environment-Based Configuration

```python
import os
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config

def create_client() -> Service__Fast_API__Client:
    """Create client based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')
    
    if env == 'production':
        # Remote mode with production credentials
        config = Service__Fast_API__Client__Config(
            base_url       = os.getenv('CACHE_SERVICE_URL'),
            api_key        = os.getenv('CACHE_SERVICE_API_KEY'),
            api_key_header = "X-API-Key"
        )
        return Service__Fast_API__Client(config=config)
    
    elif env == 'test':
        # In-memory mode for tests
        from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API import Cache_Service__Fast_API
        
        service = Cache_Service__Fast_API().setup()
        config  = Service__Fast_API__Client__Config()
        client  = Service__Fast_API__Client(config=config)
        
        client._requests._app = service.app
        client._requests._setup_mode()
        
        return client
    
    else:  # development
        # Local server mode
        from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API import Cache_Service__Fast_API
        from osbot_fast_api.utils.Fast_API_Server import Fast_API_Server
        
        service = Cache_Service__Fast_API().setup()
        server  = Fast_API_Server(app=service.app)
        server.start()
        
        config = Service__Fast_API__Client__Config(
            base_url   = server.url(),
            verify_ssl = False
        )
        
        return Service__Fast_API__Client(config=config)

# Usage
client = create_client()
```

---

## Known Limitations

Based on the codebase analysis, the following features have known issues or are incomplete:

### Issues in Some Client Versions

1. **Hash-Based Retrieval**
   - `retrieve__hash__cache_hash__string`, `retrieve__hash__cache_hash__json`, `retrieve__hash__cache_hash__binary` may have path template issues in some versions
   - **Workaround**: Use ID-based retrieval instead
   - Status: Fixed in v0.10.1+

2. **ZIP Operations**
   - ZIP creation, manipulation, and batch operations may not be fully implemented in some client versions
   - **Workaround**: Use REST API directly for ZIP operations
   - Status: Under development

3. **Delete Operations**
   - `delete__cache_id` method may have path template issues in some versions
   - **Workaround**: Use `admin_storage().file__delete()` with full path
   - Status: Fixed in v0.10.1+

4. **Exists Operations**
   - `exists__hash__cache_hash` may have path template issues in some versions
   - **Workaround**: Try retrieving and handle 404 errors
   - Status: Under review

### Version-Specific Notes

- **v0.3.0 and earlier**: Limited admin operations, no custom file IDs
- **v0.10.1+**: Most issues resolved, full admin operations available

---

## Troubleshooting

### Connection Issues

```python
# Verify client configuration
print(f"Base URL: {client.config.base_url}")
print(f"API Key Header: {client.config.api_key_header}")
print(f"API Key Set: {bool(client.config.api_key)}")

# Test connectivity
try:
    health = client.info().health()
    print(f"Service healthy: {health}")
except Exception as e:
    print(f"Connection failed: {e}")
    # Check if it's a connection error or auth error
    if "401" in str(e):
        print("Authentication failed - check API key")
    elif "404" in str(e):
        print("Service not found - check base URL")
    else:
        print("Network error - check connectivity")
```

### Authentication Issues

```python
# Check environment variables
import os

key_name = os.getenv('AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME')
key_value = os.getenv('AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE')
url = os.getenv('URL__TARGET_SERVER__CACHE_SERVICE')

print(f"Key Name: {key_name}")
print(f"Key Value: {'SET' if key_value else 'NOT SET'}")
print(f"URL: {url}")
```

### Debug Mode

```python
# Enable request logging
import logging

logging.basicConfig(level=logging.DEBUG)

# Requests will show full details
result = client.store().store__string(
    strategy="direct",
    namespace="debug",
    body="test"
)
```

### Common Error Scenarios

```python
# 404 Not Found - Cache entry doesn't exist
try:
    data = client.retrieve().retrieve__cache_id__json(
        cache_id="non-existent",
        namespace="test"
    )
except Exception as e:
    print("Cache miss - entry not found")

# 401 Unauthorized - Invalid API key
# Check AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE

# 400 Bad Request - Invalid parameters
# Verify strategy, namespace, and body are correct

# 500 Internal Server Error - Server-side issue
# Check service logs or contact support
```

---

## API Reference Summary

### Store Operations
- `store().store__string(strategy, namespace, body)`
- `store().store__json(strategy, namespace, body)`
- `store().store__binary(strategy, namespace, body)`
- `store().store__string__cache_key(namespace, strategy, cache_key, body, file_id='', json_field_path='')`
- `store().store__json__cache_key(namespace, strategy, cache_key, body, file_id='', json_field_path='')`
- `store().store__binary__cache_key(namespace, strategy, cache_key, body, file_id='')`

### Retrieve Operations
- `retrieve().retrieve__cache_id(cache_id, namespace)`
- `retrieve().retrieve__cache_id__string(cache_id, namespace)`
- `retrieve().retrieve__cache_id__json(cache_id, namespace)`
- `retrieve().retrieve__cache_id__binary(cache_id, namespace)`
- `retrieve().retrieve__hash__cache_hash(cache_hash, namespace)` ⚠️ May have issues in some versions
- `retrieve().retrieve__cache_id__metadata(cache_id, namespace)`
- `retrieve().retrieve__cache_id__config(cache_id, namespace)`

### Data Operations (Child Data)
- `data_store().data__store_string(cache_id, namespace, body)`
- `data_store().data__store_json(cache_id, namespace, body)`
- `data_store().data__store_binary(cache_id, namespace, body)`
- `data_store().data__store_string__with__id(cache_id, namespace, data_file_id, body)`
- `data_store().data__store_json__with__id(cache_id, namespace, data_file_id, body)`
- `data_store().data__store_binary__with__id(cache_id, namespace, data_file_id, body)`
- `data_store().data__store_string__with__id_and_key(cache_id, namespace, data_key, data_file_id, body)`
- `data_store().data__store_json__with__id_and_key(cache_id, namespace, data_key, data_file_id, body)`
- `data_store().data__store_binary__with__id_and_key(cache_id, namespace, data_key, data_file_id, body)`
- `data().retrieve().data__string__with__id(cache_id, namespace, data_file_id)`
- `data().retrieve().data__json__with__id(cache_id, namespace, data_file_id)`
- `data().retrieve().data__binary__with__id(cache_id, namespace, data_file_id)`
- `data().delete().delete__all__data__files(cache_id, namespace)`
- `data().delete().delete__data__file(cache_id, namespace, data_file_id)`

### Namespace Operations (v0.10.1+)
- `namespaces().list()`
- `namespace().stats(namespace)`
- `namespace().file_hashes(namespace)`
- `namespace().file_ids(namespace)`

### Admin Operations
- `admin_storage().bucket_name()`
- `admin_storage().file__exists(path)`
- `admin_storage().file__json(path)`
- `admin_storage().file__bytes(path)`
- `admin_storage().file__delete(path)`
- `admin_storage().files__in__path(path, return_full_path=False, recursive=False)`
- `admin_storage().files__all__path(path)`
- `admin_storage().folders(path='', return_full_path=False, recursive=False)`

### Info Operations
- `info().health()`
- `info().status()`
- `info().versions()`

---

## Feature Summary

### ✅ Fully Working Features

- String, JSON, and Binary storage (all methods)
- Key-based storage with semantic paths
- ID-based retrieval (all types)
- Metadata and configuration retrieval
- Child data operations (complete CRUD)
- Namespace operations (list, stats, file operations)
- Admin storage operations (files, folders, deletion)
- Server and info operations
- Health checks
- Custom file identifiers (v0.10.1+)
- Selective JSON field hashing (v0.10.1+)
- Three client execution modes (v0.10.1+)

### ⚠️ Known Issues or Incomplete

- Hash-based retrieval (path template issues in some versions)
- ZIP operations (not fully implemented in some client versions)
- Delete by cache_id (may have issues in some versions)
- Exists check by hash (may have issues in some versions)

**Note**: Most issues are resolved in v0.10.1+. For missing features, use the REST API directly or upgrade to the latest client version.

---

## Support and Resources

- **GitHub Repository**: [github.com/the-cyber-boardroom/MGraph-AI__Service__Cache__Client](https://github.com/the-cyber-boardroom/MGraph-AI__Service__Cache__Client)
- **PyPI Package**: [pypi.org/project/mgraph-ai-service-cache-client](https://pypi.org/project/mgraph-ai-service-cache-client)
- **Documentation**: [docs.mgraph.ai/cache-service](https://docs.mgraph.ai/cache-service)
- **Service Endpoint**: [cache.dev.mgraph.ai](https://cache.dev.mgraph.ai)
- **Issue Tracker**: GitHub Issues for bug reports and feature requests

### Note on Fast_API__Client__Builder

**The `Fast_API__Client__Builder` utility is not recommended for production use.** It was designed to auto-generate client code from the service API, but this approach proved to be only ~80% effective and required significant manual corrections to the generated client code.

Instead, use direct client configuration as shown throughout this document:

```python
# ✓ Recommended: Direct configuration
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config

config = Service__Fast_API__Client__Config(
    base_url       = "https://cache.dev.mgraph.ai",
    api_key        = "your-api-key",
    api_key_header = "X-API-Key"
)
client = Service__Fast_API__Client(config=config)

# ✗ Not recommended: Fast_API__Client__Builder
# from mgraph_ai_service_cache_client.client_builder.Fast_API__Client__Builder import Fast_API__Client__Builder
# builder = Fast_API__Client__Builder()
# builder.configure_client(client)  # Unreliable
```

---

## Version Compatibility

- **Current Client Version**: v0.10.1
- **Service Version**: v0.6.0+
- **Python**: 3.8+
- **Key Dependencies**:
  - `osbot-utils` (Type_Safe framework)
  - `osbot-fast-api` (FastAPI infrastructure)
  - `requests` (HTTP client)

### Version History

- **v0.10.1**: Custom file IDs, selective JSON hashing, enhanced admin ops, namespace management
- **v0.5.69 / v0.3.0**: Core functionality, five storage strategies, hierarchical data
- **v0.1.3**: Initial release

---

## Changelog

### v0.10.1 (Current - 2025-01-20)

**New Features:**
- ✨ Added `file_id` parameter for custom file naming in `cache_key` operations
- ✨ Added `json_field_path` for selective JSON field hashing
- ✨ Added namespace management operations (list, stats, file_hashes, file_ids)
- ✨ Enhanced admin operations (folders method, recursive listings)
- ✨ Added ephemeral testing patterns with in-memory mode
- ✨ Three client execution modes (REMOTE, IN_MEMORY, LOCAL_SERVER)

**Improvements:**
- 🐛 Fixed path handling in various operations
- 🐛 Resolved hash-based retrieval issues
- 🐛 Fixed delete operations
- 📚 Comprehensive documentation updates
- 🔒 Enhanced Type_Safe integration

### v0.5.69 / v0.3.0 (2024)

**Initial Public Release:**
- Core store/retrieve operations (string, JSON, binary)
- Five storage strategies (DIRECT, TEMPORAL, TEMPORAL_LATEST, TEMPORAL_VERSIONED, KEY_BASED)
- Hierarchical data support with child files
- Content-addressable storage with SHA-256 hashing
- Admin operations (file management)
- Type_Safe framework integration
- Multiple storage backend support

### v0.1.3 (2024)

**Pre-release:**
- Basic cache operations
- Initial API structure
- Development tooling

---

## Summary

The MGraph-AI Cache Service Python client provides a comprehensive, type-safe interface to a production-ready caching system with:

**Core Capabilities:**
- Content-addressable storage with automatic deduplication
- Five flexible storage strategies for different use cases
- Hierarchical data organization with child files
- Complete namespace isolation for multi-tenancy
- Binary, JSON, and string data support
- Comprehensive admin and management operations

**Advanced Features (v0.10.1+):**
- Custom file identifiers for human-readable paths
- Selective JSON field hashing for partial matching
- Namespace management and statistics
- Enhanced folder and file operations
- Three client execution modes for development and production

**Developer Experience:**
- Type_Safe framework for runtime validation and security
- Automatic sanitization of inputs
- Clear error messages and debugging support
- Ephemeral testing with in-memory mode
- Comprehensive API documentation

**Production Ready:**
- S3-backed for scalability and durability
- AWS Lambda compatible
- Multi-backend support (S3, SQLite, Local, In-Memory)
- Health checks and monitoring
- Immutable storage with version history

This merged document combines all information from both versions, ensuring no content is lost while maintaining clarity and usability for LLM-assisted development.

---

**End of Merged LLM Brief - v2.0**