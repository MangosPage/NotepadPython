import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk
import webbrowser
import json
import os

class Notepad:
      def __init__(self, root):
          self.root = root
          self.root.title("Notepad")
          self.root.geometry("800x600")
          
          # Add custom icon
          self.root.iconbitmap("Notepad_22522.ico")  # Make sure to have this icon file in the same directory

          self.notebook = ttk.Notebook(self.root)
          self.notebook.pack(expand=True, fill="both")

          self.tabs = []
          
          self.load_settings()

          self.create_new_tab()

          self.menu_bar = tk.Menu(self.root)
          self.root.config(menu=self.menu_bar)

          self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
          self.menu_bar.add_cascade(label="File", menu=self.file_menu)
          self.file_menu.add_command(label="New", command=self.new_file)
          self.file_menu.add_command(label="Open", command=self.open_file)
          self.file_menu.add_command(label="Save", command=self.save_file)
          self.file_menu.add_separator()
          self.file_menu.add_command(label="Exit", command=self.root.quit)

          self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
          self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
          self.edit_menu.add_command(label="Cut", command=lambda: self.get_current_text_area().event_generate("<<Cut>>"))
          self.edit_menu.add_command(label="Copy", command=lambda: self.get_current_text_area().event_generate("<<Copy>>"))
          self.edit_menu.add_command(label="Paste", command=lambda: self.get_current_text_area().event_generate("<<Paste>>"))
          self.edit_menu.add_separator()
          self.edit_menu.add_command(label="Highlight", command=self.highlight_text)

          self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
          self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
          self.settings_menu.add_command(label="Adjust Font", command=self.adjust_font)
          self.settings_menu.add_command(label="Adjust Indent", command=self.adjust_indent)
          self.settings_menu.add_command(label="Save Settings", command=self.save_settings)

          self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
          self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
          self.help_menu.add_command(label="Credits", command=self.show_credits)

          # Add GitHub button
          self.github_button = tk.Button(self.root, text="Github Repo", command=self.open_github)
          self.github_button.pack(side=tk.BOTTOM, pady=5)

      def create_new_tab(self, title="Untitled"):
          frame = ttk.Frame(self.notebook)
          text_area = tk.Text(frame, wrap="word", undo=True)
          text_area.pack(expand=True, fill="both")
          text_area.configure(font=self.current_font, tabs=self.current_indent * 7, fg=self.current_fg, bg=self.current_bg)
          self.notebook.add(frame, text=title)
          self.tabs.append(text_area)
          self.notebook.select(frame)

      def get_current_text_area(self):
          return self.tabs[self.notebook.index("current")]

      def new_file(self):
          self.create_new_tab()

      def open_file(self):
          file = filedialog.askopenfile(defaultextension=".npy", filetypes=[("Notepad Python", "*.npy*"), ("Notepad Python", "*.npy"), ("Notepad LINUX", "*.nl"), ("Notepad Mac", "*.nm"),("Notepad Verse", "*.nvc"), ("All Files", "*.*")])
          if file:
              self.create_new_tab(title=file.name.split("/")[-1])
              self.get_current_text_area().delete(1.0, tk.END)
              self.get_current_text_area().insert(1.0, file.read())

      def save_file(self):
          file = filedialog.asksaveasfile(defaultextension=".npy", filetypes=[("Notepad Python", "*.npy"), ("Notepad Python", "*.npy"), ("Notepad LINUX", "*.nl"), ("Notepad Mac", "*.nm"),("Notepad Verse", "*.nvc"), ("All Files", "*.*")])
          if file:
              data = self.get_current_text_area().get(1.0, tk.END)
              file.write(data)
              file.close()
              self.notebook.tab("current", text=file.name.split("/")[-1])

      def adjust_font(self):
          font_window = tk.Toplevel(self.root)
          font_window.title("Adjust Font")
        
          font_family = tk.StringVar(value=self.current_font.actual()['family'])
          font_size = tk.IntVar(value=self.current_font.actual()['size'])
        
          tk.Label(font_window, text="Font Family:").grid(row=0, column=0, padx=5, pady=5)
          font_family_entry = tk.Entry(font_window, textvariable=font_family)
          font_family_entry.grid(row=0, column=1, padx=5, pady=5)
        
          tk.Label(font_window, text="Font Size:").grid(row=1, column=0, padx=5, pady=5)
          font_size_entry = tk.Entry(font_window, textvariable=font_size)
          font_size_entry.grid(row=1, column=1, padx=5, pady=5)
        
          def apply_font():
              try:
                  new_font = font.Font(family=font_family.get(), size=font_size.get())
                  for text_area in self.tabs:
                      text_area.configure(font=new_font)
                  self.current_font = new_font
                  font_window.destroy()
              except:
                  messagebox.showerror("Error", "Invalid font settings")
        
          tk.Button(font_window, text="Apply", command=apply_font).grid(row=2, column=0, columnspan=2, pady=10)

      def adjust_indent(self):
          indent_window = tk.Toplevel(self.root)
          indent_window.title("Adjust Indent")
        
          indent_size = tk.IntVar(value=self.current_indent)
        
          tk.Label(indent_window, text="Indent Size:").grid(row=0, column=0, padx=5, pady=5)
          indent_size_entry = tk.Entry(indent_window, textvariable=indent_size)
          indent_size_entry.grid(row=0, column=1, padx=5, pady=5)
        
          def apply_indent():
              try:
                  new_indent = indent_size.get()
                  for text_area in self.tabs:
                      text_area.configure(tabs=new_indent * 7)
                  self.current_indent = new_indent
                  indent_window.destroy()
              except:
                  messagebox.showerror("Error", "Invalid indent size")
        
          tk.Button(indent_window, text="Apply", command=apply_indent).grid(row=1, column=0, columnspan=2, pady=10)

      def show_credits(self):
          credits_window = tk.Toplevel(self.root)
          credits_window.title("Credits")
          credits_window.geometry("300x100")
          
          credits_text = "Notepad Python\n\nDeveloped by: Mycodespace.dev\nVersion: 1.0"
          credits_label = tk.Label(credits_window, text=credits_text, justify=tk.CENTER)
          credits_label.pack(expand=True)

      def open_github(self):
          webbrowser.open("https://github.com/MangosPage/Notepad-Python")

      def highlight_text(self):
          try:
              text_area = self.get_current_text_area()
              if text_area.tag_ranges(tk.SEL):
                  start = text_area.index(tk.SEL_FIRST)
                  end = text_area.index(tk.SEL_LAST)
                  
                  color = tk.colorchooser.askcolor(title="Choose highlight color")[1]
                  if color:
                      text_area.tag_add("highlight", start, end)
                      text_area.tag_config("highlight", background=color)
              else:
                  messagebox.showinfo("Info", "You need to select text to highlight!")
          except:
              messagebox.showerror("Error", "This feature does not seem to work properly maybe go to the repo and update your version of Notepad Python.")

      def save_settings(self):
          settings = {
              'font_family': self.current_font.actual()['family'],
              'font_size': self.current_font.actual()['size'],
              'indent': self.current_indent,
              'fg': self.current_fg,
              'bg': self.current_bg,
          }
          with open('notepad_settings.json', 'w') as f:
              json.dump(settings, f)
          messagebox.showinfo("Settings Saved", "Your settings have been saved and will be applied next time you open Notepad Python.")

      def load_settings(self):
          try:
              if os.path.exists('notepad_settings.json'):
                  with open('notepad_settings.json', 'r') as f:
                      settings = json.load(f)
                  self.current_font = font.Font(family=settings['font_family'], size=settings['font_size'])
                  self.current_indent = settings['indent']
                  self.current_fg = settings['fg']
                  self.current_bg = settings['bg']
              else:
                  self.set_default_settings()
          except Exception as e:
              print(f"Error loading settings: {e}")
              self.set_default_settings()

      def set_default_settings(self):
          self.current_font = font.Font(family="Arial", size=12)
          self.current_indent = 4
          self.current_fg = "black"
          self.current_bg = "white"
if __name__ == "__main__":
      root = tk.Tk()
      notepad = Notepad(root)
      root.mainloop()


