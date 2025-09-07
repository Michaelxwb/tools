# iFlow CLI Context - Developer Toolkit

## Project Overview
A comprehensive PyQt5-based developer toolkit providing essential utilities for JSON formatting, timestamp conversion, and Redis database management.

## Project Structure

```
/Users/jahan/workspace/tools/
├── toolkit_main.py              # Main application entry point
├── requirements.txt             # Python dependencies
├── tools/                       # Tool implementations
│   ├── __init__.py
│   ├── base_tool.py            # Base class for all tools
│   ├── json_formatter_tool.py  # JSON formatting and validation
│   ├── timestamp_converter_tool.py  # Unix timestamp conversion
│   └── redis_tool.py           # Redis connection and management
├── install_pyinstaller.py      # PyInstaller installation helper
└── [build scripts and icons]
```

## Tools Available

### 1. JSON Formatter Tool (`tools/json_formatter_tool.py`)
**Features:**
- JSON formatting with proper indentation
- JSON compression (minification)
- JSON validation with detailed error reporting
- Tree view visualization of JSON structure
- File import/export functionality
- Support for both JSON and Python dictionary formats
- Smart parsing with error recovery

**Key Components:**
- `JSONFormatterTool` class extending `BaseTool`
- Real-time tree view with expand/collapse functionality
- Detailed error dialogs with line/column indicators
- Copy-to-clipboard functionality for results

### 2. Timestamp Converter Tool (`tools/timestamp_converter_tool.py`)
**Features:**
- Real-time Unix timestamp display
- Timestamp to human-readable date conversion
- Date to timestamp conversion (with second/millisecond options)
- Live update toggle (play/pause functionality)
- Copy-to-clipboard for all values
- Support for multiple date formats
- Boundary checking for valid timestamp ranges

**Key Components:**
- `TimestampConverterTool` class extending `BaseTool`
- QTimer-based real-time updates
- Comprehensive date format parsing
- Visual feedback for all operations

### 3. Redis Tool (`tools/redis_tool.py`)
**Features:**
- **Connection Modes:**
  - Single Redis server connection
  - Redis Cluster connection
  - Database selection (0-15) for single mode
- **Data Type Support:**
  - String values
  - List operations (view, add, delete)
  - Set operations (view, add, delete)
  - Sorted Set (ZSET) operations
  - Hash operations (view, add, delete fields)
- **Key Management:**
  - Key browsing and filtering
  - Key copying to clipboard
  - Key deletion with confirmation
  - TTL display and modification
- **Threading:**
  - Asynchronous operations with `RedisConnectionThread`
  - Non-blocking UI during Redis operations
  - Progress indicators for long operations

**Key Components:**
- `RedisTool` class extending `BaseTool`
- `RedisConnectionThread` for async operations
- Comprehensive error handling and user feedback
- Consistent styling with other tools

## Technical Stack

### Dependencies
```
PyQt5>=5.15.0          # GUI framework
redis>=4.0.0           # Redis client library
```

### Architecture
- **MVC Pattern:** Each tool follows Model-View-Controller pattern
- **Base Tool Class:** `BaseTool` provides common functionality
- **Threading:** Redis operations use QThread for async execution
- **Error Handling:** Comprehensive error dialogs with detailed messages
- **Styling:** Consistent visual design across all tools

## Usage Instructions

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python toolkit_main.py
```

### Building Executable
```bash
# Install PyInstaller (if needed)
python install_pyinstaller.py

# Build executable
pyinstaller --onefile --windowed --icon=icon.ico toolkit_main.py
```

### Redis Tool Configuration
1. **Single Mode:**
   - Host: Redis server hostname/IP
   - Port: Redis server port (default 6379)
   - Password: Optional authentication
   - Database: 0-15 (selectable)

2. **Cluster Mode:**
   - Host: Any cluster node hostname/IP
   - Port: Cluster node port (default 6379)
   - Password: Optional authentication

## Recent Bug Fixes

### Security Fixes
- **JSON Formatter:** Removed `ast.literal_eval` usage to prevent code injection
- **Input Validation:** Added strict JSON parsing with detailed error reporting

### Logic Fixes
- **Timestamp Converter:** Fixed duplicate multiplication in unit conversion
- **Boundary Checking:** Added proper validation for timestamp ranges (1970-2038)

### UI Fixes
- **Stop Button:** Fixed QTimer management for proper start/stop functionality
- **Styling:** Updated button colors and visual feedback for better UX
- **Error Dialogs:** Enhanced error messages with context and suggestions

## Development Guidelines

### Adding New Tools
1. Create new tool class extending `BaseTool`
2. Implement required methods: `setup_ui()`, `cleanup()`
3. Add tool button in `toolkit_main.py`
4. Follow existing styling patterns
5. Add comprehensive error handling

### Code Style
- **Naming:** Use descriptive names in English and Chinese
- **Comments:** Include both English and Chinese comments
- **Error Handling:** Always provide user-friendly error messages
- **Threading:** Use QThread for any blocking operations

## File Locations

### Core Files
- `toolkit_main.py:1-200` - Main application window
- `tools/base_tool.py:1-50` - Base tool class
- `tools/json_formatter_tool.py:1-500` - JSON formatting tool
- `tools/timestamp_converter_tool.py:1-400` - Timestamp conversion tool
- `tools/redis_tool.py:1-600` - Redis management tool

### Configuration
- `requirements.txt:1-5` - Python dependencies
- `install_pyinstaller.py:1-150` - PyInstaller installation helper

## Known Issues & Solutions

### Common Issues
1. **Redis Connection Timeout:** Check network connectivity and Redis server status
2. **JSON Parse Errors:** Use the detailed error dialog for debugging
3. **Timestamp Range Errors:** Ensure timestamps are within 1970-2038 range

### Performance Considerations
- Large JSON files (>10MB) may cause UI lag
- Redis operations on large datasets use pagination
- Threading prevents UI freezing during long operations

## Future Enhancements

### Planned Features
- Database connection tools (MySQL, PostgreSQL)
- API testing tools
- Code formatting tools
- File conversion utilities
- Enhanced Redis features (pub/sub, Lua scripts)

### Technical Improvements
- Settings persistence
- Keyboard shortcuts
- Dark mode support
- Plugin system for extensibility