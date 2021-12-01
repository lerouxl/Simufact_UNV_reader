# Simufact_UNV_reader
Python class to read UNV files produced for Simufact 2021.

## For who this code is?:
This code is intended for people using Simufact 2021 and would like to import unv results in python.

## Installation:
1. Copy `unvreader.py` in your project
2. Install the requirement with `pip install -r requirements.txt`
3. Import the Unv_process class in your code with `from unvreader import Unv_process`

## Example
```python
from unvreader import Unv_process

UNV_FILE = r"examples\surface-cantileverXbeam-mm_76.unv"

unv = Unv_process()
unv.load_file(UNV_FILE)
unv.generate_mesh()

# Print the printing time of the simulation
print(f"Time: {unv.time_human}")
# Print the available data in the unv file
print(unv)

# Display
unv.display_data("displacement_vector")
```
Text output:

<img src="https://raw.githubusercontent.com/hy-son/Simufact_UNV_reader/main/imgs/output_example.PNG">

Comparison between Simufact display and display_data:

<img src="https://raw.githubusercontent.com/hy-son/Simufact_UNV_reader/main/imgs/displacement_vector_comparison_example.PNG">

*(The base plate was not extracted in the unv file)*
## Available functions:
- `load_file(path: str)`: Used to load the UNV file. This will parse the UNV file and add the extracted results to the object.
- `generate_mesh()`: Will generate the mesh using trimesh and the data contained in the UNV file.
- `display_data(key: str)`: Map on the mesh the extracted value from the key. In case there is multiple data per vertices, **the mean of those value is displayed**.

## Available variables:
- `time_human` -> `str` containing the simulated time for the simulation.
- `keys` -> `list` list of all available results. Can be displayed by printing the object as show in example. 
- keys -> `ndarray`:  numpy array containing the results.

## Limitation
This reader is not an official one as is provided as is.
The UNV files are providing some information that are not used in this reader such as:
- Faces informations:
<img src="https://raw.githubusercontent.com/hy-son/Simufact_UNV_reader/reader_limitation/imgs/faces_blocks.PNG">
  
- Vertices information:
<img src="https://raw.githubusercontent.com/hy-son/Simufact_UNV_reader/reader_limitation/imgs/coordinate_block.PNG">
  
## Errors
### ImportError('no graph engines available!'):
This errors is due to the installation of trimesh.
To solve this problem, run this command:
`pip install trimesh[easy]` or `pip install trimesh[all]`
