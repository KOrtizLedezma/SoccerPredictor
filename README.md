# Soccer Predictor

Soccer Predictor is a simple application designed to analyze and predict soccer match results using historical data.

Built with Python, the app is bundled into a portable Linux executable for easy use without requiring Python installation.

## How to Run

1. Go into the executable folder:

```bash
cd soccer_predictor_linux
```

2. Make sure the executable has run permissions:

```bash
chmod +x SoccerPredictor
```

3. Run the application:

```bash
./SoccerPredictor
```

Note: The `data/` folder containing `results.csv` must be located next to the executable.

## Build Instructions (for developers)

If you want to build the executable yourself:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Install PyInstaller if needed:

```bash
pip install pyinstaller
```

3. Build the executable for Linux:

```bash
pyinstaller --name SoccerPredictor --onefile --add-data "data:data" src/main.py
```

4. The build output will be inside the `dist/` folder.

## Requirements

- Python 3.13
- pandas
- scikit-learn
- pyinstaller (for building the executable)

(Optional for developers)

## License

This project is licensed under the terms described in the *LICENSE* file.

## Notes

- This `README` assumes the current focus is the Linux executable.
- For a Windows version, a separate build must be created using PyInstaller on a Windows environment.

## Disclaimer

Soccer Predictor is intended for educational and entertainment purposes only. <br/>
The project uses basic statistical models to attempt predictions based on historical data; it does not guarantee or ensure the accuracy of match outcomes. <br/>
Use of this application for betting or financial decision-making is strongly discouraged. <br/>
