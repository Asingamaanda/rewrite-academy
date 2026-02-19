import asyncio
import edge_tts

async def generate_voiceover():
    """Generate voiceover audio using Edge-TTS"""
    with open("limits_narration.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    voice = "en-US-GuyNeural"
    rate = "-20%"
    output_file = "limits_voiceover.mp3"
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)
    
    print(f"✓ Voiceover generated successfully: {output_file}")
    print(f"  Voice: {voice} (deep, warm male)")
    print(f"  Speed: {rate} (slow and soothing)")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
