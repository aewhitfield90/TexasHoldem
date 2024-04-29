import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath('../'))  # Adjust path as necessary to reach the project's parent directory

# Ensure the card_info_lut_builder module is in the Python path or properly imported
from card_info_lut_builder import CardInfoLutBuilder

def run_clustering(
    low_card_rank=10,
    high_card_rank=14,
    n_river_clusters=50,
    n_turn_clusters=50,
    n_flop_clusters=50,
    n_simulations_river=6,
    n_simulations_turn=6,
    n_simulations_flop=6,
    save_dir="clustering"    
):
    """Run clustering with specified parameters."""
    
    print(f"Data will be saved in: {save_dir}")

    builder = CardInfoLutBuilder(
        n_simulations_river,
        n_simulations_turn,
        n_simulations_flop,
        low_card_rank,
        high_card_rank,
        save_dir
    )

    builder.compute(
        n_river_clusters,
        n_turn_clusters,
        n_flop_clusters,
    )

    print("Clustering completed and data saved in:", save_dir)


if __name__ == "__main__":
    # These parameters can be adjusted or taken from sys.argv if needed
    run_clustering()
