import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from tkinter import font as tkfont
from library_management_system import LibraryManagementSystem, User, PrintedBook, EBook
import os
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except Exception:
    HAS_PIL = False

class LibraryUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        # Window size and style — start maximized for full view
        try:
            self.root.state('zoomed')
        except Exception:
            # fallback to fullscreen if state not supported
            try:
                self.root.attributes('-fullscreen', True)
            except Exception:
                self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Treeview", font=("Segoe UI", 10))
        # background and icon placeholders
        self.bg_photo = None
        self.icon_photo = None
        self.lib = LibraryManagementSystem()

        # Add default users (admin has a password)
        self.admin = User("U1", "Ravindra", role="Admin", password="admin123")
        self.member = User("U2", "Vinod", role="member")
        self.lib.add_user(self.admin)
        self.lib.add_user(self.member)

        # Current user
        self.current_user = None

        # --- Header Frame ---
        self.header_frame = ttk.Frame(root, padding=15)
        self.header_frame.pack(side="top", fill="x", padx=0, pady=0)
        
        ttk.Label(self.header_frame, text="Library Management System", font=("Segoe UI", 18, "bold")).pack(pady=10)

        # --- Frames ---
        self.login_frame = ttk.Frame(root, padding=30)
        # let login frame expand so it centers in the large window
        self.login_frame.pack(expand=True)

        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill='both', expand=True)

        # Footer frame shown on the login page (hidden after login)
        self.footer_frame = tk.Frame(root, bg='black', height=1500)
        self.footer_frame.pack(side='bottom', fill='x')
        self.footer_image = None
        # load a footer image if available
        try:
            image_candidates = ["ravindra1.jpg", "logo.jpg", "library.jpg", "library.png"]
            img_path = None
            for name in image_candidates:
                if os.path.exists(name):
                    img_path = name
                    break
            if HAS_PIL and img_path:
                img = Image.open(img_path)
                img = img.resize((64, 64), getattr(Image, "Resampling", Image).LANCZOS)
                self.footer_image = ImageTk.PhotoImage(img)
                logo_lbl = tk.Label(self.footer_frame, image=self.footer_image, bg='black')
                logo_lbl.pack(side='left', padx=12, pady=8)
            else:
                logo_lbl = tk.Label(self.footer_frame, text="", bg='black')
                logo_lbl.pack(side='left', padx=12, pady=8)
        except Exception:
            pass

        # Text area in footer
        txt_frame = tk.Frame(self.footer_frame, bg='black')
        txt_frame.pack(side='left', padx=8, pady=8)
        tk.Label(txt_frame, text="Admin: Ravindra  Singh", fg='white', bg='black', font=("Segoe UI", 10, "bold")).pack(anchor='w')
        tk.Label(txt_frame, text="Contact: +91-9759029731", fg='white', bg='black').pack(anchor='w')
        tk.Label(txt_frame, text="About: Simple Library Management System", fg='white', bg='black').pack(anchor='w')

        self.create_login_ui()

    def set_background_image(self):
        """Load and display a background image for Admin users if available."""
        if not self.current_user or self.current_user.role != "Admin":
            return

        # Try to find an image in the project folder
        image_candidates = ["lib.jpg", "lib.png", "library.jpg", "library.png", "library_bg.jpg", "library_bg.png"]
        img_path = None
        for name in image_candidates:
            if os.path.exists(name):
                img_path = name
                break
        if not HAS_PIL:
            return

        try:
            if img_path:
                img = Image.open(img_path)
            else:
                # Create a simple placeholder image with text
                img = Image.new('RGB', (900, 220), color=(240, 240, 230))
                try:
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.load_default()
                    text = "Library"
                    w, h = draw.textsize(text, font=font)
                    draw.text(((900 - w) / 2, (220 - h) / 2), text, fill=(30, 30, 30), font=font)
                except Exception:
                    pass

            # Resize to fit the main UI area width (attempt to match frame)
            try:
                target_w = max(300, self.main_frame.winfo_width())
            except Exception:
                target_w = 900
            # If frame width is not yet calculated (0 or 1), fall back to screen width
            if not target_w or target_w < 50:
                try:
                    target_w = self.root.winfo_screenwidth()
                except Exception:
                    target_w = 900
            target_h = 220
            img = img.resize((target_w, target_h), getattr(Image, "Resampling", Image).LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.main_frame, image=self.bg_photo)
            bg_label.image = self.bg_photo
            # span the main columns and fill horizontally
            bg_label.grid(row=1, column=0, columnspan=4, pady=6, sticky='ew')
        except Exception:
            return

    def set_login_background(self):
        """Load and display a background image behind the login form if available."""
        if not HAS_PIL:
            return

        image_candidates = ["image.jpg", "login.jpg", "image.png", "login.png", "images/image.jpg", "images/login.jpg"]
        img_path = None
        for name in image_candidates:
            if os.path.exists(name):
                img_path = name
                break

        try:
            if img_path:
                img = Image.open(img_path)
            else:
                return

            # Dynamically size background to the current screen/window
            try:
                screen_w = self.root.winfo_screenwidth()
                screen_h = self.root.winfo_screenheight()
            except Exception:
                screen_w, screen_h = 900, 600
            target_w = max(300, screen_w - 200)
            target_h = max(120, int(screen_h * 0.22))

            img = img.resize((target_w, target_h), getattr(Image, "Resampling", Image).LANCZOS)
            self.login_bg = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.login_frame, image=self.login_bg)
            bg_label.image = self.login_bg
            # place behind widgets and ensure it fills the login frame
            bg_label.place(relx=0.5, rely=0.5, anchor='center')
            bg_label.lower()
        except Exception:
            return

    def _set_window_icon(self):
        """Set window icon if an icon file exists (prefers .ico on Windows)."""
        icon_candidates = ["library.ico", "icon.ico", "library.png", "icon.png"]
        for ic in icon_candidates:
            if os.path.exists(ic):
                try:
                    if ic.lower().endswith('.ico'):
                        self.root.iconbitmap(ic)
                    else:
                        if HAS_PIL:
                            img = Image.open(ic)
                            img = img.resize((64, 64), getattr(Image, "Resampling", Image).LANCZOS)
                            self.icon_photo = ImageTk.PhotoImage(img)
                            try:
                                self.root.iconphoto(False, self.icon_photo)
                            except Exception:
                                pass
                except Exception:
                    pass
                break

    def create_login_ui(self):
        ttk.Label(self.login_frame, text="Login as User ID", font=("Segoe UI", 16)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.user_var = tk.StringVar()
        self.user_entry = ttk.Entry(self.login_frame, textvariable=self.user_var, width=40, font=("Segoe UI", 12))
        self.user_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Password field (optional — required only for Admin)
        ttk.Label(self.login_frame, text="Password (admin only)", font=("Segoe UI", 16)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.pwd_var = tk.StringVar()
        self.pwd_entry = ttk.Entry(self.login_frame, textvariable=self.pwd_var, width=40, show='*', font=("Segoe UI", 12))
        self.pwd_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Make the login button expand to full width of the two columns
        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=16, sticky='ew')

        # try to set a background image for the login area
        self.set_login_background()

    def login(self):
        uid = self.user_entry.get().strip()
        if uid in self.lib.users:
            user = self.lib.users[uid]
            # If admin, require password from the form
            if user.role == "Admin":
                pwd = self.pwd_var.get()
                if not pwd:
                    messagebox.showerror("Error", "Admin password is required")
                    return
                if not hasattr(user, 'password') or user.password != pwd:
                    messagebox.showerror("Error", "Incorrect password")
                    return
            self.current_user = user
            self.lib.Login(self.current_user)
            messagebox.showinfo("Login", f"Logged in as {self.current_user.name} ({self.current_user.role})")
            # hide login UI and footer, then show main UI
            try:
                self.login_frame.pack_forget()
            except Exception:
                pass
            try:
                self.footer_frame.pack_forget()
            except Exception:
                pass
            self.create_main_ui()
        else:
            messagebox.showerror("Error", "User not found")

    def create_main_ui(self):
        # make main_frame visible now that user is logged in
        try:
            # avoid double-packing if already packed
            if not self.main_frame.winfo_ismapped():
                self.main_frame.pack(fill='both', expand=True)
        except Exception:
            try:
                self.main_frame.pack(fill='both', expand=True)
            except Exception:
                pass

        # Button frame for centering
        button_frame = ttk.Frame(self.main_frame)
        # allow the button frame to stretch horizontally
        button_frame.grid(row=0, column=0, columnspan=4, pady=10, sticky='ew')
        # apply icon and background for admin users
        self._set_window_icon()
        self.set_background_image()
        
        # Buttons for actions (all in first row)
        col = 0
        # create buttons and let them expand horizontally to share the full line
        ttk.Button(button_frame, text="Show All Books", command=self.show_books).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
        col += 1
        ttk.Button(button_frame, text="Search Books", command=self.search_books).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
        col += 1
        ttk.Button(button_frame, text="Borrow Book", command=self.borrow_book).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
        col += 1
        ttk.Button(button_frame, text="Return Book", command=self.return_book).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
        col += 1

        if self.current_user.role == "Admin":
            ttk.Button(button_frame, text="Add Book", command=self.add_book).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
            col += 1
            ttk.Button(button_frame, text="Remove Book", command=self.remove_book).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
            col += 1

        ttk.Button(button_frame, text="Save Data", command=self.lib.save_data).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
        col += 1
        ttk.Button(button_frame, text="Load Data", command=self.lib.load_data).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
        col += 1
        ttk.Button(button_frame, text="Logout", command=self.logout).grid(row=0, column=col, padx=6, pady=6, sticky='ew')
        # Make each button column expand equally to fill the available width
        for i in range(max(1, col + 1)):
            button_frame.columnconfigure(i, weight=1)

        # Treeview for displaying books
        self.tree = ttk.Treeview(self.main_frame, columns=("ISBN", "Title", "Author", "Kind", "Extra", "Borrowed"), show="headings", height=18)
        for col in ("ISBN", "Title", "Author", "Kind", "Extra", "Borrowed"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140 if col == "Title" else 100)
        self.tree.grid(row=3, column=0, columnspan=4, pady=10, sticky='nsew')
        # Add vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=3, column=4, sticky='ns', pady=10)

        # Make tree expand if window resized
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

    def logout(self):
        """Log out current user and return to the login screen."""
        try:
            self.lib.current_user = None
        except Exception:
            pass

        # Hide main UI
        try:
            self.main_frame.pack_forget()
        except Exception:
            try:
                self.main_frame.grid_forget()
            except Exception:
                pass

        # Clear treeview if present
        try:
            if hasattr(self, 'tree'):
                for r in self.tree.get_children():
                    self.tree.delete(r)
        except Exception:
            pass

        # Reset login entries
        try:
            self.user_var.set('')
            self.pwd_var.set('')
        except Exception:
            pass

        # Show login frame and footer again
        try:
            self.login_frame.pack(expand=True)
        except Exception:
            try:
                self.login_frame.pack()
            except Exception:
                pass
        try:
            self.footer_frame.pack(side='bottom', fill='x')
        except Exception:
            pass

        messagebox.showinfo("Logout", "You have been logged out.")

    def show_books(self):
        # hide home panel if visible
        try:
            self.home_label.grid_forget()
        except Exception:
            pass

        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in self.lib.fetch_all_books():
            kind = "Printed" if isinstance(b, PrintedBook) else "EBook" if isinstance(b, EBook) else "Book"
            extra = f"{b.pages} pages" if isinstance(b, PrintedBook) else f"{b.file_size} MB" if isinstance(b, EBook) else "-"
            borrowed = "Yes" if getattr(b, 'borrowed', False) else "No"
            self.tree.insert("", "end", values=(b.isbn, b.title, b.author, kind, extra, borrowed))

    def show_home(self):
        """Display a simple home/welcome panel in the main area."""
        # hide tree view
        try:
            self.tree.grid_forget()
        except Exception:
            pass
        # remove existing home label if any
        try:
            self.home_label.grid_forget()
        except Exception:
            pass

        welcome = f"Welcome {self.current_user.name if self.current_user else ''} to the Library Management System"
        self.home_label = ttk.Label(self.main_frame, text=welcome, font=("Segoe UI", 14), anchor="center")
        self.home_label.grid(row=2, column=0, columnspan=4, pady=20)

    def search_books(self):
        keyword = simpledialog.askstring("Search", "Enter keyword:")
        if keyword:
            results = self.lib.search_books(keyword)
            messagebox.showinfo("Search Results", "\n".join([str(b) for b in results]) if results else "No books found.")

    def add_book(self):
        # Keep the window focused and prevent minimizing
        try:
            self.root.attributes('-topmost', True)
        except Exception:
            pass
        
        try:
            isbn = simpledialog.askstring("Add Book", "Enter ISBN:", parent=self.root)
            if not isbn:
                return
            
            title = simpledialog.askstring("Add Book", "Enter Title:", parent=self.root)
            if not title:
                return
            
            author = simpledialog.askstring("Add Book", "Enter Author:", parent=self.root)
            if not author:
                return
            
            kind = simpledialog.askstring("Add Book", "Enter Kind (printed/ebook):", parent=self.root)
            if not kind:
                messagebox.showerror("Error", "Kind is required.", parent=self.root)
                return
            
            kind = kind.lower()
            if kind == "printed":
                pages_str = simpledialog.askstring("Add Book", "Enter Number of Pages:", parent=self.root)
                if not pages_str:
                    messagebox.showerror("Error", "Number of pages is required.", parent=self.root)
                    return
                try:
                    pages = int(pages_str)
                except (ValueError, TypeError):
                    messagebox.showerror("Error", "Pages must be a valid integer.", parent=self.root)
                    return
                self.lib.add_book(PrintedBook(isbn, title, author, pages))
            elif kind == "ebook":
                size_str = simpledialog.askstring("Add Book", "Enter File Size (MB):", parent=self.root)
                if not size_str:
                    messagebox.showerror("Error", "File size is required.", parent=self.root)
                    return
                try:
                    size = float(size_str)
                except (ValueError, TypeError):
                    messagebox.showerror("Error", "File size must be a valid number.", parent=self.root)
                    return
                self.lib.add_book(EBook(isbn, title, author, size))
            else:
                messagebox.showerror("Error", "Kind must be 'printed' or 'ebook'.", parent=self.root)
                return
            
            messagebox.showinfo("Success", "Book added successfully.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}", parent=self.root)
        finally:
            # Restore window state
            try:
                self.root.attributes('-topmost', False)
            except Exception:
                pass

    def remove_book(self):
        isbn = simpledialog.askstring("Remove Book", "Enter ISBN:")
        self.lib.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed successfully.")

    def borrow_book(self):
        isbn = simpledialog.askstring("Borrow Book", "Enter ISBN:")
        if not isbn:
            return
        try:
            # perform borrow
            self.lib.borrow_book(isbn, self.current_user.user_id)
            book = self.lib.books.get(isbn)
            title = book.title if book else isbn
            user_name = self.current_user.name if self.current_user else "User"
            messagebox.showinfo("Success", f"Book {title} borrowed by {user_name}")
            self.show_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        isbn = simpledialog.askstring("Return Book", "Enter ISBN:")
        if not isbn:
            return
        try:
            self.lib.return_book(isbn)
            book = self.lib.books.get(isbn)
            title = book.title if book else isbn
            messagebox.showinfo("Success", f"{title} returned successfully.")
            self.show_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryUI(root)
    root.mainloop()