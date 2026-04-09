# COMP_GRP_50：Team Formation Platform for Group Projects(StudyMate)
COMP2090SEF GROUP PROJECT FROM GRP_50
## 📖Contents

- [Members of group and Labour of division](#members-of-group-and-labour-of-division)
- [Introduction of project](#introduction-of-project)
- [The structure of project](#the-structure-of-project)
- [Features](#features)
- [Installation and Execute](#installation-and-execute)
- [Implementation notes](#implementation-notes)
- [Contact](#contact)
  
## Members of group and Labour of division
Leader: ZHAO DongRu 14077179
- Project Framework
- Write main.py
- Write README.md and User_guide.md
- Write test_data.json
- Design and write OOP_models.py
- Design matching.py
- Revise and review two reports

members: 
1. JIANG Jun 14125968
- Design and write OOP_models.py
- Write data_manager.py
- Implement matching.py
- Assiste in writing test_data.json
- Write Study Report


2. CHUNG ChingWang 12877060 
- write GUI.py
- Design and implement OOP_models.py
- Design matching.py and assiste in its implementation
- Write Project Report


## Introduction of project

This project aims to address the challenge students face in finding teammates for course group work. Through a desktop graphical user interface application, it enables user registration and login, posting/browsing of team formation posts, and utilizes an intelligent matching algorithm to recommend the most suitable teammates for users.

To achieve optimal matching between students and project posts, the system models the problem using a **bipartite graph​ data structure**, where students and posts form two disjoint sets of vertices. The matching is solved by the **Hungarian algorithm**, which guarantees a globally optimal one-to-one assignment. Compatibility is determined by a weighted score​ that considers skills match, academic stage, language, background and school.

## The structure of project 
- `COMP_GRP_50/`  
- `main.py`              # Program entry point, initializes data and starts the GUI event loop  
- `data_manager.py`      # Handles all JSON data loading, saving, and basic queries  
- `OOP_models.py`        # OOP Core: Defines the User, Student, Post, and MatchingGraph classes  
- `matching.py`          # Core Algorithm: Constructs bipartite graphs and implements the Hungarian Algorithm for optimal matching  
- `GUI.py`               # Tkinter GUI, contains all user interaction interfaces  
- `test_data.json`       # Pre-configured test data to verify system workflows  
- `README.md`            # This file
- `User Guide.md`        # Provide detailed instructions on how to run the program
## Features
User System:  Supports user registration, login, and personal profile management.

Post Management: Enables creating, editing, deleting, and browsing team formation posts.

Intelligent Recommendation: Recommends highly compatible posts to users via a multi-dimensional scoring algorithm (considering skills, academic stage, language, background, and school).

Advanced Matching:  Integrates the Hungarian Algorithm to achieve optimal one-to-one, conflict-free assignments in specific scenarios.

Data Persistence:  Stores user and post data in JSON files.

## Installation and Execute

#### 1. Install Dependencies  
Your project uses `tkinter` and `json`:  
- `json` is a built-in Python library, **no installation required**.  
- `tkinter` is usually included as a built-in library, but if an error "tkinter not found" occurs, install as follows:  


#### 2. Check if tkinter is Already Installed  
Open a terminal in VSCode (shortcut `Ctrl + ` ` or `Terminal -> New Terminal`), enter the following command (note the space):
  ```bash
  python3 -m tkinter
  ```
- **Success**: If a test window pops up (showing "This is Tcl/Tk X.X.X" or similar), tkinter is already installed. **No further action is required**. You can run `main.py` directly.  
- **Failure**: If the error "No module named tkinter" appears, install via `pip` (for Windows/macOS):  

  Enter in the terminal:
  ```bash\
  pip install tk
#### 3. Run the Project  
Ensure that `test_data.json` and `main.py` are in matching paths (refer to the directory structure explanation above), then run the following command in the VSCode terminal:
  ```bash
  python3 main.py
  ```

#### 4.Input data
We have already set up a dedicated test user. So when you access the Login/Register page, you can simply enter test_user​ in the username field and test12​ in the password field. After clicking the login button, you will successfully enter the program.

 username:
 ```
 test_user
 ```
 password:
 ```
 test12
 ```

 

## Implementation notes

#### 1.Algorithm Implementation 

The core matching algorithm in matching.pyis implemented based on the standard Hungarian algorithm (Kuhn–Munkres algorithm) for solving the assignment problem. The structure and steps of the HungarianSolverclass (including matrix reduction, zero covering, and augmenting path search) follow the canonical description of this algorithm. This foundational implementation was adapted and integrated into the project's specific context of bipartite graph matching between users and posts.

#### 2.Use of AI Programming Assistant

-Documentation & Comments: Helping to draft clear, concise module-level and inline comments to improve code maintainability and explain key algorithmic steps.

-Code Optimization: Assisting in refining function interfaces and improving the robustness of data validation logic.

## Contact
If you have any problems about the group project, please email the leader `s1407717@live.hkmu.edu.hk`.
  
