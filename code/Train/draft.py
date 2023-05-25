import numpy as np
        
def init_bins(self, lower_bound, upper_bound, num_bins):
        # Begin your code
        """
        Explain code:
        linspace can part [lower_bound, upper_bound] into {num} evenly spaced points
        To slice interval into {num_bins} subinterval, we need {num_bins+1} points
        return np array that excluding the first and last element
        """
        return np.linspace(lower_bound, upper_bound, num = num_bins+1)[1:-1]
        # End your code
def discretize_value(self, value, bins):
    # Begin your code
    """
    Explain code:
    np.digitize let 2 neighbor points in bins is considered as a interval
    ex: bins has 4 points, so it has 3 interval
    return value is interval index which given value is located at including lower_bound and upper_bound in init_bins
    if in the first interval, return value is 0, and so on
    """
    return np.digitize(value, bins)
    # End your code
def coordinate_discretize(self, coordinate):
    # if coordinate is negitave, sign is -1, else is 1
    sign = None
    if coordinate < 0:
        sign = -1
    else:
        sign = 1
    positive_int = int(abs(coordinate))
    result = (positive_int + 0.5) * sign
    return result
def addTermOfXZ(self, yaw_discrete, current_XPos, current_ZPos):
    target_XPos = None
    target_ZPos = None
    if yaw_discrete == 0:
        target_XPos = current_XPos
        target_ZPos = current_ZPos + 0.6
    elif yaw_discrete == 1:
        target_XPos = current_XPos - 0.7
        target_ZPos = current_ZPos + 0.7
    elif yaw_discrete == 2:
        target_XPos = current_XPos - 0.6
        target_ZPos = current_ZPos
    elif yaw_discrete == 3:
        target_XPos = current_XPos - 0.7
        target_ZPos = current_ZPos - 0.7
    elif yaw_discrete == 4:
        target_XPos = current_XPos
        target_ZPos = current_ZPos - 0.6
    elif yaw_discrete == 5:
        target_XPos = current_XPos + 0.7
        target_ZPos = current_ZPos - 0.7
    elif yaw_discrete == 6:
        target_XPos = current_XPos + 0.6
        target_ZPos = current_ZPos
    elif yaw_discrete == 7:
        target_XPos = current_XPos + 0.7
        target_ZPos = current_ZPos + 0.7
    return target_XPos, target_ZPos
# input current state and action, it will give you the next state
def step(self, action, world_state):
    
    return

def moveStraight(self, agent_host, factor, world_state):
    flag = False
    move_speed = factor * 0.5
    # agent_host.sendCommand('move {}'.format(move_speed))
    done = False
    XPos_discrete = world_state[0]
    ZPos_discrete = world_state[2]
    yaw_discrete = world_state[3]
    while not done and flag is False:
        latest_ws = agent_host.peekWorldState()
        print(f'Move straight, Latest world state is: {latest_ws}, done is {done}')
        # If there are some new observations
        if latest_ws.number_of_observations_since_last_state > 0:
            obs_text = latest_ws.observations[-1].text
            obs = json.loads(obs_text)
            print(f'Peek World State is:{obs}')
            current_ZPos = float(obs[u'ZPos'])
            current_XPos = float(obs[u'XPos'])
            # current_yaw = float(obs[u'Yaw'])
            # current_yaw_interval = self.discretize_value(current_yaw, self.yaw_bins)
            # x_add_term, z_add_term = self.addTermOfXZ(yaw_discrete)
            # print(f'Current yaw is: {yaw_discrete}, x term is{x_add_term}, z term is {z_add_term}')
            # target_ZPos = current_ZPos + z_add_term
            # target_XPos = current_XPos + x_add_term
            (target_XPos, target_ZPos) = self.addTermOfXZ(yaw_discrete, current_XPos, current_ZPos)
            # use manhattan distance to calculate distance between current and target
            # manhattan distance: x + z 
            # 1 gaussian distance ~ 1.414 manhattan distance
            # target_manhattan = current_ZPos + current_XPos + 1.414
            print(f'Init Current XPos is {current_XPos}, ZPos is {current_ZPos}, target XPos is {target_XPos}, target ZPos is {target_ZPos}')
            while not done and ((abs(current_XPos - target_XPos) > 0.3) or (abs(current_ZPos - target_ZPos) > 0.3)):
                time.sleep(0.1)
                agent_host.sendCommand('move {}'.format(move_speed))
                latest_ws = agent_host.peekWorldState()
                # If there are some new observations
                if latest_ws.number_of_observations_since_last_state > 0:
                    obs_text = latest_ws.observations[-1].text
                    obs = json.loads(obs_text)
                    # print(f'Peek World State is:{obs}')
                    current_ZPos = float(obs[u'ZPos'])
                    current_XPos = float(obs[u'XPos'])
                    if latest_ws.is_mission_running == False or obs[u'IsAlive'] == False or int(obs[u'Life']) == 0:
                        done = True
                    else:
                        done = False
                    agent_host.sendCommand('move {}'.format(move_speed))
                    print(obs)
                    print(f'Current XPos is {current_XPos}, ZPos is {current_ZPos}, target XPos is {target_XPos}, target ZPos is {target_ZPos}')
                    if (abs(current_XPos - target_XPos) < 0.3) and (abs(current_ZPos - target_ZPos) < 0.3):
                        agent_host.sendCommand('move 0')
                        break
            flag = True
            agent_host.sendCommand('move 0')
    print(f'move straight {factor} success!')
    return
# forward is look at Z position
def turnDegree(self, agent_host, factor, world_state):
    # obs_text = world_state.observations[-1].text
    # obs = json.loads(obs_text)
    # print(f'Argument World State is:{obs}')
    flag = False
    turn_speed = factor * 0.3
    agent_host.sendCommand('turn {}'.format(turn_speed))
    isAlive = True
    last_timeAlive = None
    print(world_state)
    print(f'Current yaw interval is:{world_state[3]}')
    # world_state[3] is current yaw interval
    target_yaw = ((world_state[3] + 1) % 8)* 45
    while isAlive and isAlive and flag is False:
        latest_ws = agent_host.peekWorldState()
        print(f'TurnDegree, Latest world state is: {latest_ws}')
        # If there are some new observations
        if latest_ws.number_of_observations_since_last_state > 0:
            obs_text = latest_ws.observations[-1].text
            obs = json.loads(obs_text)
            print(f'Peek World State is:{obs}')
            current_yaw = int(obs[u'Yaw'])
            # factor = 1: turn west, factor = -1: turn east
            # init_target_yaw = factor * 45 + current_yaw
            # if factor == 1:
            #     target_yaw = (init_target_yaw) % 360
            # else:
            #     target_yaw = init_target_yaw + 360 if init_target_yaw < -360 else init_target_yaw
            print(f'Init Current yaw is {current_yaw}, target yaw is {target_yaw}')
            while isAlive and abs(current_yaw - target_yaw) > 5:
                time.sleep(0.1)
                agent_host.sendCommand('turn {}'.format(turn_speed))
                latest_ws = agent_host.peekWorldState()
                # If there are some new observations
                if latest_ws.number_of_observations_since_last_state > 0:
                    obs_text = latest_ws.observations[-1].text
                    obs = json.loads(obs_text)
                    current_yaw = int(obs[u'Yaw'])
                    timeAlive = obs[u'TimeAlive']
                    if timeAlive == last_timeAlive:
                        isAlive = False
                    last_timeAlive = timeAlive
                    agent_host.sendCommand('turn {}'.format(turn_speed))
                    print(obs)
                    print(f'Current yaw is {current_yaw}, target yaw is {target_yaw}, isAlive is: {isAlive}')
            flag = True
            agent_host.sendCommand('turn 0')