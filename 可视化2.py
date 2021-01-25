#_*_  coding:utf-8 _*_
import numpy as np
import matplotlib.pyplot as plt

if __name__  == "__main__":
    # 球员能力表
    plt.style.use('bmh')

    # font = FontProperties(fname='', size=20)

    ability_size = 5
    ability_label = ['happy_love', 'sad_guilty', 'angry_hatred', 'surprise_afraid', 'other_emotion', 'happy_love']

    ax1 = plt.subplot(221, projection='polar')
    ax2 = plt.subplot(222, projection='polar')
    ax3 = plt.subplot(223, projection='polar')
    ax4 = plt.subplot(224, projection='polar')

    data = {
        '1st': [38.281250, 33.593750, 23.437500, 4.687500, 0.000000],
        '2nd': [46.754386, 22.719298, 22.719298, 4.122807, 3.684211],
        '3rd': [48.795181, 29.518072, 13.855422, 4.216867, 3.614458],
        '4th': [52.825908, 18.419967, 19.183168, 4.785479, 4.785479]
    }

    theta = np.linspace(0, 2*np.pi, 5, endpoint=False)
    theta = np.append(theta, theta[0])

    data['1st'] = np.append(data['1st'], data['1st'][0])
    ax1.plot(theta, data['1st'], color=(0.6, 0.4, 0))
    ax1.fill(theta, data['1st'], color=(0.6, 0.4, 0), alpha=0.3)
    ax1.set_xticks(theta)
    ax1.set_yticks([20, 30, 40, 50, 60])
    ax1.set_xticklabels(ability_label, size=7.5)
    ax1.set_yticklabels([20, 30, 40, 50, 60], size=7)
    n = 0
    for unit in data['1st']:
        angle = theta[n]
        ax1.annotate(unit, xy=(angle, unit+1), xytext=(angle + 0.05, unit + 13),
            arrowprops=dict(facecolor='r', headlength=4, headwidth=4, width=1), size=7)
        n +=1
    ax1.set_title('2019.12.8 ~ 2020.1.22', position=(0.2, 1), size = 12, color=(0.6, 0.4, 0))

    data['2nd'] = np.append(data['2nd'], data['2nd'][0])
    ax2.plot(theta, data['2nd'], color=(0.9,0.3,0.2))
    ax2.fill(theta, data['2nd'], color=(0.9,0.3,0.2), alpha=0.3)
    ax2.set_xticks(theta)
    ax2.set_yticks([20, 30, 40, 50, 60])
    ax2.set_xticklabels(ability_label, size=7.5)
    ax2.set_yticklabels([20, 30, 40, 50, 60], size=7)
    n = 0
    for unit in data['2nd']:
        angle = theta[n]
        ax2.annotate(unit, xy=(angle, unit+1), xytext=(angle + 0.05, unit + 13),
            arrowprops=dict(facecolor='r', headlength=4, headwidth=4, width=1), size=7)
        n += 1
    ax2.set_title('2020.1.23 ~ 2020.2.7', position=(0.2, 1), size = 12, color=(0.9,0.3,0.2))

    data['3rd'] = np.append(data['3rd'], data['3rd'][0])
    ax3.plot(theta, data['3rd'], color=(0.8, 0.1, 0.3))
    ax3.fill(theta, data['3rd'], color=(0.8, 0.1, 0.3), alpha=0.3)
    ax3.set_xticks(theta)
    ax3.set_yticks([20, 30, 40, 50, 60])
    ax3.set_xticklabels(ability_label, size=7.5)
    ax3.set_yticklabels([20, 30, 40, 50, 60], size=7)
    n = 0
    for unit in data['3rd']:
        angle = theta[n]
        ax3.annotate(unit, xy=(angle, unit+1), xytext=(angle + 0.05, unit + 13),
                     arrowprops=dict(facecolor='r', headlength=4, headwidth=4, width=1), size=7)
        n += 1
    ax3.set_title('2020.2.8 ~ 2020.2.13', position=(0.2, 1), size = 12, color=(0.8, 0.1, 0.3))

    data['4th'] = np.append(data['4th'], data['4th'][0])
    ax4.plot(theta, data['4th'], color=(0.5, 0, 0))
    ax4.fill(theta, data['4th'], color=(0.5, 0, 0), alpha=0.3)
    ax4.set_xticks(theta)
    ax4.set_yticks([20, 30, 40, 50, 60])
    ax4.set_xticklabels(ability_label, size=7.5)
    ax4.set_yticklabels([20, 30, 40, 50, 60], size=7)
    n = 0
    for unit in data['4th']:
        angle = theta[n]
        ax4.annotate(unit, xy=(angle, unit+1), xytext=(angle + 0.05, unit + 13),
                     arrowprops=dict(facecolor='r', headlength=4, headwidth=4, width=1), size=7)
        n += 1
    ax4.set_title('2020.2.14 ~ 2020.6.30', position=(0.2, 1), size = 12, color=(0.5, 0, 0))

    plt.show()