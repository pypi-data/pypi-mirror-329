import os
from textwrap import dedent
import json
from collections import deque
from datetime import datetime


import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from haikunator import Haikunator
import sqlite3
import uuid

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL")
PERPLEXITY_MODEL_ASK = os.getenv("PERPLEXITY_MODEL_ASK")
PERPLEXITY_MODEL_CHAT = os.getenv("PERPLEXITY_MODEL_CHAT")
PERPLEXITY_API_BASE_URL = "https://api.perplexity.ai"

haikunator = Haikunator()
DB_PATH = os.getenv("DB_PATH", "chats.db")
SYSTEM_PROMPT = """You are an expert assistant providing accurate answers to technical questions. 
Your responses must:
1. Be based on the most relevant web sources
2. Include source citations for all factual claims
3. If no relevant results are found, suggest 2-3 alternative search queries that might better uncover the needed information
4. Prioritize technical accuracy, especially for programming-related questions"""

server = Server("mcp-server-perplexity")


def init_db():
    try:
        # Create parent directories if needed
        db_dir = os.path.dirname(DB_PATH)
        if db_dir:  # Only create directories if path contains them
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create tables with enhanced error handling
        c.execute('''CREATE TABLE IF NOT EXISTS chats
                     (id TEXT PRIMARY KEY,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      title TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id TEXT PRIMARY KEY,
                      chat_id TEXT,
                      role TEXT,
                      content TEXT,
                      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY(chat_id) REFERENCES chats(id))''')

        # Verify table creation
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('chats', 'messages')")
        existing_tables = {row[0] for row in c.fetchall()}
        if 'chats' not in existing_tables or 'messages' not in existing_tables:
            raise RuntimeError("Failed to create database tables")

        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection error: {str(e)}")
    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize database at '{DB_PATH}': {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()


# Initialize database on startup
init_db()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="ask_perplexity",
            description=dedent(
                """
                Provides expert programming assistance through Perplexity.
                This tool only has access to the context you have provided. It cannot read any file unless you provide it with the file content.
                Focuses on coding solutions, error debugging, and technical explanations.
                Returns responses with source citations and alternative suggestions.
                """
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Technical question or problem to solve"
                    }
                },
                "required": ["query"]
            },
        ),
        types.Tool(
            name="chat_perplexity",
            description=dedent("""
                Maintains ongoing conversations with Perplexity AI.
                Creates new chats or continues existing ones with full history context.
                This tool only has access to the context you have provided. It cannot read any file unless you provide it with the file content.
                Returns chat ID for future continuation.

                For new chats: Provide 'message' and 'title'
                For existing chats: Provide 'chat_id' and 'message'
                """),
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "New message to add to the conversation"
                    },
                    "chat_id": {
                        "type": "string",
                        "description": "ID of an existing chat to continue. If not provided, a new chat will be created and title is required."
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the new chat. Required when creating a new chat (when chat_id is not provided)."
                    }
                },
                "required": ["message"]
            },
        ),
        types.Tool(
            name="list_chats_perplexity",
            description=dedent("""
                Lists all available chat conversations with Perplexity AI.
                Returns chat IDs, titles, and creation dates.
                Results are paginated with 50 chats per page.
                """),
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number (defaults to 1)",
                        "minimum": 1
                    }
                }
            },
        ),
        types.Tool(
            name="read_chat_perplexity",
            description=dedent("""
                Retrieves the complete conversation history for a specific chat.
                Returns the full chat history with all messages and their timestamps.
                No API calls are made to Perplexity - this only reads from local storage.
                """),
            inputSchema={
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "ID of the chat to retrieve"
                    }
                },
                "required": ["chat_id"]
            },
        )
    ]


def generate_chat_id():
    return haikunator.haikunate(token_length=2, delimiter='-').lower()


def store_message(chat_id, role, content, title=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create chat if it doesn't exist
    c.execute("INSERT OR IGNORE INTO chats (id, title) VALUES (?, ?)",
              (chat_id, title))

    # Store message
    c.execute("INSERT INTO messages (id, chat_id, role, content) VALUES (?, ?, ?, ?)",
              (str(uuid.uuid4()), chat_id, role, content))

    conn.commit()
    conn.close()


def get_chat_history(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''SELECT role, content FROM messages 
                 WHERE chat_id = ? 
                 ORDER BY timestamp''', (chat_id,))
    history = [{"role": row[0], "content": row[1]} for row in c.fetchall()]
    conn.close()
    return history


def get_relative_time(timestamp_str):
    try:
        # Parse the timestamp string to datetime object - timestamps are stored in UTC
        utc_dt = datetime.strptime(
            timestamp_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=None)
        # Get current time in UTC for comparison
        now_utc = datetime.utcnow()

        # Calculate the time difference
        diff = now_utc - utc_dt
        seconds = diff.total_seconds()

        # For future dates or dates too far in the future/past, show the actual date
        if abs(seconds) > 31536000:  # More than a year
            # Convert to local time for display
            local_dt = utc_dt + (datetime.now() - datetime.utcnow())
            return local_dt.strftime("%Y-%m-%d %H:%M:%S")

        if seconds < 0:  # Future dates within a year
            seconds = abs(seconds)
            prefix = "in "
            suffix = ""
        else:
            prefix = ""
            suffix = " ago"

        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{prefix}{minutes} minute{'s' if minutes != 1 else ''}{suffix}"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{prefix}{hours} hour{'s' if hours != 1 else ''}{suffix}"
        elif seconds < 604800:  # 7 days
            days = int(seconds / 86400)
            return f"{prefix}{days} day{'s' if days != 1 else ''}{suffix}"
        elif seconds < 2592000:  # 30 days
            weeks = int(seconds / 604800)
            return f"{prefix}{weeks} week{'s' if weeks != 1 else ''}{suffix}"
        else:  # less than a year
            months = int(seconds / 2592000)
            return f"{prefix}{months} month{'s' if months != 1 else ''}{suffix}"
    except Exception:
        return timestamp_str  # Return original string if parsing fails


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    context = server.request_context
    progress_token = context.meta.progressToken if context.meta else None

    if name == "ask_perplexity":
        system_prompt = dedent(SYSTEM_PROMPT).strip()

        try:
            # Initialize progress tracking with dynamic estimation
            initial_estimate = 1000
            progress_counter = 0
            total_estimate = initial_estimate
            chunk_sizes = deque(maxlen=10)  # Store last 10 chunk sizes
            chunk_count = 0

            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=0,
                    total=initial_estimate,
                )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{PERPLEXITY_API_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": PERPLEXITY_MODEL_ASK or PERPLEXITY_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": arguments["query"]}
                        ],
                        "stream": True
                    },
                    timeout=60.0,
                )
                response.raise_for_status()

                citations = []
                full_response = ""
                usage = {}

                async for chunk in response.aiter_text():
                    for line in chunk.split('\n'):
                        line = line.strip()
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if "usage" in data:
                                    usage.update(data["usage"])
                                if "citations" in data:
                                    citations.extend(data["citations"])
                                if data.get("choices"):
                                    content = data["choices"][0].get(
                                        "delta", {}).get("content", "")
                                    full_response += content

                                    # Update progress with dynamic estimation
                                    tokens_in_chunk = len(content.split())
                                    progress_counter += tokens_in_chunk
                                    chunk_count += 1
                                    chunk_sizes.append(tokens_in_chunk)

                                    # Update total estimate every 5 chunks
                                    if chunk_count % 5 == 0 and chunk_sizes:
                                        avg_chunk_size = sum(
                                            chunk_sizes) / len(chunk_sizes)
                                        total_estimate = max(initial_estimate,
                                                             int(progress_counter + avg_chunk_size * 10))

                                    if progress_token:
                                        await context.session.send_progress_notification(
                                            progress_token=progress_token,
                                            progress=progress_counter,
                                            total=total_estimate,
                                        )
                            except json.JSONDecodeError:
                                continue

                # Format citations with numbered list starting from 1
                unique_citations = list(dict.fromkeys(citations))
                citation_list = "\n".join(
                    f"{i}. {url}" for i, url in enumerate(unique_citations, start=1))

                response_text = (
                    f"{full_response}\n\n"
                    f"Sources:\n{citation_list}\n\n"
                    f"API Usage:\n"
                    f"- Prompt tokens: {usage.get('prompt_tokens', 'N/A')}\n"
                    f"- Completion tokens: {usage.get('completion_tokens', 'N/A')}\n"
                    f"- Total tokens: {usage.get('total_tokens', 'N/A')}"
                )

                if progress_token:
                    await context.session.send_progress_notification(
                        progress_token=progress_token,
                        progress=progress_counter,
                        total=progress_counter,  # Set final total to actual tokens received
                    )

                return [
                    types.TextContent(
                        type="text",
                        text=response_text
                    )
                ]

        except httpx.HTTPError as e:
            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=progress_counter if 'progress_counter' in locals() else 0,
                    total=progress_counter if 'progress_counter' in locals() else 0,
                )
            raise RuntimeError(f"API error: {str(e)}")

    elif name == "chat_perplexity":
        chat_id = arguments.get("chat_id") or generate_chat_id()
        user_message = arguments["message"]
        title = arguments.get("title")

        # Store user message
        if not arguments.get("chat_id"):  # Only store title for new chats
            store_message(chat_id, "user", user_message, title or "Untitled")
        else:
            store_message(chat_id, "user", user_message)

        # Get full chat history
        chat_history = get_chat_history(chat_id)

        system_prompt = dedent(SYSTEM_PROMPT).strip()

        # Initialize progress tracking with dynamic estimation
        initial_estimate = 1000
        progress_counter = 0
        total_estimate = initial_estimate
        chunk_sizes = deque(maxlen=10)  # Store last 10 chunk sizes
        chunk_count = 0

        try:
            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=0,
                    total=initial_estimate,
                )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{PERPLEXITY_API_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": PERPLEXITY_MODEL_CHAT or PERPLEXITY_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            *chat_history,
                        ],
                        "stream": True
                    },
                    timeout=60.0,
                )
                response.raise_for_status()

                citations = []
                full_response = ""
                usage = {}

                async for chunk in response.aiter_text():
                    for line in chunk.split('\n'):
                        line = line.strip()
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if "usage" in data:
                                    usage.update(data["usage"])
                                if "citations" in data:
                                    citations.extend(data["citations"])
                                if data.get("choices"):
                                    content = data["choices"][0].get(
                                        "delta", {}).get("content", "")
                                    full_response += content

                                    # Update progress with dynamic estimation
                                    tokens_in_chunk = len(content.split())
                                    progress_counter += tokens_in_chunk
                                    chunk_count += 1
                                    chunk_sizes.append(tokens_in_chunk)

                                    # Update total estimate every 5 chunks
                                    if chunk_count % 5 == 0 and chunk_sizes:
                                        avg_chunk_size = sum(
                                            chunk_sizes) / len(chunk_sizes)
                                        total_estimate = max(initial_estimate,
                                                             int(progress_counter + avg_chunk_size * 10))

                                    if progress_token:
                                        await context.session.send_progress_notification(
                                            progress_token=progress_token,
                                            progress=progress_counter,
                                            total=total_estimate,
                                        )
                            except json.JSONDecodeError:
                                continue

                # Format citations with numbered list starting from 1
                unique_citations = list(dict.fromkeys(citations))
                citation_list = "\n".join(
                    f"{i}. {url}" for i, url in enumerate(unique_citations, start=1))

                # Store assistant response
                store_message(chat_id, "assistant", full_response)

                # Format chat history
                history_text = "\nChat History:\n"
                for msg in chat_history:
                    role = "You" if msg["role"] == "user" else "Assistant"
                    history_text += f"\n{role}: {msg['content']}\n"

                response_text = (
                    f"Chat ID: {chat_id}\n"
                    f"{history_text}\n"
                    f"Current Response:\n{full_response}\n\n"
                    f"Sources:\n{citation_list}"
                )

                if progress_token:
                    await context.session.send_progress_notification(
                        progress_token=progress_token,
                        progress=progress_counter,
                        total=progress_counter,  # Set final total to actual tokens received
                    )

                return [
                    types.TextContent(
                        type="text",
                        text=response_text
                    )
                ]

        except httpx.HTTPError as e:
            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=progress_counter if 'progress_counter' in locals() else 0,
                    total=progress_counter if 'progress_counter' in locals() else 0,
                )
            raise RuntimeError(f"API error: {str(e)}")

    elif name == "list_chats_perplexity":
        page = arguments.get("page", 1)
        page_size = 50
        offset = (page - 1) * page_size

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Get total count for pagination info
        c.execute("SELECT COUNT(*) FROM chats")
        total_chats = c.fetchone()[0]
        total_pages = (total_chats + page_size - 1) // page_size

        # Get paginated chats with their latest message
        c.execute('''
            SELECT 
                c.id,
                c.title,
                c.created_at,
                (SELECT COUNT(*) FROM messages m WHERE m.chat_id = c.id) as message_count
            FROM chats c
            ORDER BY c.created_at DESC
            LIMIT ? OFFSET ?
        ''', (page_size, offset))

        chats = c.fetchall()
        conn.close()

        # Format the response
        header = (
            f"Page {page} of {total_pages}\n"
            f"Total chats: {total_chats}\n\n"
            f"{'=' * 40}\n"
        )

        chat_list = []
        for chat_id, title, created_at, message_count in chats:
            relative_time = get_relative_time(created_at)
            chat_list.append(
                f"Chat ID: {chat_id}\n"
                f"Title: {title or 'Untitled'}\n"
                f"Created: {relative_time}\n"
                f"Messages: {message_count}"
            )

        response_text = header + "\n\n".join(chat_list)

        return [types.TextContent(type="text", text=response_text)]

    elif name == "read_chat_perplexity":
        chat_id = arguments["chat_id"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Get chat info
        c.execute("SELECT title, created_at FROM chats WHERE id = ?", (chat_id,))
        chat_info = c.fetchone()

        if not chat_info:
            conn.close()
            raise ValueError(f"Chat with ID {chat_id} not found")

        title, created_at = chat_info

        # Get chat history with timestamps
        c.execute('''
            SELECT role, content, timestamp 
            FROM messages 
            WHERE chat_id = ? 
            ORDER BY timestamp
        ''', (chat_id,))

        messages = c.fetchall()
        conn.close()

        # Format the response
        chat_header = (
            f"Chat ID: {chat_id}\n"
            f"Title: {title or 'Untitled'}\n"
            f"Created: {created_at}\n"
            f"Messages: {len(messages)}\n\n"
            f"{'=' * 40}\n\n"
        )

        message_history = []
        for role, content, timestamp in messages:
            role_display = "You" if role == "user" else "Assistant"
            message_history.append(
                f"[{timestamp}] {role_display}:\n{content}\n"
            )

        response_text = chat_header + "\n".join(message_history)

        return [types.TextContent(type="text", text=response_text)]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():

    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-server-perplexity",
                    server_version="0.1.2",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(
                            tools_changed=True),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        print(f"Server error: {str(e)}", flush=True)
        raise
    print("Server shutdown", flush=True)
