Here’s your `README.md` rewritten using proper Markdown formatting and conventions:

```markdown
# 📚 GENAI Storybook Generator

A personal project to showcase the creative potential of generative AI through the production of **illustrated storybooks** with AI-generated **text, images, narration, and video**.

🎥 **Watch the development video**: [https://www.youtube.com/watch?v=-J7iqhTrEvA&ab_channel=Epoch](https://www.youtube.com/watch?v=-J7iqhTrEvA&ab_channel=Epoch)

---

## ✨ Features

- ✍️ **Text Generation** using transformer models
- 🎨 **Image Generation** for each scene
- 🔊 **Audio Narration** using text-to-speech (Tortoise TTS)
- 📹 **Video Compilation** combining scenes and audio

---

## 📁 Project Structure

```

bookGenerator-master/
│
├── main.py                 # Entry point for full pipeline
├── story\_generator.py      # Handles text and structure generation
├── audio\_generator.py      # Text-to-speech narration
├── video\_generator.py      # Assembles video from story assets
├── config.json             # Configuration for generation
├── imageToSave.png         # Sample image output
├── .gitignore              # Git exclusions
├── .idea/                  # IDE metadata

````

---

## 🧠 How It Works

1. **Generate a story** using `story_generator.py`
2. **Create scene images** for story text
3. **Narrate story** using Tortoise TTS via `audio_generator.py`
4. **Compile into video** using `video_generator.py`

All generated assets (text, images, audio, video) are saved in a structured output directory.

---

## 🛠 Installation

```bash
git clone https://github.com/yourusername/bookGenerator.git
cd bookGenerator
pip install torch torchaudio transformers
````

Make sure to install [FFmpeg](https://ffmpeg.org/download.html) and add it to your system path.

---

## 🚀 Usage

```bash
python main.py
```

Outputs will be created in a `/Stories/` folder, containing:

* 📜 Generated story text
* 🖼 Scene illustrations
* 🎧 Narrated audio
* 🎞 Final video compilation

> 🔧 You may need to adjust file paths in `main.py` to match your local environment.

---

## 📹 Demo Video

See the full project walkthrough and results here:
[![Watch on YouTube](https://img.youtube.com/vi/-J7iqhTrEvA/0.jpg)](https://www.youtube.com/watch?v=-J7iqhTrEvA&ab_channel=Epoch)

---

## 🧪 Purpose

Created as a **Programming Paradigms final project** at **The University of Texas at Austin**, this project explores the intersection of creative storytelling and generative AI technologies. It is both a technical showcase and a creative experiment.

---

## 📬 Contact

For questions, feel free to open an issue or reach out on [YouTube](https://www.youtube.com/channel/UCJYdYicg93L3B7hguMBe71Q).

```

Let me know if you’d like to include example outputs or screenshots.
```
