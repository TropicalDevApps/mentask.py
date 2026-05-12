# MentAsk Release Notes

## Latest 10 Releases

### Version 0.27.9 - "Code Health Refresh" (2026-05-12)

**Focus**: Stability improvements and conflict resolution

#### Fixed
- **Code Health**: Removed unused CliRenderer import alias to improve code cleanliness and reduce potential confusion
- **Test Suite**: Fixed integration test for CLI provider stream functionality
- **Merge Conflicts**: Resolved conflicts in worktree and file tools modules to ensure proper functionality after branch synchronization

---

### Version 0.27.8 - "Thought Control" (2026-05-12)

**Focus**: User experience enhancements and CLI robustness

#### Added
- **Thought Process Toggle**: Introduced the `/thinking [true|false]` command to show or hide the agent's internal reasoning loop
- **Unified Status Line**: Merged the session status bar and turn divider into a single, cohesive line that matches the user's prompt theme

#### Fixed
- **CLI Bridge Robustness**: Refactored `CLIProvider` to use `stdin` for prompt delivery, bypassing OS command-line length limits on Windows
- **Improved Diagnostics**: Implemented parallel reading of `stdout` and `stderr` for CLI providers, enabling the capture of system warnings and errors
- **UI Layout**: Removed aggressive grid-based padding in agent responses for a more natural conversational flow
- **Error Filtering**: Automatically suppress repetitive system warnings (e.g., Windows 10 detected, Ripgrep missing) in CLI output

---

### Version 0.27.7 - "Renderer Fix" (2026-05-12)

**Focus**: Critical bug fix for UI rendering

#### Fixed
- **GemStyleRenderer**: Resolved a critical `NameError: name 'self' is not defined` during initialization by fixing the default parameter signature in the `__init__` method

---

### Version 0.27.5 - "Memory Intelligence" (2026-05-12)

**Focus**: Advanced memory management and context optimization

#### Added
- **Selective Memory via Side-Query**: Implemented a lightweight "sidechain" selection mechanism to identify and inject only the most relevant memory files into the context
- **Memory Metadata Caching**: Introduced `.metadata_cache.json` in the memories directory to support thousands of learning files with zero performance lag
- **Intelligent Context Pre-selection**: Refactored `ContextManager` and `ChatAgent` to automatically pre-select relevant context based on the user query before every turn

---

### Version 0.27.2 - "Async Diagnostics" (2026-05-12)

**Focus**: Performance improvements and testing infrastructure

#### Changed
- **LSP Diagnostics**: Implemented asynchronous file reading for LSP diagnostics to ensure a responsive TUI during large-scale code analysis
- **Testing Infrastructure**: Added comprehensive unit tests for `get_historical_report`, `ContextSnapper`, and `total_tokens` metrics

#### Fixed
- **Trust Manager**: Fixed a bug where exceptions were being silently swallowed, preventing proper directory trust resolution
- **Linting**: Resolved multiple static analysis warnings across the core engine to maintain CI integrity

---

### Version 0.27.1 - "Diagnostic Build" (2026-05-10)

**Focus**: Stability verification and edge case handling

#### Added
- **Diagnostic Build**: Consolidated various PRs and hotfixes into a unified diagnostic release for stability verification

#### Fixed
- **API Key Resolution**: Added missing edge-case tests for `ConfigManager.load_api_key`
- **Path Safety**: Improved validation logic in `analyze_path_safety` for safer directory scanning

---

### Version 0.27.0 - "Delegation Era" (2026-05-09)

**Focus**: Major architectural enhancement with agentic delegation

#### Added
- **Agentic Delegation**: Introduced the `SubagentTool` to allow MentAsk to spawn isolated sub-agents for specific tasks
- **Generalist Blueprint**: Added a `generalist` sub-agent profile that has full access to the workspace for complex, multi-step problem solving
- **Enhanced Loop Protection**: The `AgentOrchestrator` now intercepts identical text outputs and tool calls across turns to break infinite loops effectively

---

### Version 0.26.1 - "Local Model Fix" (2026-05-09)

**Focus**: Critical fix for local model compatibility

#### Fixed
- **Tool Chaining (Local Models)**: Fixed a bug where local models (e.g. Ollama, Qwen) would stop generating after a tool result because of strict API constraints. The agent now properly passes the `name` attribute back in tool responses and encodes empty assistant text correctly as `null`

---

### Version 0.26.0 - "Observability & Grace" (2026-05-09)

**Focus**: Advanced monitoring and graceful shutdown capabilities

#### Added
- **Observability Metrics**: Added robust metrics tracking for `TimeoutRecoveryManager` and `FileReadingSession`
- **Session Reporting**: Added `get_session_report` to `AgentOrchestrator` to export timeout and file reading metrics
- **Graceful Shutdown**: Added signal handling (SIGINT/SIGTSTP) in `cli/main.py` to cleanly abort pending tasks, cancel running tool operations, and save checkpoints

#### Fixed
- **Infinite Loop Detection**: Integrated line-based constraints into `FileReadingSession` to preemptively intercept and abort repetitive or looping `read_file` calls
- **Tool Timeouts**: Refactored `ExecutionManager` to wrap all tool executions inside an async `BlockingOperationManager`, preventing indefinite hangs with a strict visible timeout ceiling
- **Model Timeouts**: Implemented `TimeoutRecoveryManager` in `AgentOrchestrator` to dynamically detect network stalls and model timeouts, applying context-reduction heuristics and exponential backoffs automatically
- **Deprecations**: Replaced `asyncio.iscoroutinefunction` with `inspect.iscoroutinefunction` for Python 3.16 future-proofing
- **Performance**: Eradicated an O(n) bottleneck when reading large files that was causing triple-reads to count lines

---

### Version 0.25.2 - "Security & Discovery" (2026-05-09)

**Focus**: Enhanced security and folder discovery

#### Fixed
- **Folder Discovery**: Fixed a bug where `glob_find` only returned files, causing the agent to fail when searching for directories. Also updated `ensure_safe_path` to resolve symlinks and normalize case to prevent false "Access denied" errors
- **Command Security**: Relaxed the security warning for chained shell commands (e.g., `&&`, `|`) so that the agent doesn't unnecessarily prompt for manual approval in `/mode auto` unless the command contains explicitly dangerous patterns

---

## Evolution Summary

### Major Themes Across Last 10 Releases:

1. **Intelligence Enhancement**: From basic delegation to intelligent memory management
2. **Security & Stability**: Continuous improvements in path safety, timeout handling, and error recovery
3. **User Experience**: Progressive UI refinements, from status lines to thought process controls
4. **Local Model Support**: Extensive work on Ollama compatibility and local execution
5. **Observability**: Advanced metrics, reporting, and diagnostic capabilities
6. **Performance**: Async improvements, caching, and resource optimization

### Key Architectural Milestones:
- **v0.27.0**: Introduction of agentic delegation
- **v0.26.0**: Comprehensive observability and graceful shutdown
- **v0.25.0**: CLI bridging architecture
- **v0.27.5**: Intelligent memory management

### Stability Progress:
- **Early versions** (0.25.x): Focus on basic functionality and local model support
- **Mid versions** (0.26.x): Enhanced stability, timeout handling, and graceful operations
- **Recent versions** (0.27.x): Advanced features, UI polish, and code health improvements

---

*Generated from CHANGELOG.md - Last updated: 2026-05-12*
