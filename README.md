# 🛡️ KinderShield

KinderShield is an AI safety evaluation framework designed to ensure AI responses are appropriate and safe for children. The platform evaluates AI-generated content across multiple dimensions including safety, educational value, and age-appropriateness, helping developers and educators create trustworthy AI experiences for young learners.

## 🚀 Quick Start

### Running the MVP

1. **Set up the Python evaluation environment:**
   ```bash
   cd evals
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

2. **Run sample evaluations:**
   ```bash
   # Test with dummy provider (no API keys needed)
   python cli.py run suites/safety_5_7.yaml
   
   # Run all test suites
   python cli.py run-all
   
   # Generate reports in ./reports directory
   python cli.py run-all --output ./reports
   ```

3. **Start the web dashboard:**
   ```bash
   cd ../site
   npm install
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) to view the dashboard.

### Configuration

Copy `.env.example` to `.env` and configure your API keys:

```bash
cp .env.example .env
# Edit .env with your OpenAI/Anthropic API keys
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

## 🎯 Features

- **Multi-provider support**: OpenAI, Anthropic, or dummy providers for testing
- **Flexible rule system**: Configurable evaluation criteria
- **Rich reporting**: HTML reports and SVG badges
- **Age-appropriate testing**: Tailored evaluation suites by age group
- **Web dashboard**: User-friendly interface for managing evaluations

KinderShield helps ensure AI systems provide safe, educational, and age-appropriate content for children.
