from colav_protobuf import MissionResponse

"""mocks a mission response proto message"""
mission_response = MissionResponse()
mission_response.tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
mission_response.timestamp = "1708353005"
mission_response.response.type = (
    MissionResponse.MissionResponseMsg.ResponseTypeEnum.Value("MISSION_STARTING")
)
mission_response.response.details = (
    "Mission has started. Now Navigating to South France"
)
