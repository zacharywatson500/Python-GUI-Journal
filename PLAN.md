# Project: Persistent Professional Journal
## Architecture Goals
- **Stability:** Use background threading for all File I/O to keep UI responsive.
- **Resilience:** Implement robust error handling for "File Locked" or "Permission Denied" scenarios.
- **Performance:** Use a "Memory-Mapped" approach for searching (load entries into RAM).

## Current Feature Set
1. **Core UI:** - Title Entry, Content Text Area, and Scrollbar.
   - A "Status Bar" (Label) at the bottom for silent notifications (instead of popups).
2. **Data Handling:**
   - **Save Logic:** When 'Save' is clicked, validate input, add to `queue.Queue`, and clear UI.
   - **Worker Thread:** A background daemon thread that monitors the queue and appends to `entries.txt`.
3. **New Feature: Search & Sync:**
   - **Startup:** Load existing `entries.txt` into a RAM variable (`self.journal_data`).
   - **Search Bar:** A top-level search field that filters entries in real-time.
   - **Sync:** Ensure every new save updates both the `entries.txt` file and the `self.journal_data` RAM variable.

## Technical Constraints
- Use `threading` and `queue` for thread-safety.
- Handle `utf-8` encoding for emojis/special characters.
- Use `tk.after()` for status bar message timeouts (4 seconds).