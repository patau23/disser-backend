import json

from flask import Blueprint, request, jsonify
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole
from av import VideoFrame
import cv2

from models.drunkselfie_model import predict_with_model as intox_predict
from models.mtcnn_model import predict_with_model as mtcnn_predict


def create_blueprint():
    bp = Blueprint('webrtc', __name__)

    @bp.post('/offer')
    async def offer():
        print(123)
        params = await request.get_json()
        offer = RTCSessionDescription(**params['sdp'])

        pc = RTCPeerConnection()
        channel_holder = {'channel': None}

        @pc.on('datachannel')
        def on_datachannel(channel):
            channel_holder['channel'] = channel

        @pc.on('track')
        def on_track(track):
            if track.kind == 'video':
                pc.addTrack(VideoTransformTrack(track, channel_holder))
            else:
                pc.addTrack(track)

            @track.on('ended')
            async def on_ended():
                await pc.close()

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return jsonify({'sdp': {
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        }})

    return bp


class VideoTransformTrack(VideoStreamTrack):
    kind = 'video'

    def __init__(self, track, holder):
        super().__init__()
        self.track = track
        self.holder = holder

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format='bgr24')

        # intox = intox_predict(img)
        mtcnn = mtcnn_predict(img)
        intox = mtcnn_predict(img)

        if self.holder['channel']:
            try:
                self.holder['channel'].send(json.dumps({'intox': intox, 'mtcnn': mtcnn}))
            except Exception:
                pass

        cv2.putText(img, f'intox: {intox}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, f'mtcnn: {mtcnn}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        new_frame = VideoFrame.from_ndarray(img, format='bgr24')
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame
