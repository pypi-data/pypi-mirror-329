import os
import streamlit.components.v1 as components

_RELEASE = True  # リリース時は True、開発中は False にしてください

if not _RELEASE:
    _component_func = components.declare_component(
        "audio_player",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    _component_func = components.declare_component("audio_player", path=build_dir)

def audio_player(audio, format="audio/wav", clear_key=None, key=None):
    """
    Render the audio player component.

    Parameters:
      audio (str or None): Base64-encoded audio data. Pass a new value when a new audio is added.
      format (str): Audio MIME type (default: "audio/wav").
      clear_key (int or None): When this value changes (e.g. incremented), the component will force-stop current playback and clear its queue.
      key (str): A fixed key to ensure the component's internal state persists across reruns.
    """
    component_value = _component_func(
        audio=audio, format=format, clearKey=clear_key, key=key, default=None
    )
    return component_value
