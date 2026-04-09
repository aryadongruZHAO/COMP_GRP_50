# StudyMate User Guide 
COMP2090SEF GROUP PROJECT FROM GRP_50

This guide helps you set up, run, and use the StudyMate application — a tool that uses **bipartite graphs​** and the **Hungarian algorithm**​ to match students with study group posts (or projects) based on compatibility.

## 1. Prerequisites
- Python 3.8+ installed on your system.

- Basic familiarity with running Python scripts in a terminal.

## 2. Installation & Setup
### 2.1 Install Dependencies

StudyMate uses two key libraries:
- `tkinte`: Python’s GUI library (often bundled with Python on Windows/macOS).

- `json`: Python’s built-in library for JSON data handling (no installation needed).

If tkinter is missing (e.g., error: No module named 'tkinter' ), install it using a system-appropriate method:


- **Linux (Ubuntu/Debian)**:
  ```bash\
  sudo apt-get install python3-tk
  ```
  
- **Windows/macOS**： 
  - Tkinter is usually included with the official Python installer.
    
  - If it is missing, reinstall Python from the official source and make sure Tcl/Tk (Tkinter) support is included.
    
### 2.2 Verify tkinter Installation
To confirm tkinterworks:
1. Open a terminal (e.g., in VSCode: Terminal → New Terminal).

2. Run:
  ```bash\
  python3 -m tkinter
  ```

3. A test window (showing “This is Tcl/Tk X.X.X”) should appear. If so, `tkinter` is ready.

## 3. Running the Application
1.Open a terminal in the StudyMateproject directory.

2.Run:
  ```bash\
  python3 main.py
  ```

3.A GUI window will launch (powered by `GUI.py` and `tkinter` ).

## 4.Input Data & Testing

We provide a pre-configured test user to help you explore the app.

### 4.1 Test Credentials
- Username:
  ```bash\
  test_user
  ```

- Password:
  ```bash\
  test12
  ```

### 4.2 How to Use the Test Account
1. After launching the app, you’ll see a Login/Register​ page.

2. Enter `test_user` in the Username field and `test12` in the Password field.

3. Click Login — you’ll be redirected to the main application interface.

## 5.Using StudyMate (Key Features)
Once you log in, you will see the StudyMate main page with these options:
### 5.1 Manage Your Posts (Create / Edit)
- Click “📝 My Posts” to view the posts published by your account.
- In My Posts , you can:
  - Click “Create Post” to publish a new post.
  - Select a post and click “View / Edit” to update it.
-When creating/editing a post, you can set:
  - `course` , `title` , `description`
  - `remaining_slots` , `deadline` , `special_requirements`
  - `contact_email `(required)
  - `required_skills` and `required_languages`(multi-select)
### 5.2 Get Intelligent Recommendations (Score-Based)
- Click “🚀 Intelligent Recommendations” to open the recommendation page.
- StudyMate will recommend active posts with remaining slots and show a ranked list with a compatibility score (0–100) .
- Each recommendation block includes:
  - Score + match level label (e.g., Highly Matched / Well Matched / Average Match)
  - Post details (course, title, description, required skills/languages, remaining slots, deadline)
  -  Contact Email (from the post)
- Click “Refresh” to re-calculate recommendations.
### 5.3 Exit
- Click “➜ Exit” to close the application.
## 6. Data Persistence
StudyMate loads preset users and posts from `test_data.json` at startup (via `data_manager.py` ).

At the moment, the GUI does not automatically save changes back to the JSON file . This means any new registrations or post edits exist only during the current run . If you close and re-open the app, the data will be reset to what is in `test_data.json` .

## 7.Troubleshooting
“tkinter not found” / `ModuleNotFoundError: tkinter`
- Tkinter is usually bundled with Python on Windows/macOS, but may be missing on some Linux setups.
- Fix (Linux): install the system package for Tkinter (for example `python3-tk` ), then re-run the app.
- Note: `pip install tk` often does not fix Tkinter, because Tkinter is a system dependency.

App won’t start / crashes immediately
- Make sure you run the correct entry file: `python main.py`
- Confirm you are using Python 3
- Ensure these files are in the same project folder: `main.py` , `GUI.py` , `matching.py` , `OOP_models.py`, `data_manager.py` , and `test_data.json`
  
Load Error: Failed to load data
- The app loads data from `test_data.json` at startup.
- Check that `test_data.json` exists in the same directory as `main.py` and the JSON format is valid (no missing commas / brackets).
- 
No recommendations shown
- Recommendations only consider posts where `is_active = true` and `remaining_slots > 0` .
- If all posts are inactive/full, the recommendation page will be empty.

## 8. Support

If you need help, contact me: ZHAO Dong RU `s1407717@live.hkmu.edu.hk`.
