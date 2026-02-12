import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import threading
import queue
import time
import re

class JournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Journal v2.0")
        self.root.geometry("900x600") 
        self.root.minsize(800, 500)
        
        # 1. DEFINE ATTRIBUTES FIRST (Critical fix for AttributeError)
        self.entries_file = "entries.txt"
        self.journal_data = []
        self.save_queue = queue.Queue()
        self.save_thread_running = True
        
        # 2. SETUP UI AND STYLES
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._setup_ui()
        
        # 3. START BACKGROUND SAVER THREAD
        self.save_thread = threading.Thread(target=self._background_saver, daemon=True)
        self.save_thread.start()
        
        # 4. LOAD EXISTING DATA
        self._load_existing_entries()

    def _setup_ui(self):
        """Creates a modern layout with a sidebar for entries and a main editor."""
        # PanedWindow allows the user to resize the sidebar
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- SIDEBAR AREA (Left Side) ---
        sidebar_frame = ttk.Frame(self.paned_window, padding="5")
        self.paned_window.add(sidebar_frame, weight=1)

        ttk.Label(sidebar_frame, text="Search Entries", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        self.search_entry = ttk.Entry(sidebar_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, pady=(0, 10))

        # Listbox to show historical entries
        self.entry_listbox = tk.Listbox(sidebar_frame, font=('Arial', 10), borderwidth=0, highlightthickness=1)
        self.entry_listbox.pack(fill=tk.BOTH, expand=True)
        self.entry_listbox.bind('<<ListboxSelect>>', self._on_select_entry)

        # --- EDITOR AREA (Right Side) ---
        content_frame = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(content_frame, weight=3)

        ttk.Label(content_frame, text="Title", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.title_entry = ttk.Entry(content_frame, font=('Arial', 12))
        self.title_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(content_frame, text="Content", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.text_area = tk.Text(content_frame, wrap=tk.WORD, font=('Arial', 11), padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Action Buttons
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        self.new_button = ttk.Button(btn_frame, text="New Entry", command=self._clear_form)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(btn_frame, text="Save Journal Entry", command=self.save_entry)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        # Status Bar for silent notifications
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def save_entry(self):
        """Validates input and adds the entry to the background save queue."""
        title = self.title_entry.get().strip()
        content = self.text_area.get("1.0", tk.END).strip()
        
        if not title or not content:
            self._show_status("Title and content are required!", "error")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry_dict = {'timestamp': timestamp, 'title': title, 'content': content}
        
        # Formatted string for the flat-file database
        entry_text = f"\n{'='*50}\n{timestamp}\nTitle: {title}\n{'='*50}\n{content}\n"
        
        self.save_queue.put((entry_text, entry_dict))
        self._show_status("Saving...", "info")
        self._clear_form()

    def _background_saver(self):
        """Worker thread that monitors the queue for new entries and writes to disk."""
        while self.save_thread_running:
            try:
                entry_text, entry_dict = self.save_queue.get(timeout=0.1)
                with open(self.entries_file, 'a', encoding='utf-8') as f:
                    f.write(entry_text)
                
                # Sync memory-mapped data and update UI
                self.journal_data.insert(0, entry_dict)
                self.root.after(0, self._refresh_listbox)
                self.root.after(0, lambda: self._show_status("Saved successfully", "success"))
                self.save_queue.task_done()
            except queue.Empty:
                continue

    def _load_existing_entries(self):
        """Parses the text file into memory on startup."""
        if not os.path.exists(self.entries_file): 
            return
        try:
            with open(self.entries_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Regex to parse the specific entry format
            entry_pattern = r'={50}\n(.*?)\nTitle: (.*?)\n={50}\n(.*?)(?=\n={50}|$)'
            matches = re.findall(entry_pattern, content, re.DOTALL)
            
            self.journal_data = []
            for ts, title, body in matches:
                self.journal_data.append({
                    'timestamp': ts.strip(), 
                    'title': title.strip(), 
                    'content': body.strip()
                })
            
            self.journal_data.reverse() # Most recent at the top
            self._refresh_listbox()
        except Exception as e:
            self._show_status(f"Error loading: {e}", "error")

    def _refresh_listbox(self, data=None):
        """Updates the sidebar listbox."""
        self.entry_listbox.delete(0, tk.END)
        display_data = data if data is not None else self.journal_data
        for entry in display_data:
            self.entry_listbox.insert(tk.END, f"{entry['timestamp']} - {entry['title']}")

    def _on_search_change(self, *args):
        """Filters the in-memory journal data based on search query."""
        query = self.search_var.get().lower()
        filtered = [e for e in self.journal_data if query in e['title'].lower() or query in e['content'].lower()]
        self._refresh_listbox(filtered)

    def _on_select_entry(self, event):
        """Loads a selected entry from the sidebar into the editor."""
        selection = self.entry_listbox.curselection()
        if selection:
            idx = selection[0]
            query = self.search_var.get().lower()
            data = [e for e in self.journal_data if query in e['title'].lower() or query in e['content'].lower()] if query else self.journal_data
            
            entry = data[idx]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, entry['title'])
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", entry['content'])

    def _clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.text_area.delete("1.0", tk.END)
        self.title_entry.focus_set()

    def _show_status(self, message, m_type):
        """Updates the status bar with a temporary message."""
        colors = {"error": "red", "success": "#008000", "info": "blue"}
        self.status_bar.configure(text=message, foreground=colors.get(m_type, "black"))
        self.root.after(4000, self._clear_status)

    def _clear_status(self):
        self.status_bar.configure(text="Ready", foreground="black")

    def cleanup(self):
        """Stops background threads before closing."""
        self.save_thread_running = False

def main():
    root = tk.Tk()
    app = JournalApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    root.mainloop()

if __name__ == "__main__":
    main()