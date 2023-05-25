from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
import MalmoPython
import os
import sys
import time
import numpy as np
import logging
import json

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import tkinter as tk

class TabQAgent(object):
    """Tabular Q-learning agent for discrete state/action spaces."""

    def __init__(self):
        self.epsilon = 0.2 # chance of taking a random action instead of the best

        self.logger = logging.getLogger(__name__)
        if False: # True if you want to see more information
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.handlers = []
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        """
        jumpbackward is not allow
        actions:
            0: forward 1
            1: backward 1
            2: jumpforward 1(jump 1 + move 1)
            3: set Yaw 45
            4: set Yaw -45
        """
        self.n_actions = 2
        # self.actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1", "jump 1", "turn 0.5", "turn -0.5"]
        self.actions = ["moveForward 1", "set Yaw 45"]
        self.q_table = {}
        self.canvas = None
        self.root = None
        # End your code
    def moveStraight(self, agent_host, factor, world_state):
        flag = False
        move_speed = factor * 0.5
        # agent_host.sendCommand('move {}'.format(move_speed))
        isAlive = True
        last_timeAlive = None
        while isAlive and flag is False:
            latest_ws = agent_host.peekWorldState()
            print(f'Move straight, Latest world state is: {latest_ws}')
            # If there are some new observations
            if latest_ws.number_of_observations_since_last_state > 0:
                obs_text = latest_ws.observations[-1].text
                obs = json.loads(obs_text)
                print(f'Peek World State is:{obs}')
                current_ZPos = float(obs[u'ZPos'])
                current_XPos = float(obs[u'XPos'])
                target_ZPos = current_ZPos + 0.70711
                target_XPos = current_XPos + 0.70711
                # use manhattan distance to calculate distance between current and target
                # manhattan distance: x + z 
                # 1 gaussian distance ~ 1.414 manhattan distance
                # target_manhattan = current_ZPos + current_XPos + 1.414
                print(f'Init Current XPos is {current_XPos}, ZPos is {current_ZPos}, target XPos is {target_XPos}, target ZPos is {target_ZPos}')
                while isAlive and abs(current_XPos - target_XPos) + abs(current_ZPos - target_ZPos) > 0.5:
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
                        timeAlive = obs[u'TimeAlive']
                        if timeAlive == last_timeAlive:
                            isAlive = False
                        last_timeAlive = timeAlive
                        agent_host.sendCommand('move {}'.format(move_speed))
                        print(obs)
                        print(f'Current XPos is {current_XPos}, ZPos is {current_ZPos}, target XPos is {target_XPos}, target ZPos is {target_ZPos}')
                flag = True
                agent_host.sendCommand('move 0')
        print(f'move straight {factor} success!')
    # forward is look at Z position
    def turnDegree(self, agent_host, factor, world_state):
        # obs_text = world_state.observations[-1].text
        # obs = json.loads(obs_text)
        # print(f'Argument World State is:{obs}')
        flag = False
        turn_speed = factor * 0.5
        agent_host.sendCommand('turn {}'.format(turn_speed))
        isAlive = True
        last_timeAlive = None
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
                init_target_yaw = factor * 45 + current_yaw
                if factor == 1:
                    target_yaw = (init_target_yaw) % 360
                else:
                    target_yaw = init_target_yaw + 360 if init_target_yaw < -360 else init_target_yaw
                print(f'Init Current yaw is {current_yaw}, target yaw is {target_yaw}')
                while isAlive and abs(current_yaw - target_yaw) > 10:
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
    
    def updateQTable( self, reward, current_state ):
        """Change q_table to reflect what we have learnt."""
        
        # retrieve the old action value from the Q-table (indexed by the previous state and the previous action)
        old_q = self.q_table[self.prev_s][self.prev_a]
        
        # TODO: what should the new action value be?
        learning_rate = 0.1  # learning rate (alpha)
        discount_factor = 0.99  # discount factor (gamma)
        max_future_q = max(self.q_table[current_state])  # maximum Q-value for the current state
        new_q = old_q + learning_rate * (reward + discount_factor * max_future_q - old_q) 
        print(self.q_table)
        # assign the new action value to the Q-table
        self.q_table[self.prev_s][self.prev_a] = new_q
        
    def updateQTableFromTerminatingState( self, reward ):
        """Change q_table to reflect what we have learnt, after reaching a terminal state."""
        
        # retrieve the old action value from the Q-table (indexed by the previous state and the previous action)
        old_q = self.q_table[self.prev_s][self.prev_a]
        
        # TODO: what should the new action value be?
        learning_rate = 0.1  # learning rate (alpha)
        new_q = old_q + learning_rate * (reward - old_q)
        
        # assign the new action value to the Q-table
        self.q_table[self.prev_s][self.prev_a] = new_q
        
    def act(self, world_state, agent_host, current_r ):
        """take 1 action in response to the current world state"""
        # print(f'Mission is running: {agent_host.getWorldState().is_mission_running}')
        obs_text = world_state.observations[-1].text
        obs = json.loads(obs_text) # most recent observation
        print(f'Current state is: {obs}')
        # Transform
        self.logger.debug(obs)
        if not u'XPos' in obs or not u'ZPos' in obs:
            self.logger.error("Incomplete observation received: %s" % obs_text)
            return 0
        current_s = "%d:%d" % (int(obs[u'XPos']), int(obs[u'ZPos']))
        self.logger.debug("State: %s (x = %.2f, z = %.2f)" % (current_s, float(obs[u'XPos']), float(obs[u'ZPos'])))
        if current_s not in self.q_table:
            self.q_table[current_s] = ([0] * len(self.actions))

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.updateQTable( current_r, current_s )

        # self.drawQ( curr_x = int(obs[u'XPos']), curr_y = int(obs[u'ZPos']) )

        # select the next action
        rnd = random.random()
        if rnd < self.epsilon:
            a = random.randint(0, len(self.actions) - 1)
            self.logger.info("Random action: %s" % self.actions[a])
        else:
            m = max(self.q_table[current_s])
            self.logger.debug("Current values: %s" % ",".join(str(x) for x in self.q_table[current_s]))
            l = list()
            for x in range(0, len(self.actions)):
                if self.q_table[current_s][x] == m:
                    l.append(x)
            y = random.randint(0, len(l)-1)
            a = l[y]
            # print(f'action list is:{l}')
            self.logger.info("Taking q action: %s" % self.actions[a])

        # try to send the selected action, only update prev_s if this succeeds
        try:
          # if world_state.is_mission_running:
          #   print('Mission is still running')
          # else:
          #   print('Mission is not running')
          # # agent_host.sendCommand('move 0')
          # agent_host.sendCommand('move 1')
          # if world_state.is_mission_running:
          #   print('Mission is still running')
          # else:
          #   print('Mission is not running')
            # move forward
            if a == 0:
                # agent_host.sendCommand("strafe 1")
                self.turnDegree(agent_host, 1, world_state)
                
                # agent_host.sendCommand('move 1')
                time.sleep(1)
                # world_state = agent_host.getWorldState()
                # obs_text = world_state.observations[-1].text
                # obs = json.loads(obs_text)
                # print(f'After move forward, World State is:{obs}')
            # move backward
            # elif a == 1:
            #     # agent_host.sendCommand("strafe -1")
            #     # self.moveStraight(agent_host, -1, world_state)
            #     agent_host.sendCommand('move -1')
            #     time.sleep(1)
            # elif a == 1:
            #     agent_host.sendCommand("move 1")
            #     agent_host.sendCommand("jump 1")
            #     time.sleep(1)
            else:
                # self.moveStraight(agent_host, 1, world_state)
                agent_host.sendCommand('move 1')
                time.sleep(1)
                # agent_host.sendCommand("turn 45")
            # elif a == 4:
            #     self.turnDegree(agent_host, -1, world_state)
            #     agent_host.sendCommand("turn -45")
            
            # agent_host.sendCommand(self.actions[a])
            self.prev_s = current_s
            self.prev_a = 0

        except RuntimeError as e:
              self.logger.error("Failed to send command: %s" % e)

        return current_r

    def run(self, agent_host):
        """run the agent on the world"""

        total_reward = 0
        
        self.prev_s = None
        self.prev_a = None
        is_first_action = True
        
        # main loop:
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:
            
            current_r = 0
            if is_first_action:
                # wait until have received a valid observation
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                    if world_state.is_mission_running and len(world_state.observations)>0 and not world_state.observations[-1].text=="{}":
                        total_reward += self.act(world_state, agent_host, current_r)
                        break
                    if not world_state.is_mission_running:
                        break
                is_first_action = False
            else:
                # wait for non-zero reward
                while world_state.is_mission_running and current_r == 0:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                # allow time to stabilise after action
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                    if world_state.is_mission_running and len(world_state.observations)>0 and not world_state.observations[-1].text=="{}":
                        total_reward += self.act(world_state, agent_host, current_r)
                        break
                    if not world_state.is_mission_running:
                        print(f'world_state is not running mission')
                        break

        # process final reward
        self.logger.debug("Final reward: %d" % current_r)
        total_reward += current_r

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.updateQTableFromTerminatingState( current_r )
            
        # self.drawQ()
    
        return total_reward
        
    def drawQ( self, curr_x=None, curr_y=None ):
        scale = 40
        world_x = 6
        world_y = 14
        if self.canvas is None or self.root is None:
            self.root = tk.Tk()
            self.root.wm_title("Q-table")
            self.canvas = tk.Canvas(self.root, width=world_x*scale, height=world_y*scale, borderwidth=0, highlightthickness=0, bg="black")
            self.canvas.grid()
            self.root.update()
        self.canvas.delete("all")
        action_inset = 0.1
        action_radius = 0.1
        curr_radius = 0.2
        action_positions = [ ( 0.5, action_inset ), ( 0.5, 1-action_inset ), ( action_inset, 0.5 ), ( 1-action_inset, 0.5 ) ]
        # (NSWE to match action order)
        min_value = -20
        max_value = 20
        for x in range(world_x):
            for y in range(world_y):
                s = "%d:%d" % (x,y)
                self.canvas.create_rectangle( x*scale, y*scale, (x+1)*scale, (y+1)*scale, outline="#fff", fill="#000")
                for action in range(4):
                    if not s in self.q_table:
                        continue
                    value = self.q_table[s][action]
                    color = int( 255 * ( value - min_value ) / ( max_value - min_value )) # map value to 0-255
                    color = max( min( color, 255 ), 0 ) # ensure within [0,255]
                    color_string = '#%02x%02x%02x' % (255-color, color, 0)
                    self.canvas.create_oval( (x + action_positions[action][0] - action_radius ) *scale,
                                             (y + action_positions[action][1] - action_radius ) *scale,
                                             (x + action_positions[action][0] + action_radius ) *scale,
                                             (y + action_positions[action][1] + action_radius ) *scale, 
                                             outline=color_string, fill=color_string )
        if curr_x is not None and curr_y is not None:
            self.canvas.create_oval( (curr_x + 0.5 - curr_radius ) * scale, 
                                     (curr_y + 0.5 - curr_radius ) * scale, 
                                     (curr_x + 0.5 + curr_radius ) * scale, 
                                     (curr_y + 0.5 + curr_radius ) * scale, 
                                     outline="#fff", fill="#fff" )
        self.root.update()

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

agent = TabQAgent()
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)


my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

# Loop until mission ends:
while world_state.is_mission_running:
    
    # agent_host.sendCommand("move 1")
    # print(".", end="")
    world_state = agent_host.getWorldState()
    # print(world_state)
    # TurnDegree(agent_host, -1)
    # jumpForward(agent_host)
    agent_host.sendCommand("turn 45")
    # agent_host.sendCommand('turn 0')
    # agent_host.sendCommand("move 1")
    print('Success Turn!')
    time.sleep(2)
    agent_host.sendCommand('turn 0')
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.
