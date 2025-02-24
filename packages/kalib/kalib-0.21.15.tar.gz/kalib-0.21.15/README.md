# Advanced Python Utilities Module

This module provides a comprehensive set of utilities for advanced Python programming, including HTTP communication, string handling, logging enhancements, introspection, dynamic importing, property descriptors, data class extensions, and serialization. It is designed to facilitate complex application development by offering robust tools that extend Python's standard capabilities.

## Table of Contents

- [HTTP Communication Utilities](#http-communication-utilities)
- [String Handling Enhancements](#string-handling-enhancements)
- [Advanced Logging System](#advanced-logging-system)
- [Introspection and Reflection Utilities](#introspection-and-reflection-utilities)
- [Dynamic Importing Tools](#dynamic-importing-tools)
- [Advanced Property Descriptors](#advanced-property-descriptors)
- [Data Class Extensions and Configuration Handling](#data-class-extensions-and-configuration-handling)
- [Serialization and Deserialization Utilities](#serialization-and-deserialization-utilities)

## HTTP Communication Utilities

### Overview

This component provides a robust toolkit for handling HTTP communication. It includes advanced features for error handling, response parsing, cookie management, and URL processing. The utilities streamline building HTTP clients and services by abstracting common patterns and offering flexible, extensible components.

### Key Features

- **HTTPException Hierarchy**: A comprehensive set of exception classes for handling HTTP errors, based on status codes and error types.
- **Response Handling**: Utilities for parsing and processing HTTP responses, including automatic JSON decoding and error checking.
- **Cookie Management**: Tools for managing HTTP cookies, including parsing and formatting.
- **URL Processing**: Classes and functions for manipulating URLs, including query parameters and path components.
- **Serialization Decorators**: Decorators to facilitate serialization and deserialization of complex objects within the HTTP context.
- **Namespace Augmentation**: Enhancements to the HTTP namespace for convenient access to common utilities like `HTTP.URL`, `HTTP.Agent`, and `HTTP.Exception`.

## String Handling Enhancements

### Overview

Provides advanced string handling utilities focused on character encoding detection, conversion, and manipulation. It defines the `Str` class, acting as a wrapper around string or bytes objects, offering methods to handle various encoding scenarios and to facilitate text processing.

### Key Features

- **Encoding and Decoding**: Convert between bytes and string representations, handling different character encodings.
- **Charset Detection**: Automatically detects the character encoding of input data using custom logic and libraries.
- **Lazy Proxying**: Proxies common string methods to the underlying string representation, allowing `Str` instances to behave like regular strings.
- **Tokenization**: Methods to split strings into tokens based on regular expression patterns.

## Advanced Logging System

### Overview

Enhances the standard Python logging system by introducing custom log levels, additional logging utilities, and a more flexible logger configuration. It provides advanced logging capabilities suitable for complex applications that require detailed logging and traceability.

### Key Features

- **Custom Log Levels**: Defines additional log levels like `NOTICE`, `DEPRECATE`, and `VERBOSE` for finer-grained logging.
- **Logger Configuration**: Supports configuration from files (e.g., `logging.toml`), environment variables, or default settings.
- **Logger Extensions**: Provides a `Logger` class with enhanced methods for logging, including context-aware logging and deduplication of messages.
- **Integration with Modules**: Automatically injects the custom logger into modules, ensuring consistent logging behavior across the application.

## Introspection and Reflection Utilities

### Overview

Offers a collection of utility functions and classes for introspection, type checking, and reflection. It includes functions to analyze objects, their types, inheritance hierarchies, and modules.

### Key Features

- **Type Checking Functions**: Utilities like `is_callable`, `is_collection`, and `is_iterable` for checking object types.
- **Inheritance Utilities**: Functions to iterate over an object's MRO, get attributes from superclasses, and analyze class hierarchies.
- **Module and Object Inspection**: Tools to get the module of an object, its fully qualified name, source file, and other metadata.
- **Stack Inspection**: Functions to analyze the call stack, filter stack traces, and determine stack frame offsets.

## Dynamic Importing Tools

### Overview

Provides utilities for dynamic importing of modules and objects, with support for caching, handling optional dependencies, and enhanced error reporting.

### Key Features

- **Dynamic Importing**: Functions like `import_object` to import modules or objects by name at runtime.
- **Caching Imports**: `cached_import` function to memoize imports and improve performance.
- **Optional Dependencies**: `optional` function to handle optional imports gracefully, returning `None` or a default value if the module is not available.
- **Error Handling**: Detailed logging and error messages to aid in debugging import issues, including suggestions for missing packages.

## Advanced Property Descriptors

### Overview

Provides advanced property descriptors for Python classes, allowing the creation of instance, class, and mixed properties with optional caching capabilities. It includes decorators and base classes to facilitate the definition of properties that can behave differently depending on access context.

### Key Features

- **Custom Property Decorators**: Decorators like `@Property.Class` and `@Property.Cached` to define properties with custom behaviors.
- **Caching Support**: Ability to cache property results, optimizing performance for expensive computations.
- **Context-Aware Properties**: Properties that can differentiate between being accessed from an instance or a class.
- **Async Support**: Supports both synchronous and asynchronous property methods.

## Data Class Extensions and Configuration Handling

### Overview

Extends the standard `dataclass` module with additional features such as validation, serialization, dynamic class creation, and integration with custom logging mechanisms.

### Key Features

- **Custom Data Classes**: Enhanced `dataclass` decorator that supports extra parameters, memoization, and custom initialization.
- **Validation**: Automatic validation of field types and default values against the defined schema.
- **Serialization Methods**: Methods like `as_dict`, `as_json`, and `as_sql` for converting instances to different formats.
- **Dynamic Class Creation**: Utilities like `autoclass` and `simple` to generate classes dynamically based on configuration schemas.
- **Operator Overloading**: Overloaded operators (`&`, `|`, `^`, `-`, `+`) for combining and comparing data class instances.

## Serialization and Deserialization Utilities

### Overview

Provides advanced serialization and deserialization utilities, supporting multiple serialization backends, compression algorithms, and encoding schemes. It allows custom serialization of complex objects, automatic detection of serialization formats, and flexible data encoding and decoding options.

### Key Features

- **Multiple Backends**: Supports serialization backends like `orjson` and standard `json`, with automatic selection.
- **Custom Serialization**: Ability to register custom serialization functions for specific classes.
- **Compression Support**: Utilizes compression libraries like `zstd` or `gzip` to compress serialized data.
- **Flexible Encoding**: Supports multiple encoding schemes such as Base16, Base32, Base64, Base85, and Base2048.
- **Automatic Backend Detection**: Deserialization functions automatically detect the serialization backend used.
- **Error Handling**: Robust exception handling and context-aware suppression of errors.
