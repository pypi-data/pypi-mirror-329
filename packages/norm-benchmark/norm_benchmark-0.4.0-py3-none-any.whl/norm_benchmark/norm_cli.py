import fire

from norm_benchmark.backend.app import main
from norm_benchmark.frontend.dashboard import create_dashboard


class Norm(object):
    def benchmark(self, model_outputs_path, to_leaderboard=False):
        main(model_outputs_path, to_leaderboard)

    def dashboard(self):
        create_dashboard()


def run():
    fire.Fire(Norm)

if __name__ == "__main__":
    run()