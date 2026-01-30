# Texas Hold'em Equity Calculator

A Monte Carlo simulation-based Texas Hold'em poker equity calculator built as an interactive web application using Streamlit.

## 🌟 Features

* 🎯 Real-time Equity Calculation: Monte Carlo simulation for accurate win probability
* 🃏 Interactive Interface: Intuitive poker card selector with visual cards
* 📊 Visual Results: Pie charts and progress bars showing equity distribution
* 🎮 Multi-stage Support: Pre-flop, flop, turn, and river calculations
* 👥 Flexible Configuration: Adjustable opponents (1-9) and simulation counts

## 🚀 Quick Start

1. Clone the Repository

   ```bash
   git clone https://github.com/Yangyang-Song/poker-equity-calculator.git
   cd poker-equity-calculator
   ```
2. Install Dependencies

   ```bash
   pip install -r requirements.txt # pip install streamlit phevaluator pandas plotly
   ```
3. Run the Application

   ```bash
   streamlit run poker_equity_calculator.py
   ```
4. Access in Browser

The app will open automatically, or you can manually can manually access the URL printed on the terminal.

## 📦 Dependencies

`streamlit>=1.28.0` - Web application framework

`phevaluator>=0.0.6` - Professional poker hand evaluation library

`pandas>=2.0.3` - Data manipulation

`plotly>=5.17.0` - Interactive charts

## 🎮 How to Use

### 1. Select Your Hole Cards

* Use dropdown menus to select rank and suit for two hole cards
* Cards display in symbol format (♠♥♦♣) in real-time

### 2. Set Community Cards

* Flop: Select 0-3 cards (toggle enabled/disabled)
* Turn: Optional 4th community card
* River: Optional 5th community card

### 3. Configure Game Parameters

* Number of Opponents: 1-9 players
* Simulation Count: 100-100,000 iterations (affects accuracy and speed)

### 4. Calculate Equity

* Click the "🚀 Calculate Equity" button to start calculation

### 5. View Results

* Equity Distribution: Pie chart and progress bars
* Detailed Metrics: Precise percentage breakdown
* Hand Strength: Hand type evaluation (Royal Flush, Four of a Kind, etc.)
* Hand Analysis: Opponent hand type probability distribution

## 🧠 Technical Details

### Monte Carlo Simulation

The application uses Monte Carlo method to simulate poker hands:

* Random Dealing: Simulates random distribution of remaining cards
* Hand Evaluation: Uses `phevaluator` library for professional hand strength assessment
* Multiple Iterations: Repeats simulation thousands of times for statistical significance
* Result Aggregation: Calculates win, lose, and tie probabilities

## 🔧 Development

### Code Structure

`simulate_montecarlo()` - Core simulation function

`calculate_exact_equity()` - Exact calculation function (river only)

`get_hand_strength()` - Hand strength evaluation

`get_card_display()` - Card display formatting

### Suggested Extensions

1. History Feature: Save and compare multiple calculations
2. Hand Management: Save and load hand configurations
3. Strategy Suggestions: Betting recommendations based on equity
4. More Poker Variants: Support for Omaha, Short Deck, etc.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venvScriptsactivate
# On Mac/Linux:
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions or suggestions:

Email: 3530737759@qq.com/ 2024141520288@stu.scu.edu.com

## ❤️Special Thanks

This project was developed with the assistance of DeepSeek AI, which provided invaluable guidance, code review, and technical explanations throughout the development process.

---

**Disclaimer:** This tool provides equity calculations for reference only. Actual poker gameplay involves strategy, reading opponents, psychology, and other factors not captured by pure mathematical simulations.

**⭐ If you find this project useful, please give it a Star!**
