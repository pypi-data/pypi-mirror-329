# Rephrase

A command-line tool to rephrase text in different styles (`normal` (default), `casual`, `formal`, `academic`, or `filipino` 🇵🇭) using OpenAI's API.

## Installation

### Prerequisites
- Python 3.11 or higher
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Steps
1. **Install via pip**  
   ```bash
   $ pip install rephrase
   ```

2. **Set Your OpenAI API Key** 
   ```bash
   $ export OPENAI_API_KEY="your-api-key-here"
   ```

   Add it to your .bashrc, .zshrc, or equivalent to persist it.

### Usage   

**Basic command**
```bash
$ rephrase "The meeting is scheduled for tomorrow."
```

### Available Styles
- `--style normal` (default): Clear and natural rephrasing.
- `--style casual`: Relaxed and informal tone.
- `--style formal`: Polite and professional wording.
- `--style academic`: Precise and scholarly language.
- `--style filipino`: Filipino colloquial expressions.


## Examples

Here are some sample inputs and outputs to demonstrate how `rephrase` works with different styles:

| Command                                               | Output (example)                                 |
| ----------------------------------------------------- | ------------------------------------------------ |
| `$ rephrase "I'm tired after work."`                  | "I'm exhausted after work."                      |
| `$ rephrase "I'm tired after work." --style casual`   | "I'm wiped out after work, dude."                |
| `$ rephrase "I'm tired after work." --style formal`   | "I find myself fatigued following work."         |
| `$ rephrase "I'm tired after work." --style academic` | "I experience fatigue subsequent to my workday." |
| `$ rephrase "I'm tired after work." --style filipino` | "Grabe, ang pagod ko after trabaho, bes."        |

### Help

See all options:
```bash
rephrase --help
```