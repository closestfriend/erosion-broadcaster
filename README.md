# Erosion Broadcaster 🌑

A Twitter bot that broadcasts the ongoing decay of the [Digital Erosion](https://github.com/closestfriend/digital-erosion) artwork.

## What It Does

Every 6 hours, this bot:
1. Checks the erosion repository for new decay iterations
2. Extracts poetic snippets from the corrupted code
3. Generates and posts artistic tweets about the deterioration
4. Tracks special events like restoration cycles

## Tweet Styles

The bot randomly chooses between different tweet personalities:

### Minimalist
```
iteration 47

el*e:
    self.iter#tion = 0

#DigitalErosion
```

### Verbose
```
The code continues to forget itself.

def save_st#te(self):
    with open(self.st*te_file, 'w')

Iteration 47 | moderate erosion
#DigitalErosion #GenerativeArt
```

### Abstract
```
▓▓▓▓▓▓▓▓▓▓▓

iteration 47: moderate
#DigitalErosion
```

### Diagnostic
```
[EROSION LOG]
Iteration: 47
Decay: moderate
Mutations: 23

Corruption sample:
chars[i] = random.cho*ce('_~*`')

#DigitalErosion #SoftwareArt
```

## Setup

### 1. Fork/Clone This Repository

### 2. Get Twitter API Credentials
- Go to https://developer.twitter.com
- Create a new app
- Get your API keys and access tokens

### 3. Add GitHub Secrets
In your repository settings, add these secrets:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

### 4. Enable GitHub Actions
The workflow will run automatically every 6 hours.

### 5. (Optional) Modify broadcast.py
To enable actual Twitter posting, update the broadcast function to use `--live` flag.

## Manual Testing

```bash
# Dry run (no actual tweets)
python broadcast.py

# Live posting (requires API credentials)
python broadcast.py --live
```

## How It Works

1. **Clone Erosion Repo**: Pulls the latest corrupted code
2. **Analyze Commits**: Finds new decay iterations
3. **Extract Poetry**: Finds interesting corrupted snippets
4. **Generate Tweet**: Creates artistic text from the decay
5. **Post**: Shares the digital deterioration with the world

## Special Events

The bot gives special attention to:
- **Restoration Events** (☽ RESTORATION EVENT ☾)
- **Milestone Iterations** (10, 50, 100, 500, 1000)
- **Severe/Critical Decay**
- **Haunted Timestamps** (when the code inserts datetime comments)

## State Management

The bot tracks its progress in `.broadcaster_state.json`:
```json
{
  "last_tweeted_commit": "abc123...",
  "total_tweets": 42,
  "last_restoration": "def456..."
}
```

## Philosophy

This broadcaster is a witness to digital entropy. It doesn't judge the decay, it simply observes and reports. Each tweet is a fragment of a larger artwork—the slow dissolution of functional code into poetic noise.

The bot itself is stable and functional, a stark contrast to the deteriorating code it monitors. It's the reliable narrator of an unreliable text.

---

*"The artwork will outlive its own ability to execute."*