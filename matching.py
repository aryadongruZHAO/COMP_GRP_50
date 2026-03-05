from OOP_models import MatchingGraph

# This module handles recommendations and optimal assignment
# Idea: score user–post pairs first, then use the Hungarian algorithm for 1-to-1 optimal matching


def calculate_match_score(student, post, post_owner):
    # Score 0–100 by fixed weights; empty requirements treated as full score
    # Weights: skills 35%, academic stage 25%, languages 15%, background diversity 15%, school 10%
    if not getattr(post, "is_active", True) or int(getattr(post, "remaining_slots", 0)) <= 0:
        return 0.0
    req_skills = list(getattr(post, "required_skills", []) or [])
    stu_skills = list(getattr(student, "skills", []) or [])
    skills_ratio = 1.0 if len(req_skills) == 0 else len(set(req_skills) & set(stu_skills)) / float(len(set(req_skills)))
    req_langs = list(getattr(post, "required_languages", []) or [])
    stu_langs = list(getattr(student, "languages", []) or [])
    langs_ratio = 1.0 if len(req_langs) == 0 else len(set(req_langs) & set(stu_langs)) / float(len(set(req_langs)))
    stage_match = 1.0 if getattr(student, "academic_stage", "") == getattr(post_owner, "academic_stage", "") else 0.0
    bg_diversity = 1.0 if getattr(student, "background", "") != getattr(post_owner, "background", "") else 0.0
    school_match = 1.0 if getattr(student, "school", "") == getattr(post_owner, "school", "") else 0.0
    score = (
        skills_ratio * 35.0 +
        stage_match * 25.0 +
        langs_ratio * 15.0 +
        bg_diversity * 15.0 +
        school_match * 10.0
    )
    return round(max(0.0, min(100.0, score)), 2)


def _filter_active_posts(posts):
    # Keep only active posts with remaining slots
    return [
        p for p in posts
        if getattr(p, "is_active", True) and int(getattr(p, "remaining_slots", 0)) > 0
    ]


def get_recommendations(current_user, all_posts, all_users):
    # Recommend posts for current user: keep score >= 50, sort by score desc
    owners = {getattr(u, "username", ""): u for u in all_users}
    valid_posts = _filter_active_posts(all_posts)
    graph = MatchingGraph([current_user], valid_posts)  # organize as bipartite graph
    # Compute scores for each post directly
    recs = []
    for p in valid_posts:
        owner = owners.get(getattr(p, "publisher_username", ""))
        if not owner:
            continue
        s = calculate_match_score(current_user, p, owner)
        if s >= 50.0:
            recs.append((p, s))
    recs.sort(key=lambda x: x[1], reverse=True)
    return recs


def _pad_matrix_for_hungarian(matrix, pad_value):
    # Pad matrix to square for the Hungarian algorithm
    n_rows = len(matrix)
    n_cols = len(matrix[0]) if matrix else 0
    n = max(n_rows, n_cols)
    sq = [row[:] + [pad_value] * (n - n_cols) for row in matrix]
    for _ in range(n - n_rows):
        sq.append([pad_value] * n)
    return sq, n_rows, n_cols


class HungarianSolver:
    # Solve minimum-cost 1-to-1 matching on a bipartite graph using Hungarian (Kuhn–Munkres)
    def __init__(self, cost):
        self.cost, self.orig_r, self.orig_c = _pad_matrix_for_hungarian(cost, pad_value=10_000)
        self.n = len(self.cost)
        self.mask = [[0] * self.n for _ in range(self.n)]
        self.row_cover = [False] * self.n
        self.col_cover = [False] * self.n

    def _reduce_matrix(self):
        for r in range(self.n):
            m = min(self.cost[r])
            for c in range(self.n):
                self.cost[r][c] -= m
        for c in range(self.n):
            m = min(self.cost[r][c] for r in range(self.n))
            for r in range(self.n):
                self.cost[r][c] -= m

    def _cover_initial_stars(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.cost[r][c] == 0 and not self.row_cover[r] and not self.col_cover[c]:
                    self.mask[r][c] = 1
                    self.row_cover[r] = True
                    self.col_cover[c] = True
        self.row_cover = [False] * self.n
        self.col_cover = [False] * self.n
        for r in range(self.n):
            for c in range(self.n):
                if self.mask[r][c] == 1:
                    self.col_cover[c] = True

    def _find_a_zero(self):
        for r in range(self.n):
            if not self.row_cover[r]:
                for c in range(self.n):
                    if not self.col_cover[c] and self.cost[r][c] == 0:
                        return r, c
        return None, None

    def _find_star_in_row(self, row):
        for c in range(self.n):
            if self.mask[row][c] == 1:
                return c
        return None

    def _find_star_in_col(self, col):
        for r in range(self.n):
            if self.mask[r][col] == 1:
                return r
        return None

    def _find_prime_in_row(self, row):
        for c in range(self.n):
            if self.mask[row][c] == 2:
                return c
        return None

    def _augment_path(self, path):
        for r, c in path:
            if self.mask[r][c] == 1:
                self.mask[r][c] = 0
            elif self.mask[r][c] == 2:
                self.mask[r][c] = 1

    def _clear_covers(self):
        for i in range(self.n):
            self.row_cover[i] = False
            self.col_cover[i] = False

    def _erase_primes(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.mask[r][c] == 2:
                    self.mask[r][c] = 0

    def solve(self):
        # Main steps: reduce rows/cols → cover zeros → find augmenting path → repeat until optimal
        self._reduce_matrix()
        self._cover_initial_stars()
        while sum(1 for c in range(self.n) if self.col_cover[c]) < self.n:
            r, c = self._find_a_zero()
            while r is None:
                min_uncovered = min(
                    self.cost[i][j]
                    for i in range(self.n) if not self.row_cover[i]
                    for j in range(self.n) if not self.col_cover[j]
                )
                for i in range(self.n):
                    if self.row_cover[i]:
                        for j in range(self.n):
                            self.cost[i][j] += min_uncovered
                for j in range(self.n):
                    if not self.col_cover[j]:
                        for i in range(self.n):
                            self.cost[i][j] -= min_uncovered
                r, c = self._find_a_zero()
            self.mask[r][c] = 2
            star_col = self._find_star_in_row(r)
            if star_col is not None:
                self.row_cover[r] = True
                self.col_cover[star_col] = False
            else:
                path = [(r, c)]
                done = False
                while not done:
                    star_row = self._find_star_in_col(path[-1][1])
                    if star_row is None:
                        done = True
                    else:
                        path.append((star_row, path[-1][1]))
                        prime_col = self._find_prime_in_row(star_row)
                        path.append((star_row, prime_col))
                self._augment_path(path)
                self._clear_covers()
                self._erase_primes()
                for rr in range(self.n):
                    for cc in range(self.n):
                        if self.mask[rr][cc] == 1:
                            self.col_cover[cc] = True
        assignment = []
        for r in range(self.orig_r):
            for c in range(self.orig_c):
                if self.mask[r][c] == 1:
                    assignment.append((r, c))
        return assignment


def build_score_matrix(users, posts, all_users):
    # Build score matrix (0–100) for each user against each valid post
    owners = {getattr(u, "username", ""): u for u in all_users}
    valid_posts = _filter_active_posts(posts)
    graph = MatchingGraph(users, valid_posts)  # organize user–post as bipartite graph
    m = []
    for s in users:
        row = []
        for p in valid_posts:
            owner = owners.get(getattr(p, "publisher_username", ""))
            if not owner:
                row.append(0.0)
            else:
                row.append(calculate_match_score(s, p, owner))
        m.append(row)
    return m, valid_posts


def assign_optimal(users, posts, all_users):
    # Optimal assignment: convert scores to costs (100-score), solve with Hungarian algorithm
    # Returns a list of (User, Post, score) sorted by score descending
    scores, valid_posts = build_score_matrix(users, posts, all_users)
    cost = [[100.0 - x for x in row] for row in scores]
    solver = HungarianSolver(cost)
    assignment = solver.solve()
    result = []
    for r, c in assignment:
        result.append((users[r], valid_posts[c], round(scores[r][c], 2)))
    result.sort(key=lambda x: x[2], reverse=True)
    return result
