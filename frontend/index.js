function App() {
    const videoRef = React.useRef(null);
    const [result, setResult] = React.useState({ intox: 'unknown', mtcnn: 'unknown' });

    React.useEffect(() => {
        const run = async () => {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            videoRef.current.srcObject = stream;

            const pc = new RTCPeerConnection();
            const dc = pc.createDataChannel('preds');
            dc.onmessage = (e) => {
                try {
                    const data = JSON.parse(e.data);
                    setResult(data);
                } catch { }
            };
            stream.getTracks().forEach(t => pc.addTrack(t, stream));

            const offer = await pc.createOffer();
            await pc.setLocalDescription(offer);
            const resp = await fetch('http://localhost:5000/api/offer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sdp: pc.localDescription })
            });
            const ans = await resp.json();
            await pc.setRemoteDescription(ans.sdp);
        };
        run();
    }, []);

    React.useEffect(() => {
        fetch('http://localhost:5000/api/test', {       
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model: 'mtcnn' })
        }).then(res => res.json()).then(data => {
            console.log('Model created:', data);
        }).catch(err => {
            console.error('Error creating model:', err);
        });
    }, []);

    return (
        <div>
            <video ref={videoRef} autoPlay playsInline width="320" />
            {/* <p>intox: {result.intox}</p> */}
            <p>mtcnn: {result.mtcnn}</p>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
