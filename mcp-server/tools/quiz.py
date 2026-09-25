"""
MCP Tool: generate_quiz
Generates academic multiple-choice quizzes with options, answers, and explanations.
"""

from typing import Optional, List, Dict, Any

# Curated university academic questions bank
QUIZ_BANK = {
    "DBMS": [
        {
            "question": "Which normal form requires the elimination of transitive dependency?",
            "options": [
                {"key": "A", "text": "First Normal Form (1NF)"},
                {"key": "B", "text": "Second Normal Form (2NF)"},
                {"key": "C", "text": "Third Normal Form (3NF)"},
                {"key": "D", "text": "Boyce-Codd Normal Form (BCNF)"}
            ],
            "correct_answer": "C",
            "explanation": "3NF requires a relation to be in 2NF and have no transitive dependencies (where a non-prime attribute depends on another non-prime attribute)."
        },
        {
            "question": "What is the primary difference between a B-Tree and a B+ Tree in database indexing?",
            "options": [
                {"key": "A", "text": "B-Trees are binary while B+ Trees have n-way branches"},
                {"key": "B", "text": "B+ Trees store actual data records only at the leaf nodes which are linked"},
                {"key": "C", "text": "B-Trees do not support disk storage"},
                {"key": "D", "text": "B+ Trees cannot be indexed"}
            ],
            "correct_answer": "B",
            "explanation": "In a B+ Tree, all data records/pointers are stored exclusively in the leaf nodes, which are linked together in a list, making range queries significantly faster."
        },
        {
            "question": "Which ACID property guarantees that once a transaction commits, its modifications cannot be lost even after a system crash?",
            "options": [
                {"key": "A", "text": "Atomicity"},
                {"key": "B", "text": "Consistency"},
                {"key": "C", "text": "Isolation"},
                {"key": "D", "text": "Durability"}
            ],
            "correct_answer": "D",
            "explanation": "Durability guarantees that once a transaction commits, its effects persist permanently in non-volatile storage via write-ahead logging (WAL)."
        },
        {
            "question": "In Strict Two-Phase Locking (Strict 2PL), when are exclusive (write) locks released?",
            "options": [
                {"key": "A", "text": "Immediately after each write statement"},
                {"key": "B", "text": "At the beginning of the shrinking phase"},
                {"key": "C", "text": "Only after the transaction commits or aborts"},
                {"key": "D", "text": "Whenever another transaction requests them"}
            ],
            "correct_answer": "C",
            "explanation": "Strict 2PL holds all exclusive locks until transaction completion (commit or rollback) to prevent dirty reads and cascading aborts."
        },
        {
            "question": "What is a functional dependency X -> Y considered if Y is a subset of X?",
            "options": [
                {"key": "A", "text": "Trivial functional dependency"},
                {"key": "B", "text": "Non-trivial functional dependency"},
                {"key": "C", "text": "Transitive dependency"},
                {"key": "D", "text": "Partial dependency"}
            ],
            "correct_answer": "A",
            "explanation": "A functional dependency X -> Y is trivial if Y is a subset of X (e.g., {Student_ID, Name} -> Name)."
        }
    ],
    "Computer Networks": [
        {
            "question": "Which layer of the OSI model is responsible for end-to-end packet delivery, flow control, and port addressing?",
            "options": [
                {"key": "A", "text": "Data Link Layer"},
                {"key": "B", "text": "Network Layer"},
                {"key": "C", "text": "Transport Layer"},
                {"key": "D", "text": "Session Layer"}
            ],
            "correct_answer": "C",
            "explanation": "The Transport Layer (Layer 4, TCP/UDP) provides end-to-end host communication, segment flow control, and port-based multiplexing."
        },
        {
            "question": "In the TCP Three-Way Handshake, what packet does the client send in response to the server's SYN-ACK?",
            "options": [
                {"key": "A", "text": "SYN"},
                {"key": "B", "text": "FIN"},
                {"key": "C", "text": "ACK"},
                {"key": "D", "text": "RST"}
            ],
            "correct_answer": "C",
            "explanation": "The handshake sequence is: Client -> SYN, Server -> SYN-ACK, Client -> ACK. Once ACK is received, the connection is ESTABLISHED."
        },
        {
            "question": "How many usable host IP addresses are available in a /24 IPv4 subnet?",
            "options": [
                {"key": "A", "text": "256"},
                {"key": "B", "text": "254"},
                {"key": "C", "text": "128"},
                {"key": "D", "text": "512"}
            ],
            "correct_answer": "B",
            "explanation": "A /24 subnet has 32 - 24 = 8 host bits (2^8 = 256). Subtracting the network address and broadcast address leaves 254 usable host addresses."
        },
        {
            "question": "Which DNS record type maps a domain name directly to an IPv4 address?",
            "options": [
                {"key": "A", "text": "CNAME Record"},
                {"key": "B", "text": "MX Record"},
                {"key": "C", "text": "A Record"},
                {"key": "D", "text": "AAAA Record"}
            ],
            "correct_answer": "C",
            "explanation": "An 'A' record maps a hostname to a 32-bit IPv4 address. 'AAAA' is used for IPv6."
        },
        {
            "question": "Which routing protocol uses Dijkstra's shortest path first algorithm?",
            "options": [
                {"key": "A", "text": "RIP (Routing Information Protocol)"},
                {"key": "B", "text": "OSPF (Open Shortest Path First)"},
                {"key": "C", "text": "BGP (Border Gateway Protocol)"},
                {"key": "D", "text": "EGP"}
            ],
            "correct_answer": "B",
            "explanation": "OSPF is a link-state routing protocol that runs Dijkstra's algorithm to compute loop-free shortest paths across a network topology."
        }
    ],
    "Artificial Intelligence": [
        {
            "question": "What is the primary role of the Model Context Protocol (MCP)?",
            "options": [
                {"key": "A", "text": "To train neural network weights faster"},
                {"key": "B", "text": "To provide an open standard for LLMs to securely connect to external tools and data sources"},
                {"key": "C", "text": "To replace GPUs in transformer computation"},
                {"key": "D", "text": "To compress image files for web view"}
            ],
            "correct_answer": "B",
            "explanation": "MCP standardizes how AI models discover and call external tools, access structured resources, and interact with private context securely."
        },
        {
            "question": "In Retrieval-Augmented Generation (RAG), what metric is most commonly used to measure semantic similarity between vector embeddings?",
            "options": [
                {"key": "A", "text": "Hamming distance"},
                {"key": "B", "text": "Cosine similarity"},
                {"key": "C", "text": "Manhattan distance only"},
                {"key": "D", "text": "Levenshtein distance"}
            ],
            "correct_answer": "B",
            "explanation": "Cosine similarity calculates the cosine of the angle between two dense embedding vectors, measuring orientation and semantic closeness independent of magnitude."
        },
        {
            "question": "In the Transformer attention equation Attention(Q, K, V) = softmax((Q*K^T)/sqrt(d_k))*V, what does d_k represent?",
            "options": [
                {"key": "A", "text": "The number of attention heads"},
                {"key": "B", "text": "The dimension of the key vectors"},
                {"key": "C", "text": "The vocabulary size"},
                {"key": "D", "text": "The batch size"}
            ],
            "correct_answer": "B",
            "explanation": "d_k is the dimensionality of the key vectors; dividing by sqrt(d_k) prevents large dot products that would push the softmax into regions with vanishing gradients."
        },
        {
            "question": "Which of the following describes an MCP Server's capability?",
            "options": [
                {"key": "A", "text": "It exposes tools, resources, and prompt templates to an MCP Client"},
                {"key": "B", "text": "It can only compile C++ binaries"},
                {"key": "C", "text": "It functions as a web browser plugin only"},
                {"key": "D", "text": "It trains foundation models from scratch"}
            ],
            "correct_answer": "A",
            "explanation": "An MCP server provides external capabilities (tools), contextual data (resources), and structured instructions (prompts) to an MCP client."
        },
        {
            "question": "Why is Chunk Overlap used when segmenting documents for RAG pipelines?",
            "options": [
                {"key": "A", "text": "To double the database storage size"},
                {"key": "B", "text": "To prevent semantic loss and split sentences across boundary splits"},
                {"key": "C", "text": "To increase hallucination rates"},
                {"key": "D", "text": "To encrypt the document"}
            ],
            "correct_answer": "B",
            "explanation": "Chunk overlap ensures that sentences or entities appearing near the border of a chunk retain their surrounding semantic context in adjacent chunks."
        }
    ]
}


def generate_quiz(
    subject: str = "DBMS",
    topic: Optional[str] = None,
    number_of_questions: Optional[int] = 5
) -> List[Dict[str, Any]]:
    """
    Generate an academic multiple-choice quiz.

    Args:
        subject: Subject of the quiz ('DBMS', 'Computer Networks', 'Artificial Intelligence').
        topic: Specific topic or module (e.g. 'Normalization', 'TCP', 'RAG').
        number_of_questions: Number of questions (default: 5).

    Returns:
        List of questions with options, correct answer, and explanation.
    """
    num = max(1, min(10, number_of_questions or 5))
    
    # Match subject key
    selected_subject = "DBMS"
    for s_key in QUIZ_BANK:
        if s_key.lower() in subject.lower() or subject.lower() in s_key.lower():
            selected_subject = s_key
            break
            
    questions = QUIZ_BANK.get(selected_subject, QUIZ_BANK["DBMS"])
    
    # Return requested count
    result = []
    for idx, q in enumerate(questions[:num]):
        result.append({
            "id": f"q_{idx + 1}",
            "subject": selected_subject,
            "topic": topic or selected_subject,
            "question": q["question"],
            "options": q["options"],
            "correct_answer": q["correct_answer"],
            "explanation": q["explanation"]
        })
        
    return result
