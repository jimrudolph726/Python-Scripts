import cProfile
import pstats
import io
import pygame
import sys
import os
from main import Game

def profile_game(output_file):
    pr = cProfile.Profile()
    pr.enable()
    print("Profiling started...")

    try:
        game = Game()
        game.run()
    except Exception as e:
        print("Error during game execution:", e)
        sys.exit(1)
    finally:
        pr.disable()
        print("Profiling ended.")

        # Save profiling results to a file
        try:
            with open(output_file, "w") as f:
                ps = pstats.Stats(pr, stream=f).sort_stats('cumulative')
                ps.print_stats()
            print(f"Profiling results saved to {output_file}")
        except Exception as e:
            print("Error while saving profiling results:", e)

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)

    # Define the output file path explicitly
    output_file_path = os.path.join(os.getcwd(), 'profile_results.txt')
    print(f"Output file will be saved to: {output_file_path}")

    try:
        profile_game(output_file_path)
    finally:
        pygame.quit()
        print("Pygame quit successfully.")
