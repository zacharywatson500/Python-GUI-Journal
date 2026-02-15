# Professional Journal v2.0

A high-performance, responsive journaling application built with Python and Tkinter. This tool is designed for stability and resilience, featuring a multi-threaded architecture to ensure the UI remains fluid even during heavy file I/O operations.

---

## 🚀 Key Features

* **Background Threading:** All file saving is handled by a dedicated worker thread using `queue.Queue`, preventing the application from freezing during disk writes.
* **Real-time Search:** A memory-mapped approach allows you to filter through your entire journal history instantly via the sidebar search bar.
* **Unicode Support:** Full support for emojis, special symbols, and multiple languages (e.g., Chinese, Arabic, Hindi) using UTF-8 encoding.
* **Modern UI:** A clean, paned layout featuring a searchable entry list, a dedicated editor, and a silent status bar for non-intrusive notifications.
* **Data Resilience:** Uses robust regex patterns to parse and organize entries within a flat-file database (`entries.txt`).

---

## 🛠 Project Structure

| File | Purpose |
| :--- | :--- |
| `journal.py` | The main application logic and UI implementation. |
| `entries.txt` | [cite_start]The flat-file database where journal entries are stored[cite: 2, 3]. |
| `stress_test.py` | A comprehensive test suite for validating app performance under extreme conditions. |
| `PLAN.md` | Architectural goals and technical constraints for the project. |
| `.gitignore` | [cite_start]Ensures `entries.txt` and Python caches remain private and out of version control[cite: 1]. |

---

## 🧪 Stress Tested for Reliability

The application has been vetted through a dedicated `stress_test.py` suite to ensure it can handle:
* **Input Floods:** Processing entries with over 1,000,000 characters.
* **Rapid Fire Saves:** Triggering 50 saves in a single second without data corruption.
* **Character Chaos:** Handling complex Unicode strings, mathematical symbols, and diverse currency icons.

---

## ⚙️ How to Run

1.  **Ensure Python 3.x is installed.**
2.  **Launch the Application:**
    ```bash
    python journal.py
    ```
3.  **Run Stress Tests (Optional):**
    ```bash
    python stress_test.py
    ```

> [cite_start]**Privacy Note:** Your personal journal data in `entries.txt` is automatically ignored by Git to keep your entries private[cite: 1].

---