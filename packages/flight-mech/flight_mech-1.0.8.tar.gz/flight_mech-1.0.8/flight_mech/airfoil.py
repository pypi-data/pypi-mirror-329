"""
Module to analyse airfoil aerodynamic properties.
"""

###########
# Imports #
###########

# Python imports #

import os
from typing import Literal

# Dependencies #

import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

# Local imports #

from flight_mech._common import plot_graph

#############
# Constants #
#############

# Define a default plane database location
default_airfoil_database = os.path.join(
    os.path.dirname(__file__), "airfoil_database")

#############
# Functions #
#############

def convert_float_or_none_to_string(value: float | None):
    if value is None:
        return ""
    return str(value)

def download_web_file(url, output_file):
    # Make the GET request to download the file
    response = requests.get(url)
    response.raise_for_status()

    # Write the file content to the specified output file
    with open(output_file, 'wb') as file:
        file.write(response.content)

def rotate_arrays(x_array: np.ndarray, z_array: np.ndarray, angle: float, rotation_center: float = 0.25, x_length: float | None = None):
    """
    Rotate the given x and z arrays.

    Parameters
    ----------
    x_array : np.ndarray
        X array to rotate.
    z_array : np.ndarray
        Z array to rotate.
    angle : float
        Angle of rotation in rad.
    rotation_center : float, optional
        Center of rotation in % of the x array, by default 0.25

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Tuple containing the rotated arrays.
    """

    if x_length is None:
        x_length = np.max(x_array)

    rotated_x_array = (x_array - x_length * rotation_center) * \
        np.cos(angle) + z_array * \
        np.sin(angle) + x_length * rotation_center
    rotated_z_array = -(x_array - x_length * rotation_center) * \
        np.sin(angle) + z_array * np.cos(angle)

    return rotated_x_array, rotated_z_array

def naca_airfoil_generator(maximum_camber: float | None = None, maximum_camber_position: float | None = None, maximum_thickness: float | None = None, naca_name: str | None = None, nb_points: int = 200):
    """
    Generate a NACA airfoil.

    Parameters
    ----------
    maximum_camber : float
        Maximum camber value.
    maximum_camber_position : float
        Maximum camber position.
    thickness : float
        Maximum thickness value.
    naca_name : str
        Name of the NACA airfoil. If provided, the other geometry parameters will not be used.
    nb_points : int, optional
        Number of points, by default 200
    """

    if naca_name is not None:
        naca_digits = naca_name.lower().replace("naca", "").replace("_", "")
        maximum_camber = int(naca_digits[0]) / 100
        maximum_camber_position = int(naca_digits[1]) / 10
        maximum_thickness = int(naca_digits[2:]) / 100

    def y_c(x):
        """Camber line equation"""
        res = (maximum_camber / maximum_camber_position**2) * (2 * maximum_camber_position * x - x**2) * (x < maximum_camber_position) \
            + (maximum_camber / (1 - maximum_camber_position)**2) * (1 - 2 * maximum_camber_position +
                                                                     2 * maximum_camber_position * x - x**2) * (x >= maximum_camber_position)

        return res

    def y_t(x):
        """Thickness equation"""
        a0 = 0.2969
        a1 = -0.126
        a2 = -0.3516
        a3 = 0.2843
        a4 = -0.1036
        res = (maximum_thickness / 0.2) * (a0 * x**0.5 + a1 *
                                           x + a2 * x**2 + a3 * x**3 + a4 * x ** 4)
        return res

    # Define x coordinates array
    x_array = np.linspace(0, 1, nb_points)

    # Compute camber and thickness
    camber_z_array = y_c(x_array)
    thickness_array = y_t(x_array)

    # Compute intrados and extrados
    intrados_z_array = camber_z_array - thickness_array
    extrados_z_array = camber_z_array + thickness_array

    # Create the airfoil
    airfoil = Airfoil()
    airfoil.x_array = x_array
    airfoil.intrados_z_array = intrados_z_array
    airfoil.extrados_z_array = extrados_z_array

    return airfoil

###########
# Classes #
###########

class Airfoil:
    """
    Class to define an airfoil and compute its characteristics.
    """

    name: str | None = None
    extrados_z_array: np.ndarray | None = None
    intrados_z_array: np.ndarray | None = None
    _x_array: np.ndarray
    _chord_length: float
    _a0: float | None = None
    _a1: float | None = None
    _a2: float | None = None

    def __init__(self, airfoil: str | None = None):
        if airfoil in self.list_airfoils_in_database():
            self.load_database_airfoil(airfoil)
        elif airfoil is not None:
            self.load_selig_file(airfoil)

    @property
    def camber_z_array(self) -> np.ndarray:
        """
        Array of the camber line z coordinates.
        """
        camber_z_array = (self.extrados_z_array + self.intrados_z_array) / 2
        return camber_z_array

    @property
    def chord_z_array(self) -> np.ndarray:
        """
        Array of the chord line z coordinates.
        """
        x_0 = 0
        x_1 = self.chord_length
        y_0 = self.extrados_z_array[0] + self.intrados_z_array[0]
        y_1 = self.extrados_z_array[-1] + self.intrados_z_array[-1]
        slope = (y_1 - y_0) / (x_1 - x_0)
        return slope * self.x_array + y_0

    @property
    def thickness_array(self) -> np.ndarray:
        """
        Array of the thickness of the airfoil.
        """
        thickness_array = (self.extrados_z_array - self.camber_z_array) * 2
        return thickness_array

    @property
    def max_thickness(self) -> float:
        """
        Max thickness value.
        """
        max_thickness = np.max(self.extrados_z_array -
                               self.intrados_z_array) / self.chord_length
        return max_thickness

    @max_thickness.setter
    def max_thickness(self, value: float):
        # Compute new values
        ratio = value / self.max_thickness
        new_extrados_z_array = self.camber_z_array + self.thickness_array * ratio / 2
        new_intrados_z_array = self.camber_z_array - self.thickness_array * ratio / 2

        # Modify the airfoil shape
        self.extrados_z_array = new_extrados_z_array
        self.intrados_z_array = new_intrados_z_array

    @property
    def max_thickness_location(self) -> float:
        """
        Location of the max thickness value in x.
        """
        max_thickness_idx = np.argmax(self.extrados_z_array -
                                      self.intrados_z_array)
        max_thickness_location = self.x_array[max_thickness_idx]
        return max_thickness_location

    @property
    def max_camber(self) -> float:
        """
        Max camber value.
        """
        max_camber = np.max(np.abs(self.camber_z_array -
                            self.chord_z_array)) / self.chord_length
        return max_camber

    @max_camber.setter
    def max_camber(self, value):
        # Compute new value
        ratio = value / self.max_camber
        prev_max_thickness = self.max_thickness
        chord_to_extrados = self.extrados_z_array - self.chord_z_array
        chord_to_intrados = self.intrados_z_array - self.chord_z_array
        new_extrados_z_array = self.chord_z_array + chord_to_extrados * ratio
        new_intrados_z_array = self.chord_z_array + chord_to_intrados * ratio

        # Modify the shape
        self.extrados_z_array = new_extrados_z_array
        self.intrados_z_array = new_intrados_z_array

        # Reset the thickness
        self.max_thickness = prev_max_thickness

    @property
    def max_camber_location(self) -> float:
        """
        Location of the max camber value in x.
        """
        max_camber_idx = np.argmax(np.abs(self.camber_z_array -
                                          self.chord_z_array))
        max_camber_location = self.x_array[max_camber_idx]
        return max_camber_location

    @property
    def x_array(self) -> np.ndarray:
        """
        Array of x coordinates used for the airfoil definition.
        """
        return self._x_array

    @x_array.setter
    def x_array(self, value: np.ndarray):
        if self.extrados_z_array is not None and self.intrados_z_array is not None:
            if self._x_array.size == self.extrados_z_array.size:
                self.re_interpolate(value, update_x_array=False)
            self._x_array = value
        else:
            self._x_array = value
        self._chord_length = np.max(value)

    @property
    def chord_length(self) -> float:
        """
        Length of the chord.
        """
        return self._chord_length

    @chord_length.setter
    def chord_length(self, value):
        ratio = value / self._chord_length
        self.x_array = self.x_array * ratio
        self.extrados_z_array = self.extrados_z_array * ratio
        self.intrados_z_array = self.intrados_z_array * ratio

    @property
    def x_selig_array(self) -> np.ndarray:
        x_selig_array = np.concatenate(
            (self.x_array, self.x_array[::-1], [self.x_array[0]]), axis=0)
        return x_selig_array

    @property
    def z_selig_array(self) -> np.ndarray:
        z_selig_array = np.concatenate(
            (self.extrados_z_array, self.intrados_z_array[::-1], [self.extrados_z_array[0]]), axis=0)
        return z_selig_array

    def get_chord_incidence(self):
        angle_of_incidence = np.atan(
            (self.chord_z_array[-1] - self.chord_z_array[0]) / (self.chord_length))
        return angle_of_incidence

    def set_chord_at_zero_incidence(self):
        # Remove chord offset
        chord_z_offset = -self.chord_z_array[0]
        self.extrados_z_array += chord_z_offset
        self.intrados_z_array += chord_z_offset

        # Rotate chord
        chord_incidence = self.get_chord_incidence()
        new_x_array, new_extrados_z_array = rotate_arrays(
            self.x_array, self.extrados_z_array, chord_incidence, 0)
        new_x_array, new_intrados_z_array = rotate_arrays(
            self.x_array, self.intrados_z_array, chord_incidence, 0)
        self._x_array = new_x_array
        self.extrados_z_array = new_extrados_z_array
        self.intrados_z_array = new_intrados_z_array

    def list_airfoils_in_database(self, airfoil_data_folder: str = default_airfoil_database):
        """
        Return the list of airfoils stored in the database.

        Parameters
        ----------
        airfoil_data_folder : str, optional
            Name of the airfoil database folder, by default default_airfoil_database

        Returns
        -------
        list
            List of airfoils stored in the database.
        """

        file_names_list = os.listdir(airfoil_data_folder)
        airfoil_names_list = [e.replace(".txt", "") for e in file_names_list]

        return airfoil_names_list

    def load_database_airfoil(self, airfoil_name: str, airfoil_data_folder: str = default_airfoil_database):
        """
        Load an airfoil contained in the database.

        Parameters
        ----------
        airfoil_name : str
            Name of the airfoil.
        airfoil_data_folder : str, optional
            Folder containing the airfoil file, by default default_airfoil_database
        """

        file_path = os.path.join(airfoil_data_folder, airfoil_name + ".txt")
        self.load_selig_file(file_path, skiprows=1)

    def load_selig_file(self, file_path: str, skiprows: int = 1):
        """
        Load an airfoil contained in a selig txt file.

        Parameters
        ----------
        file_path : str
            Path of the file to load.
        skiprows : int, optional
            Number of rows to skip at the beginning of the file, by default 1
        """

        # Extract airfoil name
        with open(file_path, "r") as file:
            first_line = file.readline()
        self.name = first_line.replace("\n", "")

        # Extract airfoil coordinates
        file_content = np.loadtxt(file_path, skiprows=skiprows)
        x_selig_array = file_content[:, 0]
        z_selig_array = file_content[:, 1]
        self.import_xz_selig_arrays(x_selig_array, z_selig_array)

    def import_xz_selig_arrays(self, x_selig_array: np.ndarray, z_selig_array: np.ndarray):
        """
        Import x and z arrays containing an airfoil in selig format.

        Parameters
        ----------
        x_selig_array : np.ndarray
            X coordinates.
        z_selig_array : np.ndarray
            Z coordinates.
        """

        # Compute the x derivative to split parts of the airfoil
        x_diff = np.zeros(x_selig_array.shape)
        x_diff[:-1] = x_selig_array[1:] - x_selig_array[:-1]
        x_diff[-1] = x_diff[-2]

        # Split parts
        diff_sign = x_diff * x_diff[0]
        common_point = np.argmax(diff_sign < 0)
        diff_sign[common_point] = 0
        part_1_x = x_selig_array[diff_sign >= 0]
        part_1_z = z_selig_array[diff_sign >= 0]
        part_2_x = x_selig_array[diff_sign <= 0]
        part_2_z = z_selig_array[diff_sign <= 0]

        # Extract all x locations
        self.x_array = np.unique(x_selig_array)

        # Reorder arrays for interpolation
        part_1_order = np.argsort(part_1_x)
        part_2_order = np.argsort(part_2_x)

        # Interpolate both parts on all x locations
        part_1_z_interpolated = np.interp(
            self.x_array, part_1_x[part_1_order], part_1_z[part_1_order])
        part_2_z_interpolated = np.interp(
            self.x_array, part_2_x[part_2_order], part_2_z[part_2_order])

        # Assign depending on which part is extrados or intrados
        if np.mean(part_1_z_interpolated) > np.mean(part_2_z_interpolated):
            self.extrados_z_array = part_1_z_interpolated
            self.intrados_z_array = part_2_z_interpolated
        else:
            self.extrados_z_array = part_2_z_interpolated
            self.intrados_z_array = part_1_z_interpolated

        # Rotate the chord to make sure it is at zero incidence
        self.set_chord_at_zero_incidence()

    def plot(self, hold_plot=False, show_chord=False, show_camber_line=False):
        """
        Plot the geometry of the airfoil.

        Parameters
        ----------
        hold_plot : bool, optional
            Indicate if the plot shall be kept for later, by default False
        show_chord : bool, optional
            Display the chord line if true, by default False
        show_camber_line : bool, optional
            Display the camber line if true, by default False
        """

        # Concatenate extrados and intrados to plot a single line
        x_plot = np.concatenate(
            (self.x_array, self.x_array[::-1], [self.x_array[0]]), axis=0)
        y_plot = np.concatenate(
            (self.extrados_z_array, self.intrados_z_array[::-1], [self.extrados_z_array[0]]), axis=0)

        # Plot extrados and intrados
        plt.plot(x_plot, y_plot, label=self.name)
        plt.axis("equal")

        # Plot chord if needed
        if show_chord:
            plt.plot(self.x_array, self.chord_z_array,
                     "--", label=f"chord {self.name}")

        # Plot camber if needed
        if show_camber_line:
            plt.plot(self.x_array, self.camber_z_array,
                     "--", label=f"camber {self.name}")

        # Display the plot if needed
        if hold_plot is False:
            plt.legend()
            plt.grid()
            plt.title("Airfoil visualization")
            plt.show()

    def re_interpolate(self, new_x_array: np.ndarray, update_x_array: bool = True):
        """
        Re-interpolate the extrados and intrados on the given array.

        Parameters
        ----------
        new_x_array : np.ndarray
            New x array on which to interpolate.
        update_x_array : bool, optional
            Indicate wether to update the x array, by default True
        """

        # Create interpolation functions
        extrados_function = make_interp_spline(
            self.x_array, self.extrados_z_array)
        intrados_function = make_interp_spline(
            self.x_array, self.intrados_z_array)

        # Interpolate on new points
        self.extrados_z_array = extrados_function(new_x_array)
        self.intrados_z_array = intrados_function(new_x_array)

        # Update x array if needed
        if update_x_array:
            self.x_array = new_x_array

    def import_from_airfoiltools(
            self,
            airfoil_name: str = "",
            max_thickness: float | None = None,
            min_thickness: float | None = None,
            max_camber: float | None = None,
            min_camber: float | None = None,
            maximise_glide_ratio_at_reynolds: Literal["50k", "100k",
                                                      "200k", "500k", "1M", "2M", "5M"] | None = None,
            airfoil_data_folder: str = default_airfoil_database):
        """
        Import an airfoil from airfoiltools.

        Parameters
        ----------
        airfoil_name : str, optional
            Name of the airfoil to search, by default ""
        max_thickness : float | None, optional
            Max thickness value in percent, by default None
        min_thickness : float | None, optional
            Min thickness value in percent, by default None
        max_camber : float | None, optional
            Max camber value in percent, by default None
        min_camber : float | None, optional
            Min camber value in percent, by default None
        maximise_glide_ratio_at_reynolds : Literal["50k", "100k", "200k", "500k", "1M", "2M", "5M"] | None, optional
            Indicate Reynolds number to sort by optimal ratio, by default None
        airfoil_data_folder : str, optional
            Folder containing the airfoil database, by default default_airfoil_database

        Warning
        -------
        The thickness and camber values must be expressed in percents.

        Raises
        ------
        ValueError
            Raise error if no corresponding profile is found.
        """

        # Define the URL for the search
        search_url = "http://airfoiltools.com/search/index"

        # Set the sort mode
        if maximise_glide_ratio_at_reynolds is not None:
            sort_mode = str(9 + ["50k", "100k", "200k", "500k", "1M",
                                 "2M", "5M"].index(maximise_glide_ratio_at_reynolds))
        else:
            sort_mode = "1"

        # Convert input parameters to string
        max_thickness = convert_float_or_none_to_string(max_thickness)
        min_thickness = convert_float_or_none_to_string(min_thickness)
        max_camber = convert_float_or_none_to_string(max_camber)
        min_camber = convert_float_or_none_to_string(min_camber)

        # Set the query parameters
        params = {
            "MAirfoilSearchForm[textSearch]": airfoil_name,
            "MAirfoilSearchForm[maxThickness]": max_thickness,
            "MAirfoilSearchForm[minThickness]": min_thickness,
            "MAirfoilSearchForm[maxCamber]": max_camber,
            "MAirfoilSearchForm[minCamber]": min_camber,
            "MAirfoilSearchForm[grp]": "",
            "MAirfoilSearchForm[sort]": sort_mode,
            "yt0": "Search"
        }

        # Make the GET request to the search page
        response = requests.get(search_url, params=params)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first research proposal link (specific to the provided element structure)
        proposal_link = soup.find('a', string="Airfoil details")

        if proposal_link and 'href' in proposal_link.attrs:
            airfoil_code = proposal_link["href"].split("?")[1]
            selig_file_link = "http://airfoiltools.com/airfoil/seligdatfile?" + airfoil_code
            airfoil_name = airfoil_code.replace(
                "airfoil=", "").replace("-il", "")
            output_file_path = os.path.join(
                airfoil_data_folder, airfoil_name + ".txt")
            download_web_file(selig_file_link, output_file_path)
            print(f"Airfoil {airfoil_name} successfully downloaded.")
            self.load_database_airfoil(airfoil_name, airfoil_data_folder)
        else:
            raise ValueError("No corresponding airfoil found.")

    def re_interpolate_with_cosine_distribution(self, nb_points: int):
        """
        Re-interpolate the extrados and the intrados on a x array defined by a cosine distribution.

        Parameters
        ----------
        nb_points : int
            Number of points in the cosine distribution.
        """

        theta_chord_array = np.linspace(0, np.pi, nb_points)
        x_array = (self.chord_length / 2) * (1 - np.cos(theta_chord_array))
        self.x_array = x_array

    def compute_airfoil_fourrier_coefficients(self, nb_points: int = 1000):
        """
        Compute the airfoil Fourrier's coefficients to be able to compute lift and moment values.

        Parameters
        ----------
        nb_points : int
            Number of points to use for the interpolation.

        Returns
        -------
        tuple[float,float,float]
            Fourier's coefficients.
        """

        # Generate a linear distribution of angles for interpolation
        theta_chord_array = np.linspace(0, np.pi, nb_points)

        # Compute x locations for each angle
        x_from_theta_array = (self.chord_length / 2) * \
            (1 - np.cos(theta_chord_array))
        self.x_array = x_from_theta_array

        # Compute the derivative of the camber line
        camber_z_derivative_array = np.gradient(
            self.camber_z_array, self.x_array)

        # Compute the coefficients
        self._a0 = (1 / np.pi) * \
            np.trapezoid(camber_z_derivative_array, theta_chord_array)
        self._a1 = (2 / np.pi) *\
            np.trapezoid(camber_z_derivative_array *
                         np.cos(theta_chord_array), theta_chord_array)
        self._a2 = (2 / np.pi) *\
            np.trapezoid(camber_z_derivative_array *
                         np.power(np.cos(theta_chord_array), 2), theta_chord_array)

        return self._a0, self._a1, self._a2

    def compute_lift_coefficient(self, alpha: float):
        """
        Compute the lift coefficient for a given angle of incidence.

        Parameters
        ----------
        alpha : float
            Angle of incidence in radians.

        Returns
        -------
        float
            Lift coefficient.
        """

        # Compute Fourrier's coefficients if needed
        if self._a0 is None:
            self.compute_airfoil_fourrier_coefficients()

        # Compute lift coefficient
        C_L = 2 * np.pi * alpha + np.pi * (self._a1 - 2 * self._a0)

        return C_L

    def compute_momentum_coefficient_at_leading_edge(self, alpha: float):
        """
        Compute the momentum coefficient at leading edge for a given angle of incidence.

        Parameters
        ----------
        alpha : float
            Angle of incidence in radians.

        Returns
        -------
        float
            Momentum coefficient.
        """

        # Compute Fourrier's coefficients if needed
        if self._a0 is None:
            self.compute_airfoil_fourrier_coefficients()

        # Compute momentum coefficient
        C_m0 = -(np.pi / 2) * ((alpha - self._a0) + self._a1 - self._a2 / 2)

        return C_m0

    def compute_momentum_coefficient_at_aero_center(self, alpha: float):
        """
        Compute the momentum coefficient at the aerodynamic center for a given angle of incidence.

        Parameters
        ----------
        alpha : float
            Angle of incidence in radians.

        Returns
        -------
        float
            Momentum coefficient.
        """

        # Compute the momentum coefficient at leading edge
        C_m0 = self.compute_momentum_coefficient_at_leading_edge(alpha)

        # Move it at the aero center
        C_m = C_m0 + 0.25 * self.chord_length * \
            self.compute_lift_coefficient(alpha)

        return C_m

    def plot_CL_graph(self,
                      alpha_min: float = -1,
                      alpha_max: float = 1,
                      nb_points: int = 100,
                      mode: Literal["deg", "rad"] = "rad",
                      hold_plot: bool = False,
                      save_path: str | None = None,
                      clear_before_plot: bool = False):
        """
        Plot the CL graph of the airfoil.

        Parameters
        ----------
        alpha_min : float, optional
            Minimum value of alpha, by default -1
        alpha_max : float, optional
            Maximum value of alpha, by default 1
        nb_points : int, optional
            Number of points, by default 100
        mode : Literal["deg", "rad"], optional
            Mode for alpha definition, by default "rad"
        hold_plot : bool, optional
            Indicate wether to display the plot or keep it, by default False
        save_path : str | None, optional
            Path to save the figure, by default None
        clear_before_plot : bool, optional
            Indicate wether to clear the plot before display, by default False
        """

        # Define the array of angle of incidence
        alpha_array_comp = np.linspace(alpha_min, alpha_max, nb_points)

        # Convert it in radians if needed for the computations
        if mode == "deg":
            alpha_array_graph = alpha_array_comp * 180 / np.pi
        else:
            alpha_array_graph = alpha_array_comp

        # Compute the lift coefficient
        CL_array = self.compute_lift_coefficient(alpha_array_comp)

        # Plot the graph
        plot_graph(
            alpha_array_graph,
            CL_array,
            data_label=self.name,
            title="Lift coefficient",
            use_grid=True,
            save_path=save_path,
            hold_plot=hold_plot,
            clear_before_plot=clear_before_plot,
            x_label=f"alpha [{mode}]",
            y_label="CL"
        )

    def plot_Cm_graph(self,
                      alpha_min: float = -1,
                      alpha_max: float = 1,
                      nb_points: int = 100,
                      mode: Literal["deg", "rad"] = "rad",
                      location: Literal["leading_edge",
                                        "aero_center"] = "aero_center",
                      hold_plot: bool = False,
                      save_path: str | None = None,
                      clear_before_plot: bool = False):
        """
        Plot the Cm graph of the airfoil.

        Parameters
        ----------
        alpha_min : float, optional
            Minimum value of alpha, by default -1
        alpha_max : float, optional
            Maximum value of alpha, by default 1
        nb_points : int, optional
            Number of points, by default 100
        mode : Literal["deg", "rad"], optional
            Mode for alpha definition, by default "rad"
        location : Literal["leading_edge","aero_center"]
            Location of the Cm, by default "aero_center"
        hold_plot : bool, optional
            Indicate wether to display the plot or keep it, by default False
        save_path : str | None, optional
            Path to save the figure, by default None
        clear_before_plot : bool, optional
            Indicate wether to clear the plot before display, by default False
        """

        # Define the array of angle of incidence
        alpha_array_comp = np.linspace(alpha_min, alpha_max, nb_points)

        # Convert it in radians if needed for the computations
        if mode == "deg":
            alpha_array_graph = alpha_array_comp * 180 / np.pi
        else:
            alpha_array_graph = alpha_array_comp

        # Compute the lift coefficient
        if location == "aero_center":
            Cm_array = self.compute_momentum_coefficient_at_aero_center(
                alpha_array_comp)
        else:
            Cm_array = self.compute_momentum_coefficient_at_leading_edge(
                alpha_array_comp)

        # Plot the graph
        plot_graph(
            alpha_array_graph,
            Cm_array,
            data_label=self.name,
            title="Momentum coefficient",
            use_grid=True,
            save_path=save_path,
            hold_plot=hold_plot,
            clear_before_plot=clear_before_plot,
            x_label=f"alpha [{mode}]",
            y_label="Cm"
        )

    def get_rotated_selig_arrays(self, angle: float, rotation_center: float = 0.25):
        """
        Returns the selig arrays of the airfoil rotated by a given angle.

        Parameters
        ----------
        angle : float
            Angle of rotation.
        rotation_center : float
            Center of rotation in fraction of the chord.

        Returns
        -------
        tuple[np.ndarray,np.ndarray]
            Tuple containing the selig arrays.
        """

        rotated_x_array, rotated_z_array = rotate_arrays(
            self.x_selig_array, self.z_selig_array, angle, rotation_center, x_length=self.chord_length)

        return rotated_x_array, rotated_z_array

    def compute_alpha_zero_lift(self):
        """
        Compute the angle of incidence for which the airfoil's lift is zero.

        Returns
        -------
        float
            Angle of incidence at zero lift.
        """

        # Compute coefficients if needed
        if self._a0 is None:
            self.compute_airfoil_fourrier_coefficients()

        # Compute the angle
        alpha = (self._a0 * 2 - self._a1) / 2

        return alpha
