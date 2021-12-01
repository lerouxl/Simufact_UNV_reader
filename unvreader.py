import trimesh
import numpy as np
from typing import Sequence


class Unv_process:
    def __init__(self):
        """
        This class is used to read unv files, extract the data and is able to display them
        """
        self.keys = []
        self.description = {"2412": "faces_coordinates",
                            "2411": "vertices_coordinates",
                            "164": "unit",
                            "2414": "simulation_results",
                            "Contained bodies:": "contained_bodies",

                            }

    def __str__(self):
        txt = "Object containing the information of the unv file\n"
        for k in self.keys:
            txt = txt + "\t-" + str(k) + "\n"
        return txt

    def __repr__(self):
        return self.__str__()

    def _add(self, key: str, content: Sequence[str]):
        """
        Method to add to the UNV object a key and a value. Should be used to store the different block of the unv file
        """
        try:
            key = self.description[key]
            setattr(self, key, content)
        except:
            key = key.lower().replace(" ", "_")

            setattr(self, key, np.array([row.split() for row in content[14::2]], dtype=float))  # Remove the header

        self.keys.append(key)

    def load_file(self, path: str):
        """Load a unv file to this object"""

        # Define control value
        is_reading_new_content = False
        will_read_title = False
        will_read_content = False
        title = None
        data = []

        # Load file
        with open(path, 'r', encoding='cp1252') as file:
            # For each line, will determine if this is a new data block or content
            for line in file:
                # If this is a change of data block and save previous block to self
                if line.strip() == "-1":
                    is_reading_new_content = True
                    will_read_title = True

                    if title:
                        # For the results of the simulation, the true title his bellow
                        if title == "2414":
                            title = data[1]
                        self._add(title, data)
                        title = None
                        data = []

                # If this the title of the block
                elif will_read_title:
                    title = line.strip()
                    will_read_title = False
                    will_read_content = True

                # If this is the content of the block
                elif will_read_content:
                    data.append(line.replace("\n", ""))
                    if not hasattr(self, 'time'):
                        if line[0:5] == "Time:":
                            time = line.split()[1]
                            time = float(time)
                            self.time = time
                            m, s = divmod(time, 60)
                            h, m = divmod(m, 60)
                            self.time_human = f"{int(h)}:{int(m)}:{int(s)}"

        self.__extract_vertice__()  # Extract the vertices

    def __extract_vertice__(self):
        # If the data had not been extracted, stop
        if not hasattr(self, 'data_2411'):
            Exception("Data not loaded, run 'load_file' before ")

        self.vertices = np.zeros((len(self.vertices_coordinates) // 2, 3))
        # The data are containing vertice ID and coordinate, we only consider the coordinate
        for i, vertice_line in enumerate(self.vertices_coordinates[1::2]):
            coords = vertice_line.split()  # Separate the X,Y,Z
            coords = [float(c) for c in coords]  # Transform the coordinate text in float

            # Put the coordinate in the vertices
            self.vertices[i] = np.array(coords)

    def __extract_faces__(self):
        # If the data had not been extracted, stop
        if not hasattr(self, 'data_2412'):
            Exception("Data not loaded, run 'load_file' before ")

        self.faces = np.zeros((len(self.faces_coordinates) // 2, 3), dtype=int)

        for i, faces_line in enumerate(self.faces_coordinates[1::2]):
            fa = faces_line.split()  # Separate the vertices ID, Vertice1, vertice 2 and other information
            fa = [int(f) - 1 for f in fa[0:3]]
            fa = np.array(fa)  # Transform the coordinate text in float

            # Put the coordinate in the vertices
            self.faces[i] = fa

    def generate_mesh(self):
        """Wil generate the mesh by loading the value from the unv data
        """
        # If vertice and edges are not computed, compute them
        if not hasattr(self, "vertices"):
            self.__extract_vertice__()
        if not hasattr(self, "faces"):
            self.__extract_faces__()

        self.mesh = trimesh.Trimesh(vertices=self.vertices, faces=self.faces, process=False)

    def display_data(self, key: str):
        """Will display information base on a key, if there is multiple value per vertices a mean will be done"""
        if not hasattr(self, key):
            Exception("Key not existing")

        features = getattr(self, key)
        features = features.mean(axis=1)
        self.mesh.visual.vertex_colors = trimesh.visual.interpolate(features, color_map='viridis')
        return self.mesh.show()