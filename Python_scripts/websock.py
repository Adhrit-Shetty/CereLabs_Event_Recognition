import asyncio
import websockets
import cv2
import numpy as np
import json
count=0
async def hello(websocket, path):
    global count
    video = cv2.VideoCapture("rtsp://admin:admin1234@192.168.1.207:1027/MPEG-4/ch06/main/av_stream")
    while True: 
        print('here!'+str(count))
        print(video)    
        rval, frame = video.read()
        # print(frame)
        if count == 0:
            await websocket.send(json.dumps({"height":np.shape(frame)[0],"width":np.shape(frame)[1]}))
            count = 10
        print(rval)
        if rval:
            format,img = cv2.imencode('.jpg',frame)
            print(img)
            await websocket.send(img.tobytes())
            # print("> {}".format(greeting))
    #     for i in range(4):
    #         a.append(x[b:b+chunk_size])
    #         b+=chunk_size
    #     message='@@ '+' '.join(map(str,np.shape(frame)))+" "+str(np.shape(a)[0])+" "+str(chunk_size)
    #     x = 100-len(message)
    #     for i in range(x):
    #         message+='-'
    #     client.sendto(message.encode('utf-8'), (host, port))
    #     for i in range(np.shape(a)[0]):
    #         client.sendto(a[i], (host, port))
    # else:
    #     message='##'
    #     x = 100-len(message)
    #     for i in range(x):
    #         message+='-'
    #     client.sendto(message.encode('utf-8'), (host, port))
    #     client.close()
    #     break

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()