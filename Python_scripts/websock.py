import asyncio
import websockets
import cv2
import numpy as np
import json
import sys
import traceback
import logging
import os
if os.path.exists('./example.log'):
    os.remove('./example.log')
logging.basicConfig(filename='./example.log',level=logging.INFO)
ct=0
async def hello(websocket, path):
    global ct
    print('here!!')
    logging.info('here!')
    try:
        print(sys.argv[1])
        video = cv2.VideoCapture(sys.argv[2])
        while True:
            rval, frame = video.read()
            if rval:
                ct+=1
                if ct %50 == 0:
                    pong_waiter = await websocket.ping()
                    await pong_waiter
                    print (pong_waiter) 
                format, img = cv2.imencode('.jpg', frame)
                # print(frame)
                await websocket.send(img.tobytes())
            else:
                print("Exiting...")
                await websocket.send(json.dumps({"message": 'No frames to send'}))
                exit()
    except:
        tb = traceback.format_exc()
        logging.info("Unexpected error: {}".format(sys.exc_info()[0]))  
        print(sys.exc_info()[0])
if __name__ == "__main__":
    print(sys.version_info)
    logging.info(sys.version_info)  
    try:
        arg = sys.argv
        if len(arg) > 2:
            logging.info(sys.argv)  
            print(sys.argv)
            # First argument is free port number
            # Second argument is the video or rtsp link
            start_server = websockets.serve(hello, 'localhost', int(sys.argv[1]))
            logging.info('server started')
            asyncio.get_event_loop().run_until_complete(start_server)
            logging.info('server started')
            asyncio.get_event_loop().run_forever()
            logging.info('server started')
        else:
            print('Exiting as no source is specified')
    except:
        tb = traceback.format_exc()
        logging.info("Unexpected error: {}".format(sys.exc_info()[0]))  
        print ("Unexpected error: {}".format(sys.exc_info()[0]))
        print (tb)