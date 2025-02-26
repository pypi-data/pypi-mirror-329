#!/usr/bin/env python3

import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Adjust these paths as necessary:
DESKTOP_PATH = os.path.expanduser("~/Desktop")
PHILE_PATH   = os.path.join(DESKTOP_PATH, ".phile")

class ScreenshotOrganizer:
    def __init__(self, root, images):
        self.root = root
        self.root.title("Screenshot Organizer")
        self.images = images
        self.current_index = 0

        # Ensure the .phile directory exists
        os.makedirs(PHILE_PATH, exist_ok=True)

        # Main container
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Image display
        self.img_label = tk.Label(self.frame, bg="gray")
        self.img_label.pack(side=tk.LEFT, expand=True)

        # Right panel (description + buttons)
        self.right_panel = tk.Frame(self.frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Description entry
        tk.Label(self.right_panel, text="Description:").pack(anchor=tk.NW)
        self.desc_text = tk.Text(self.right_panel, height=10, width=40)
        self.desc_text.pack(pady=5)

        # Buttons
        self.button_frame = tk.Frame(self.right_panel)
        self.button_frame.pack(side=tk.BOTTOM, pady=(20, 0))

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_screenshot)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_screenshot)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Display the first screenshot if available
        if self.images:
            self.display_image()
        else:
            messagebox.showinfo("No Screenshots", "No screenshots found on the Desktop.")
            self.root.quit()

    def display_image(self):
        # Clear any existing text
        self.desc_text.delete("1.0", tk.END)

        # Load current image
        img_path = self.images[self.current_index]
        img = Image.open(img_path)

        # Optionally, resize if you want to fit in a certain dimension
        # (here we just do a simple max size of 800x600 to prevent enormous windows)
        max_width, max_height = 800, 600
        img.thumbnail((max_width, max_height))

        self.tk_img = ImageTk.PhotoImage(img)
        self.img_label.configure(image=self.tk_img)

        # Update window title to reflect which file we are on
        self.root.title(f"Screenshot Organizer [{self.current_index + 1}/{len(self.images)}]")

    def save_screenshot(self):
        """Save the screenshot + description to ~/.phile"""
        description = self.desc_text.get("1.0", tk.END).strip()

        # If no description is provided, ask the user if they want to continue
        if not description:
            if not messagebox.askyesno(
                "No Description",
                "You haven't provided a description. Save anyway?"
            ):
                return  # user clicked 'No', so don't proceed

        img_path = self.images[self.current_index]
        basename = os.path.splitext(os.path.basename(img_path))[0]

        # Create a subfolder in .phile with the screenshot's basename
        folder_path = os.path.join(PHILE_PATH, basename)
        os.makedirs(folder_path, exist_ok=True)

        # Move the image into that folder
        new_image_path = os.path.join(folder_path, os.path.basename(img_path))
        shutil.move(img_path, new_image_path)

        # Save the description as a text file
        desc_file_path = os.path.join(folder_path, "description.txt")
        with open(desc_file_path, "w", encoding="utf-8") as f:
            f.write(description)

        messagebox.showinfo("Saved", f"Screenshot + description saved to:\n{folder_path}")
        self.next_screenshot()

    def delete_screenshot(self):
        """Delete the current screenshot from the Desktop."""
        img_path = self.images[self.current_index]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Delete {os.path.basename(img_path)}?"):
            os.remove(img_path)
            messagebox.showinfo("Deleted", f"Deleted {os.path.basename(img_path)}")
            self.next_screenshot()

    def next_screenshot(self):
        """Go to the next screenshot or close if none left."""
        self.current_index += 1
        if self.current_index >= len(self.images):
            messagebox.showinfo("Done", "No more screenshots to process.")
            self.root.quit()
        else:
            self.display_image()


def main():
    # Gather all files on Desktop that start with 'Screenshot'
    screenshots = []
    for file in os.listdir(DESKTOP_PATH):
        if file.startswith("Screenshot"):
            full_path = os.path.join(DESKTOP_PATH, file)
            # Basic check: only add if it's actually a file, not a directory
            if os.path.isfile(full_path):
                screenshots.append(full_path)

    root = tk.Tk()
    app = ScreenshotOrganizer(root, screenshots)
    root.mainloop()

if __name__ == "__main__":
    main()
