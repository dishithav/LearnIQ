import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import json
import random
from datetime import date, datetime
from auth import init_auth_db, register_user, authenticate_user

# =========================================================
# LEARNIQ — ADAPTIVE AI TUTOR
# Rule-based adaptive learning prototype (no live AI API)
# =========================================================

st.set_page_config(
    page_title="LearnIQ | Adaptive AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "learniq.db"
init_auth_db()

# Each built-in subject has 10 questions.
# Format: question, options, correct answer, topic, explanation
quiz_data = {
    "Python": [
        ("Which keyword defines a function?", ["func", "def", "function", "define"], "def", "Functions", "Python uses the def keyword to define a function."),
        ("Which data type stores True or False?", ["int", "str", "bool", "float"], "bool", "Data types", "The bool type stores Boolean values: True or False."),
        ("Which symbol starts a single-line comment in Python?", ["//", "#", "/*", "$"], "#", "Syntax", "A hash symbol starts a Python comment."),
        ("Which method adds an item to the end of a list?", ["add()", "append()", "insertEnd()", "push()"], "append()", "Lists", "append() adds one item to the end of a list."),
        ("What is the result of 3 ** 2?", ["5", "6", "9", "8"], "9", "Operators", "** is the exponentiation operator."),
        ("Which collection stores key-value pairs?", ["List", "Tuple", "Dictionary", "Set"], "Dictionary", "Collections", "A dictionary stores data as key-value pairs."),
        ("Which loop repeats while a condition is true?", ["for", "while", "repeat", "loop"], "while", "Loops", "A while loop continues as long as its condition is true."),
        ("What does len('hello') return?", ["4", "5", "6", "hello"], "5", "Built-in functions", "len() returns the number of items or characters."),
        ("Which keyword is used to handle an exception?", ["catch", "error", "except", "final"], "except", "Exception handling", "Python uses try and except to handle exceptions."),
        ("What is the index of the first item in a Python list?", ["0", "1", "-1", "It depends"], "0", "Lists", "Python sequences use zero-based indexing.")
    ],
    "C Programming": [
        ("Which function is the usual entry point of a C program?", ["start()", "main()", "begin()", "run()"], "main()", "Basics", "Execution of a standard C program begins at main()."),
        ("Which symbol ends most C statements?", [".", ":", ";", ","], ";", "Syntax", "A semicolon terminates most C statements."),
        ("Which format specifier is used for an integer?", ["%f", "%c", "%d", "%s"], "%d", "Input and output", "%d is commonly used for an int."),
        ("Which header provides printf()?", ["stdlib.h", "stdio.h", "string.h", "math.h"], "stdio.h", "Headers", "stdio.h declares standard input/output functions."),
        ("What is the first array index in C?", ["0", "1", "-1", "2"], "0", "Arrays", "C arrays use zero-based indexing."),
        ("Which operator gives the address of a variable?", ["*", "&", "%", "#"], "&", "Pointers", "The address-of operator is &."),
        ("Which loop executes its body at least once?", ["for", "while", "do-while", "none"], "do-while", "Loops", "A do-while loop checks its condition after the body."),
        ("Which data type stores a single character?", ["string", "char", "int", "float"], "char", "Data types", "char stores a character value."),
        ("Which statement selects among multiple cases?", ["if", "switch", "goto", "break"], "switch", "Control flow", "switch selects a branch based on an expression."),
        ("What does NULL commonly represent for a pointer?", ["Address zero/no valid object", "A character", "A loop", "A file"], "Address zero/no valid object", "NULL represents a null pointer value.")
    ],
    "Java": [
        ("Which keyword is used to create a class in Java?", ["class", "define", "struct", "object"], "class", "Classes", "The class keyword declares a Java class."),
        ("Which method is the common Java program entry point?", ["start()", "main()", "run()", "init()"], "main()", "Basics", "The main method is the standard entry point for a Java application."),
        ("Which type stores true or false?", ["int", "boolean", "char", "String"], "boolean", "Data types", "boolean stores true or false."),
        ("Which keyword creates an object?", ["make", "new", "class", "this"], "new", "Objects", "The new keyword creates an object."),
        ("Which concept allows one class to acquire another class's features?", ["Encapsulation", "Inheritance", "Compilation", "Casting"], "Inheritance", "OOP", "Inheritance lets a class derive from another class."),
        ("Which collection does not allow duplicate elements?", ["ArrayList", "HashSet", "LinkedList", "Vector"], "HashSet", "Collections", "A HashSet stores unique elements."),
        ("Which block is used to handle exceptions?", ["try-catch", "if-else", "for-next", "switch-case"], "try-catch", "Exceptions", "try-catch handles exceptions."),
        ("Which keyword prevents a class from being inherited?", ["static", "private", "final", "void"], "final", "OOP", "A final class cannot be subclassed."),
        ("Which operator compares primitive values for equality?", ["=", "==", "!=", "=>"], "==", "Operators", "== compares primitive values."),
        ("Which package is automatically imported in Java?", ["java.util", "java.io", "java.lang", "java.net"], "java.lang", "Packages", "java.lang is automatically available.")
    ],
    "Data Structures & Algorithms": [
        ("Which data structure follows FIFO?", ["Stack", "Queue", "Tree", "Graph"], "Queue", "Queues", "A queue removes items in first-in, first-out order."),
        ("Which data structure follows LIFO?", ["Queue", "Stack", "Heap", "Graph"], "Stack", "Stacks", "A stack follows last-in, first-out order."),
        ("What is the time complexity of binary search on a sorted array?", ["O(n)", "O(log n)", "O(n²)", "O(1)"], "O(log n)", "Searching", "Binary search halves the search space each step."),
        ("Which structure uses nodes with left and right children?", ["Binary tree", "Queue", "Stack", "Hash table"], "Binary tree", "Trees", "A binary tree node has at most two children."),
        ("Which sorting algorithm repeatedly selects the smallest remaining item?", ["Merge sort", "Selection sort", "Quick sort", "Heap sort"], "Selection sort", "Sorting", "Selection sort selects the minimum item for each position."),
        ("Which data structure is commonly used for BFS?", ["Stack", "Queue", "Array only", "Heap"], "Queue", "Graph algorithms", "Breadth-first search uses a queue."),
        ("What is the average lookup time of a well-designed hash table?", ["O(n)", "O(log n)", "O(1)", "O(n²)"], "O(1)", "Hashing", "Hash tables provide average constant-time lookup."),
        ("Which traversal visits root, left, then right?", ["Inorder", "Preorder", "Postorder", "Level order"], "Preorder", "Trees", "Preorder traversal visits root before its subtrees."),
        ("What does a linked list store in each node?", ["Only an index", "Data and link(s)", "Only a key", "A whole tree"], "Data and link(s)", "Linked lists", "A node stores data and references to other nodes."),
        ("Which algorithmic technique solves problems by combining subproblems?", ["Divide and conquer", "Random guessing", "Linear scan only", "Brute force only"], "Divide and conquer", "Algorithms", "Divide and conquer breaks a problem into smaller subproblems.")
    ],
    "DBMS": [
        ("What does DBMS stand for?", ["Data Backup Management System", "Database Management System", "Digital Base Machine Software", "Data Binary Management Service"], "Database Management System", "Fundamentals", "A DBMS manages databases."),
        ("Which SQL command retrieves data?", ["GET", "OPEN", "SELECT", "FETCHALL"], "SELECT", "SQL", "SELECT retrieves rows from a table."),
        ("Which key uniquely identifies a row?", ["Foreign key", "Primary key", "Candidate value", "Duplicate key"], "Primary key", "Keys", "A primary key uniquely identifies each row."),
        ("Which SQL command adds a new row?", ["INSERT", "UPDATE", "ALTER", "DROP"], "INSERT", "SQL", "INSERT adds rows to a table."),
        ("What does SQL stand for?", ["Structured Query Language", "Simple Question Language", "System Query Logic", "Sequential Query List"], "Structured Query Language", "SQL", "SQL means Structured Query Language."),
        ("Which normal form removes partial dependency?", ["1NF", "2NF", "3NF", "BCNF only"], "2NF", "Normalization", "Second normal form removes partial dependency on a candidate key."),
        ("Which command changes existing row values?", ["CHANGE", "UPDATE", "MODIFY TABLE", "REPLACE DB"], "UPDATE", "SQL", "UPDATE modifies existing rows."),
        ("What is a foreign key used for?", ["Encrypting a table", "Linking related tables", "Sorting rows", "Deleting duplicates"], "Linking related tables", "Keys", "A foreign key references a key in another or the same table."),
        ("Which property means a transaction is all-or-nothing?", ["Consistency", "Isolation", "Atomicity", "Durability"], "Atomicity", "Transactions", "Atomicity ensures a transaction fully succeeds or is rolled back."),
        ("Which SQL clause filters grouped results?", ["WHERE", "ORDER BY", "HAVING", "LIMIT"], "HAVING", "SQL", "HAVING filters groups after GROUP BY.")
    ],
    "Operating Systems": [
        ("What is the main role of an operating system?", ["Design websites", "Manage hardware and software resources", "Compile every program", "Create databases"], "Manage hardware and software resources", "OS basics", "An OS manages resources and provides services to applications."),
        ("Which is an example of an operating system?", ["Python", "Linux", "HTML", "MySQL"], "Linux", "OS basics", "Linux is an operating system."),
        ("What is a process?", ["A program in execution", "A file extension", "A keyboard key", "A network cable"], "A program in execution", "Processes", "A process is a running instance of a program."),
        ("Which scheduling algorithm uses time slices?", ["FCFS", "Round Robin", "SJF", "Priority only"], "Round Robin", "CPU scheduling", "Round Robin gives processes time slices in rotation."),
        ("What is a deadlock?", ["A fast CPU", "Processes waiting indefinitely for resources", "A file backup", "A type of memory"], "Processes waiting indefinitely for resources", "Deadlocks", "Deadlock is a condition where processes cannot proceed due to resource waits."),
        ("Which memory is typically fastest?", ["Hard disk", "RAM", "CPU cache", "USB drive"], "CPU cache", "Memory", "CPU cache is faster and closer to the processor than main memory."),
        ("What does RAM stand for?", ["Read Access Memory", "Random Access Memory", "Run Active Memory", "Rapid Allocation Module"], "Random Access Memory", "Memory", "RAM means Random Access Memory."),
        ("What is virtual memory?", ["Extra CPU cores", "Memory management using storage to extend address space", "A graphics card", "A type of keyboard"], "Memory management using storage to extend address space", "Memory", "Virtual memory provides an abstraction of a larger memory space."),
        ("Which component decides which process gets CPU time?", ["Compiler", "Scheduler", "File manager", "Loader only"], "Scheduler", "CPU scheduling", "The CPU scheduler selects a process to run."),
        ("What is a thread?", ["A lightweight unit of execution within a process", "A storage device", "A network protocol", "A file system"], "A lightweight unit of execution within a process", "Threads", "A thread is an execution unit within a process.")
    ],
    "Computer Networks": [
        ("What does LAN stand for?", ["Large Area Network", "Local Area Network", "Linked Access Node", "Long Access Network"], "Local Area Network", "Networking basics", "LAN connects devices in a limited area."),
        ("Which protocol is used to browse secure websites?", ["HTTP", "HTTPS", "FTP", "SMTP"], "HTTPS", "Protocols", "HTTPS secures web communication using encryption."),
        ("Which device forwards packets between networks?", ["Switch", "Router", "Keyboard", "Repeater only"], "Router", "Network devices", "Routers forward packets between networks."),
        ("What does IP stand for?", ["Internet Protocol", "Internal Program", "Input Port", "Information Process"], "Internet Protocol", "Protocols", "IP means Internet Protocol."),
        ("Which layer is responsible for routing in the OSI model?", ["Physical", "Data Link", "Network", "Application"], "Network", "OSI model", "The Network layer handles logical addressing and routing."),
        ("Which protocol translates domain names to IP addresses?", ["DHCP", "DNS", "FTP", "SSH"], "DNS", "Protocols", "DNS resolves domain names to IP addresses."),
        ("What is the default port for HTTPS?", ["21", "25", "80", "443"], "443", "Ports", "HTTPS commonly uses TCP port 443."),
        ("Which topology connects all devices to a central device?", ["Ring", "Bus", "Star", "Mesh"], "Star", "Topologies", "Star topology connects devices through a central hub or switch."),
        ("What does DHCP provide automatically?", ["Domain names", "IP configuration", "Encryption keys", "Web pages"], "IP configuration", "Protocols", "DHCP automatically assigns IP configuration to clients."),
        ("Which protocol is connection-oriented?", ["UDP", "TCP", "IP", "ARP"], "TCP", "Protocols", "TCP establishes a connection and provides reliable ordered delivery.")
    ],
    "AI & Machine Learning": [
        ("What does AI stand for?", ["Automated Internet", "Artificial Intelligence", "Advanced Input", "Algorithm Integration"], "Artificial Intelligence", "AI basics", "AI means Artificial Intelligence."),
        ("What is machine learning?", ["A way for systems to learn patterns from data", "Only writing HTML", "A computer hardware part", "A database language"], "A way for systems to learn patterns from data", "ML basics", "Machine learning uses data to learn patterns and make predictions."),
        ("Which task is classification?", ["Predicting house price", "Sorting emails as spam or not spam", "Grouping customers without labels", "Compressing a file"], "Sorting emails as spam or not spam", "Supervised learning", "Classification predicts a category or class."),
        ("Which learning uses labelled examples?", ["Unsupervised learning", "Supervised learning", "Reinforcement only", "Random learning"], "Supervised learning", "Learning types", "Supervised learning trains on labelled examples."),
        ("What is a feature in a dataset?", ["An input variable", "The final report", "A computer cable", "A model error only"], "An input variable", "Data", "Features are input variables used by a model."),
        ("What is overfitting?", ["Model performs well on new data", "Model memorizes training data and generalizes poorly", "Model has no parameters", "Data is sorted"], "Model memorizes training data and generalizes poorly", "Model evaluation", "Overfitting occurs when a model fits training data too closely."),
        ("Which metric is the fraction of correct predictions?", ["Accuracy", "Latency", "Recall only", "Loss only"], "Accuracy", "Evaluation", "Accuracy is correct predictions divided by all predictions."),
        ("What is an epoch in model training?", ["One full pass through training data", "A single feature", "A type of database", "A network address"], "One full pass through training data", "Training", "An epoch is one complete pass through the training dataset."),
        ("Which field focuses on understanding images?", ["Computer vision", "Database design", "Networking", "Operating systems"], "Computer vision", "AI applications", "Computer vision enables machines to interpret visual information."),
        ("What does NLP stand for?", ["Natural Language Processing", "Network Link Protocol", "Numeric Learning Program", "New Logic Process"], "Natural Language Processing", "AI applications", "NLP deals with processing human language.")
    ],
    "Git & GitHub": [
        ("What is Git?", ["A programming language", "A version control system", "A web browser", "A database"], "A version control system", "Git basics", "Git tracks changes to files over time."),
        ("Which command copies a remote repository locally?", ["git push", "git clone", "git merge", "git status"], "git clone", "Commands", "git clone creates a local copy of a repository."),
        ("Which command records staged changes?", ["git commit", "git pull", "git init", "git log"], "git commit", "Commands", "git commit records staged changes in repository history."),
        ("Which command shows the working tree status?", ["git status", "git start", "git showall", "git branch"], "git status", "Commands", "git status shows changed and staged files."),
        ("What is GitHub?", ["A code hosting and collaboration platform", "A compiler", "An operating system", "A programming loop"], "A code hosting and collaboration platform", "GitHub basics", "GitHub hosts Git repositories and collaboration tools."),
        ("Which command sends local commits to a remote?", ["git fetch", "git push", "git add", "git diff"], "git push", "Commands", "git push uploads local commits to a remote repository."),
        ("Which command stages a file?", ["git add", "git stageall", "git commit", "git upload"], "git add", "Commands", "git add stages changes for the next commit."),
        ("What is a branch used for?", ["Separate line of development", "Deleting a repository", "Changing a file type", "Running a server"], "Separate line of development", "Branches", "Branches let developers work on changes independently."),
        ("What does a pull request help with?", ["Reviewing and merging proposed changes", "Installing Python", "Formatting a disk", "Creating passwords"], "Reviewing and merging proposed changes", "Collaboration", "Pull requests support review and discussion before merging."),
        ("Which file commonly explains a repository?", ["README.md", "main.exe", "index.dll", "notes.tmp"], "README.md", "Documentation", "README files describe the project and how to use it.")
    ],
    "Linux": [
        ("Which command lists files and folders?", ["pwd", "ls", "cd", "mkdir"], "ls", "Commands", "ls lists directory contents."),
        ("Which command shows the current directory?", ["pwd", "ls", "rm", "touch"], "pwd", "Commands", "pwd prints the working directory."),
        ("Which command changes directory?", ["mv", "cd", "cp", "cat"], "cd", "Commands", "cd changes the current directory."),
        ("Which command creates a directory?", ["mkdir", "rmdir", "touch", "grep"], "mkdir", "File management", "mkdir creates a directory."),
        ("Which command displays file contents?", ["cat", "chmod", "ps", "kill"], "cat", "Commands", "cat outputs file contents."),
        ("Which command copies files?", ["mv", "cp", "rm", "pwd"], "cp", "File management", "cp copies files and directories."),
        ("Which command changes file permissions?", ["chmod", "chown", "grep", "echo"], "chmod", "Permissions", "chmod changes file mode permissions."),
        ("Which command searches text patterns?", ["grep", "mkdir", "cd", "date"], "grep", "Commands", "grep searches input for matching patterns."),
        ("Which symbol commonly represents the home directory?", ["/", "~", "#", "*"], "~", "Filesystem", "The tilde commonly expands to the current user's home directory."),
        ("Which command shows running processes?", ["ps", "ls", "touch", "clear"], "ps", "Processes", "ps displays information about running processes.")
    ],
    "Cloud Computing": [
        ("What is cloud computing?", ["Using computing services over a network", "Only storing files on USB", "A type of keyboard", "Offline printing"], "Using computing services over a network", "Cloud basics", "Cloud computing provides computing resources over a network, commonly the internet."),
        ("What does IaaS stand for?", ["Infrastructure as a Service", "Internet as a System", "Input as a Service", "Integration and Storage"], "Infrastructure as a Service", "Service models", "IaaS provides virtualized computing infrastructure."),
        ("Which is an example of object storage use?", ["Storing photos and backups", "Executing CPU instructions", "Cooling a processor", "Connecting a keyboard"], "Storing photos and backups", "Storage", "Object storage is suitable for unstructured data such as images and backups."),
        ("What is scalability?", ["Ability to handle changing workload", "Deleting all data", "Changing a password", "Turning off a network"], "Ability to handle changing workload", "Cloud concepts", "Scalability means resources can adapt to workload demand."),
        ("What does SaaS provide?", ["Ready-to-use software over a network", "Physical servers only", "Network cables", "A programming language"], "Ready-to-use software over a network", "Service models", "SaaS delivers applications to users over a network."),
        ("What is a public cloud?", ["Cloud services offered for use by multiple customers", "A laptop with no internet", "A private USB drive", "A local text editor"], "Cloud services offered for use by multiple customers", "Deployment models", "A public cloud provider offers services to many customers."),
        ("What is elasticity in cloud computing?", ["Automatically adjusting resources with demand", "Changing screen brightness", "Compressing source code", "Renaming files"], "Automatically adjusting resources with demand", "Cloud concepts", "Elasticity adjusts resource capacity as demand changes."),
        ("What does PaaS stand for?", ["Platform as a Service", "Program as a Server", "Private access and Storage", "Protocol as Software"], "Platform as a Service", "Service models", "PaaS provides a platform for developing and deploying applications."),
        ("Why are backups important?", ["To help recover data after loss", "To increase screen size", "To change CPU speed", "To remove all security"], "To help recover data after loss", "Reliability", "Backups support data recovery after accidental loss or failure."),
        ("What is a cloud region?", ["A geographic area containing cloud infrastructure", "A file extension", "A password type", "A programming loop"], "A geographic area containing cloud infrastructure", "Infrastructure", "A region is a geographic location where cloud resources are hosted.")
    ],
    "DevOps & CI/CD": [
        ("What is the main goal of DevOps?", ["Improve collaboration and software delivery", "Replace all developers", "Only design logos", "Stop testing"], "Improve collaboration and software delivery", "DevOps basics", "DevOps combines practices that improve collaboration and delivery."),
        ("What does CI stand for?", ["Continuous Integration", "Computer Interface", "Code Installation", "Central Internet"], "Continuous Integration", "CI/CD", "CI means Continuous Integration."),
        ("What does CD commonly stand for in CI/CD?", ["Continuous Delivery or Deployment", "Code Design", "Central Database", "Computer Debugging"], "Continuous Delivery or Deployment", "CI/CD", "CD can mean Continuous Delivery or Continuous Deployment."),
        ("What is a pipeline?", ["Automated sequence of build, test, and delivery steps", "A physical water pipe", "A database row", "A keyboard shortcut"], "Automated sequence of build, test, and delivery steps", "Pipelines", "A CI/CD pipeline automates software workflow steps."),
        ("Why are automated tests used in CI?", ["To detect issues early", "To make code longer", "To remove version control", "To avoid building software"], "To detect issues early", "Testing", "Automated tests provide quick feedback about changes."),
        ("What is Infrastructure as Code?", ["Managing infrastructure using machine-readable definitions", "Drawing server diagrams only", "Writing user manuals", "Typing commands randomly"], "Managing infrastructure using machine-readable definitions", "Automation", "Infrastructure as Code defines infrastructure in files that can be versioned."),
        ("Which practice helps package apps with dependencies?", ["Containerization", "Defragmentation", "Screen recording", "Word processing"], "Containerization", "Containers", "Containers package an application with its dependencies."),
        ("What is monitoring used for?", ["Observing system health and performance", "Writing source code automatically", "Changing variable names", "Deleting logs"], "Observing system health and performance", "Operations", "Monitoring helps teams detect performance and availability issues."),
        ("What is a deployment?", ["Releasing software to an environment", "Deleting a branch", "Writing a comment", "Formatting a document"], "Releasing software to an environment", "Release", "Deployment makes a software version available in an environment."),
        ("Why use version control in DevOps?", ["Track changes and support collaboration", "Increase file size", "Replace all testing", "Hide code history"], "Track changes and support collaboration", "Version control", "Version control tracks changes and supports team workflows.")
    ],
    "Mathematics": [
        ("What is 5 × 6?", ["11", "25", "30", "35"], "30", "Arithmetic", "5 multiplied by 6 equals 30."),
        ("What is the square of 4?", ["8", "12", "16", "20"], "16", "Powers", "4 squared is 4 × 4 = 16."),
        ("What is 100 divided by 10?", ["5", "10", "20", "50"], "10", "Arithmetic", "100 divided by 10 equals 10."),
        ("What is the value of 2³?", ["6", "8", "9", "12"], "8", "Powers", "2 cubed is 2 × 2 × 2 = 8."),
        ("What is the sum of angles in a triangle?", ["90°", "180°", "270°", "360°"], "180°", "Geometry", "The interior angles of a triangle sum to 180 degrees."),
        ("What is 15% of 200?", ["15", "20", "30", "40"], "30", "Percentages", "0.15 × 200 = 30."),
        ("What is the next prime number after 7?", ["8", "9", "10", "11"], "11", "Number theory", "11 is the next integer after 7 with exactly two positive divisors."),
        ("What is the slope of y = 3x + 2?", ["2", "3", "5", "1"], "3", "Algebra", "In y = mx + c, the slope is m."),
        ("What is the perimeter of a square with side 4?", ["8", "12", "16", "20"], "16", "Geometry", "Perimeter of a square is 4 × side."),
        ("What is the mean of 2, 4, and 6?", ["3", "4", "5", "6"], "4", "Statistics", "The mean is (2 + 4 + 6) / 3 = 4.")
    ],
    "Science": [
        ("Which planet is known as the Red Planet?", ["Earth", "Mars", "Jupiter", "Venus"], "Mars", "Astronomy", "Mars appears reddish due to iron oxide on its surface."),
        ("What gas do plants absorb during photosynthesis?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "Carbon dioxide", "Biology", "Plants use carbon dioxide during photosynthesis."),
        ("What is the chemical formula of water?", ["CO2", "O2", "H2O", "NaCl"], "H2O", "Chemistry", "A water molecule contains two hydrogen atoms and one oxygen atom."),
        ("Which force pulls objects toward Earth?", ["Magnetism", "Gravity", "Friction", "Tension"], "Gravity", "Physics", "Gravity attracts objects with mass."),
        ("What is the basic unit of life?", ["Atom", "Cell", "Tissue", "Organ"], "Cell", "Biology", "The cell is the basic structural and functional unit of life."),
        ("Which part of the plant absorbs most water?", ["Flower", "Roots", "Fruit", "Leaf"], "Roots", "Biology", "Roots absorb water and minerals from the soil."),
        ("What is the SI unit of electric current?", ["Volt", "Watt", "Ampere", "Ohm"], "Ampere", "Physics", "Electric current is measured in amperes."),
        ("Which gas is most abundant in Earth's atmosphere?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Argon"], "Nitrogen", "Earth science", "Nitrogen makes up about 78% of Earth's atmosphere."),
        ("At what temperature does pure water freeze at standard pressure?", ["0°C", "10°C", "50°C", "100°C"], "0°C", "Chemistry", "Pure water freezes at 0 degrees Celsius at standard pressure."),
        ("Which organ pumps blood through the body?", ["Lungs", "Brain", "Heart", "Kidney"], "Heart", "Biology", "The heart pumps blood through the circulatory system.")
    ],
    "Computer Science": [
        ("What does CPU stand for?", ["Central Processing Unit", "Computer Personal Unit", "Control Program Utility", "Central Power Unit"], "Central Processing Unit", "Computer basics", "CPU means Central Processing Unit."),
        ("Which is an input device?", ["Monitor", "Printer", "Keyboard", "Speaker"], "Keyboard", "Hardware", "A keyboard sends input to a computer."),
        ("What does HTML stand for?", ["Hyper Text Markup Language", "High Text Machine Language", "Hyper Tool Markup Language", "Home Text Markup Language"], "Hyper Text Markup Language", "Web basics", "HTML means HyperText Markup Language."),
        ("Which component stores data temporarily while programs run?", ["RAM", "SSD", "DVD", "Printer"], "RAM", "Hardware", "RAM temporarily stores active data and instructions."),
        ("Which is an example of system software?", ["Operating system", "Photo", "Presentation", "Web page"], "Operating system", "Software", "An operating system is system software."),
        ("What is an algorithm?", ["A step-by-step problem-solving procedure", "A computer screen", "A storage cable", "A file format"], "A step-by-step problem-solving procedure", "Algorithms", "An algorithm is a finite sequence of steps to solve a problem."),
        ("Which number system uses only 0 and 1?", ["Decimal", "Binary", "Octal", "Hexadecimal"], "Binary", "Number systems", "Binary is base 2 and uses 0 and 1."),
        ("What does URL identify?", ["A resource address on the web", "A CPU instruction", "A memory chip", "A programming variable"], "A resource address on the web", "Web basics", "A URL identifies the location of a resource."),
        ("Which device displays visual output?", ["Mouse", "Monitor", "Microphone", "Scanner"], "Monitor", "Hardware", "A monitor displays visual output."),
        ("What is debugging?", ["Finding and fixing errors in a program", "Deleting the operating system", "Installing a keyboard", "Changing a screen"], "Finding and fixing errors in a program", "Programming", "Debugging is the process of identifying and correcting bugs.")
    ]
}

SUBJECT_ICONS = {
    "Python": "🐍", "C Programming": "💻", "Java": "☕",
    "Data Structures & Algorithms": "🧩", "DBMS": "🗄️",
    "Operating Systems": "⚙️", "Computer Networks": "🌐",
    "AI & Machine Learning": "🤖", "Git & GitHub": "🐙",
    "Linux": "🐧", "Cloud Computing": "☁️", "DevOps & CI/CD": "🚀",
    "Mathematics": "🧠", "Science": "🔬", "Computer Science": "🎓"
}

# -------------------- DATABASE --------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student TEXT NOT NULL,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                accuracy REAL NOT NULL,
                weak_topics TEXT,
                wrong_answers TEXT,
                quiz_date TEXT NOT NULL
            )
        """)

def save_result(student, subject, score, total, accuracy, weak_topics, wrong_answers):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO quiz_results
            (student, subject, score, total, accuracy, weak_topics, wrong_answers, quiz_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student, subject, score, total, accuracy,
            json.dumps(weak_topics), json.dumps(wrong_answers), str(date.today())
        ))

def load_results(student):
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT subject, score, total, accuracy, weak_topics, wrong_answers, quiz_date
            FROM quiz_results WHERE student = ? ORDER BY id
        """, (student,)).fetchall()
    results = []
    for row in rows:
        results.append({
            "Subject": row[0], "Score": row[3], "Raw Score": row[1],
            "Total": row[2], "Weak Topics": json.loads(row[4] or "[]"),
            "Wrong Answers": json.loads(row[5] or "[]"), "Date": row[6]
        })
    return results

init_db()

# -------------------- SESSION STATE --------------------
if "student" not in st.session_state:
    if "student" not in st.session_state:
        st.session_state.student = "Student"
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = "Python"
if "history" not in st.session_state:
    st.session_state.history = []
if "history_loaded" not in st.session_state:
    st.session_state.history = load_results(st.session_state.student)
    st.session_state.history_loaded = True
if "custom_questions" not in st.session_state:
    st.session_state.custom_questions = []
if "custom_quiz" not in st.session_state:
    st.session_state.custom_quiz = None
if "revision_done" not in st.session_state:
    st.session_state.revision_done = False

# -------------------- DESIGN --------------------
# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap');

:root {
    --cream: #fff8ef;
    --white: #ffffff;
    --sage: #87977a;
    --sage-dark: #65785b;
    --peach: #f3c9b5;
    --beige: #eee0d0;
    --brown: #55483f;
    --muted: #817266;
}

/* Apply Nunito without breaking Streamlit icons */
html, body, .stApp,
.stApp p,
.stApp label,
.stApp li,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp input,
.stApp textarea,
.stApp button {
    font-family: 'Nunito', sans-serif;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--cream) !important;
    color: var(--brown) !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: var(--sage) !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3, h4 {
    color: var(--brown) !important;
    font-weight: 900 !important;
}

p, label, li {
    color: var(--brown);
}

.stButton > button,
.stFormSubmitButton > button {
    background: var(--sage) !important;
    color: white !important;
    border: none !important;
    border-radius: 13px !important;
    padding: .65rem 1.2rem !important;
    font-weight: 800 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: var(--sage-dark) !important;
    color: white !important;
}

div[data-testid="stMetric"] {
    background: white !important;
    border: 1px solid var(--beige) !important;
    border-radius: 18px !important;
    padding: 16px !important;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--brown) !important;
}

div[data-testid="stForm"] {
    background: white !important;
    border: 1px solid var(--beige) !important;
    border-radius: 18px !important;
    padding: 18px !important;
}

[data-testid="stAlert"] {
    background: #fff0e5 !important;
    border: 1px solid var(--peach) !important;
    border-radius: 15px !important;
    color: var(--brown) !important;
}

[data-testid="stAlert"] * {
    color: var(--brown) !important;
}

.stTextInput input,
.stTextArea textarea,
[data-baseweb="select"] > div {
    background: white !important;
    color: var(--brown) !important;
    border: 1px solid var(--beige) !important;
    border-radius: 12px !important;
}

[data-testid="stRadio"] *,
[data-testid="stCheckbox"] * {
    color: var(--brown) !important;
}

input[type="radio"],
input[type="checkbox"] {
    accent-color: var(--sage) !important;
}

[data-testid="stProgressBar"] > div > div {
    background: var(--sage) !important;
}

.hero {
    background: linear-gradient(110deg, #f8dfc9, #fff0d8) !important;
    border: 1px solid var(--peach);
    border-radius: 24px;
    padding: 26px;
    margin: 12px 0 22px;
}

.hero h2 {
    color: var(--brown) !important;
    font-size: 28px;
    margin: 0 0 10px;
}

.hero p {
    color: var(--muted) !important;
    margin: 4px 0;
}

.hero-art {
    font-size: 72px;
    float: right;
    margin: 4px 22px 0 10px;
}

.subject-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
}

.subject-card {
    background: white !important;
    border: 1px solid var(--beige) !important;
    border-radius: 18px;
    padding: 14px;
    min-height: 155px;
    box-shadow: 0 6px 18px #55483f12;
    transition: .2s;
}

.subject-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px #55483f25;
}

.subject-icon {
    font-size: 42px;
    text-align: center;
}

.subject-name {
    font-weight: 900;
    color: var(--sage-dark) !important;
    text-align: center;
    padding: 8px 0 3px;
}

.subject-desc {
    font-size: 12px;
    color: var(--muted) !important;
    text-align: center;
}

.info-card {
    background: white !important;
    border: 1px solid var(--beige) !important;
    border-radius: 18px;
    padding: 18px;
    margin: 8px 0;
}

.small-note {
    color: var(--muted) !important;
    font-size: 13px;
}

a {
    color: var(--sage-dark) !important;
}

footer {
    visibility: hidden;
}

@media(max-width: 900px) {
    .subject-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}
/* WHITE TEXT INSIDE GREEN SIDEBAR */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] a {
    color: #ffffff !important;
}
/* STREAMLIT TOP TOOLBAR */
[data-testid="stHeader"] {
    background: #fff8ef !important;
}

[data-testid="stToolbar"] {
    background: #fff8ef !important;
}

[data-testid="stHeader"] * {
    color: #55483f !important;
}

[data-testid="stDecoration"] {
    background: #87977a !important;
}
/* FIX INPUT BOXES */
div[data-baseweb="input"] {
    background: white !important;
    border: 1px solid #e5d4c3 !important;
    border-radius: 13px !important;
    box-shadow: none !important;
}

div[data-baseweb="input"]:focus-within {
    border: 2px solid #87977a !important;
    box-shadow: none !important;
}

div[data-baseweb="input"] input {
    color: #55483f !important;
    background: white !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #a8998b !important;
    opacity: 1 !important;
}

/* FIX SIDEBAR RADIO CIRCLES */
[data-testid="stSidebar"] [data-testid="stRadio"] svg {
    color: white !important;
    fill: white !important;
}

/* FIX DARK MESSAGE BOX */
[data-testid="stAlert"],
[data-testid="stAlert"] > div {
    background: #fff0e5 !important;
    border: 1px solid #f3c9b5 !important;
    color: #55483f !important;
    border-radius: 15px !important;
}

/* REMOVE DARK INPUT OUTLINES */
input, textarea {
    outline-color: #87977a !important;
}

/* REMOVE NAVY SIDEBAR CARD */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #f3e8d9 !important;
    color: #55483f !important;
}
/* FIX CREATE QUIZ TEXT VISIBILITY */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea,
[data-testid="stMain"] select {
    color: #55483f !important;
    -webkit-text-fill-color: #55483f !important;
    background-color: #ffffff !important;
    opacity: 1 !important;
}

[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #a8998b !important;
    -webkit-text-fill-color: #a8998b !important;
    opacity: 1 !important;
}

[data-testid="stMain"] label,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p {
    color: #55483f !important;
}

[data-testid="stMain"] [data-baseweb="select"] * {
    color: #55483f !important;
}

[data-testid="stMain"] [data-baseweb="input"] {
    border: 1px solid #e5d4c3 !important;
    border-radius: 13px !important;
    box-shadow: none !important;
}
/* PEACH BOX INSIDE GREEN SIDEBAR */
[data-testid="stSidebar"] [data-testid="stAlert"],
[data-testid="stSidebar"] [data-testid="stAlert"] * {
    background-color: #fff0e5 !important;
    color: #55483f !important;
    -webkit-text-fill-color: #55483f !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] {
    border: 1px solid #f3c9b5 !important;
    border-radius: 15px !important;
}
/* ===== CREATE QUIZ — LEARNIQ DESIGN ===== */

.quiz-creator-hero {
    background: linear-gradient(120deg, #f5dfcf, #fff0df);
    border: 1px solid #edcbb7;
    border-radius: 24px;
    padding: 25px;
    margin: 10px 0 22px;
}

.quiz-creator-hero h2 {
    color: #55483f !important;
    font-size: 27px;
    font-weight: 900;
    margin-bottom: 8px;
}

.quiz-creator-hero p {
    color: #817266 !important;
    font-size: 15px;
}

.quiz-progress-card {
    background: #ffffff;
    border: 1px solid #eee0d0;
    border-radius: 18px;
    padding: 17px;
    margin: 15px 0;
}

.quiz-question-card {
    background: #fffaf4;
    border: 1px solid #eee0d0;
    border-radius: 15px;
    padding: 12px 16px;
    margin: 8px 0;
}

.quiz-section-heading {
    color: #65785b !important;
    font-size: 20px;
    font-weight: 900;
    margin: 18px 0 10px;
}

[data-testid="stForm"] {
    background: #ffffff !important;
    border: 1px solid #ead9c8 !important;
    border-radius: 20px !important;
    padding: 22px !important;
}
/* ===== WHITE TEXT INSIDE GREEN PANELS THROUGHOUT LEARNIQ ===== */

/* Green backgrounds and panels */
div[style*="background-color: #87977a"],
div[style*="background: #87977a"],
div[style*="background-color: #65785b"],
div[style*="background: #65785b"],
.green-panel,
.green-card,
[data-testid="stAlert"] {
    color: #ffffff !important;
}

/* Text inside green panels */
.green-panel *,
.green-card * {
    color: #ffffff !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* Green buttons */
.stButton button {
    color: #ffffff !important;
}

/* Green success messages */
[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #ffffff !important;
}
/* CREATE YOUR OWN QUIZ — GREEN PANELS WITH WHITE TEXT */

[data-testid="stMain"] [style*="background: #87977a"],
[data-testid="stMain"] [style*="background-color: #87977a"],
[data-testid="stMain"] [style*="background: #65785b"],
[data-testid="stMain"] [style*="background-color: #65785b"] {
    color: #ffffff !important;
}

[data-testid="stMain"] [style*="background: #87977a"] *,
[data-testid="stMain"] [style*="background-color: #87977a"] *,
[data-testid="stMain"] [style*="background: #65785b"] *,
[data-testid="stMain"] [style*="background-color: #65785b"] * {
    color: #ffffff !important;
}
/* ===== FORCE WHITE TEXT ON GREEN BUTTONS ===== */

[data-testid="stMain"] .stButton button,
[data-testid="stMain"] .stButton button *,
[data-testid="stMain"] [data-testid="stFormSubmitButton"] button,
[data-testid="stMain"] [data-testid="stFormSubmitButton"] button *,
[data-testid="stMain"] button[kind="primary"],
[data-testid="stMain"] button[kind="primary"] * {
    color: #ffffff !important;
}

/* Green panels and their text */
[data-testid="stMain"] .green-panel,
[data-testid="stMain"] .green-panel * {
    color: #ffffff !important;
}

/* Make button text bold */
[data-testid="stMain"] .stButton button,
[data-testid="stMain"] [data-testid="stFormSubmitButton"] button {
    font-weight: 800 !important;
}

/* LearnIQ sidebar styling */
[data-testid="stSidebar"] {
    background-color: #87977a !important;
}

[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #f3c9b5 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HELPERS --------------------
def get_latest_accuracy(subject):
    matches = [r for r in st.session_state.history if r["Subject"] == subject]
    return matches[-1]["Score"] if matches else None

def recommended_level(subject):
    accuracy = get_latest_accuracy(subject)
    if accuracy is None:
        return "Beginner"
    if accuracy >= 85:
        return "Advanced"
    if accuracy >= 60:
        return "Intermediate"
    return "Beginner"

def show_subject_cards():
    cards = list(quiz_data.items())
    for start in range(0, len(cards), 4):
        cols = st.columns(4)
        for col, (subject, questions) in zip(cols, cards[start:start + 4]):
            with col:
                st.markdown(
                    f"<div class='subject-card'><div class='subject-icon'>{SUBJECT_ICONS.get(subject,'📘')}</div>"
                    f"<div class='subject-name'>{subject}</div><div class='subject-desc'>10 practice questions</div></div>",
                    unsafe_allow_html=True
                )

def run_quiz(subject, questions, quiz_key):
    st.subheader(f"{SUBJECT_ICONS.get(subject, '📝')} {subject} Quiz")
    st.caption(f"{len(questions)} questions • Choose one answer for each question.")
    with st.form(quiz_key):
        answers = []
        for i, item in enumerate(questions):
            question, options, correct, topic, explanation = item
            st.markdown(f"**Q{i + 1}. {question}**")
            answer = st.radio(
                "Select your answer",
                options,
                key=f"{quiz_key}_{i}",
                index=None
            )
            answers.append(answer)
            st.divider()
        submitted = st.form_submit_button("Submit Quiz", use_container_width=True)

    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Please answer all questions before submitting.")
            return
        score = 0
        weak_topics = []
        wrong_answers = []
        for i, item in enumerate(questions):
            question, options, correct, topic, explanation = item
            if answers[i] == correct:
                score += 1
            else:
                if topic not in weak_topics:
                    weak_topics.append(topic)
                wrong_answers.append({
                    "question": question,
                    "your_answer": answers[i],
                    "correct_answer": correct,
                    "explanation": explanation,
                    "topic": topic
                })
        accuracy = round(score / len(questions) * 100, 1)
        save_result(st.session_state.student, subject, score, len(questions), accuracy, weak_topics, wrong_answers)
        result = {
            "Subject": subject, "Score": accuracy, "Raw Score": score,
            "Total": len(questions), "Weak Topics": weak_topics,
            "Wrong Answers": wrong_answers, "Date": str(date.today())
        }
        st.session_state.history.append(result)
        st.success("Quiz submitted successfully!")
        st.metric("Your score", f"{score}/{len(questions)}")
        st.metric("Accuracy", f"{accuracy}%")
        if accuracy >= 85:
            st.balloons()
            st.success("Excellent work! Your next recommended level is Advanced.")
        elif accuracy >= 60:
            st.info("Good effort! Keep practising to strengthen your understanding.")
        else:
            st.warning("Let's revise the basics and try again. You can improve!")
        if weak_topics:
            st.write("**Topics to revise:** " + ", ".join(weak_topics))
        else:
            st.write("You answered every question correctly. Great job!")

# -------------------- LOGIN SYSTEM --------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    div[data-testid="stForm"] {
        max-width: 480px;
        margin: auto;
        padding: 25px;
    }

    div[data-testid="stTabs"] {
        max-width: 530px;
        margin: auto;
    }
    /* Hide password visibility button */
[data-testid="stInputPassword"] button,
[data-testid="stInputPasswordToggle"],
button[aria-label="Show password"],
button[aria-label="Hide password"] {
    display: none !important;
}
}
/* Make Create Account tab text visible */
button[data-baseweb="tab"] {
    color: #654321 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #3F6B50 !important;
    font-weight: bold !important;
}
/* Fix email and password input colours */
div[data-testid="stTextInput"] input {
    color: #55463F !important;
    background-color: #FFFCF7 !important;
    -webkit-text-fill-color: #55463F !important;
}

/* Fix Chrome autofill colours */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
    -webkit-text-fill-color: #55463F !important;
    -webkit-box-shadow: 0 0 0 1000px #FFFCF7 inset !important;
}

/* FIX STREAMLIT ICONS AND ARROW OVERLAPPING */
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons,
[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded" !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 24px !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    direction: ltr !important;
    font-feature-settings: "liga" !important;
    -webkit-font-feature-settings: "liga" !important;
}

/* Keep Smart Revision question text properly aligned */
[data-testid="stExpander"] summary {
    font-family: 'Nunito', sans-serif !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}

[data-testid="stExpander"] summary p {
    font-family: 'Nunito', sans-serif !important;
}
</style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>✦ LearnIQ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Your personal learning companion</p>", unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs(["Sign In", "Create Account"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password", label_visibility="visible")
            
            login_button = st.form_submit_button("Sign In", use_container_width=True)

        if login_button:
            result = authenticate_user(email, password)

            if result:
                st.session_state.student = result[0]
                st.session_state.user_email = result[1]
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect email or password.")

    with signup_tab:
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            new_email = st.text_input("Email Address")
            new_password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_button = st.form_submit_button("Create Account", use_container_width=True)

        if signup_button:
            if not name.strip() or not new_email.strip() or not new_password:
                st.error("Please fill in all fields.")
            elif "@" not in new_email or "." not in new_email:
                st.error("Please enter a valid email address.")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(name, new_email, new_password)

                if success:
                    st.success(message + " Please sign in.")
                else:
                    st.error(message)

    st.stop()

# ------------------------------------------------------
# -------------------- SIDEBAR --------------------
st.sidebar.markdown(
    "<div style='text-align:center;padding:12px 4px 18px;font-size:27px;font-weight:900;'>✦ LearnIQ</div>",
    unsafe_allow_html=True
)
st.sidebar.markdown("<div style='font-size:11px;letter-spacing:2px;color:#e3e5ff;'>YOUR LEARNING SPACE</div>", unsafe_allow_html=True)
pages = [
    "Home", "My Courses", "AI Tutor", "Create Your Own Quiz",
    "My Learning DNA", "Smart Revision", "My Progress", "Settings"
]
page = st.sidebar.radio("MENU", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
st.session_state.page = page
st.sidebar.markdown("---")
st.sidebar.markdown(f"👩‍🎓 **{st.session_state.student}**")
st.sidebar.caption("LEARN • PRACTISE • GROW")
st.sidebar.info("Your learning companion for every subject.")
if st.sidebar.button("🚪 Sign Out", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.pop("user_email", None)
    st.rerun()

# -------------------- HOME --------------------
if page == "Home":
    st.markdown(
        f"<div class='hero'><div class='hero-art'>👩‍💻✨</div>"
        f"<h2>Welcome to LearnIQ, {st.session_state.student}!</h2>"
        "<p>Learn something new, practise with quizzes, and grow at your own pace.</p>"
        "<p>Small steps today. Strong skills tomorrow. 🚀</p></div>",
        unsafe_allow_html=True
    )
    total_quizzes = len(st.session_state.history)
    average = round(sum(r["Score"] for r in st.session_state.history) / total_quizzes, 1) if total_quizzes else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("Quizzes completed", total_quizzes)
    c2.metric("Average accuracy", f"{average}%")
    c3.metric("Available subjects", len(quiz_data))
    st.subheader("🌈 Explore your subjects")
    show_subject_cards()
    st.subheader("✨ Quick start")
    chosen = st.selectbox("Choose a subject to practise", list(quiz_data.keys()))
    if st.button("Start learning", use_container_width=False):
        st.session_state.selected_subject = chosen
        st.session_state.page = "My Courses"
        st.rerun()

# -------------------- MY COURSES --------------------
elif page == "My Courses":
    st.title("📚 My Courses")
    subject_list = list(quiz_data.keys())
    current = st.session_state.selected_subject
    if current not in subject_list:
        current = subject_list[0]
    subject = st.selectbox("Choose a subject", subject_list, index=subject_list.index(current))
    st.session_state.selected_subject = subject
    level = recommended_level(subject)
    st.info(f"Recommended level: **{level}** — based on your latest quiz result in {subject}.")
    run_quiz(subject, quiz_data[subject], f"standard_quiz_{subject}")

# -------------------- AI TUTOR --------------------
elif page == "AI Tutor":
    st.title("🤖 AI Tutor")
    st.write("Your study suggestions are based on your quiz performance.")
    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.markdown(f"<div class='info-card'><h3>Latest learning result</h3><b>{latest['Subject']}</b><br>Accuracy: <b>{latest['Score']}%</b></div>", unsafe_allow_html=True)
        if latest["Score"] >= 85:
            st.success("You have a strong grasp of this quiz. Try a new subject or challenge yourself with advanced practice.")
        elif latest["Score"] >= 60:
            st.info("You are making progress. Review the topics you missed and practise again.")
        else:
            st.warning("Start with the fundamentals. Read the explanations in Smart Revision, then retake the quiz.")
        if latest["Weak Topics"]:
            st.write("**Suggested focus:** " + ", ".join(latest["Weak Topics"]))
    else:
        st.info("Complete your first quiz to receive personalised study suggestions.")
    st.caption("Note: LearnIQ currently uses rule-based recommendations. It does not connect to a live generative AI model.")

# -------------------- CREATE YOUR OWN QUIZ --------------------
# -------------------- CREATE YOUR OWN QUIZ --------------------
elif page == "Create Your Own Quiz":

    st.markdown("""
    <div class="quiz-creator-hero">
        <h2>✨ Design Your Own Quiz</h2>
        <p>Create questions, challenge your knowledge, and share learning with others.</p>
        <p>📚 Your ideas. Your questions. Your learning journey.</p>
    </div>
    """, unsafe_allow_html=True)

    quiz_title = st.text_input(
        "📝 Give your quiz a title",
        placeholder="Example: My Operating Systems Quiz"
    )

    st.markdown(
        "<div class='quiz-section-heading'>🌷 Add your questions</div>",
        unsafe_allow_html=True
    )

    with st.form("add_custom_question", clear_on_submit=True):

        q_text = st.text_input(
            "Your question",
            placeholder="Type your question here..."
        )

        st.caption("Add four answer options.")

        col1, col2 = st.columns(2)

        with col1:
            opt1 = st.text_input("Option A", placeholder="First answer")
            opt2 = st.text_input("Option B", placeholder="Second answer")

        with col2:
            opt3 = st.text_input("Option C", placeholder="Third answer")
            opt4 = st.text_input("Option D", placeholder="Fourth answer")

        col3, col4 = st.columns(2)

        with col3:
            correct_label = st.selectbox(
                "✅ Correct option",
                ["A", "B", "C", "D"]
            )

        with col4:
            explanation = st.text_input(
                "💡 Explanation (optional)",
                placeholder="Explain the correct answer"
            )

        add_question = st.form_submit_button(
            "＋ Add Question",
            use_container_width=True
        )

    if add_question:

        values = [
            q_text.strip(),
            opt1.strip(),
            opt2.strip(),
            opt3.strip(),
            opt4.strip()
        ]

        if not all(values):
            st.error("Please fill in the question and all four options.")

        else:
            options = values[1:]
            correct = options[["A", "B", "C", "D"].index(correct_label)]

            st.session_state.custom_questions.append((
                values[0],
                options,
                correct,
                "Custom topic",
                explanation.strip() or f"The correct answer is {correct}."
            ))

            st.success(
                f"Question added successfully! "
                f"({len(st.session_state.custom_questions)}/10)"
            )

    # PROGRESS
    question_count = len(st.session_state.custom_questions)

    st.markdown("<div class='quiz-progress-card'>", unsafe_allow_html=True)
    st.write(f"**📊 Quiz creation progress: {question_count}/10 questions**")
    st.progress(min(question_count / 10, 1.0))

    if question_count < 10:
        st.caption(f"{10 - question_count} more question(s) needed to complete your quiz.")
    else:
        st.success("🎉 All 10 questions are ready!")
    st.markdown("</div>", unsafe_allow_html=True)

    # QUESTION PREVIEW
    if st.session_state.custom_questions:

        st.markdown(
            "<div class='quiz-section-heading'>📋 Your question collection</div>",
            unsafe_allow_html=True
        )

        for i, q in enumerate(st.session_state.custom_questions):

            with st.container(border=True):
                st.markdown(f"**Question {i + 1}**")
                st.write(q[0])
                st.caption("Options: " + "  •  ".join(q[1]))
                st.caption("Correct answer: " + q[2])

    # ACTION BUTTONS
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button(
            "↩ Undo Last Question",
            disabled=not st.session_state.custom_questions,
            use_container_width=True
        ):
            st.session_state.custom_questions.pop()
            st.rerun()

    with col_b:
        if st.button(
            "🗑 Clear Questions",
            use_container_width=True
        ):
            st.session_state.custom_questions = []
            st.session_state.custom_quiz = None
            st.rerun()

    # SAVE QUIZ
    if question_count == 10:

        st.markdown("---")

        if st.button(
            "🎉 Save My Quiz",
            use_container_width=True
        ):
            st.session_state.custom_quiz = {
                "title": quiz_title.strip() or "My Custom Quiz",
                "questions": st.session_state.custom_questions.copy()
            }
            st.success("Your custom quiz is ready!")

    # TAKE QUIZ
    if st.session_state.custom_quiz:

        st.markdown("---")
        st.markdown(
            "<div class='quiz-section-heading'>🚀 Take Your Created Quiz</div>",
            unsafe_allow_html=True
        )

        st.info(
            f"Your quiz: {st.session_state.custom_quiz['title']}"
        )

        run_quiz(
            st.session_state.custom_quiz["title"],
            st.session_state.custom_quiz["questions"],
            "custom_quiz_form"
        )
# -------------------- LEARNING DNA --------------------
elif page == "My Learning DNA":
    st.title("🧬 My Learning DNA")
    if not st.session_state.history:
        st.info("Complete a quiz to discover your learning profile.")
    else:
        scores = [r["Score"] for r in st.session_state.history]
        avg = round(sum(scores) / len(scores), 1)
        subject_scores = {}
        for subject in quiz_data:
            attempts = [r["Score"] for r in st.session_state.history if r["Subject"] == subject]
            if attempts:
                subject_scores[subject] = round(sum(attempts) / len(attempts), 1)
        best = max(subject_scores, key=subject_scores.get) if subject_scores else "Not enough data"
        needs_work = min(subject_scores, key=subject_scores.get) if subject_scores else "Not enough data"
        a, b, c = st.columns(3)
        a.metric("Overall accuracy", f"{avg}%")
        b.metric("Quizzes completed", len(scores))
        c.metric("Subjects explored", len(subject_scores))
        st.subheader("Your learning profile")
        if avg >= 85:
            st.success("Confident Learner 🌟 — You are performing strongly. Keep challenging yourself.")
        elif avg >= 60:
            st.info("Growing Learner 🌱 — You are building understanding with each attempt.")
        else:
            st.warning("Foundation Builder 🧱 — Focus on core concepts and use Smart Revision.")
        st.write(f"**Strongest subject:** {best}")
        st.write(f"**Subject to practise more:** {needs_work}")
        if subject_scores:
            st.subheader("Subject performance")
            
# -------------------- SMART REVISION --------------------
elif page == "Smart Revision":
    st.title("🔁 Smart Revision")
    wrong_items = []
    for result in st.session_state.history:
        for item in result.get("Wrong Answers", []):
            wrong_items.append((result["Subject"], item))
    if not wrong_items:
        st.success("No missed questions yet. Complete a quiz and any incorrect answers will appear here.")
    else:
        st.write("Review the questions you missed and understand why the correct answer is right.")
        for i, (subject, item) in enumerate(reversed(wrong_items), 1):
            with st.expander(f"{i}. {subject} — {item['question']}"):
                st.write("**Your answer:** " + str(item["your_answer"]))
                st.write("**Correct answer:** " + str(item["correct_answer"]))
                st.write("**Topic:** " + str(item.get("topic", "General")))
                st.info(item["explanation"])

# -------------------- MY PROGRESS --------------------
elif page == "My Progress":
    st.title("📊 My Progress")
    if st.session_state.history:
        scores = [r["Score"] for r in st.session_state.history]
        c1, c2, c3 = st.columns(3)
        c1.metric("Quizzes completed", len(scores))
        c2.metric("Average accuracy", f"{round(sum(scores) / len(scores), 1)}%")
        c3.metric("Best score", f"{max(scores)}%")
        st.subheader("Quiz history")
        st.dataframe([
            {
                "Subject": r["Subject"], "Score": f"{r['Raw Score']}/{r['Total']}",
                "Accuracy": f"{r['Score']}%", "Date": r["Date"]
            } for r in reversed(st.session_state.history)
        ], use_container_width=True, hide_index=True)
        st.subheader("Performance chart")
        chart_data = {}
        for r in st.session_state.history:
            chart_data.setdefault(r["Subject"], []).append(r["Score"])
        pass
    else:
        st.info("Your progress will appear here after you complete a quiz.")

# -------------------- SETTINGS --------------------
elif page == "Settings":
    st.title("⚙️ Settings")
    new_name = st.text_input("Your name", value=st.session_state.student)
    if st.button("Save name"):
        st.session_state.student = new_name.strip() or "Student"
        st.session_state.history = load_results(st.session_state.student)
        st.success("Name saved!")
        st.rerun()
    st.divider()
    st.subheader("Reset progress")
    st.warning("This removes saved quiz history for the current student.")
    confirm_reset = st.checkbox("I understand that my quiz history will be deleted.")
    if st.button("Clear my quiz history", disabled=not confirm_reset):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM quiz_results WHERE student = ?", (st.session_state.student,))
        st.session_state.history = []
        st.success("Your quiz history has been cleared.")
        st.rerun()

st.markdown("---")
st.caption("LearnIQ | Adaptive AI Tutor • Learn • Practise • Improve")
import altair as alt

st.subheader("Performance Chart")

chart_data = {}

for r in st.session_state.history:
    chart_data.setdefault(r["Subject"], []).append(r["Score"])

if chart_data:
    rows = [
        {
            "Subject": subject,
            "Average Score": round(sum(scores) / len(scores), 1)
        }
        for subject, scores in chart_data.items()
    ]

    max_score = max(row["Average Score"] for row in rows)
    axis_max = max(max_score * 1.25, 1)

    chart = (
    alt.Chart(alt.Data(values=rows))
    .mark_bar(size=40, color="#789477")
    .encode(
        x=alt.X(
            "Average Score:Q",
            title="Average Score",
            scale=alt.Scale(domain=[0, 100]),
            axis=alt.Axis(
                labelColor="#59483F",
                titleColor="#59483F",
                grid=False
            )
        ),
        y=alt.Y(
            "Subject:N",
            title=None,
            axis=alt.Axis(
                labelColor="#59483F",
                labelFontSize=14
            )
        ),
        tooltip=[
            alt.Tooltip("Subject:N"),
            alt.Tooltip("Average Score:Q")
        ]
    )
    .properties(
        width=650,
        height=180,
        background="#FFF8F0"
    )
    .configure_view(
        strokeWidth=0
    )
)

    st.altair_chart(chart, use_container_width=True)

else:
    st.info("No performance data available yet.")