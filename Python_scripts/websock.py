import asyncio
import websockets
import cv2
import numpy as np
import json
import sys
import traceback
import logging
logging.basicConfig(filename='./example.log',level=logging.DEBUG)
count = 0


async def hello(websocket, path):
    print('here!!')
    logging.info('here!')
    try:
        global count
        print(sys.argv[1])
        video = cv2.VideoCapture(sys.argv[2])
        while True:
            print('here!' + str(count))
            print(video)
            rval, frame = video.read()
            # print(frame)
            print(rval)
            if rval:
                if count == 0:
                    await websocket.send(json.dumps({"height": np.shape(frame)[0], "width": np.shape(frame)[1]}))
                    count = 10
                format, img = cv2.imencode('.jpg', frame)
                print(img)
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
    logging.debug('-------------------------------------------------------------------------')
    logging.info(sys.version_info)  
    # logging.warning('And this, too')
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