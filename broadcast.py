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
from twitter_integration import TwitterPoster

class ErosionBroadcaster:
    def __init__(self):
        self.erosion_repo = "https://github.com/closestfriend/digital-erosion.git"
        self.local_erosion_path = Path("./erosion_clone")
        self.state_file = Path(".broadcaster_state.json")
        self.twitter = TwitterPoster()
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
    
    def should_use_hashtags(self, commit, iteration, decay_level):
        """Decide whether to include hashtags based on various factors"""
        # Always use hashtags for restoration events (special occasions)
        if "RESTORATION" in commit['message']:
            return True
        
        # Use hashtags for milestone iterations
        try:
            iter_num = int(iteration)
            if iter_num in [1, 10, 50, 100, 500, 1000] or iter_num % 100 == 0:
                return True
        except (ValueError, TypeError):
            pass
        
        # Use hashtags for severe/critical decay (dramatic moments)
        if decay_level in ['severe', 'critical']:
            return True
        
        # Random chance: 30% of the time for regular tweets
        return random.random() < 0.3

    def get_hashtags(self, style_name, is_restoration=False):
        """Get appropriate hashtags based on context"""
        base_tags = ["#DigitalErosion"]
        
        if is_restoration:
            return base_tags + ["#ConceptualArt"]
        
        # Vary hashtags by style
        style_tags = {
            "diagnostic": ["#SoftwareArt"],
            "abstract": ["#CodePoetry"],
            "verbose": ["#GenerativeArt"],
            "minimalist": []  # Minimalist style avoids extra tags
        }
        
        return base_tags + style_tags.get(style_name, [])

    def generate_tweet(self, commit):
        """Generate a poetic tweet from a commit"""
        iteration_match = re.search(r'iteration (\d+)', commit['message'])
        iteration = iteration_match.group(1) if iteration_match else "∞"
        
        # Detect restoration events
        if "RESTORATION" in commit['message']:
            tweet = f"☽ RESTORATION EVENT ☾\n\n"
            tweet += f"iteration {iteration}\n\n"
            tweet += "the code remembers itself\nimperfectly"
            
            # Always include hashtags for restoration events
            hashtags = self.get_hashtags("restoration", is_restoration=True)
            tweet += f"\n\n{' '.join(hashtags)}"
            return tweet
        
        # Extract decay level
        decay_match = re.search(r'(\w+) erosion', commit['message'])
        decay_level = decay_match.group(1) if decay_match else "unknown"
        
        # Get a corrupted snippet
        snippet = self.get_corrupted_snippet(commit['hash'])
        
        # Decide whether to use hashtags
        use_hashtags = self.should_use_hashtags(commit, iteration, decay_level)
        
        # Choose tweet style
        styles = [
            ("minimalist", self.minimalist_tweet),
            ("verbose", self.verbose_tweet),
            ("abstract", self.abstract_tweet),
            ("diagnostic", self.diagnostic_tweet)
        ]
        
        style_name, style_func = random.choice(styles)
        return style_func(iteration, decay_level, snippet, commit, use_hashtags, style_name)
    
    def minimalist_tweet(self, iteration, decay_level, snippet, commit, use_hashtags, style_name):
        """Minimal, poetic style"""
        if snippet:
            # Clean up the snippet for poetry
            snippet = snippet.strip()[:100]
            tweet = f"iteration {iteration}\n\n{snippet}"
        else:
            tweet = f"iteration {iteration}: {decay_level} decay"
        
        if use_hashtags:
            hashtags = self.get_hashtags(style_name)
            tweet += f"\n\n{' '.join(hashtags)}"
        
        return tweet
    
    def verbose_tweet(self, iteration, decay_level, snippet, commit, use_hashtags, style_name):
        """More descriptive style"""
        intro = random.choice([
            f"The code continues to forget itself.",
            f"Hour {iteration}: progressive deterioration.",
            f"Syntax dissolves into memory.",
            f"The program dreams of its own entropy."
        ])
        
        if snippet:
            snippet = snippet.strip()[:120]
            tweet = f"{intro}\n\n{snippet}\n\nIteration {iteration} | {decay_level} erosion"
        else:
            tweet = f"{intro}\n\nIteration {iteration}: {decay_level} erosion"
        
        if use_hashtags:
            hashtags = self.get_hashtags(style_name)
            tweet += f"\n{' '.join(hashtags)}"
        
        return tweet
    
    def abstract_tweet(self, iteration, decay_level, snippet, commit, use_hashtags, style_name):
        """Abstract, artistic style"""
        if snippet and any(char in snippet for char in ['*', '#', '~', '`']):
            # If we have good corruption, let it speak
            visual = ""
            for char in snippet[:50]:
                if char in ['*', '#', '~', '`', '.', ' ', '\t']:
                    visual += char
            
            if visual.strip():
                tweet = f"{visual}\n\niteration {iteration}"
                if use_hashtags:
                    hashtags = self.get_hashtags(style_name)
                    tweet += f"\n{' '.join(hashtags)}"
                return tweet
        
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
        
        tweet = f"{bar}\n\niteration {iteration}: {decay_level}"
        if use_hashtags:
            hashtags = self.get_hashtags(style_name)
            tweet += f"\n{' '.join(hashtags)}"
        
        return tweet
    
    def diagnostic_tweet(self, iteration, decay_level, snippet, commit, use_hashtags, style_name):
        """Technical, diagnostic style"""
        mutations_match = re.search(r'(\d+) mutations', commit['message'])
        mutations = mutations_match.group(1) if mutations_match else "?"
        
        tweet = f"[EROSION LOG]\n"
        tweet += f"Iteration: {iteration}\n"
        tweet += f"Decay: {decay_level}\n"
        tweet += f"Mutations: {mutations}"
        
        if snippet and len(snippet) < 100:
            tweet += f"\n\nCorruption sample:\n{snippet[:80]}"
        
        if use_hashtags:
            hashtags = self.get_hashtags(style_name)
            tweet += f"\n\n{' '.join(hashtags)}"
        
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
                    # Actually post to Twitter
                    if self.twitter.connected:
                        tweet_id = self.twitter.post_tweet(tweet)
                        if tweet_id:
                            print(f"✓ Tweet posted successfully: https://twitter.com/i/web/status/{tweet_id}")
                        else:
                            print("⚠ Failed to post tweet")
                    else:
                        print("⚠ Twitter not connected, cannot post tweet")
                
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