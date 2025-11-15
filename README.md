# BMI Calculator

A simple BMI (Body Mass Index) calculator built in Python with both command-line and graphical user interface (GUI) versions.

## Features

- **Command-Line Version**: Interactive CLI for calculating BMI with input validation.
- **GUI Version**: Tkinter-based interface for user-friendly interaction.
- **Data Storage**: SQLite database to store user data and BMI records.
- **History and Trends**: View historical BMI data and visualize trends with matplotlib graphs.
- **Input Validation**: Ensures weight and height are positive numbers.
- **BMI Categories**: Automatically categorizes BMI as Underweight, Normal weight, Overweight, or Obese.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- SQLite3 (included with Python)
- Matplotlib (install via `pip install matplotlib`)

## Installation

1. Clone or download the project files.
2. Install matplotlib if not already installed:
   ```
   pip install matplotlib
   ```

## Usage

### Command-Line Version
Run the CLI version:
```
python3 bmi_calculator.py
```
Enter weight in kg and height in meters when prompted.

### GUI Version
Run the GUI version:
```
python3 bmi_gui.py
```
- Select or add a user.
- Enter weight and height.
- Calculate BMI and view results.
- Access history and trend plots.

## BMI Categories

- Underweight: BMI < 18.5
- Normal weight: 18.5 ≤ BMI < 25
- Overweight: 25 ≤ BMI < 30
- Obese: BMI ≥ 30

## Files

- `bmi_calculator.py`: Command-line BMI calculator.
- `bmi_gui.py`: GUI version with database and plotting.
- `bmi_data.db`: SQLite database (created automatically).
- `README.md`: This file.

## Testing

The calculator has been tested with various inputs:
- Valid inputs: Correct BMI calculation and categorization.
- Invalid inputs: Negative, zero, or non-numeric values are rejected.
- Edge cases: Boundary values for each BMI category.

## License

This project is open-source. Feel free to use and modify.
