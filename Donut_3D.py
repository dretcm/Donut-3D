import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from skvideo import io

def rotate(theta, axis='x'):
        sin = lambda x: np.sin(np.radians(x))
        cos = lambda x: np.cos(np.radians(x))
        if axis == 'x':
                x = np.array([[1,0,0], [0,cos(theta),-sin(theta)], [0,sin(theta),cos(theta)]])
                return x
        elif axis == 'y':
                y = np.array([[cos(theta),0,sin(theta)], [0,1,0], [-sin(theta),0,cos(theta)]])
                return y
        z = np.array([[cos(theta),-sin(theta),0], [sin(theta),cos(theta),0], [0,0,1]])
        return z

def generate_donut(path='d:\images'):
        
        if os.path.exists(path):
                os.system(f'DEL /F /A {path}')
        else:
                os.mkdir(path)
                
        until = 360 # 360°
        c = np.arange(0,until+1)
        colors = (c)

        b = np.array([[1],[1],[1]])
        x,y,z = [],[],[]

        for a in np.arange(0,until+1):
                xyz = rotate(a,axis='y').dot(b)
                x.extend(xyz[0])
                y.extend(xyz[1])
                z.extend(xyz[2])


        for a in np.arange(0,until+1):
                fig = plt.figure(figsize = (10, 6))
                ax = plt.axes(projection ="3d")

                aux = rotate(a,axis='x').dot(np.array([x,y,z])) # vector transformation
                
                ax.scatter3D(aux[0], aux[1], aux[2], c=colors, cmap=plt.get_cmap('hsv'), marker='^')

                ax.set_xlabel('X-axis', fontweight ='bold')
                ax.set_ylabel('Y-axis', fontweight ='bold') 
                ax.set_zlabel('Z-axis', fontweight ='bold')

                ax.set_xlim(-2,2)
                ax.set_ylim(-2,2)
                ax.set_zlim(-2,2)

                plt.title("Donut")
                # plt.show()
                
                plt.savefig(f'{path}\img{a}.jpg')
                

def generate_video(path, lenght):

        writer = io.FFmpegWriter("D:\Grabacion.avi", outputdict={
              '-vcodec': 'libx264',  #use the h.264 codec
              '-crf': '0',           #set the constant rate factor to 0, which is lossless
              '-preset':'veryslow'   #the slower the better compression, in princple, try 
                                 #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
        })
        
        
        for i in range(lenght):
            img = cv2.imread(path+'\\'+f'img{i}.jpg')
            frame = np.asarray(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            writer.writeFrame(frame[:,:,::-1])

        writer.close()


if __name__ == '__name__':
        path = r"D:\images"
        generate_donut(path)
        generate_video(path,361) # path, number of images.
