import fire
import subprocess
import os
from norm_benchmark.backend.app import main
# from norm_benchmark.frontend.dashboard import create_dashboard


class Norm(object):
    def benchmark(self, model_outputs_path, ground_truths_path, to_leaderboard=False):
        main(model_outputs_path, ground_truths_path, to_leaderboard)

    def dashboard(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        dashboard_script = os.path.join(current_dir, 'frontend/dashboard.py')
        
        # Ensure the path is correct or raise an error if not found
        if not os.path.exists(dashboard_script):
            raise FileNotFoundError(f"Dashboard script not found at {dashboard_script}")
        
        subprocess.run(["streamlit", "run", dashboard_script])


def run():
    fire.Fire(Norm)

if __name__ == "__main__":
    run()