import tkinter as tk
from tkinter import ttk
import threading
from src import model

def start_ui():
    def load_model_background():
        nonlocal trained_model, feature_columns, teams
        trained_model, feature_columns = model.load_model()

        # Extract all teams
        home_teams = [col[5:] for col in feature_columns if col.startswith('Home_')]
        away_teams = [col[5:] for col in feature_columns if col.startswith('Away_')]
        teams = sorted(list(set(home_teams + away_teams)))  # Unique, sorted list

        window.after(0, model_loaded)

    def model_loaded():
        try:
            progress_bar.stop()  # Stop bar moving
        except tk.TclError:
            pass  # If the bar is already destroyed, ignore

        show_main_ui()

    def show_main_ui():
        loading_frame.destroy()

        main_frame = tk.Frame(window)
        main_frame.pack(pady=20)

        title_label = tk.Label(main_frame, text="Select Teams", font=("Arial", 16))
        title_label.pack(pady=10)

        teams_frame = tk.Frame(main_frame)
        teams_frame.pack(pady=10)

        home_team_combo = ttk.Combobox(teams_frame, values=teams, state="readonly", width=25)
        home_team_combo.pack(side="left", padx=10)

        vs_label = tk.Label(teams_frame, text="VS", font=("Arial", 14, "bold"))
        vs_label.pack(side="left", padx=5)

        away_team_combo = ttk.Combobox(teams_frame, values=teams, state="readonly", width=25)
        away_team_combo.pack(side="left", padx=10)

        predict_button = tk.Button(main_frame, text="Predict", command=lambda: on_predict(home_team_combo, away_team_combo, result_label))
        predict_button.pack(pady=10)

        result_label = tk.Label(main_frame, text="", justify="left")
        result_label.pack(pady=10)

    def on_predict(home_team_combo, away_team_combo, result_label):
        home_team = home_team_combo.get().strip()
        away_team = away_team_combo.get().strip()

        if not home_team or not away_team:
            tk.messagebox.showerror("Error", "Please select both Home and Away teams.")
            return

        try:
            probabilities = model.predict_match(trained_model, feature_columns, home_team, away_team)
            result_text = f"Prediction for {home_team} (Home) vs {away_team} (Away):\n\n"
            for result, prob in probabilities.items():
                result_text += f"{result}: {prob:.2f}\n"
            result_label.config(text=result_text)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    # ----- Create main window -----
    window = tk.Tk()
    window.title("Soccer Match Predictor")
    window.geometry("600x300")
    window.resizable(False, False)

    # Loading screen
    loading_frame = tk.Frame(window)
    loading_frame.pack(expand=True)

    loading_label = tk.Label(loading_frame, text="Setting up the match...", font=("Arial", 16))
    loading_label.pack(pady=30)

    progress_bar = ttk.Progressbar(loading_frame, orient="horizontal", mode="indeterminate", length=300)
    progress_bar.pack(pady=10)
    progress_bar.start(10)  # Smooth left-to-right movement

    teams = []
    trained_model = None
    feature_columns = None

    # Start background loading
    threading.Thread(target=load_model_background).start()

    window.mainloop()
