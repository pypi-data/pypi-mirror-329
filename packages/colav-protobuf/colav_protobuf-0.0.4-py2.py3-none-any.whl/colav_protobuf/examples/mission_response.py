from colav_protobuf import MissionResponse

"""mocks a mission response proto message"""
mission_response = MissionResponse()
mission_response.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
mission_response.mission_start_timestamp = "1708353005"
mission_response.mission_response = MissionResponse.MissionResponseEnum.Value(
    "MISSION_STARTING"
)
mission_response.mission_response_details = (
    "Mission has started. Now Navigating to South France"
)
