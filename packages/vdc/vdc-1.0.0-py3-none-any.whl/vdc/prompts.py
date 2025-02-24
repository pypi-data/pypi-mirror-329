class ImagePairQGPrompt:
    """Template for generating image-text pair verification questions"""
    
    @staticmethod
    def format(text: str, num_questions: int) -> str:
        return f"""Based on the following text caption of an image, generate {num_questions} yes/no questions to verify the consistency between the text and an image. The questions should:
1. Cover all key information points from the text.  
2. Be clear and specific.
3. Be answerable by observing an image.
4. Be diverse and not repeat the same information.
5. The expected answer must be "yes" since we assume the text and image are consistent.
6. Use "Q:" and "A:" format. Each line should contain a single question and answer pair.

Text Caption:
{text}

Example output format:
Q: Is there [something mentioned in text] in the image? A: Yes
Q: Does the image contain a [something mentioned in text]? A: Yes

Please only output the Q&A pairs, do not include any other text."""

class ImagePairQAPrompt:
    """Template for image-based question answering"""
    
    @staticmethod
    def format(question: str) -> str:
        return f"""Please carefully observe the image and answer the following question. Your answer should be:
1. Accurate and objective
2. Based only on visible information in the image
3. Concise and direct
4. Preferably a simple yes/no response

Question: {question}

Answer:"""

class VideoPairQGPrompt:
    """Template for video-text pair question generation"""
    # ... Reserved for video-related prompts
    pass

class VideoPairQAPrompt:
    """Template for video-based question answering"""
    # ... Reserved for video-related prompts
    pass 