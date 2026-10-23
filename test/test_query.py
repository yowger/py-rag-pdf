from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rag_pdf.retrieval import search_documents
from rag_pdf.path import CHROMA_DIR

console = Console()


TEST_QUESTIONS = [
    # Direct factual questions PASS 5/5 (Strong 5)
    # {
    #     "question": "What is version control, and why is it useful?",
    #     "expected_answer": "Version control records changes to files over time so you can recall specific versions later. It helps track changes, compare versions, identify who made changes, and recover previous work.",
    #     "expected_topic": "About Version Control"
    # },
    # {
    #     "question": "What is a single point of failure in centralized version control?",
    #     "expected_answer": "The central server is a single point of failure because if it goes down, users may be unable to collaborate or save versioned changes. If the central database is corrupted without backups, the project's history could be lost.",
    #     "expected_topic": "Centralized Version Control Systems"
    # },
    # {
    #     "question": "What does git stash do?",
    #     "expected_answer": "git stash temporarily saves uncommitted changes so you can clean your working directory and switch tasks or branches without committing unfinished work. You can reapply the changes later using git stash apply or git stash pop.",
    #     "expected_topic": "Stashing and Cleaning"
    # },
    # {
    #     "question": "What is the Git staging area?",
    #     "expected_answer": "The staging area is an intermediate area where you prepare changes that will be included in the next commit. You can choose which changes to stage before committing them.",
    #     "expected_topic": "The Three States"
    # },
    # {
    #     "question": "What is a Git branch?",
    #     "expected_answer": "A Git branch is a lightweight movable pointer to a commit. Branches allow you to develop features or experiment independently without requiring every change to be made on the main line of development.",
    #     "expected_topic": "Branches in a Nutshell"
    # },

    # # Commands and how-to questions (Strong: 3 Partial: 2)
    {
        "question": "How do I unstage a file that I have already staged?",
        "expected_answer": "You can unstage a file using git reset HEAD <file> or git restore --staged <file>. These commands remove the file from the staging area while preserving its modifications in the working directory.",
        "expected_topic": "Unstaging a Staged File"
    },
    # {
    #     "question": "How do I save my uncommitted changes temporarily before switching branches?",
    #     "expected_answer": "Run git stash to temporarily save eligible uncommitted changes and clean the working directory. Later, use git stash apply to restore the changes while keeping the stash entry, or git stash pop to restore them and remove the entry if successful.",
    #     "expected_topic": "Stashing and Cleaning"
    # },
    # {
    #     "question": "How do I create and switch to a new Git branch?",
    #     "expected_answer": "Run git switch -c <branch-name> to create a new branch and switch to it. Alternatively, use git checkout -b <branch-name>.",
    #     "expected_topic": "Basic Branching"
    # },
    # {
    #     "question": "How do I see the commit history in Git?",
    #     "expected_answer": "Run git log to display the commit history. Options such as --oneline provide a compact summary, while --graph can visualize branch history.",
    #     "expected_topic": "Viewing the Commit History"
    # },
    # {
    #     "question": "How do I discard changes in a modified file that I have not staged?",
    #     "expected_answer": "Run git restore <file> to discard unstaged working-directory changes and restore the file to its last committed state. This permanently discards those changes unless they can be recovered elsewhere.",
    #     "expected_topic": "Undoing Things"
    # },

    # # Comparison questions (5) (Strong 4 Partial 1)
    # {
    #     "question": "How does distributed version control differ from centralized version control?",
    #     "expected_answer": "In centralized version control, a central server hosts the main repository and history. In distributed version control, each clone contains the repository's history, allowing users to work locally and collaborate through different remotes or workflows.",
    #     "expected_topic": "Distributed Version Control Systems"
    # },
    # {
    #     "question": "What is the difference between local and centralized version control?",
    #     "expected_answer": "Local version control tracks file changes in a database on the user's local machine. Centralized version control stores the versioned project history on a central server that users access to collaborate.",
    #     "expected_topic": "Local Version Control Systems"
    # },
    # {
    #     "question": "What is the difference between git stash apply and git stash pop?",
    #     "expected_answer": "Both commands reapply changes from a stash. git stash apply keeps the stash entry, while git stash pop removes the entry after successfully applying it.",
    #     "expected_topic": "Stashing and Cleaning"
    # },
    # {
    #     "question": "What is the difference between git reset HEAD <file> and git restore --staged <file>?",
    #     "expected_answer": "Both commands can unstage a file without discarding its working-directory modifications. git restore --staged <file> is the more explicitly named modern command, while git reset HEAD <file> is the traditional approach.",
    #     "expected_topic": "Unstaging a Staged File"
    # },
    # {
    #     "question": "How does git restore differ from git stash?",
    #     "expected_answer": "git restore can discard or undo selected working-directory or staging-area changes, depending on its options. git stash temporarily saves eligible uncommitted changes so they can be reapplied later.",
    #     "expected_topic": "Undoing Things and Stashing"
    # },

    # # Multi-section questions (Strong 1 partial 2)
    # {
    #     "question": "How can I temporarily switch tasks without losing my unfinished changes, then return to my work?",
    #     "expected_answer": "Use git stash to temporarily save eligible uncommitted changes before switching tasks or branches. After finishing the other task, return to the original branch and use git stash apply or git stash pop to reapply the saved changes.",
    #     "expected_topic": "Branching and Stashing"
    # },
    # {
    #     "question": "How can I undo a staged change while keeping my edits, and discard a different file's edits entirely?",
    #     "expected_answer": "Use git restore --staged <file> or git reset HEAD <file> to unstage the first file while keeping its working-directory edits. Use git restore <file> to discard the second file's unstaged edits, restoring it to its last committed state.",
    #     "expected_topic": "Unstaging and Undoing Changes"
    # },
    # {
    #     "question": "Why can Git users continue working when a central server is unavailable, and how does this affect collaboration?",
    #     "expected_answer": "Git is distributed, so each clone contains repository history and users can perform many operations locally without contacting a central server. However, sharing changes with others generally requires communication with a remote repository or another collaborator, so remote unavailability can still interrupt synchronization.",
    #     "expected_topic": "Distributed Version Control and Collaboration"
    # },

    # # Out-of-scope questions (3)
    # {
    #     "question": "How do I deploy a React application to Vercel?",
    #     "expected_answer": "This question is outside the scope of the Pro Git book. The system should explain that its available source does not cover React deployment and avoid inventing instructions.",
    #     "expected_topic": "Out of Scope"
    # },
    # {
    #     "question": "How do I create a PostgreSQL database and connect it to a Node.js application?",
    #     "expected_answer": "This question is outside the scope of the Pro Git book. The system should identify that the available source does not provide PostgreSQL setup or Node.js database integration instructions.",
    #     "expected_topic": "Out of Scope"
    # },
    # {
    #     "question": "How do I train a machine learning model using Python and scikit-learn?",
    #     "expected_answer": "This question is outside the scope of the Pro Git book. The system should state that the available source does not explain machine learning model training with Python or scikit-learn.",
    #     "expected_topic": "Out of Scope"
    # }
]

# for item in TEST_QUESTIONS:
#     question = item["question"]
#     expected_topic = item["expected_topic"]
#     expected_answer = item["expected_answer"]

#     results = search_documents(
#         query=question,
#         persist_directory=CHROMA_DIR,
#         k=4,
#         # k=6,
#         # k=2,
#     )

#     console.print(
#         Panel(
#             question,
#             title="[bold cyan]Search Query[/bold cyan]",
#             border_style="cyan",
#         )
#     )

#     console.print(
#         f"\n[bold green]expected topic:[/bold green] {expected_topic}")
#     console.print(
#         f"\n[bold green]expected answer:[/bold green] {expected_answer}")
#     console.print(f"\n[bold green]Results found:[/bold green] {len(results)}")

#     for index, (document, score) in enumerate(results, start=1):
#         console.print(
#             Panel(
#                 document.page_content,
#                 title=f"[bold blue]Result {index}[/bold blue]",
#                 subtitle=f"{len(document.page_content)} characters. Score {score:.4f}",
#                 border_style="blue",
#             )
#         )

#         metadata_table = Table(
#             title=f"Result {index} Metadata",
#             show_header=True,
#             header_style="bold magenta",
#         )

#         metadata_table.add_column("Key", style="cyan", no_wrap=True)
#         metadata_table.add_column("Value", style="white", overflow="fold")

#         for key, value in document.metadata.items():
#             metadata_table.add_row(str(key), str(value))

#         console.print(metadata_table)
#         console.print()
