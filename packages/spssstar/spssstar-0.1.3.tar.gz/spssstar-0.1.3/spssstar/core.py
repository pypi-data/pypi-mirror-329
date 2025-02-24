import hashlib
import random
import math


class EncodedStar:
    def __init__(self, position, color, size, animation):
        """
        Represents an individual star in the star map.
        :param position: Tuple (x, y) representing the star's position.
        :param color: Tuple (R, G, B) representing the star's color.
        :param size: Integer representing the star's radius.
        :param animation: Dictionary containing twinkling parameters.
        """
        self.position = position
        self.color = color
        self.size = size
        self.animation = animation

    def to_dict(self):
        """
        Convert the star object to a dictionary for serialization.
        :return: Dictionary representation of the star.
        """
        return {
            "position": self.position,
            "color": self.color,
            "size": self.size,
            "animation": self.animation
        }


class StarMap:
    def __init__(self, width=400, height=400, boundary_radius=150):
        """
        Represents the entire star map.
        :param width: Width of the canvas.
        :param height: Height of the canvas.
        :param boundary_radius: Radius of the circular boundary.
        """
        self.width = width
        self.height = height
        self.boundary_radius = boundary_radius
        self.center = (width // 2, height // 2)
        self.stars = []
        self.metadata = {}

    def add_star(self, star):
        """
        Add a star to the star map.
        :param star: EncodedStar object.
        """
        self.stars.append(star)

    def to_dict(self):
        """
        Convert the star map to a dictionary for serialization.
        :return: Dictionary representation of the star map.
        """
        return {
            "stars": [star.to_dict() for star in self.stars],
            "metadata": self.metadata
        }


class StarEncoder:
    def __init__(self, width=400, height=400, boundary_radius=150):
        """
        Initialize the encoder with the dimensions of the canvas.
        :param width: Width of the canvas.
        :param height: Height of the canvas.
        :param boundary_radius: Radius of the circular boundary.
        """
        self.width = width
        self.height = height
        self.boundary_radius = boundary_radius
        self.center = (width // 2, height // 2)

    def hash_to_seed(self, input_data):
        """
        Generate a deterministic seed from input data using SHA-256.
        :param input_data: Input data (e.g., session ID, URL).
        :return: Integer seed.
        """
        hash_value = hashlib.sha256(str(input_data).encode()).hexdigest()
        return int(hash_value, 16) % (2**32)

    def encode_position(self, session_id, index):
        """
        Encode a session ID into a star position within the circular boundary.
        :param session_id: Unique session identifier.
        :param index: Index of the star (to ensure unique positions).
        :return: Tuple (x, y) representing the star's position.
        """
        seed = self.hash_to_seed(f"{session_id}-{index}")
        random.seed(seed)
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, self.boundary_radius)
        x = int(self.center[0] + radius * math.cos(angle))
        y = int(self.center[1] + radius * math.sin(angle))
        return x, y

    def encode_color(self, session_id, priority="medium"):
        """
        Encode a session ID into a star color based on priority.
        :param session_id: Unique session identifier.
        :param priority: Priority level ("high", "medium", "low").
        :return: Tuple (R, G, B) representing the star's color.
        """
        seed = self.hash_to_seed(f"{session_id}-color")
        random.seed(seed)
        if priority == "high":
            return (255, 0, 0)  # Red
        elif priority == "medium":
            return (0, 0, 255)  # Blue
        else:
            return (0, 255, 0)  # Green

    def encode_twinkling_pattern(self, session_id):
        """
        Encode a session ID into a twinkling pattern.
        :param session_id: Unique session identifier.
        :return: Dictionary containing twinkling parameters.
        """
        seed = self.hash_to_seed(f"{session_id}-twinkle")
        random.seed(seed)
        amplitude = random.randint(50, 150)
        frequency = random.randint(1, 5)
        return {"amplitude": amplitude, "frequency": frequency}

    def encode_star_map(self, session_id, num_stars=10):
        """
        Encode a session ID into a full star map.
        :param session_id: Unique session identifier.
        :param num_stars: Number of stars to generate.
        :return: StarMap object representing the encoded star map.
        """
        star_map = StarMap(width=self.width, height=self.height, boundary_radius=self.boundary_radius)
        star_map.metadata["session_id"] = session_id
        for i in range(num_stars):
            x, y = self.encode_position(session_id, i)
            base_color = self.encode_color(session_id, priority="medium")
            twinkling_pattern = self.encode_twinkling_pattern(f"{session_id}-twinkle-{i}")
            radius = random.randint(2, 5)  # Random radius for visual variety
            star = EncodedStar(
                position=(x, y),
                color=base_color,
                size=radius,
                animation=twinkling_pattern
            )
            star_map.add_star(star)
        return star_map