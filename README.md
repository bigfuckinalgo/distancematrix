# distancematrix

This is a Python script to calculate a distance matrix, i.e. the distances for all permutations between a set of two locations. It relies on the Bing Maps API to get these distances.
In the context of this project, distance matrices were necessary to have the costs - in terms of travel time and km distance - for any combination of two teams on one league level playing in the same division.

## Setup

This script was developed with Python3 and currently only has one non-Python standardlib dependency. You can install it with `pip3 install -r requirements.txt`.

Furthermore, you will need to have a Bing Maps API key and save it in a `secrets.py` in the project directory with `bing_maps_key = yourapikey` as the content.

## Running the script

`python3 matrix.py` runs the script that calls the Bing Maps distance API and writes the distance matrix JSON. For this to work, the file specified within `with open("kl_b-junioren_niedersachsen.json", "r") as f:` has to be presented (We can't share this input data on GitHub, due to requirements by the Challenge provider).

## CSV output

Originally this script was developed with a CSV file as output, but we preferred to have JSON as both input and output. However, the lines of code to (also) create a CSV are still included in the file - just commented out.
