# Streamlit Audio Queue Player

This is a custom Streamlit component that plays audio files sequentially. It maintains an internal queue on the frontend so that when you send audio (as a base64 string) from Streamlit, they are played one after another.

## Features

- **Internal Queue:** New audio items are added to a queue and played sequentially.
- **Persistent State:** The component uses a fixed key so that its internal state is preserved across Streamlit reruns.
- **Easy Integration:** Simply call `audio_player(audio, format="audio/wav", key="...")` from your Streamlit app.
- **Automatic Refresh Example:** An included sample app automatically refreshes every 1 second.

## Installation

```bash
pip install streamlit-audio-queue-player
```

## Usage
In a Streamlit App
A sample Streamlit app is provided under the example/ directory. For example:

```bash
streamlit run example/app.py
```

In your app, you can add audio to the playback queue as follows:

```python
import streamlit as st
import base64
from streamlit_audio_queue_player import audio_player

st.title("Demo: Streamlit Audio Player Component")

# Example: When the button is pressed, a dummy audio file is added to the queue.
if st.button("Add Dummy Audio"):
    try:
        with open("dummy.wav", "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        # Call the component with a fixed key so that its internal queue is preserved.
        audio_player(audio_b64, format="audio/wav", key="audio_player")
    except Exception as e:
        st.error(f"Error loading dummy audio: {e}")
else:
    # Even if no new audio is provided, call the component to maintain its state.
    audio_player(None, format="audio/wav", key="audio_player")
```

### For Forcing Stop / Clearing the Queue
You can force-stop the current audio and clear the playback queue by providing a new clear_key value. For example, include a "Clear Audio Queue" button that increments an internal counter:

```py
if "clear_key" not in st.session_state:
    st.session_state["clear_key"] = 0

if st.button("Clear Audio Queue"):
    st.session_state["clear_key"] += 1

audio_player(
    None,
    format="audio/wav",
    clear_key=st.session_state["clear_key"],
    key="audio_player"
)
```

### Automatic Refresh Sample
The sample app under example/app.py includes a 1-second refresh loop using st.rerun to simulate a dynamic UI while preserving the component's internal state.


## dummy.wav

https://www3.jvckenwood.com/pro/soft_dl/pa-d_message/aisatu.html 