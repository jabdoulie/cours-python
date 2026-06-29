## **Introduction to Version Control and Git**

### **1. What is Version Control?**

- **Definition:**
  - A system that records changes to files over time so that you can recall specific versions later.
- **Purpose:**
  - Track the history of changes.
  - Collaborate with multiple developers.
  - Restore previous versions in case of errors.

### **2. Types of Version Control Systems**

- **Local Version Control Systems:**
  - Store revisions on a local hard disk.
  - Simple but limited in collaboration.
- **Centralized Version Control Systems (CVCS):**
  - Example: Subversion (SVN), Perforce.
  - Single server contains all the versioned files.
  - Collaboration over a network.
  - **Limitations:**
    - Single point of failure.
    - Network dependency.
- **Distributed Version Control Systems (DVCS):**
  - Example: **Git**, Mercurial.
  - Every contributor has a local copy of the entire repository.
  - **Advantages:**
    - No single point of failure.
    - Offline work capabilities.
    - Enhanced collaboration.

### **3. Introduction to Git**

- **What is Git?**
  - A distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
- **History:**
  - Created by Linus Torvalds in 2005 for Linux kernel development.
- **Key Features:**
  - **Distributed Architecture:**
    - Each developer has a full copy of the repository.
  - **Performance:**
    - Optimized for speed.
  - **Security:**
    - Uses SHA-1 hashing to identify and verify content.
  - **Flexibility:**
    - Supports non-linear development workflows.

---

## **Key Concepts in Git**

### **1. Repositories**

- **Local Repository:**
  - The `.git` directory in your project folder.
  - Contains all of the necessary metadata and object database.
- **Remote Repository:**
  - Hosted on a server (e.g., GitHub, GitLab, Bitbucket).
  - Used for collaboration.


### **2. Branches**

- **Definition:**
  - A movable pointer to a commit.
- **Default Branch:**
  - `master` or `main` (modern default).
- **Purpose:**
  - Facilitate parallel development.
  - Isolate features, bug fixes, or experiments.



### **3. Workflows**

- **Centralized Workflow:**
  - All changes are committed to the main branch.
- **Feature Branch Workflow:**
  - Use branches to develop features independently.
- **Gitflow Workflow:**
  - Defines strict branching model (feature, develop, release, hotfix branches).

---

## **Slide 3: Basic Git Workflow**

### **1. Setting Up a Repository**

- **Initialize a New Repository:**

  ```bash
  git init
  ```

- **Clone an Existing Repository:**

  ```bash
  git clone https://github.com/username/repository.git
  ```

### **2. Making Changes**

- **Check Repository Status:**

  ```bash
  git status
  ```

- **View Changes (Diff):**

  ```bash
  git diff
  ```

### **3. Staging Changes**

- **Add Files to Staging Area:**

  ```bash
  git add filename         # Add specific file
  git add .                # Add all changes in the current directory
  ```

- **Remove Files from Staging Area:**

  ```bash
  git reset filename
  ```

### **4. Committing Changes**

- **Commit Staged Changes with a Message:**

  ```bash
  git commit -m "Commit message describing changes"
  ```

- **Amend Last Commit:**

  ```bash
  git commit --amend -m "Updated commit message"
  ```

### **5. Working with Branches**

- **List Branches:**

  ```bash
  git branch
  ```

- **Create a New Branch:**

  ```bash
  git branch feature-branch
  ```

- **Switch to a Branch:**

  ```bash
  git checkout feature-branch
  ```

- **Create and Switch to a New Branch:**

  ```bash
  git checkout -b feature-branch
  ```

### **6. Merging Branches**

- **Merge Branch into Current Branch:**

  ```bash
  git checkout main
  git merge feature-branch
  ```

- **Resolve Merge Conflicts:**
  - Occurs when changes conflict.
  - Edit conflicting files to resolve.
  - Stage and commit resolved files.

### **7. Remote Repositories**

- **View Remote Repositories:**

  ```bash
  git remote -v
  ```

- **Add a Remote Repository:**

  ```bash
  git remote add origin https://github.com/username/repository.git
  ```

- **Fetch and Pull Changes:**

  ```bash
  git fetch origin        # Fetches changes but doesn't merge
  git pull origin main    # Fetches and merges changes
  ```

- **Push Changes to Remote:**

  ```bash
  git push origin main
  ```

### **8. Undoing Changes**

- **Discard Changes in Working Directory:**

  ```bash
  git checkout -- filename
  ```

- **Unstage Changes:**

  ```bash
  git reset HEAD filename
  ```

- **Revert a Commit:**

  ```bash
  git revert commit_hash
  ```

- **Reset to a Previous Commit:**

  ```bash
  git reset --hard commit_hash
  ```

  *Use with caution; this can overwrite local changes.*

### **9. Viewing Commit History**

- **Basic Log:**

  ```bash
  git log
  ```

- **One-line Summary:**

  ```bash
  git log --oneline
  ```

- **Graphical Representation:**

  ```bash
  git log --oneline --graph --all
  ```

### **10. Collaboration Workflow**

- **Forking and Pull Requests:**
  - **Fork Repository:** Create a personal copy on GitHub.
  - **Clone Forked Repository:** Work locally.
  - **Commit and Push Changes:** Push to your fork.
  - **Create Pull Request:** Propose changes to the original repository.

- **Code Reviews:**
  - Collaborators review code before merging.
  - Ensures code quality and adherence to standards.

