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