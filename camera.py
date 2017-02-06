import numpy as np

class Camera():
    """
    Represents a camera view within the scene
    """
    def __init__(self, pos, look_position, x_pixels, y_pixels, field_of_view, distance_from_plane):
        self.pos = pos
        self.look_vector = (pos - look_position)
        self.look_vector /= np.linalg.norm(self.look_vector)

        self.x_pixels = x_pixels
        self.y_pixels = y_pixels

        # Using the given paramaters, generate the paramters 
        # for the plane of the view frustrum
        self._obtain_basis_vectors()
        self._obtain_look_parameters(field_of_view, distance_from_plane)


        # Some basic checks on the parameters
        assert 0 < field_of_view < 180
        assert x_pixels > 0 and isinstance(x_pixels, int)
        assert y_pixels > 0 and isinstance(y_pixels, int)

    def vector_from_pixels(self, x_pos, y_pos):
        """
        Generates a view vector for the camera for a given
        pair of pixel values. 
        """
        # Ray should be cast within the camera frame
        assert x_pos < self.x_pixels and y_pos < self.y_pixels
        y_component = (self._v * (y_pos/self.y_pixels))
        x_component = (self._u * (x_pos * self.width/self.x_pixels))
        look_vector = self.lower_plane_position + x_component  + y_component
        return look_vector / np.linalg.norm(look_vector)

    def _obtain_basis_vectors(self):
        """
        Using the look position and the camera position,
        creates a set of basis vectors for the virtual view
        plane
        """
        self._u = -np.cross(np.array([1,0,0], dtype=np.float64), self.look_vector)
        self._u /= np.linalg.norm(self._u)
        self._v = np.cross(self._u, self.look_vector) # Guaranteed to be normalized
    def _obtain_look_parameters(self, field_of_view, distance_from_plane):
        """
        Using the given pixel values, generates the virtual
        height and width of the view plane
        """
        aspect_ratio = self.x_pixels/self.y_pixels
        C = self.pos - self.look_vector
        self.height = 2 * distance_from_plane * np.tan(field_of_view/180 * np.pi * 0.5)
        self.width = self.height * aspect_ratio
        self.lower_plane_position = C - (self._u * self.width/2) - (self._v * self.height/2)


