#!/usr/bin/env python3
"""
Erosion Broadcaster: Witness the Digital Decay
Tweets snippets from the deteriorating code, creating poetry from corruption.
"""

import os
import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
import re

class ErosionBroadcaster:
    def __init__(self):
        self.erosion_repo = "https://github.com/closestfriend/digital-erosion.git"
        self.local_erosion_path = Path("./erosion_clone")
        self.state_file = Path(".broadcaster_state.json")
        self.load_state()
        
    def load_state(self):
        """Load the last known state of the broadcaster"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                "last_tweeted_commit": None,
                "total_tweets": 0,
                "last_restoration": None
            }
    
    def save_state(self):
        """Save the current state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def clone_or_pull_erosion(self):
        """Get the latest erosion repository state"""
        if not self.local_erosion_path.exists():
            subprocess.run(["git", "clone", self.erosion_repo, str(self.local_erosion_path)], 
                         capture_output=True)
        else:
            subprocess.run(["git", "pull"], cwd=self.local_erosion_path, capture_output=True)
    
    def get_recent_commits(self, limit=10):
        """Get recent commit information"""
        result = subprocess.run(
            ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%s|%ai"],
            cwd=self.local_erosion_path,
            capture_output=True,
            text=True
        )
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                hash_val, message, date = line.split('|')
                commits.append({
                    "hash": hash_val,
                    "message": message,
                    "date": date
                })
        return commits
    
    def get_corrupted_snippet(self, commit_hash):
        """Extract a poetic snippet from the corrupted code"""
        # Get the erosion.py file at specific commit
        result = subprocess.run(
            ["git", "show", f"{commit_hash}:erosion.py"],
            cwd=self.local_erosion_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return None
        
        lines = result.stdout.split('\n')
        
        # Find interesting corrupted lines
        corrupted_lines = []
        for i, line in enumerate(lines):
            # Look for lines with visible corruption
            if any(char in line for char in ['#', '*', '~', '`', '\t']) and len(line.strip()) > 0:
                # Check for syntax errors or interesting patterns
                if re.search(r'[a-z]\*[a-z]|[a-z]#[a-z]|^\s*\.|^\s*#\s*\d{4}', line):
                    corrupted_lines.append((i, line))
            # Also catch broken syntax
            elif re.search(r'el\*e:|with#|def\s+\w+#|chars\s+i\]', line):
                corrupted_lines.append((i, line))
        
        if not corrupted_lines:
            # If no obvious corruption, pick random non-empty lines
            non_empty = [(i, l) for i, l in enumerate(lines) if l.strip()]
            if non_empty:
                return random.choice(non_empty)[1][:280]
            return None
        
        # Select the most interesting corruption
        line_num, chosen_line = random.choice(corrupted_lines)
        
        # Sometimes include context
        if random.random() < 0.3 and line_num > 0:
            context = lines[line_num - 1] if line_num > 0 else ""
            return f"{context}\n{chosen_line}"[:280]
        
        return chosen_line[:280]
    
    def get_diff_snippet(self, commit_hash):
        """Get a visual diff showing the decay"""
        result = subprocess.run(
            ["git", "diff", f"{commit_hash}~1", commit_hash, "--", "erosion.py"],
            cwd=self.local_erosion_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 or not result.stdout:
            return None
        
        # Find interesting diff chunks
        diff_lines = result.stdout.split('\n')
        changes = []
        
        for i, line in enumerate(diff_lines):
            if line.startswith('-') and not line.startswith('---'):
                # Find what was removed
                removed = line[1:]
                # Look for the corresponding addition
                for j in range(i+1, min(i+5, len(diff_lines))):
                    if diff_lines[j].startswith('+') and not diff_lines[j].startswith('+++'):
                        added = diff_lines[j][1:]
                        if len(removed) > 10 and len(added) > 10:
                            changes.append((removed, added))
                        break
        
        if changes:
            removed, added = random.choice(changes)
            return f"was:\n{removed[:100]}\n\nnow:\n{added[:100]}"
        
        return None
    
    def generate_tweet(self, commit):
        """Generate a poetic tweet from a commit"""
        iteration_match = re.search(r'iteration (\d+)', commit['message'])
        iteration = iteration_match.group(1) if iteration_match else "∞"
        
        # Detect restoration events
        if "RESTORATION" in commit['message']:
            tweet = f"☽ RESTORATION EVENT ☾\n\n"
            tweet += f"iteration {iteration}\n\n"
            tweet += "the code remembers itself\nimperfectly\n\n"
            tweet += "#DigitalErosion #ConceptualArt"
            return tweet
        
        # Extract decay level
        decay_match = re.search(r'(\w+) erosion', commit['message'])
        decay_level = decay_match.group(1) if decay_match else "unknown"
        
        # Get a corrupted snippet
        snippet = self.get_corrupted_snippet(commit['hash'])
        
        # Choose tweet style
        styles = [
            self.minimalist_tweet,
            self.verbose_tweet,
            self.abstract_tweet,
            self.diagnostic_tweet
        ]
        
        style = random.choice(styles)
        return style(iteration, decay_level, snippet, commit)
    
    def minimalist_tweet(self, iteration, decay_level, snippet, commit):
        """Minimal, poetic style"""
        if snippet:
            # Clean up the snippet for poetry
            snippet = snippet.strip()[:100]
            return f"iteration {iteration}\n\n{snippet}\n\n#DigitalErosion"
        else:
            return f"iteration {iteration}: {decay_level} decay\n\n#DigitalErosion"
    
    def verbose_tweet(self, iteration, decay_level, snippet, commit):
        """More descriptive style"""
        intro = random.choice([
            f"The code continues to forget itself.",
            f"Hour {iteration}: progressive deterioration.",
            f"Syntax dissolves into memory.",
            f"The program dreams of its own entropy."
        ])
        
        if snippet:
            snippet = snippet.strip()[:120]
            return f"{intro}\n\n{snippet}\n\nIteration {iteration} | {decay_level} erosion\n#DigitalErosion #GenerativeArt"
        else:
            return f"{intro}\n\nIteration {iteration}: {decay_level} erosion\n#DigitalErosion"
    
    def abstract_tweet(self, iteration, decay_level, snippet, commit):
        """Abstract, artistic style"""
        if snippet and any(char in snippet for char in ['*', '#', '~', '`']):
            # If we have good corruption, let it speak
            visual = ""
            for char in snippet[:50]:
                if char in ['*', '#', '~', '`', '.', ' ', '\t']:
                    visual += char
            
            if visual.strip():
                return f"{visual}\n\niteration {iteration}\n#DigitalErosion #CodePoetry"
        
        # Create abstract representation
        decay_symbols = {
            "minimal": "░",
            "slight": "▒", 
            "moderate": "▓",
            "severe": "█",
            "critical": "▪"
        }
        
        symbol = decay_symbols.get(decay_level, "·")
        bar = symbol * min(int(iteration) % 20 + 1, 20)
        
        return f"{bar}\n\niteration {iteration}: {decay_level}\n#DigitalErosion"
    
    def diagnostic_tweet(self, iteration, decay_level, snippet, commit):
        """Technical, diagnostic style"""
        mutations_match = re.search(r'(\d+) mutations', commit['message'])
        mutations = mutations_match.group(1) if mutations_match else "?"
        
        tweet = f"[EROSION LOG]\n"
        tweet += f"Iteration: {iteration}\n"
        tweet += f"Decay: {decay_level}\n"
        tweet += f"Mutations: {mutations}\n"
        
        if snippet and len(snippet) < 100:
            tweet += f"\nCorruption sample:\n{snippet[:80]}\n"
        
        tweet += "\n#DigitalErosion #SoftwareArt"
        return tweet
    
    def should_tweet(self, commit):
        """Determine if we should tweet about this commit"""
        # Always tweet restorations
        if "RESTORATION" in commit['message']:
            return True
        
        # Don't tweet the same commit twice
        if commit['hash'] == self.state.get('last_tweeted_commit'):
            return False
        
        # Tweet based on iteration number (every 6 hours = every 6 iterations)
        iteration_match = re.search(r'iteration (\d+)', commit['message'])
        if iteration_match:
            iteration = int(iteration_match.group(1))
            # Tweet every 6 iterations, or if it's a milestone
            if iteration % 6 == 0 or iteration in [10, 50, 100, 500, 1000]:
                return True
        
        # Tweet if decay is severe or critical
        if 'severe' in commit['message'] or 'critical' in commit['message']:
            return True
        
        return False
    
    def broadcast(self, dry_run=True):
        """Main broadcast function"""
        print(f"[{datetime.now()}] Starting erosion broadcast...")
        
        # Update local copy of erosion repo
        self.clone_or_pull_erosion()
        
        # Get recent commits
        commits = self.get_recent_commits(limit=20)
        
        if not commits:
            print("No commits found")
            return
        
        # Find commits to tweet about
        for commit in commits:
            if self.should_tweet(commit):
                tweet = self.generate_tweet(commit)
                
                if dry_run:
                    print(f"\n{'='*50}")
                    print(f"Would tweet ({len(tweet)} chars):")
                    print(f"{'='*50}")
                    print(tweet)
                    print(f"{'='*50}\n")
                else:
                    # This is where we'd actually post to Twitter
                    # For now, just log it
                    print(f"Tweet posted: {tweet[:50]}...")
                
                self.state['last_tweeted_commit'] = commit['hash']
                self.state['total_tweets'] += 1
                
                if "RESTORATION" in commit['message']:
                    self.state['last_restoration'] = commit['hash']
                
                self.save_state()
                
                # Only tweet once per run
                break
        else:
            print("No new commits to tweet about")

if __name__ == "__main__":
    import sys
    
    broadcaster = ErosionBroadcaster()
    dry_run = "--live" not in sys.argv
    
    if dry_run:
        print("Running in DRY RUN mode (no actual tweets)")
        print("Use --live flag to actually post tweets")
    
    broadcaster.broadcast(dry_run=dry_run)