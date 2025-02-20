import argparse
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS

def makeWordCloud(textPath: str, pngPath: str, outputPath: str, stopwordsPath: str):
    """Makes a wordcloud from a text file in the shape of the 
    non-transparent pixels of the PNG at pngPath and saves it to outputPath.
    
    Additionally, it reads custom stopwords from stopwordsPath and adds them
    to the default STOPWORDS.
    """
    # Read the text file.
    with open(textPath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Load the image as a numpy array.
    mask = np.array(Image.open(pngPath))
    
    # If the PNG has an alpha channel, ignore it by taking only the first three channels (RGB)
    if mask.ndim == 3 and mask.shape[2] == 4:
        mask = mask[:, :, :3]

    # Load custom stopwords from the provided file.
    custom_stopwords = set()
    with open(stopwordsPath, 'r', encoding='utf-8') as sw_file:
        for line in sw_file:
            # Strip each line to remove any extra whitespace or newline characters
            word = line.strip()
            if word:
                custom_stopwords.add(word)
    
    # Combine default STOPWORDS with custom stopwords.
    stopwords = set(STOPWORDS).union(custom_stopwords)
    
    # Create the word cloud object.
    wc = WordCloud(background_color="black",
                   mask=mask,
                   stopwords=stopwords,
                   contour_width=3,
                   contour_color='steelblue',
                   max_font_size=100,
                   min_font_size=5,
                   max_words=1000,
                   scale=10)
    
    # Generate the word cloud from text.
    wc.generate(text)
    
    # Save the word cloud image to the output file.
    wc.to_file(outputPath)
    print(f"Word cloud saved to {outputPath}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("textPath", help="Path to the input text file")
    parser.add_argument("pngPath", help="Path to the input PNG file to be used as mask")
    parser.add_argument("outputPath", help="Path to save the output word cloud image")
    parser.add_argument("--stopwords", help="Path to a file of stopwords to exclude from the word cloud (one per line)")
    args = parser.parse_args()

    makeWordCloud(args.textPath, args.pngPath, args.outputPath, args.stopwords)
