import os
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

start_time = time.time()

args = sys.argv

if len(args) != 7:
    print("Usage: python3 car.py <NUM_DEVICES> <LANE_LENGTH> <LANE_WIDTH> <TIME_DURATION> <CIRCLE1_RADIUS> <CRCLE2_RADIUS>")
    sys.exit()

# Constants
NUM_DEVICES = int(args[1]) #100
LANE_LENGTH = int(args[2]) #1000
LANE_WIDTH = int(args[3]) #2
TIME_DURATION = int(args[4]) #3600 #simulation time
CIRCLE1_RADIUS = int(args[5]) #250
CIRCLE2_RADIUS = int(args[6]) #300

FPS = 1
movFPS = 30 #動画のフレームレート

# Setup
random.seed(42)
np.random.seed(42)
if not os.path.exists(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/'):
    os.makedirs(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/nodes/')

def initialize_devices():
    devices = []
    for i in range(NUM_DEVICES):
        x = random.uniform(0, LANE_LENGTH)
        #y = random.choice([0, LANE_WIDTH])
        y = random.randint(0, LANE_WIDTH-1)
        speed = random.uniform(55/3.6, 65/3.6)
        direction = 1 if (y%2) == 0 else -1
        devices.append({'id': i, 'x': x, 'y': y, 'speed': speed, 'direction': direction})
    return devices

def update_device(device, dt):
    device['x'] += device['speed'] * device['direction'] * dt
    if device['x'] > LANE_LENGTH:
        device['x'] -= LANE_LENGTH
    elif device['x'] < 0:
        device['x'] += LANE_LENGTH
    return device

#def inside_circle(device, circle_radius):
#    return device['x']**2 + (device['y']*LANE_WIDTH)**2 < circle_radius**2

def inside_circle(device, circle_radius):
    dx = device['x'] - LANE_LENGTH / 2
    dy = device['y'] * LANE_WIDTH - LANE_WIDTH / 2
    return dx**2 + dy**2 < circle_radius**2


def plot_devices(devices, ax, frame):
    for device in devices:
        if inside_circle(device, CIRCLE1_RADIUS):
            color = 'red'
            in_or_out = 0
        elif inside_circle(device, CIRCLE2_RADIUS):
            color = 'orange'
            in_or_out = 1
        else:
            color = 'blue'
            in_or_out = 2

        ax.scatter(device['x'], device['y'], color=color)

        # Save device data to CSV
        #print(frame)
        if(frame%FPS==0):
            data = {'time': [frame/FPS], 'x': [device['x']], 'y': [device['y']], 'in_or_out': [in_or_out]}
            df = pd.DataFrame(data)
            if frame == 0:
                df.to_csv(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/nodes/node_{device["id"]}.csv', index=False, header=True)
            else:
                df.to_csv(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/nodes/node_{device["id"]}.csv', mode='a', index=False, header=False)

#1行目削除
#for i in range(NUM_DEVICES):
#    df = pd.read_csv(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/nodes/node_{i}.csv')
#    print(df)
#    df = df.drop(0)
#    print(df)
#    df.to_csv(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/nodes/node_{i}.csv',index=False)


# Animation
fig, ax = plt.subplots(figsize=(10, 3))
plt.xlim([0, LANE_LENGTH]+1)
plt.xticks(np.arange(0,LANE_LENGTH,50))
num_lane = []
name_lane = []
for i in range(LANE_WIDTH):
    num_lane.append(i)
    name_lane.append(f'lane{i+1}')

#print('num_lane',num_lane,'name_lane',name_lane,)

#plt.yticks([0, 1], ['lane1', 'lane2'])
plt.yticks(num_lane, name_lane)
devices = initialize_devices()
for device in devices:
    with open(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/nodes/node_{device["id"]}.csv', 'w') as f:
        f.write('time,x,y,in_or_out\n')

def animate(frame):
    ax.clear()
    plt.xlim([0, LANE_LENGTH])
    plt.xticks(np.arange(0,LANE_LENGTH,50))
    plt.ylim([0, LANE_WIDTH])
    plt.yticks(num_lane, name_lane)
    #plt.yticks([0, 1], ['lane1', 'lane2'])
    ax.set_xlim(0, LANE_LENGTH+1)
    ax.set_ylim(-0.5, LANE_WIDTH)

    circle1 = plt.Circle((LANE_LENGTH/2, LANE_WIDTH/2), CIRCLE1_RADIUS, color='green', fill=False)
    circle2 = plt.Circle((LANE_LENGTH/2, LANE_WIDTH/2), CIRCLE2_RADIUS, color='purple', fill=False)
    ax.add_artist(circle1)
    ax.add_artist(circle2)

    for device in devices:
        update_device(device, 1/FPS)
    plot_devices(devices, ax,frame)

    ax.text(10, LANE_WIDTH-0.3, f'Time: {frame}s', fontsize=12)

#ani = FuncAnimation(fig, animate, interval=100)
ani = FuncAnimation(fig, animate, frames=range(TIME_DURATION * FPS), interval=10, repeat=False)

ani.save(f'result/num_{NUM_DEVICES}-{TIME_DURATION}s/animation.mp4', writer='ffmpeg', fps=movFPS, dpi=300)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"実行時間: {elapsed_time} 秒")

#plt.show()
