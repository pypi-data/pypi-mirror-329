from colav_protobuf import ControllerFeedback

"""mocks controller feedback"""
controller_feedback = ControllerFeedback()
controller_feedback.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
controller_feedback.agent_tag = "EF12_WORKBOAT"
controller_feedback.ctrl_mode = ControllerFeedback.CTRLMode.Value("CRUISE")
controller_feedback.ctrl_status = ControllerFeedback.CTRLStatus.Value("ACTIVE")
controller_feedback.ctrl_cmd.velocity = float(15.0)
controller_feedback.ctrl_cmd.yaw_rate = float(0.2)

controller_feedback.timestamp = "1708853235"
