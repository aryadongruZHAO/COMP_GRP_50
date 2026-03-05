import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from OOP_models import User, Post, ALLOWED_BACKGROUNDS, ALLOWED_SCHOOLS, ALLOWED_LANGUAGES, ALLOWED_SKILLS
from data_manager import query
from matching import get_recommendations


class LoginWindow(tk.Toplevel):
    def __init__(self, root, all_users, all_posts):
        super().__init__(root)
        self.root = root
        self.all_users = all_users
        self.all_posts = all_posts
        self.current_user = None
        self.title("StudyMate - Login")
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Label(frm, text="Username").pack(anchor="w")
        self.username_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.username_var).pack(fill="x", pady=4)
        ttk.Label(frm, text="Password").pack(anchor="w")
        self.password_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.password_var, show="*").pack(fill="x", pady=4)
        btns = ttk.Frame(frm)
        btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="Login", command=self._on_login).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(btns, text="Register", command=self._on_register).pack(side="left", expand=True, fill="x", padx=4)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _on_login(self):
        u = self.username_var.get().strip()
        p = self.password_var.get().strip()
        user = None
        for x in self.all_users:
            if x.username == u and x.password == p:
                user = x
                break
        if not user:
            messagebox.showerror("Error", "Incorrect username or password")
            return
        self.current_user = user
        self.destroy()
        MainWindow(self.root, self.current_user, self.all_users, self.all_posts)

    def _on_register(self):
        self.destroy()
        RegisterWindow(self.root, self.all_users, self.all_posts)


class RegisterWindow(tk.Toplevel):
    def __init__(self, root, all_users, all_posts):
        super().__init__(root)
        self.root = root
        self.all_users = all_users
        self.all_posts = all_posts
        self.title("StudyMate - Register")
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=12, pady=14)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.stage = tk.StringVar()
        self.background = tk.StringVar(value=ALLOWED_BACKGROUNDS[0] if ALLOWED_BACKGROUNDS else "")
        self.school = tk.StringVar(value=ALLOWED_SCHOOLS[0] if ALLOWED_SCHOOLS else "")
        # Place widgets one by one for clarity
        ttk.Label(frm, text="Username").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.username).pack(fill="x", pady=3)

        ttk.Label(frm, text="Password").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.password, show="*").pack(fill="x", pady=5)

        ttk.Label(frm, text="Academic Stage").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.stage).pack(fill="x", pady=7)

        ttk.Label(frm, text="Background").pack(anchor="w")
        ttk.Combobox(frm, values=ALLOWED_BACKGROUNDS, textvariable=self.background, state="readonly").pack(fill="x", pady=4)

        ttk.Label(frm, text="School").pack(anchor="w")
        ttk.Combobox(frm, values=ALLOWED_SCHOOLS, textvariable=self.school, state="readonly").pack(fill="x", pady=9)

        ttk.Label(frm, text="Skills (multi-select)").pack(anchor="w")
        skills_height = min(12, max(6, len(ALLOWED_SKILLS) // 3 or 6))
        self.skills_lb = tk.Listbox(frm, selectmode=tk.MULTIPLE, height=skills_height)
        for s in ALLOWED_SKILLS:
            self.skills_lb.insert(tk.END, s)
        self.skills_lb.pack(fill="x", pady=6)

        ttk.Label(frm, text="Languages (multi-select)").pack(anchor="w")
        langs_height = min(6, max(3, len(ALLOWED_LANGUAGES)))
        self.languages_lb = tk.Listbox(frm, selectmode=tk.MULTIPLE, height=langs_height)
        for l in ALLOWED_LANGUAGES:
            self.languages_lb.insert(tk.END, l)
        self.languages_lb.pack(fill="x", pady=4)

        btns = ttk.Frame(frm)
        btns.pack(fill="x", pady=10)
        ttk.Button(btns, text="Submit", command=self._on_submit).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(btns, text="Back to Login", command=self._on_back).pack(side="left", expand=True, fill="x", padx=4)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _on_submit(self):
        try:
            skills = [self.skills_lb.get(i) for i in self.skills_lb.curselection()]
            languages = [self.languages_lb.get(i) for i in self.languages_lb.curselection()]
            user = User(
                username=self.username.get().strip(),
                password=self.password.get().strip(),
                background=self.background.get().strip(),
                school=self.school.get().strip(),
                academic_stage=self.stage.get().strip(),
                skills=skills,
                languages=languages,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
            return
        self.all_users.append(user)
        messagebox.showinfo("Success", "Registration successful. You are now logged in.")
        self.destroy()
        MainWindow(self.root, user, self.all_users, self.all_posts)

    def _on_back(self):
        self.destroy()
        LoginWindow(self.root, self.all_users, self.all_posts)


class MainWindow(tk.Toplevel):
    def __init__(self, root, current_user, all_users, all_posts):
        super().__init__(root)
        self.root = root
        self.current_user = current_user
        self.all_users = all_users
        self.all_posts = all_posts
        self.title(f"StudyMate - Main Page (Welcome,{self.current_user.username})")
        ttk.Button(self, text="📝 My Posts", command=self._open_my_posts).pack(fill="x", padx=8, pady=6)
        ttk.Button(self, text="🚀 Intelligent Recommendations", command=self._open_recommendations).pack(fill="x", padx=8, pady=6)
        ttk.Button(self, text="➜ Exit", command=self._quit).pack(fill="x", padx=8, pady=6)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _open_my_posts(self):
        self.destroy()
        MyPostsWindow(self.root, self.current_user, self.all_users, self.all_posts)

    def _open_recommendations(self):
        self.destroy()
        RecommendationWindow(self.root, self.current_user, self.all_users, self.all_posts)

    def _quit(self):
        self.destroy()
        try:
            self.root.destroy()
        except:
            pass


class MyPostsWindow(tk.Toplevel):
    def __init__(self, root, current_user, all_users, all_posts):
        super().__init__(root)
        self.root = root
        self.current_user = current_user
        self.all_users = all_users
        self.all_posts = all_posts
        self.title("My Posts")
        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(fill="both", expand=True, padx=8, pady=6)
        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=8, pady=6)
        ttk.Button(btns, text="Create Post", command=self._create_post).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(btns, text="View / Edit", command=self._edit_selected).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(btns, text="Back to Home", command=self._back_main).pack(side="left", expand=True, fill="x", padx=4)
        self._refresh_list()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for p in self.all_posts:
            if getattr(p, "publisher_username", "") == self.current_user.username:
                tag = "Active" if getattr(p, "is_active", True) else "Inactive"
                self.listbox.insert(tk.END, f"{p.title} [{tag}]")

    def _get_selected_post(self):
        idx = self.listbox.curselection()
        if not idx:
            return None
        title_text = self.listbox.get(idx[0]).split(" [")[0]
        for p in self.all_posts:
            if getattr(p, "publisher_username", "") == self.current_user.username and p.title == title_text:
                return p
        return None

    def _create_post(self):
        PostEditorWindow(self.root, self.current_user, self.all_users, self.all_posts, mode="create")

    def _edit_selected(self):
        p = self._get_selected_post()
        if not p:
            messagebox.showerror("Error", "Please select a post first")
            return
        PostEditorWindow(self.root, self.current_user, self.all_users, self.all_posts, mode="edit", post=p)

    def _back_main(self):
        self.destroy()
        MainWindow(self.root, self.current_user, self.all_users, self.all_posts)


class PostEditorWindow(tk.Toplevel):
    def __init__(self, root, current_user, all_users, all_posts, mode="create", post=None):
        super().__init__(root)
        self.root = root
        self.current_user = current_user
        self.all_users = all_users
        self.all_posts = all_posts
        self.mode = mode
        self.post = post
        self.title("Create New Post" if mode == "create" else "Edit Post")
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=12, pady=14)
        # Place inputs in order for clarity
        self.course_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.desc_text = tk.Text(frm, height=4)  # Use multi-line for description
        self.slots_var = tk.StringVar()
        self.deadline_var = tk.StringVar()
        self.spec_req_var = tk.StringVar()
        self.contact_email_var = tk.StringVar()

        ttk.Label(frm, text="course").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.course_var).pack(fill="x", pady=3)

        ttk.Label(frm, text="title").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.title_var).pack(fill="x", pady=5)

        ttk.Label(frm, text="description").pack(anchor="w")
        self.desc_text.pack(fill="x", pady=7)

        ttk.Label(frm, text="remaining_slots").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.slots_var).pack(fill="x", pady=4)

        ttk.Label(frm, text="deadline").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.deadline_var).pack(fill="x", pady=3)

        ttk.Label(frm, text="special_requirements").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.spec_req_var).pack(fill="x", pady=6)

        ttk.Label(frm, text="contact_email").pack(anchor="w")
        ttk.Entry(frm, textvariable=self.contact_email_var).pack(fill="x", pady=5)

        ttk.Label(frm, text="required_skills (multi-select)").pack(anchor="w")
        skills_height = min(12, max(6, len(ALLOWED_SKILLS) // 3 or 6))
        self.skills_lb = tk.Listbox(frm, selectmode=tk.MULTIPLE, height=skills_height)
        for s in ALLOWED_SKILLS:
            self.skills_lb.insert(tk.END, s)
        self.skills_lb.pack(fill="x", pady=6)
        ttk.Label(frm, text="required_languages (multi-select)").pack(anchor="w")
        langs_height = min(6, max(3, len(ALLOWED_LANGUAGES)))
        self.languages_lb = tk.Listbox(frm, selectmode=tk.MULTIPLE, height=langs_height)
        for l in ALLOWED_LANGUAGES:
            self.languages_lb.insert(tk.END, l)
        self.languages_lb.pack(fill="x", pady=4)
        btns = ttk.Frame(frm)
        btns.pack(fill="x", pady=10)
        ttk.Button(btns, text="Save", command=self._on_save).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="left", expand=True, fill="x", padx=4)
        if self.mode == "edit" and self.post:
            self._populate_from_post()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _populate_from_post(self):
        self.course_var.set(self.post.course)
        self.title_var.set(self.post.title)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert(tk.END, self.post.description or "")
        self.slots_var.set(str(self.post.remaining_slots))
        self.deadline_var.set(self.post.deadline or "")
        self.spec_req_var.set(self.post.special_requirements or "")
        self.contact_email_var.set(getattr(self.post, "contact_email", "") or "")
        for i, s in enumerate(ALLOWED_SKILLS):
            if s in getattr(self.post, "required_skills", []):
                self.skills_lb.selection_set(i)
        for i, l in enumerate(ALLOWED_LANGUAGES):
            if l in getattr(self.post, "required_languages", []):
                self.languages_lb.selection_set(i)

    def _on_save(self):
        try:
            remaining_slots = int(self.slots_var.get().strip() or "0")
        except ValueError:
            messagebox.showerror("Error", "remaining_slots must be a number")
            return
        data = {
            "course": self.course_var.get().strip(),
            "title": self.title_var.get().strip(),
            "description": self.desc_text.get("1.0", tk.END).strip(),
            "required_skills": [self.skills_lb.get(i) for i in self.skills_lb.curselection()],
            "required_languages": [self.languages_lb.get(i) for i in self.languages_lb.curselection()],
            "remaining_slots": remaining_slots,
            "deadline": self.deadline_var.get().strip() or None,
            "special_requirements": self.spec_req_var.get().strip() or None,
            "is_active": True,
            "contact_email": self.contact_email_var.get().strip(),
        }
        if not data["contact_email"]:
            messagebox.showerror("Error", "Please fill in contact_email")
            return
        if self.mode == "create":
            p = Post.from_dict(data, publisher_username=self.current_user.username)
            self.all_posts.append(p)
            messagebox.showinfo("Success", "Post created successfully")
        else:
            self.post.course = data["course"]
            self.post.title = data["title"]
            self.post.description = data["description"]
            self.post.required_skills = data["required_skills"]
            self.post.required_languages = data["required_languages"]
            self.post.remaining_slots = data["remaining_slots"]
            self.post.deadline = data["deadline"]
            self.post.special_requirements = data["special_requirements"]
            self.post.is_active = data["is_active"]
            self.post.contact_email = data["contact_email"]
            messagebox.showinfo("Success", "Post updated successfully")
        self.destroy()


class RecommendationWindow(tk.Toplevel):
    def __init__(self, root, current_user, all_users, all_posts):
        super().__init__(root)
        self.root = root
        self.current_user = current_user
        self.all_users = all_users
        self.all_posts = all_posts
        self.title("Recommendations")
        self.text = scrolledtext.ScrolledText(self, width=80, height=24)
        self.text.pack(fill="both", expand=True, padx=10, pady=6)
        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=10, pady=8)
        ttk.Button(btns, text="Refresh", command=self._refresh).pack(side="left", padx=4)
        ttk.Button(btns, text="Back to Home", command=self._back_main).pack(side="right", padx=4)
        self._refresh()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _refresh(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        recs = get_recommendations(self.current_user, self.all_posts, self.all_users)
        for post, score in recs:
            level = "👍👍👍Highly Matched" if score >= 80 else ("✅✅Well Matched" if score >= 60 else "⚪️Average Match")
            block = []
            block.append(f"[{score:.2f}] {level}")
            block.append(f"Course: {post.course}")
            block.append(f"Title: {post.title}")
            block.append(f"Description: {post.description}")
            block.append(f"Required Skills: {', '.join(post.required_skills) or 'None'}")
            block.append(f"Required Languages: {', '.join(post.required_languages) or 'None'}")
            block.append(f"Remaining Slots: {post.remaining_slots}")
            block.append(f"Deadline: {post.deadline or 'None'}")
            contact_email = getattr(post, 'contact_email', '') or 'Not provided'
            block.append(f"Contact Email: {contact_email if contact_email else 'Not provided'}")
            self.text.insert(tk.END, "\n".join(block) + "\n" + "-" * 30 + "\n")
        self.text.configure(state="disabled")

    def _back_main(self):
        self.destroy()
        MainWindow(self.root, self.current_user, self.all_users, self.all_posts)
