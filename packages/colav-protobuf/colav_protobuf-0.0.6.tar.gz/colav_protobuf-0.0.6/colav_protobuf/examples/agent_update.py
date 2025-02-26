from colav_protobuf import AgentUpdate

"""mocks a agent update proto message"""
agent_update = AgentUpdate()
agent_update.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
agent_update.agent_tag = "EF12_WORKBOAT"
agent_update.state.pose.position.x = float(3_675_830.74)
agent_update.state.pose.position.y = float(-272_412.13)
agent_update.state.pose.position.z = float(4_181_577.70)
agent_update.state.pose.orientation.x = 0
agent_update.state.pose.orientation.y = 0
agent_update.state.pose.orientation.z = 0
agent_update.state.pose.orientation.w = 1

agent_update.state.velocity = 20
agent_update.state.yaw_rate = 0.2
agent_update.state.acceleration = 1

agent_update.timestamp = "1708853235"
