"""
Automated Text-to-Speech Generation for Chapter 1
Generates high-quality narration audio for all scenes
"""

import os
from pathlib import Path

print("Installing required TTS packages...")
print("This may take a minute...\n")

# Install dependencies
import subprocess
import sys

try:
    import edge_tts
    print("✓ edge-tts already installed")
except ImportError:
    print("Installing edge-tts (Microsoft's free high-quality TTS)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts

import asyncio

# Define all narration segments
narration_segments = {
    "01_TitleCard": """
Welcome to Grade 9 Mathematics, Chapter 1: Whole Numbers.
In this lesson, we'll explore the fundamental concepts of numbers, learn essential calculation techniques, and solve real-world problems involving ratios, rates, and proportions.
Let's begin!
""",

    "02_Section1_Title": """
Section 1: Types of Numbers
""",

    "03_NaturalNumbers": """
Let's start with natural numbers. These are the numbers we use for counting: one, two, three, four, and so on.
Natural numbers have special properties. When you add two natural numbers, you always get another natural number. For example, seven plus nine equals sixteen.
The same is true for multiplication. Six times eight equals forty-eight, which is also a natural number.
We say that natural numbers are closed under addition and multiplication.
However, natural numbers are NOT closed under subtraction. If we try to calculate five minus twenty, we can't get a natural number as the answer.
""",

    "04_WholeNumbers": """
Whole numbers are simply natural numbers plus zero.
Notice how zero is highlighted here. It's a very special number!
Zero is called the identity element for addition. When you add zero to any number, the number stays the same. Twenty-four plus zero equals twenty-four. One fifty-seven plus zero equals one fifty-seven.
Adding zero doesn't change the value!
""",

    "05_IntegerNumbers": """
Now let's extend our number system to include integers. Integers are whole numbers PLUS negative numbers.
Look at the number line. Integers extend in both directions, from negative infinity on the left, through zero in the middle, to positive infinity on the right.
Now subtraction always works! Five minus eight equals negative three. One hundred minus one sixty-five equals negative sixty-five.
Integers also give us additive inverses. Twenty plus negative twenty equals zero. One thirty-five plus negative one thirty-five equals zero.
These pairs of numbers that add to zero are called additive inverses of each other.
""",

    "06_RationalNumbers": """
Let's solve a real problem. Five people want to share twelve chocolate bars equally. How much does each person get?
Twelve divided by five doesn't give us a whole number. But we can express the answer as a fraction: twelve-fifths, or as a decimal: two point four.
This is where rational numbers come in. A rational number is any number that can be written as a fraction, one integer divided by another integer.
Three-quarters equals zero point seven five. Twenty-three tenths equals two point three. Both fractions and decimals are rational numbers.
""",

    "07_IrrationalNumbers": """
Here's an interesting question. What number, multiplied by itself, equals two?
One times one equals one, too small.
Two times two equals four, too big.
We can try decimal numbers, but we'll never find an exact fraction that works.
The answer is the square root of two, which is approximately one point four one four two one. But this decimal goes on forever without repeating!
Numbers like this, that cannot be written as fractions, are called irrational numbers.
Other examples include the square root of three, the square root of five, and the famous number pi.
""",

    "08_Section2_Title": """
Section 2: Calculations with Whole Numbers
""",

    "09_EstimatingRounding": """
A shop owner wants to buy chickens at thirty-eight rand each. With ten thousand rand, can he buy two hundred and fifty chickens?
Let's estimate by rounding. Thirty-eight rand rounds to forty rand. Two hundred and fifty times forty equals ten thousand rand exactly!
So yes, he can buy about two hundred and fifty chickens, maybe even a bit more!
Now let's calculate exactly. Ten thousand divided by thirty-eight equals two hundred and sixty-three point one five.
He can buy two hundred and sixty-three chickens!
Estimation gives us a quick answer, and then we can calculate precisely if needed.
""",

    "10_ColumnAddition": """
Let's learn how to add large numbers using columns. We'll calculate thirty-seven fifty-eight plus fifty-four eighty-six.
First, we write the numbers in columns, lining up the place values.
Start with the units column. Eight plus six equals fourteen. Write four in the units place, and carry one to the tens column.
In the tens column, five plus eight plus the carried one equals fourteen. Write four, carry one.
Hundreds: seven plus four plus one equals twelve. Write two, carry one.
Thousands: three plus five plus one equals nine.
The answer is nine thousand, two hundred and forty-four!
""",

    "11_ColumnMultiplication": """
Multiplying large numbers in columns is similar to addition. Let's multiply thirty-four eighty-nine by forty-seven.
First, multiply thirty-four eighty-nine by seven. This gives us twenty-four thousand, four hundred and twenty-three.
Next, multiply thirty-four eighty-nine by forty. This equals one hundred and thirty-nine thousand, five hundred and sixty.
Finally, add these two results together.
The final answer is one hundred and sixty-three thousand, nine hundred and eighty-three!
""",

    "12_LongDivision": """
Long division requires breaking the problem into manageable steps. Let's divide thirteen thousand, two hundred and fifty-four by fifty-six.
First estimate: How many fifty-sixes fit into thirteen thousand two hundred and fifty-four? About two hundred. Two hundred times fifty-six equals eleven thousand, two hundred.
Subtract this from thirteen thousand two hundred and fifty-four. We get two thousand and fifty-four remaining.
Next estimate: Thirty times fifty-six equals one thousand, six hundred and eighty. Subtract this to get three hundred and seventy-four.
Final estimate: Six times fifty-six equals three hundred and thirty-six. We're left with a remainder of thirty-eight.
Add up our estimates: two hundred plus thirty plus six equals two hundred and thirty-six.
So thirteen thousand two hundred and fifty-four divided by fifty-six equals two hundred and thirty-six, with a remainder of thirty-eight.
""",

    "13_Section3_Title": """
Section 3: Multiples and Factors
""",

    "14_LCMExample": """
Let's find the Lowest Common Multiple, or L C M, of six and fifteen.
Multiples of six are: six, twelve, eighteen, twenty-four, thirty, and so on.
Multiples of fifteen are: fifteen, thirty, forty-five, sixty, and so on.
The common multiples are the numbers that appear in both lists: thirty, sixty, ninety.
The smallest common multiple is thirty. Therefore, the L C M of six and fifteen is thirty!
""",

    "15_HCFExample": """
Now let's find the Highest Common Factor, or H C F, of two thousand three hundred and ten, and three thousand five hundred and ten.
First, we break each number into prime factors.
Two thousand three hundred and ten equals two times three times five times seven times eleven.
Three thousand five hundred and ten equals two times three times three times five times thirteen.
The common prime factors are two, three, and five.
Multiply these together: two times three times five equals thirty.
The H C F is thirty!
""",

    "16_Section4_Title": """
Section 4: Ratio, Rate, and Proportion
""",

    "17_ApplePickingRate": """
Moeneba picks apples at a rate of five apples per minute.
This is an example of a rate, a quantity per unit of time.
How many apples will Moeneba pick in fifteen minutes?
Simply multiply: five apples per minute times fifteen minutes equals seventy-five apples!
Rates help us predict quantities over time.
""",

    "18_BiscuitRatio": """
A biscuit recipe uses ingredients in a specific ratio. For every five parts of flour, we need two parts of oatmeal and one part of cocoa powder.
We write this ratio as five to two to one.
If we're using five hundred grams of flour, how much of each ingredient do we need?
The total ratio parts are five plus two plus one, which equals eight parts.
Five hundred grams divided by five parts equals one hundred grams per part.
Oatmeal: two parts times one hundred grams equals two hundred grams.
Cocoa: one part times one hundred grams equals one hundred grams.
Ratios help us scale recipes perfectly!
""",

    "19_SpeedDistanceTime": """
Speed, distance, and time are related by a simple formula.
Speed equals distance divided by time.
Distance equals speed times time.
And time equals distance divided by speed.
Let's solve a problem. A car travels three hundred and sixty kilometers in exactly four hours. What is the speed?
Using our formula: Speed equals distance divided by time. Speed equals three hundred and sixty kilometers divided by four hours.
The speed is ninety kilometers per hour!
""",

    "20_ProportionProblem": """
Let's combine what we've learned about rates and proportions.
Three people pick apples at different rates. Moeneba picks at five apples per minute, Kate at fifteen per minute, and Garth at twelve per minute.
In ten minutes, how many apples will they pick altogether?
Moeneba: five times ten equals fifty apples.
Kate: fifteen times ten equals one hundred and fifty apples.
Garth: twelve times ten equals one hundred and twenty apples.
Total: fifty plus one fifty plus one twenty equals three hundred and twenty apples!
""",

    "21_Chapter1Summary": """
Let's review what we've learned in Chapter 1.
We explored different types of numbers: natural, whole, integers, rational, and irrational.
We mastered calculation techniques including estimation, rounding, column addition, multiplication, and long division.
We learned about multiples and factors, including how to find the lowest common multiple and highest common factor.
And we solved real-world problems using ratios, rates, and proportions.
These fundamental skills will serve you well throughout your mathematics journey!
""",

    "22_EndCard": """
Congratulations! You've completed Chapter 1: Whole Numbers!
You've developed essential number sense, learned powerful estimation techniques, mastered calculation methods, and solved real-world problems.
Keep practicing these skills, and get ready for Chapter 2: Integers!
Great work!
"""
}


async def generate_audio(text, output_file, voice="en-US-AriaNeural"):
    """Generate audio using Microsoft Edge TTS"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


async def generate_all_audio():
    """Generate audio for all segments"""
    
    # Create output directory
    output_dir = Path("media/audio/chapter1_narration")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("GENERATING TEXT-TO-SPEECH NARRATION")
    print("=" * 70)
    print(f"\nVoice: en-US-AriaNeural (Microsoft Edge TTS)")
    print(f"Output directory: {output_dir}")
    print(f"Total segments: {len(narration_segments)}\n")
    
    successful = 0
    failed = 0
    
    for idx, (filename, text) in enumerate(narration_segments.items(), 1):
        output_file = output_dir / f"{filename}.mp3"
        
        try:
            print(f"[{idx}/{len(narration_segments)}] Generating: {filename}.mp3")
            await generate_audio(text.strip(), str(output_file))
            print(f"  ✓ Saved: {output_file.name}")
            successful += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"Success: {successful}/{len(narration_segments)}")
    print(f"Failed: {failed}")
    print(f"\nAudio files saved in: {output_dir}")
    
    # Create a combined narration file
    print("\n" + "=" * 70)
    print("COMBINING ALL AUDIO FILES")
    print("=" * 70)
    
    # Create file list for FFmpeg
    filelist_path = output_dir / "filelist.txt"
    with open(filelist_path, 'w') as f:
        for filename in narration_segments.keys():
            audio_file = output_dir / f"{filename}.mp3"
            if audio_file.exists():
                # FFmpeg format
                abs_path = audio_file.absolute()
                path_str = str(abs_path).replace('\\', '/')
                f.write(f"file '{path_str}'\n")
    
    combined_output = output_dir / "Chapter1_Complete_Narration.mp3"
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(filelist_path),
        "-c", "copy",
        "-y",
        str(combined_output)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"\n✓ Combined narration created: {combined_output.name}")
        
        if combined_output.exists():
            size_mb = combined_output.stat().st_size / (1024 * 1024)
            print(f"Size: {size_mb:.2f} MB")
        
        # Clean up filelist
        filelist_path.unlink()
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error combining audio: {e}")
    except FileNotFoundError:
        print("✗ FFmpeg not found. Individual audio files are available.")
        print("   Install FFmpeg to combine them automatically.")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Review the generated audio files")
    print("2. Use the combined narration or individual scene files")
    print("3. Run the background music script to add to video")
    print("4. Or use video editing software to sync manually")


# Available voices (uncomment to list all available voices)
async def list_available_voices():
    """List all available TTS voices"""
    voices = await edge_tts.list_voices()
    print("\nAvailable English voices:")
    print("-" * 70)
    for voice in voices:
        if voice["Locale"].startswith("en-"):
            print(f"{voice['ShortName']}: {voice['Locale']} - {voice['Gender']}")
    print("-" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CHAPTER 1 - AUTOMATED TTS GENERATION")
    print("=" * 70)
    print("\nThis script generates high-quality narration using Microsoft Edge TTS")
    print("(Free, no API key required!)\n")
    
    # Uncomment to see all available voices
    # asyncio.run(list_available_voices())
    
    # Generate all audio
    asyncio.run(generate_all_audio())
    
    print("\n✓ TTS Generation Complete!")
    print("\nTo use a different voice, edit the 'voice' parameter in the script.")
    print("Popular voices:")
    print("  - en-US-AriaNeural (Female, clear)")
    print("  - en-US-GuyNeural (Male, professional)")
    print("  - en-GB-SoniaNeural (British Female)")
    print("  - en-AU-NatashaNeural (Australian Female)")
