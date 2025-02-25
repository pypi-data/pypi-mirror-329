from colav_protobuf import MissionRequest

# Mock mission request proto message
mission_request = MissionRequest()

# Mission metadata
mission_request.tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
mission_request.mission_start_timestamp = (
    "1708353000"  # UNIX timestamp (epoch time in seconds)
)

# Static Vessel Information
mission_request.vessel.tag = "EF12_WORKBOAT"
mission_request.vessel.type = MissionRequest.Vessel.VesselType.HYDROFOIL
mission_request.vessel.vessel_constraints.max_acceleration = 2.0
mission_request.vessel.vessel_constraints.max_deceleration = -1.0
mission_request.vessel.vessel_constraints.max_velocity = 30.0
mission_request.vessel.vessel_constraints.min_velocity = 15.0
mission_request.vessel.vessel_constraints.max_yaw_rate = 0.2
mission_request.vessel.vessel_geometry.safety_threshold = 5

# Earth-Centered, Earth-Fixed Cartesian Coordinates North Belfast Lough in meters
mission_request.mission_init_position.x = float(3675900.74)
mission_request.mission_init_position.y = float(-372412.13)
mission_request.mission_init_position.z = float(5181577.70)

# Earth-Centered, Earth-Fixed Cartesian Coordinates South France near Marseille in meters
# WON'T USE THIS METRIC IN LOCAL MOTION PLANNER! GOOD FOR GLOBAL PLANNING
mission_request.mission_goal_position.x = float(4680627.4)
mission_request.mission_goal_position.z = float(503374.5)
mission_request.mission_goal_position.y = float(4299351.3)

# Acceptance radius in meters of the goal waypoint for autonomous navigation.
mission_request.mission_goal_acceptance_radius = float(5.0)
