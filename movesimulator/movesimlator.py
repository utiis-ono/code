import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 定数の定義
n_devices = 100 # 端末の数
n_steps = 100 # シミュレーションのステップ数
xlim = (0, 1000) # x軸の範囲
ylim = (0, 1000) # y軸の範囲
alpha = 0.2 # 移動の速さの係数
radius = 250 # 円の半径
center = (500, 500) # 円の中心座標

# ランダムウェイポイントモデルに基づく座標の生成
x0 = np.random.uniform(*xlim, n_devices)
y0 = np.random.uniform(*ylim, n_devices)
dest_x = np.random.uniform(*xlim, n_devices)
dest_y = np.random.uniform(*ylim, n_devices)

# 座標の初期化
x = x0.copy()
y = y0.copy()

# CSVファイルへの書き込みの準備
time = pd.date_range(start=pd.Timestamp.now(), periods=n_steps, freq='1S')
columns = ['time'] + [f'device_{i}_x' for i in range(n_devices) ] + [f'device_{i}_y' for i in range(n_devices) ]
#columns=['time', *[f'device{i}_x,device{i}_y' for i in range(n_devices)]]
df  = pd.DataFrame(columns=columns)

# アニメーションのフレームごとの処理
def update(frame):
    global x, y, dest_x, dest_y, df, df2
    
    # 移動先に到着した端末の新しい移動先をランダムに指定
    arrived = np.sqrt((x - dest_x)**2 + (y - dest_y)**2) < 1
    dest_x[arrived] = np.random.uniform(*xlim, np.sum(arrived))
    dest_y[arrived] = np.random.uniform(*ylim, np.sum(arrived))
    
    # 移動先の座標を計算
    dx = dest_x - x
    dy = dest_y - y
    dist = np.sqrt(dx**2 + dy**2)
    v = alpha * dist
    v = np.minimum(v, dist)
    theta = np.arctan2(dy, dx)
    dx_move = v * np.cos(theta)
    dy_move = v * np.sin(theta)
    x += dx_move
    y += dy_move
    
    # 範囲外に出た端末の位置を修正
    x = np.clip(x, *xlim)
    y = np.clip(y, *ylim)
    
    # CSVファイルに書き込み
    data = [frame+1] + [coord for xy in zip(x, y) for coord in xy]
    #print(data)
    df.loc[len(df)] = data
    
    # 散布図のプロット
    plt.clf()
    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.scatter(x, y)

    # 円のプロット
    circle = plt.Circle(center, radius, fill=False)
    plt.gca().add_artist(circle)

    # 円の内部にいる端末のマーカーの色を変更
    in_circle = np.sqrt((x - center[0])**2 + (y - center[1])**2) < radius
    plt.scatter(x[in_circle], y[in_circle], marker='o', s=20, c='red')

    # 円の外部にいる端末のマーカーの色を変更
    plt.scatter(x[~in_circle], y[~in_circle], marker='o', s=20, c='blue')

    # 軸のラベルを設定
    plt.xlabel('x')
    plt.ylabel('y')

    # タイトルを設定
    plt.title(f'Time: {frame}')

    # 凡例を設定
    #plt.legend(['Circle Inside', 'Circle Outside'])
    
    # タイトルの設定
    plt.title(f'Simulation Frame: {frame}')
    
    return []

# アニメーション
fig = plt.figure(figsize=(8, 8))
ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=100)

# 動画の保存
ani.save('random_waypoint.mp4')

# CSVファイルの保存
df.to_csv('random_waypoint.csv', index=False)


#in_cercleかどうかのcsv
for i in range(n_devices):
    device_id_x = "device" + "_" + str(i) + "_" + "x"
    device_id_y = "device" + "_" + str(i) + "_" + "x"
    df2 = pd.DataFrame(columns=['time', 'in-out'])
    for j in range(n_steps):
        print(df.loc[device_id_x,str(j)])
        #print(np.sqrt((float(df.loc[device_id_x,str(j)]) - center[0])**2 + float((df.loc[device_id_y,str(j)]) - center[1])**2))
        




