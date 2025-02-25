from colav_protobuf import ObstaclesUpdate
import random
from typing import List
import numpy as np
from enum import Enum
from shapely.geometry import Polygon

mock_agent_x = 3_675_830.74
mock_agent_y = -272_412.13
mock_agent_z = 4_181_577.70


class ObstacleTypeEnum(Enum):
    UNSPECIFIED = ObstaclesUpdate.ObstacleType.UNSPECIFIED
    VESSEL = ObstaclesUpdate.ObstacleType.VESSEL
    LAND_MASS = ObstaclesUpdate.ObstacleType.LAND_MASS
    BUOY = ObstaclesUpdate.ObstacleType.BUOY


def obstacles_update(num_dynamic_obstacles: int = 4, num_static_obstacles: int = 2):
    """mocks an obstacles update"""
    if (num_static_obstacles < 0) or (num_static_obstacles < 0):
        raise ValueError(
            "invalid obstacle number please enusre obstacles number is greater than or equal to 0"
        )

    obstacles_update = ObstaclesUpdate()
    obstacles_update.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
    obstacles_update.tiemstamp = "1708353005"
    obstacles_update.timestep = "000000000012331"

    obstacles_update = _mock_dynamic_obstacles(
        obstacle_update=obstacles_update, num_dynamic_obstacles=num_dynamic_obstacles
    )
    obstacles_update = _mock_static_obstacles(
        obstacles_update=obstacles_update, num_static_obstacles=num_static_obstacles
    )

    return obstacles_update


def _mock_dynamic_obstacles(
    agent_position: List[float, float, float],
    obstacles_update: ObstaclesUpdate,
    detection_range: float = 1000,
    num_dynamic_obstacles: int = 5,
) -> ObstaclesUpdate:
    """mocks dynamic obstacles in the obstacle update"""
    obstacle_class = "DYNAMIC_OBSTACLE"
    for x in range(0, num_dynamic_obstacles):
        obstacle_type = random.choice(list(ObstacleTypeEnum))
        obstacles_update.dynamic_obstacles[x].id.tag = (
            f"{obstacle_class}_{obstacle_type.name}_{x}"
        )
        obstacles_update.dynamic_obstacles[x].id.type = obstacle_type.value

        p = _random_position(position=agent_position, range=detection_range)
        obstacles_update.dynamic_obstacles[x].state.pose.position.x = float(p[0])
        obstacles_update.dynamic_obstacles[x].state.pose.position.y = float(p[1])
        obstacles_update.dynamic_obstacles[x].state.pose.position.z = float(p[2])

        q = _random_quaternion()
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.x = float(q[0])
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.y = float(q[1])
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.z = float(q[2])
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.w = float(q[3])

        obstacles_update.dynamic_obstacles[x].geometry.acceptance_radius = float(
            random.uniform(float(1.2), float(5))
        )

        random_polyshape_vertices = _random_polyshape(min_vertices=3, max_vertices=15)

        for i in range(0, random_polyshape_vertices.size):
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points.add()
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points[
                i - 1
            ].position.x = random_polyshape_vertices[0]
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points[
                i - 1
            ].position.y = random_polyshape_vertices[1]
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points[
                i - 1
            ].position.z = 0
            # TODO: Need to get rid of orientation for polyshape vertices.
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points[
                i - 1
            ].orientation.x = 0
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points[
                i - 1
            ].orientation.y = 0
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points[
                i - 1
            ].orientation.z = 0
            obstacles_update.dynamic_obstacles[x].geometry.polyshape_points[
                i - 1
            ].orientation.w = 1

        obstacles_update.dynamic_obstacles[x].state.velocity = random.uniform(
            float(15), float(30)
        )
        obstacles_update.dynamic_obstacles[x].state.yaw_rate = random.uniform(
            float(0), float(2.0)
        )

    return obstacles_update


def _mock_static_obstacles(
    obstacles_update: ObstaclesUpdate, num_static_obstacles: int = 5
) -> ObstaclesUpdate:
    """mocks static obstacle sin teh obstacle update"""
    for x in range(0, num_static_obstacles):
        pass
    return obstacles_update


def _random_polyshape(min_vertices: int = 3, max_vertices: int = 15):
    """Generate a random 2D polyshape with a random number of vertices."""
    # Random number of vertices between min and max
    num_vertices = random.randint(min_vertices, max_vertices)

    # Generate random points (x, y) within a given range
    points = []
    for _ in range(num_vertices):
        x = random.uniform(-100, 100)  # Adjust the range as needed
        y = random.uniform(-100, 100)
        points.append((x, y))

    # Create a polygon using Shapely to check validity
    polygon = Polygon(points)

    # Ensure the points form a valid, non-self-intersecting polygon
    if not polygon.is_valid or polygon.is_empty:
        return _random_polyshape(
            min_vertices, max_vertices
        )  # Recursively regenerate if invalid

    # Return the vertices as a list of points
    return np.array(polygon.exterior.xy).T


def _random_position(
    position: List[float, float, float], range: float
) -> List[float, float, float]:
    """returns an obstacle random position based within the detection_range of a mock agent vessel"""
    try:
        return [
            float(random.uniform(position[0] - range, position[0] + range)),
            float(random.uniform(position[1] - range, position[1] + range)),
            float(random.uniform(position[2] - range, position[2] + range)),
        ]
    except Exception as e:
        raise e


def _random_quaternion():
    """Generate a random unit quaternion."""
    q = np.random.normal(0, 1, 4)  # Random values from normal distribution
    q /= np.linalg.norm(q)  # Normalize to make it a unit quaternion
    return q
