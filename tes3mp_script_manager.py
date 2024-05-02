import tkinter as tk
from tkinter import filedialog, Listbox, messagebox
import os
import shutil
import re

CONFIG_FILE = "config.txt"

class ScriptManager(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        self.import_location_label = tk.Label(self, text="Choose script import location:")
        self.import_location_label.pack(side="top", padx=10, pady=(10, 5))

        self.import_location_entry = tk.Entry(self, width=50)
        self.import_location_entry.pack(side="top", padx=10, pady=5)

        self.browse_import_location_button = tk.Button(self, text="Browse Directory", command=self.browse_import_location)
        self.browse_import_location_button.pack(side="top", pady=5)

        self.custom_scripts_label = tk.Label(self, text="Select customScripts.lua file:")
        self.custom_scripts_label.pack(side="top", padx=10, pady=(10, 5))

        self.custom_scripts_entry = tk.Entry(self, width=50)
        self.custom_scripts_entry.pack(side="top", padx=10, pady=5)

        self.browse_custom_scripts_button = tk.Button(self, text="Browse customScripts.lua", command=self.browse_custom_scripts)
        self.browse_custom_scripts_button.pack(side="top", pady=5)

        self.script_to_import_label = tk.Label(self, text="Select script to import:")
        self.script_to_import_label.pack(side="top", padx=10, pady=(10, 5))

        self.script_to_import_entry = tk.Entry(self, width=50)
        self.script_to_import_entry.pack(side="top", padx=10, pady=5)

        self.browse_script_button = tk.Button(self, text="Browse Script to Import", command=self.browse_script)
        self.browse_script_button.pack(side="top", pady=5)

        self.custom_name_label = tk.Label(self, text="Enter custom name:")
        self.custom_name_label.pack(side="top", padx=10, pady=(10, 5))

        self.custom_name_entry = tk.Entry(self, width=50)
        self.custom_name_entry.pack(side="top", padx=10, pady=5)

        self.import_button = tk.Button(self, text="Import Script", command=self.import_script)
        self.import_button.pack(side="top", pady=10)

        self.wipe_button = tk.Button(self, text="Completely Wipe Custom Scripts", command=self.wipe_custom_scripts)
        self.wipe_button.pack(side="top", pady=5)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.load_scripts_list)
        self.refresh_button.pack(side="top", pady=5)

        self.script_list_label = tk.Label(self, text="Currently Added Custom Scripts:")
        self.script_list_label.pack(side="top", pady=(10, 0))
        self.script_listbox = Listbox(self, width=50, height=10)
        self.script_listbox.pack(side="top", padx=10, pady=5)

        self.remove_button = tk.Button(self, text="Remove Selected Entry", command=self.remove_selected_entry)
        self.remove_button.pack(side="top", pady=5)

        self.load_scripts_list()

    def browse_import_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.import_location_entry.delete(0, tk.END)
            self.import_location_entry.insert(0, directory)
            self.save_config()

    def browse_custom_scripts(self):
        filepath = filedialog.askopenfilename(filetypes=[("Lua files", "*.lua")])
        if filepath:
            self.custom_scripts_entry.delete(0, tk.END)
            self.custom_scripts_entry.insert(0, filepath)
            self.save_config()

    def browse_script(self):
        filepath = filedialog.askopenfilename(filetypes=[("Lua files", "*.lua")])
        if filepath:
            self.script_to_import_entry.delete(0, tk.END)
            self.script_to_import_entry.insert(0, filepath)

    def import_script(self):
        import_location = self.import_location_entry.get()
        custom_scripts_file = self.custom_scripts_entry.get()
        script_to_import = self.script_to_import_entry.get()
        custom_name = self.custom_name_entry.get()

        if not import_location or not custom_scripts_file or not script_to_import:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        if not custom_name:
            messagebox.showerror("Error", "Please enter a custom name.")
            return

        # Check for duplicate custom names
        custom_names = [item.split()[0] for item in self.script_listbox.get(0, tk.END)]
        if custom_name in custom_names:
            messagebox.showerror("Error", "Custom name must be unique.")
            return

        script_name = os.path.basename(script_to_import)
        destination_path = os.path.join(import_location, script_name)
        shutil.copy(script_to_import, destination_path)

        with open(custom_scripts_file, 'a') as file:
            file.write(f'-- {custom_name}\n')
            file.write(f'require("{os.path.relpath(import_location, start=os.path.dirname(custom_scripts_file))}/{script_name[:-4]}")\n')

        messagebox.showinfo("Success", "Script imported successfully!")
        self.load_scripts_list()

    def wipe_custom_scripts(self):
        custom_scripts_file = self.custom_scripts_entry.get()
        if not custom_scripts_file:
            messagebox.showerror("Error", "Please select a customScripts.lua file.")
            return

        with open(custom_scripts_file, 'w') as file:
            file.write("")

        messagebox.showinfo("Success", "Custom scripts completely wiped!")
        self.load_scripts_list()

    def remove_selected_entry(self):
        selected_index = self.script_listbox.curselection()
        if selected_index:
            selected_item = self.script_listbox.get(selected_index)
            custom_scripts_file = self.custom_scripts_entry.get()
            if not custom_scripts_file:
                messagebox.showerror("Error", "Please select a customScripts.lua file.")
                return

            with open(custom_scripts_file, 'r') as file:
                lines = file.readlines()

            # Find the line with the custom name comment matching the selected entry
            for i, line in enumerate(lines):
                if selected_item.split()[0] in line and line.startswith('--'):
                    # Extract file path from require declaration
                    match = re.search(r'require\("(.*)"\)', lines[i+1])
                    if match:
                        script_file_path = match.group(1)
                        # Remove custom name comment line
                        lines.pop(i)
                        # Remove the following line (require declaration)
                        lines.pop(i)
                        break

            # Write the modified lines back to customscripts.lua
            with open(custom_scripts_file, 'w') as file:
                file.writelines(lines)

            # Remove corresponding file
            script_name = os.path.basename(script_file_path)
            custom_scripts_directory = os.path.dirname(custom_scripts_file)
            script_location = os.path.join(custom_scripts_directory, script_name)
            if os.path.exists(script_location):
                os.remove(script_location)

            messagebox.showinfo("Success", "Selected entry removed!")
            self.load_scripts_list()

    def save_config(self):
        with open(CONFIG_FILE, 'w') as config:
            config.write(f"{self.import_location_entry.get()}\n")
            config.write(f"{self.custom_scripts_entry.get()}")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as config:
                lines = config.readlines()
                if len(lines) >= 2:
                    self.import_location_entry.insert(0, lines[0].strip())
                    self.custom_scripts_entry.insert(0, lines[1].strip())

        # Check button state after loading config
        self.check_button_state()

    def load_scripts_list(self):
        custom_scripts_file = self.custom_scripts_entry.get()
        if not custom_scripts_file:
            return

        self.script_listbox.delete(0, tk.END)
        with open(custom_scripts_file, 'r') as file:
            lines = file.readlines()

        i = 0
        while i < len(lines):
            if lines[i].startswith('--'):
                custom_name = lines[i].strip()[3:].strip()
                if lines[i + 1].startswith('require'):
                    require_declaration = lines[i + 1].strip().split('"')[1]
                    self.script_listbox.insert(tk.END, f'{custom_name} [{require_declaration}]')
                    i += 1
                else:
                    self.script_listbox.insert(tk.END, f'{custom_name}')
            elif lines[i].startswith('require'):
                require_declaration = lines[i].strip().split('"')[1]
                self.script_listbox.insert(tk.END, f'{require_declaration}')
            i += 1

        self.check_button_state()

    def check_button_state(self):
        if self.script_listbox.size() <= 1:
            self.remove_button.config(state="disabled")
        else:
            self.remove_button.config(state="normal")

def main():
    root = tk.Tk()
    root.title("TES3MP Script Manager")
    app = ScriptManager(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
