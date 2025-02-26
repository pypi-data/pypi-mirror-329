# AkumaSubtitler 🎥✍️

**The ultimate tool for adding professional subtitles to your videos with ease.**

---

## Features ✨

- 🎙 **AI-Powered Subtitles**: Automatically generate subtitles using OpenAI's Whisper.
- 🎨 **Custom Styling**: Full control over subtitle appearance (fonts, colors, positions).
- 🔊 **Audio Mixing**: Blend original audio with new narration tracks.
- ⚡ **Fast Processing**: Hardware-accelerated video processing with FFmpeg.
- 🌐 **Multi-Source Support**: Works with local files and remote URLs.
- 🔧 **Extensible**: Easily add custom effects and styles.

---

## Installation 📦

```bash
pip install akumasubtitler
```

---

## Quick Start 🚀

```python
from akuma import AkumaSubtitler, SubStyle

# Initialize the subtitler
akuma = AkumaSubtitler()

# Basic usage with auto-generated subtitles
akuma.forge_video(
    video_path="input_video.mp4",
    output_path="output_video.mp4"
)

# Advanced usage with custom styling
inferno_style = SubStyle(
    font_name="Arial",
    font_size=28,
    primary_color="#FF4500",  # Orange-red
    border=3
)

akuma.forge_video(
    video_path="input_video.mp4",
    output_path="styled_video.mp4",
    audio_path="narration.mp3",
    style=inferno_style
)
```

---

## Customization Options 🎨

### Subtitle Styling (`SubStyle` Class)
```python
from akuma import SubStyle

# Custom style example
custom_style = SubStyle(
    font_name="Impact",
    font_size=24,
    primary_color="yellow",
    border=3,
    alignment="center",
    margin_v=50  # Vertical position
)
```

### Audio Mixing
- **Original Audio Volume**: Control the volume of the original video audio.
- **New Audio Volume**: Adjust the volume of the added narration track.

```python
akuma.forge_video(
    video_path="input.mp4",
    output_path="output.mp4",
    audio_path="narration.mp3",
    original_audio_volume=0.3,  # 30% original audio
    new_audio_volume=0.7        # 70% new audio
)
```

---

## Whisper Models 🧠

Choose the Whisper model size based on your needs:

| Model Size | Speed | Accuracy | Use Case                     |
|------------|-------|----------|------------------------------|
| `tiny`     | ⚡ Fast | Low      | Quick drafts                 |
| `base`     | 🚀 Fast | Medium   | General purpose (default)    |
| `small`    | 🐢 Medium | High     | High-quality subtitles       |
| `medium`   | 🐌 Slow | Very High| Professional use             |
| `large`    | 🐌🐌 Very Slow | Best   | Maximum accuracy             |

---

## Advanced Usage 🔧

### Register Custom Effects
```python
from akuma import AkumaSubtitler

@AkumaSubtitler.register_effect("custom_effect")
def custom_effect(image, progress, config):
    # Your custom effect logic here
    return transformed_image
```

### Batch Processing
```python
videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
for video in videos:
    akuma.forge_video(
        video_path=video,
        output_path=f"processed_{video}"
    )
```

---

## System Requirements 💻

- **Python**: 3.8+
- **FFmpeg**: Required for video processing.
- **GPU Support**: Recommended for faster Whisper processing (CUDA-enabled).

---

## Contributing 🤝

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? Open an issue [here](https://github.com/yourusername/AkumaSubtitler/issues).
2. **Submit Features**: Have an idea? Share it in the discussions.
3. **Code Contributions**: Fork the repo and submit a pull request.

---

## License 📄

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Support 🆘

For help or questions, please:
- Open an issue on [GitHub](https://github.com/yourusername/AkumaSubtitler/issues).
- Join our [Discussions](https://github.com/yourusername/AkumaSubtitler/discussions).

---

## Links 🔗

- **GitHub Repository**: [AkumaSubtitler](https://github.com/yourusername/AkumaSubtitler)
- **PyPI Package**: [akumasubtitler](https://pypi.org/project/akumasubtitler/)
- **Documentation**: [Read the Docs](https://akumasubtitler.readthedocs.io)

---

**AkumaSubtitler**: Where videos meet perfection. 🎬✨