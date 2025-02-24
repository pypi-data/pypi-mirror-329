import fire
import subprocess

from norm_benchmark.backend.app import main
# from norm_benchmark.frontend.dashboard import create_dashboard


class Norm(object):
    def benchmark(self, model_outputs_path, ground_truths_path, to_leaderboard=False):
        main(model_outputs_path, ground_truths_path, to_leaderboard)

    def dashboard(self):
        subprocess.run(["streamlit", "run", "norm_benchmark/frontend/dashboard.py"])


def run():
    fire.Fire(Norm)

if __name__ == "__main__":
    run()