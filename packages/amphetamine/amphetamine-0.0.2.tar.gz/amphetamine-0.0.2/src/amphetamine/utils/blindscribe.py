from datetime import datetime
import sys
import termios
import tty
import os
import threading
import json
from queue import Queue
from itertools import cycle
import anthropic

class Blindscribe:
    def __init__(self):
        self.queue = Queue()
        self.running = False
        self.spinner = cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
        self.client = anthropic.Anthropic()
        self.session_filename = f"blindscribe{datetime.now().strftime('%Y%m%d%H%M')}.json"
        self.entries = []
        self.entries_lock = threading.Lock()
        self.print_lock = threading.Lock()  # Add lock for thread-safe printing

    def _get_ai_comment(self, text):
        try:
            system_prompt = """You are an expert explainer with deep knowledge across many fields. Your task is to provide a very concise but insightful explanation of the text provided. Requirements:

- Be extremely concise (max 2-3 sentences)
- Focus on the core concept/question/idea
- Use clear, direct language
- Provide uncommon but relevant insights when possible
- If the text contains multiple ideas, focus on the most salient one
- If the text is unclear, make reasonable inferences about the intended meaning
- Prefer concrete details over general statements
- If there's specific context in the text (technical field, time period, etc.), incorporate it
- If the text seems to contain an error or misconception, gently note it

DO NOT:
- Include phrases like "based on the text" or "it seems"
- Provide multiple interpretations or hedging statements 
- Waste words on pleasantries or meta-commentary
- Exceed 512 tokens under any circumstances

Remember: You're writing a crisp, clear note-to-self style explanation that gets straight to the point."""

            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                system=system_prompt,
                max_tokens=512,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": text
                }]
            )
            return str(message.content)
        except Exception as e:
            return f"Error getting AI comment: {str(e)}"

    def _process_entry(self, keyword, content):
        entry = {
            "keyword": keyword,
            "timestamp": datetime.now().isoformat(),
            "char_count": len(content),
            "content": content
        }
        
        with self.entries_lock:
            self.entries.append(entry)
            self._write_entries()
        
        # Always start AI processing thread with the keyword as the query
        ai_thread = threading.Thread(
            target=self._process_ai_comment,
            args=(entry, len(self.entries) - 1, keyword)  # Pass keyword as additional argument
        )
        ai_thread.daemon = True
        ai_thread.start()

    def _process_ai_comment(self, entry, index, query):
        try:
            ai_comment = self._get_ai_comment(query)
            
            # Print the AI response immediately with thread-safe printing
            with self.print_lock:
                print("\n\nAI Response for '{}':".format(entry['keyword']))
                print("=" * 40)
                print(ai_comment)
                print("=" * 40)
                print("\nEnter keyword: ", end='', flush=True)  # Restore prompt
            
            # Update the stored entry
            with self.entries_lock:
                self.entries[index]['aiComment'] = str(ai_comment)
                self._write_entries()
        except Exception as e:
            error_msg = f"Error getting AI comment: {str(e)}"
            with self.print_lock:
                print(f"\n\nError: {error_msg}")
                print("\nEnter keyword: ", end='', flush=True)
            with self.entries_lock:
                self.entries[index]['aiComment'] = error_msg
                self._write_entries()

    def _write_entries(self):
        with open(self.session_filename, 'w') as f:
            json.dump(self.entries, f, indent=2)

    def _get_keyword(self):
        try:
            return input("\nEnter keyword: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

    def capture_session(self):
        try:
            print(f"\nStarting new session: {self.session_filename}")
            print("Press Ctrl+D to submit entry, Ctrl+C to exit")
            
            while True:
                keyword = self._get_keyword()
                if not keyword:
                    continue
                
                print(f"\nEnter text for: {keyword}")
                content = []
                
                while True:
                    try:
                        line = input()
                        content.append(line)
                    except EOFError:  # Ctrl+D
                        break
                    except KeyboardInterrupt:  # Ctrl+C
                        print("\nGoodbye!")
                        return
                
                full_content = '\n'.join(content)
                self._process_entry(keyword, full_content)
                print(f"\nEntry saved: {len(full_content)} characters")
                
        except Exception as e:
            print(f"\nUnexpected error: {e}")

def main():
    annotator = Blindscribe()
    annotator.capture_session()

if __name__ == "__main__":
    main()
