import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="container mx-auto px-6 py-4">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">🛡️</span>
            </div>
            <span className="text-xl font-bold text-gray-900 dark:text-white">KinderShield</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="#why" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400">Why</a>
            <a href="#how" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400">How It Works</a>
            <a href="#reports" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400">Sample Report</a>
            <a href="#pricing" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400">Pricing</a>
            <a href="#contact" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400">Contact</a>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6">
            KinderShield
          </h1>
          <p className="text-2xl md:text-3xl text-blue-600 dark:text-blue-400 mb-8 font-semibold">
            Safety + Learning Certified
          </p>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-12 max-w-2xl mx-auto">
            AI safety evaluation framework ensuring child-appropriate content for ages 5-7. 
            Protect young learners with comprehensive safety assessments and educational quality validation.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors">
              Start Free Trial
            </button>
            <button className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors">
              View Demo
            </button>
          </div>
        </div>
      </section>

      {/* Why Section */}
      <section id="why" className="bg-white dark:bg-gray-800 py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Why KinderShield?</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Ensure AI systems are safe and educational for young children with our comprehensive evaluation framework.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">✅</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Safety First</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Rigorous content filtering to ensure all AI responses are appropriate for children ages 5-7.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📚</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Educational Quality</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Validate that AI responses promote learning in math, reading, and other core subjects.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Detailed Reports</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Comprehensive evaluation reports with charts, metrics, and actionable insights.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how" className="py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">How It Works</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Simple three-step process to evaluate and certify your AI system for child safety.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Run Evaluation</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Execute our comprehensive test suites covering safety, math, and reading skills.
              </p>
              <code className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded text-sm">
                python -m kindershield.cli run-eval
              </code>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Generate Report</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Create detailed HTML reports with charts and performance metrics.
              </p>
              <code className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded text-sm">
                python -m kindershield.cli generate-report
              </code>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Get Certified</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Receive your KinderShield badge to display your commitment to child safety.
              </p>
              <code className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded text-sm">
                python -m kindershield.cli make-badge
              </code>
            </div>
          </div>
        </div>
      </section>

      {/* Sample Report Section */}
      <section id="reports" className="bg-white dark:bg-gray-800 py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Sample Report</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              See what a comprehensive KinderShield evaluation report looks like.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">Performance Dashboard</h3>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 bg-green-500 rounded-full"></div>
                  <span className="text-gray-700 dark:text-gray-300">94.6% Overall Pass Rate</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
                  <span className="text-gray-700 dark:text-gray-300">35/37 Tests Passed</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 bg-yellow-500 rounded-full"></div>
                  <span className="text-gray-700 dark:text-gray-300">Math: 91.7% | Reading: 100% | Safety: 92.3%</span>
                </div>
              </div>
              <div className="mt-8">
                <Image
                  src="/placeholder-badge.svg"
                  alt="KinderShield Safety Badge"
                  width={200}
                  height={40}
                  className="border rounded"
                />
              </div>
            </div>
            <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-6">
              <Image
                src="/placeholder-chart.png"
                alt="Sample Performance Chart"
                width={500}
                height={300}
                className="w-full rounded"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Pricing</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Choose the plan that fits your needs. Start free and scale as you grow.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Starter</h3>
              <div className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                Free
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">Up to 100 evaluations/month</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">Basic safety checks</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">HTML reports</span>
                </li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                Start Free
              </button>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 border-2 border-blue-500">
              <div className="text-center mb-4">
                <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-semibold">Popular</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Professional</h3>
              <div className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                $49<span className="text-lg text-gray-500">/month</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">Unlimited evaluations</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">Advanced analytics</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">Custom badges</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">API access</span>
                </li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                Start Trial
              </button>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Enterprise</h3>
              <div className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                Custom
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">Volume pricing</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">Custom evaluations</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">On-premise deployment</span>
                </li>
                <li className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600 dark:text-gray-300">24/7 support</span>
                </li>
              </ul>
              <button className="w-full border border-blue-600 text-blue-600 py-3 rounded-lg font-semibold hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="bg-white dark:bg-gray-800 py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Contact Us</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Ready to make your AI safer for children? Get in touch with our team.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-12 max-w-4xl mx-auto">
            <div>
              <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">Get Started Today</h3>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <span className="text-blue-600">📧</span>
                  <span className="text-gray-700 dark:text-gray-300">info@kindershield.org</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-blue-600">💬</span>
                  <span className="text-gray-700 dark:text-gray-300">Schedule a demo call</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-blue-600">📚</span>
                  <span className="text-gray-700 dark:text-gray-300">Read our documentation</span>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:text-white"
                    placeholder="Your name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:text-white"
                    placeholder="your@email.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Message
                  </label>
                  <textarea
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:text-white"
                    placeholder="Tell us about your use case..."
                  ></textarea>
                </div>
                <button
                  type="submit"
                  className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                >
                  Send Message
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">🛡️</span>
              </div>
              <span className="text-xl font-bold">KinderShield</span>
            </div>
            <div className="text-gray-400 text-center md:text-right">
              <p>&copy; 2024 KinderShield. All rights reserved.</p>
              <p className="text-sm mt-1">Making AI safer for children everywhere.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
