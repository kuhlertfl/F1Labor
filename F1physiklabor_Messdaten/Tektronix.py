"""Handle measurement data from the oscilloscopy Tektronix TDS2004B. """

import pathlib
import csv
import numpy as np


class File:
    """Represents the content of a CSV-File from the
    Oscilloscopy Tektronix TDS2004B.

    Args:
        filename (str or pathlib.Path): Name of the .csv-file to read. """

    def __init__(self, filename):
        self.file = pathlib.Path(filename)
        """pathlib.Path: Filname. """
        self.x = None
        """np.ndarray: horizontal coordinates of the measurement. """
        self.y = None
        """np.ndarray: vertical coordinates of the measurement. """
        self.info = dict()
        """dict: Measurement information. """

        with open(self.file) as f:
            x = []
            y = []
            for row in csv.reader(f):
                # The last two columns should be the actual measurement date.
                # Because the last column ends with a comma, we need to
                # address these coloumns with index -3 and -2.
                x.append(float(row[-3]))
                y.append(float(row[-2]))

                # Read the first two columns into a dict.
                if row[0]:
                    name = row[0]
                    value = row[1]
                    # Try to convert the value to int or to float.
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    self.info[name] = value
            self.x = np.array(x, dtype=float)
            self.y = np.array(y, dtype=float)


class Dict(dict):
    """Represents a set of measurements from the
    Oscilloscopy Tektronix TDS2004B.

    The dictionary keys represent the Source given by the oscilloscopy.

    Args:
        path (str or pathlib.Path): Direcotry containing the csv-files.
    """
    def __init__(self, path):
        super().__init__()

        self.path = pathlib.Path(path)
        if not any(self.path.glob('*.[Cc][Ss][Vv]')):
            raise FileNotFoundError(f"Keine CSV-Dateien im Verzeichnis: {self.path}")
        """pathlib.Path: Direcotry containing the csv-files."""

        # Read all csv-files in the given directory.
        for s in self.path.glob('*.[Cc][Ss][Vv]'):
            f = File(s)
            self[f.info['Source']] = f
