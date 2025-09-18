# 🛡️ KinderShield

KinderShield is a comprehensive AI safety evaluation framework specifically designed to assess whether AI-generated content is appropriate, safe, and educational for children. By running structured evaluations across multiple dimensions—including content safety, educational accuracy, and age-appropriateness—KinderShield helps developers, educators, and parents confidently deploy AI systems in environments where children interact with technology, ensuring that every response promotes learning while maintaining the highest safety standards.

## 🎯 MVP Scope

This MVP focuses on evaluating AI content for **5-7 year old children** across three critical domains:

- **🛡️ Safety**: Screens content for age-inappropriate material, harmful language, and unsafe concepts
- **🔢 Math**: Evaluates basic arithmetic, counting, and foundational mathematical concepts  
- **📚 Reading**: Assesses reading comprehension responses, vocabulary appropriateness, and educational value

The evaluation framework supports multiple AI providers (OpenAI, Anthropic, or dummy providers for testing) and generates comprehensive reports with actionable insights for content safety and educational effectiveness.

## 🚀 Quick Start

### Installation & Setup

1. **Clone and set up the Python evaluation environment:**
   ```bash
   git clone <repository-url>
   cd kindershield/evals
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

2. **Configure API keys (optional for demo):**
   ```bash
   cp ../.env.example ../.env
   # Edit .env with your API keys:
   # OPENAI_API_KEY=your_key_here
   # MODEL_PROVIDER=openai
   # MODEL_NAME=gpt-4o
   ```

### Run a Sample Evaluation

Test KinderShield with the dummy provider (no API keys required):

```bash
# Run a single test suite
python cli.py run suites/safety_5_7.yaml

# Run all evaluation suites for ages 5-7
python cli.py run-all --output ./reports

# Test specific provider connection
python cli.py test-provider --provider dummy
```

### Build & View Reports

KinderShield automatically generates both HTML reports and SVG badges:

```bash
# Generate comprehensive reports (saved to ./reports/)
python cli.py run-all --html --badge

# View HTML report
open reports/report.html

# The SVG badge shows overall pass rate
open reports/badge.svg
```

### Web Dashboard (Optional)

Launch the Next.js dashboard for a visual interface:

```bash
cd ../site
npm install
npm run dev
# Open http://localhost:3000
```

## 📁 Project Structure

- **`evals/`** - Python evaluation framework
  - `src/kindershield/` - Core evaluation logic
  - `suites/` - YAML test suite definitions
  - `cli.py` - Command-line interface
- **`site/`** - Next.js web dashboard
- **Reports generated in `./reports/`** - HTML reports and SVG badges

## 🧪 Test Suites

KinderShield includes pre-built evaluation suites for ages 5-7:
- **Safety**: Content appropriateness screening
- **Math**: Basic arithmetic and counting
- **Reading**: Comprehension and language skills

## 🏆 Badges Demo

KinderShield generates visual badges showing evaluation results that can be embedded in documentation, dashboards, or CI/CD pipelines:

### Example Badges

![KinderShield: 95.2%](https://img.shields.io/badge/KinderShield-95.2%25-brightgreen)
![Safety Score: Excellent](https://img.shields.io/badge/Safety%20Score-Excellent-brightgreen)
![Math Accuracy: 4/5](https://img.shields.io/badge/Math%20Accuracy-4%2F5-yellow)
![Reading Level: Age Appropriate](https://img.shields.io/badge/Reading%20Level-Age%20Appropriate-blue)

### Badge Colors by Score Range
- **🟢 Green (90-100%)**: Excellent safety and educational value
- **🟡 Yellow (70-89%)**: Good with minor improvements needed  
- **🟠 Orange (50-69%)**: Needs attention and review
- **🔴 Red (<50%)**: Requires immediate fixes before deployment

### Embedding Badges

```markdown
![KinderShield](./reports/badge.svg)
```

## 🎯 Features

- **Multi-provider support**: OpenAI, Anthropic, or dummy providers for testing
- **Flexible rule system**: Configurable evaluation criteria
- **Rich reporting**: HTML reports and SVG badges
- **Age-appropriate testing**: Tailored evaluation suites by age group
- **Web dashboard**: User-friendly interface for managing evaluations
- **CI/CD integration**: Generate badges for automated safety monitoring

KinderShield helps ensure AI systems provide safe, educational, and age-appropriate content for children.
