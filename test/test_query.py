from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rag_pdf.retrieval import search_documents
from rag_pdf.config import CHROMA_DIR

console = Console()

# query = "Whats Git"
# query = "Whats is version control"
# query = "How does distributed version control differ from centralized version control?"
# query = "What are the disadvantages of centralized version control?"

TEST_QUESTIONS = [
    # {
    #     "question": "What is the difference between Git and other version control systems that store file differences?",
    #     "expected_answer": "Git generally stores snapshots of the project at each commit rather than representing every version only as a set of file differences. Unchanged files can be referenced from previous snapshots, making the snapshot model efficient.",
    #     "expected_topic": "Snapshots"
    # },
    # {
    #     "question": "What are the three main states of a file in Git?",
    #     "expected_answer": "A file in Git can be modified, staged, or committed. Modified means it has changed in the working directory, staged means the changes are marked for the next commit, and committed means the data has been saved in the repository's history.",
    #     "expected_topic": "The Three States"
    # },
    # {
    #     "question": "What is the difference between the working directory, staging area, and Git repository?",
    #     "expected_answer": "The working directory contains the checked-out files you edit. The staging area records the changes selected for the next commit. The Git repository stores committed project history and related metadata.",
    #     "expected_topic": "The Three States"
    # },
    # {
    #     "question": "How do I see which files have been modified or staged?",
    #     "expected_answer": "Run `git status`. It reports the current branch and shows changes such as modified files, staged changes, and untracked files.",
    #     "expected_topic": "Recording Changes to the Repository"
    # },
    # {
    #     "question": "How do I see the actual changes I made to files before staging them?",
    #     "expected_answer": "Run `git diff` to see differences between the working directory and the staging area. This is useful for reviewing unstaged changes before adding them.",
    #     "expected_topic": "Recording Changes to the Repository"
    # },
    # {
    #     "question": "How do I view changes that are staged and ready to commit?",
    #     "expected_answer": "Run `git diff --staged` or `git diff --cached` to compare the staged changes with the last commit. This shows what will be included in the next commit.",
    #     "expected_topic": "Recording Changes to the Repository"
    # },
    # {
    #     "question": "How do I stop Git from tracking a file that is already tracked, while keeping the local file?",
    #     "expected_answer": "Run `git rm --cached <file>`. This removes the file from Git's index while leaving the working-directory copy in place. Add the file to `.gitignore` if you also want Git to ignore it in the future.",
    #     "expected_topic": "Removing Files"
    # },
    # {
    #     "question": "What is the purpose of a .gitignore file?",
    #     "expected_answer": "A `.gitignore` file tells Git which untracked files and patterns to ignore, such as generated files, build output, or local configuration. It does not automatically stop tracking files that have already been committed.",
    #     "expected_topic": "Ignoring Files"
    # },
    # {
    #     "question": "How do I change the message of my most recent commit?",
    #     "expected_answer": "Run `git commit --amend -m \"New commit message\"` to replace the message of the most recent commit. Amending creates a replacement commit, so use caution if the original commit has already been shared.",
    #     "expected_topic": "Undoing Things"
    # },
    # {
    #     "question": "How do I undo a commit that has already been shared without rewriting history?",
    #     "expected_answer": "Use `git revert <commit>`. Git creates a new commit that reverses the changes introduced by the specified commit, preserving the existing commit history.",
    #     "expected_topic": "Undoing Things"
    # },
    # {
    #     "question": "What is the difference between git reset and git revert?",
    #     "expected_answer": "`git reset` moves the current branch reference and can change what is staged or present in the working directory, depending on the options used. `git revert` creates a new commit that reverses an earlier commit's changes. Revert is generally safer for undoing commits that have already been shared.",
    #     "expected_topic": "Undoing Things"
    # },
    # {
    #     "question": "How do I create a new Git branch and switch to it?",
    #     "expected_answer": "You can run `git checkout -b <branch-name>` to create and switch to a branch in one command. On newer Git versions, `git switch -c <branch-name>` is an alternative.",
    #     "expected_topic": "Basic Branching and Merging"
    # },
    # {
    #     "question": "What does HEAD mean in Git?",
    #     "expected_answer": "HEAD is a reference to the currently checked-out commit, usually through the current branch. When you switch branches, HEAD normally points to the branch you switched to.",
    #     "expected_topic": "Branches in a Nutshell"
    # },
    # {
    #     "question": "Why is creating a branch in Git usually inexpensive?",
    #     "expected_answer": "A Git branch is essentially a lightweight movable reference to a commit, rather than a separate full copy of the project. Creating one generally involves creating a reference, making branching fast and inexpensive.",
    #     "expected_topic": "Branches in a Nutshell"
    # },
    # {
    #     "question": "What happens when I merge a branch into my current branch?",
    #     "expected_answer": "Git integrates the changes from the other branch into the current branch. Depending on the commit history, Git may perform a fast-forward or create a merge commit. If conflicting changes cannot be resolved automatically, a merge conflict occurs.",
    #     "expected_topic": "Basic Branching and Merging"
    # },
    # {
    #     "question": "What causes a merge conflict, and how do I resolve one?",
    #     "expected_answer": "A merge conflict occurs when Git cannot automatically reconcile changes, such as incompatible edits to the same part of a file. Inspect the conflicted files, edit them to the intended final content, stage the resolved files, and complete the merge with a commit when required.",
    #     "expected_topic": "Basic Branching and Merging"
    # },
    # {
    #     "question": "How can I list branches that have already been merged into my current branch?",
    #     "expected_answer": "Run `git branch --merged` to list branches whose changes are already integrated into the current branch. Review the results before deleting any branches.",
    #     "expected_topic": "Branch Management"
    # },
    # {
    #     "question": "What is a remote-tracking branch?",
    #     "expected_answer": "A remote-tracking branch is a local reference that records the state of a branch on a remote repository as last observed by Git. Examples include `origin/main`. It is updated by operations such as fetch and is not normally edited directly.",
    #     "expected_topic": "Remote Branches"
    # },
    # {
    #     "question": "What is the difference between git fetch and git pull?",
    #     "expected_answer": "`git fetch` downloads updates and remote-tracking information without integrating those changes into the current local branch. `git pull` fetches updates and then integrates them, commonly through a merge or rebase depending on configuration and options.",
    #     "expected_topic": "Working with Remotes"
    # },
    # {
    #     "question": "How do I upload a local branch to a remote repository and set its upstream?",
    #     "expected_answer": "Run `git push -u origin <branch-name>`. This pushes the branch to the remote named `origin` and sets the upstream tracking relationship for future push and pull operations.",
    #     "expected_topic": "Working with Remotes"
    # },
    # {
    #     "question": "Why can Git push be rejected because the remote contains work I do not have locally?",
    #     "expected_answer": "The remote branch may contain commits that are missing from the local branch. Fetch the remote changes, integrate them through an appropriate merge or rebase workflow, resolve any conflicts, and then push again.",
    #     "expected_topic": "Working with Remotes"
    # },
    # {
    #     "question": "What is the difference between a lightweight tag and an annotated tag?",
    #     "expected_answer": "A lightweight tag is essentially a reference to a commit. An annotated tag is a separate Git object containing information such as the tagger, date, message, and optionally a cryptographic signature. Annotated tags are generally more suitable for releases.",
    #     "expected_topic": "Tagging"
    # },
    # {
    #     "question": "How can I see the history of commits in a Git repository?",
    #     "expected_answer": "Run `git log` to view commit history, including commit identifiers, authors, dates, and messages. Options such as `--oneline` provide a compact summary, while `--graph` helps visualize branching and merges.",
    #     "expected_topic": "Viewing the Commit History"
    # },
    # {
    #     "question": "How can I find which commit introduced a particular line of code?",
    #     "expected_answer": "Run `git blame <file>` to show the commit and author information associated with each line of a file. It helps trace when and by whom lines were last changed.",
    #     "expected_topic": "Git Tools"
    # },
    # {
    #     "question": "What is the difference between centralized and distributed version control?",
    #     "expected_answer": "In centralized version control, a central server holds the main repository and clients depend on it for many operations. In distributed version control such as Git, each clone contains repository history, allowing many operations locally and providing additional copies of the history.",
    #     "expected_topic": "Distributed Version Control Systems"
    # },
    # {
    #     "question": "Why can a Git user continue working when the remote server is unavailable?",
    #     "expected_answer": "A Git clone contains local repository history, so users can inspect commits, create commits, compare changes, and work on branches locally. Network access is needed for operations that exchange data with the remote, such as fetching or pushing.",
    #     "expected_topic": "Distributed Version Control Systems"
    # },
    # {
    #     "question": "What is an interactive rebase useful for?",
    #     "expected_answer": "Interactive rebase lets you edit a sequence of commits, including reordering, rewording, combining, or removing commits. It is useful for cleaning up local history before sharing it, but rewriting commits that others already depend on can cause problems.",
    #     "expected_topic": "Rebasing"
    # },
    # {
    #     "question": "What is the difference between merging and rebasing a branch?",
    #     "expected_answer": "Merging integrates branch histories and may create a merge commit that preserves the branching structure. Rebasing reapplies commits onto a new base, producing new commit identifiers and usually a more linear history. Rebasing rewrites commit history, so it requires care with shared branches.",
    #     "expected_topic": "Rebasing"
    # },
    {
        "question": "What does git stash do, and when would I use it?",
        "expected_answer": "`git stash` saves certain uncommitted changes temporarily so you can switch tasks or branches without committing them. You can later reapply the saved changes using commands such as `git stash apply` or `git stash pop`.",
        "expected_topic": "Stashing and Cleaning"
    },
    # {
    #     "question": "How is Git's object database related to commits, trees, and blobs?",
    #     "expected_answer": "Git stores content and repository history using objects. Blob objects store file contents, tree objects represent directory structures and refer to files or subtrees, and commit objects record a snapshot's top-level tree along with information such as parent commits, author, committer, and message.",
    #     "expected_topic": "Git Internals"
    # }
]

for item in TEST_QUESTIONS:
    question = item["question"]
    expected_topic = item["expected_topic"]
    expected_answer = item["expected_answer"]

    results = search_documents(
        query=question,
        persist_directory=CHROMA_DIR,
        k=4,
        # k=6,
        # k=2,
    )

    console.print(
        Panel(
            question,
            title="[bold cyan]Search Query[/bold cyan]",
            border_style="cyan",
        )
    )

    console.print(
        f"\n[bold green]expected topic:[/bold green] {expected_topic}")
    console.print(
        f"\n[bold green]expected answer:[/bold green] {expected_answer}")
    console.print(f"\n[bold green]Results found:[/bold green] {len(results)}")

    for index, document in enumerate(results, start=1):
        console.print(
            Panel(
                document.page_content,
                title=f"[bold blue]Result {index}[/bold blue]",
                subtitle=f"{len(document.page_content)} characters",
                border_style="blue",
            )
        )

        metadata_table = Table(
            title=f"Result {index} Metadata",
            show_header=True,
            header_style="bold magenta",
        )

        metadata_table.add_column("Key", style="cyan", no_wrap=True)
        metadata_table.add_column("Value", style="white", overflow="fold")

        for key, value in document.metadata.items():
            metadata_table.add_row(str(key), str(value))

        console.print(metadata_table)
        console.print()
