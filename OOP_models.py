from typing import List, Optional, Dict, Any

# StudyMate data models: define User, Post and a bipartite MatchingGraph
# Goal: provide clean objects for recommender/assignment without worrying about field glue

ALLOWED_SCHOOLS = [
    "School of Arts and Social Sciences",
    "Lee Shau Kee School of Business and Administration",
    "School of Business",
    "School of Education and Languages",
    "School of Nursing and Health Studies",
    "School of Science and Technology",
    "School of Humanities and Social Sciences",
]

ALLOWED_BACKGROUNDS = [
    "mainland_student",
    "local_student",
    "international_student",
]

ALLOWED_LANGUAGES = [
    "Mandarin",
    "Cantonese",
    "English",
]

ALLOWED_SKILLS = [
    "Python Programming",
    "Machine Learning",
    "Algorithm Design",
    "Data Analysis",
    "Machine Learning Fundamentals",
    "Business Analysis",
    "PPT Presentation",
    "Market Research",
    "Financial Statement",
    "Report Writing",
    "Java Development",
    "UI Design",
    "Database Management",
    "React",
    "Documentation",
    "Academic Writing",
    "Qualitative Research",
    "Video Editing",
    "Git Version Control",
    "SPSS",
]

SKILL_SYNONYMS: Dict[str, str] = {
    "SPSS Analysis": "SPSS",
}

def _normalize_skill(name: str) -> str:
    return SKILL_SYNONYMS.get(name, name)


class User:
    # User: used for login, posting and receiving recommendations
    def __init__(
        self,
        username: str,
        password: str,
        background: str,
        school: str,
        academic_stage: str,
        skills: Optional[List[str]] = None,
        languages: Optional[List[str]] = None,
    ) -> None:
        # Password rule: exactly 6 alphanumeric characters (simple and consistent)
        if not isinstance(password, str) or len(password) != 6 or not password.isalnum():
            raise ValueError("invalid password: must be 6 alphanumeric characters")
        if school not in ALLOWED_SCHOOLS:
            raise ValueError(f"invalid school: {school}")
        if background not in ALLOWED_BACKGROUNDS:
            raise ValueError(f"invalid background: {background}")
        # Store basic info; normalize skill names to avoid mismatches caused by synonyms
        self.username = username
        self.password = password
        self.background = background
        self.school = school
        self.academic_stage = academic_stage
        norm_skills = [_normalize_skill(s) for s in (skills or [])]
        self.skills = list(norm_skills)
        self.languages = list(languages or [])
        invalid_skills = [x for x in self.skills if x not in ALLOWED_SKILLS]
        if invalid_skills:
            raise ValueError(f"invalid skills: {invalid_skills}")
        invalid_langs = [x for x in self.languages if x not in ALLOWED_LANGUAGES]
        if invalid_langs:
            raise ValueError(f"invalid languages: {invalid_langs}")

    def display_info(self):
        # Handy for console/debug prints
        return f"{self.username} ({self.background})"

    def to_dict(self):
        # Serialize user to dict for saving/transport
        return {
            "username": self.username,
            "password": self.password,
            "background": self.background,
            "school": self.school,
            "academic_stage": self.academic_stage,
            "skills": list(self.skills),
            "languages": list(self.languages),
        }

    @classmethod
    def from_dict(cls, data):
        # Build user from dict; contact email is kept on posts, not user
        return cls(
            username=data.get("username", ""),
            password=data.get("password", ""),
            background=data.get("background", ""),
            school=data.get("school", ""),
            academic_stage=data.get("academic_stage", ""),
            skills=[_normalize_skill(s) for s in list(data.get("skills", []))],
            languages=list(data.get("languages", [])),
        )


class Post:
    # Post: for team-up/recruitment; describes course, requirements, slots, etc.
    def __init__(
        self,
        course: str,
        title: str,
        description: str,
        required_skills: Optional[List[str]] = None,
        required_languages: Optional[List[str]] = None,
        remaining_slots: int = 0,
        deadline: Optional[str] = None,
        special_requirements: Optional[str] = None,
        publish_time: Optional[str] = None,
        is_active: bool = True,
        publisher_username: Optional[str] = None,
        contact_email: Optional[str] = None,
    ) -> None:
        # Init content and requirements; contact email lives on the post for communication
        self.course = course
        self.title = title
        self.description = description
        self.required_skills = list(required_skills or [])
        self.required_languages = list(required_languages or [])
        self.remaining_slots = int(remaining_slots)
        self.deadline = deadline
        self.special_requirements = special_requirements
        self.publish_time = publish_time
        self.is_active = bool(is_active)
        self.publisher_username = publisher_username or ""
        self.contact_email = (contact_email or "").strip()

    def to_dict(self):
        # Export to dict for saving/debugging
        return {
            "course": self.course,
            "title": self.title,
            "description": self.description,
            "required_skills": list(self.required_skills),
            "required_languages": list(self.required_languages),
            "remaining_slots": int(self.remaining_slots),
            "deadline": self.deadline,
            "special_requirements": self.special_requirements,
            "publish_time": self.publish_time,
            "is_active": bool(self.is_active),
            "publisher_username": self.publisher_username,
            "contact_email": self.contact_email,
        }

    @classmethod
    def from_dict(cls, data, publisher_username=None):
        # Create post from dict; inject publisher username if provided
        return cls(
            course=data.get("course", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            required_skills=[_normalize_skill(s) for s in list(data.get("required_skills", []))],
            required_languages=list(data.get("required_languages", [])),
            remaining_slots=int(data.get("remaining_slots", 0)),
            deadline=data.get("deadline"),
            special_requirements=data.get("special_requirements"),
            publish_time=data.get("publish_time"),
            is_active=bool(data.get("is_active", True)),
            publisher_username=data.get("publisher_username", publisher_username or ""),
            contact_email=str(data.get("contact_email", "") or ""),
        )


class MatchingGraph:
    # MatchingGraph: users and posts form a bipartite graph used for scoring/assignment
    def __init__(self, users, posts):
        # Keep references to users and posts; later steps compute match relations
        self.users = users
        self.posts = posts
        self.adjacency = {}
        self.score_matrix = []
        self.valid_posts = []

    def build_adjacency(self):
        # Strict edges: connect only if both skills and languages are satisfied
        result = {}
        for u in self.users:
            idxs = []
            for i, p in enumerate(self.posts):
                if not p.is_active:
                    continue
                if p.remaining_slots <= 0:
                    continue
                skills_ok = all(req in u.skills for req in p.required_skills)
                langs_ok = all(req in u.languages for req in p.required_languages)
                if skills_ok and langs_ok:
                    idxs.append(i)
            result[u.username] = idxs
        self.adjacency = result
        return result

    def to_dict(self):
        # Export users, posts and current adjacency
        return {
            "users": [u.to_dict() for u in self.users],
            "posts": [p.to_dict() for p in self.posts],
            "adjacency": {k: list(v) for k, v in self.adjacency.items()},
        }

    @classmethod
    def from_dict(cls, data):
        # Restore graph from dict (used for persistence/debugging)
        users_data = data.get("users", [])
        posts_data = data.get("posts", [])
        users = [User.from_dict(u) for u in users_data]
        posts = [Post.from_dict(p) for p in posts_data]
        graph = cls(users, posts)
        graph.adjacency = {k: list(v) for k, v in data.get("adjacency", {}).items()}
        return graph

    def build_score_matrix(self, owners_map, calculator):
        # Compute user–post scores on the graph and cache matrix for the Hungarian solver
        self.valid_posts = [
            p for p in self.posts
            if getattr(p, "is_active", True) and int(getattr(p, "remaining_slots", 0)) > 0
        ]
        m = []
        score_adj = {}
        for u in self.users:
            row = []
            per_user = {}
            for idx, p in enumerate(self.valid_posts):
                owner = owners_map.get(getattr(p, "publisher_username", ""))
                s = calculator(u, p, owner) if owner else 0.0
                row.append(s)
                per_user[idx] = s
            m.append(row)
            score_adj[u.username] = per_user
        self.score_matrix = m
        self.adjacency = score_adj
        return m, self.valid_posts
