from openai import OpenAI
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from prompt import PromptGenerator

# Load environment variables from .env file
load_dotenv()

class CommentReplyAI:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI comment reply system.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file or pass api_key parameter.")
        
        # Get configuration from environment variables
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '300'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        self.top_p = float(os.getenv('TOP_P', '0.9'))
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        self.prompt_generator = PromptGenerator()
        
    def analyze_comment_sentiment(self, comment: str) -> str:
        """
        Analyze the sentiment of a comment to determine appropriate tone.
        
        Args:
            comment: The user's comment text
            
        Returns:
            str: Detected sentiment ('positive', 'negative', 'neutral', 'struggling', 'questioning')
        """
        comment_lower = comment.lower()
        
        # Struggling/difficult emotions
        struggling_keywords = ['struggle', 'struggling', 'hard', 'difficult', 'doubt', 'doubting', 
                              'lost', 'confused', 'hurt', 'pain', 'afraid', 'scared', 'worried']
        
        # Positive/grateful emotions
        positive_keywords = ['thank', 'grateful', 'amazing', 'blessed', 'love', 'wonderful', 
                            'beautiful', 'inspiring', 'helped', 'encouraging']
        
        # Questioning/seeking
        questioning_keywords = ['why', 'how', 'what', 'when', 'where', 'understand', 'explain', 
                               'confused', 'unclear', 'question']
        
        if any(keyword in comment_lower for keyword in struggling_keywords):
            return 'struggling'
        elif any(keyword in comment_lower for keyword in positive_keywords):
            return 'positive'
        elif any(keyword in comment_lower for keyword in questioning_keywords):
            return 'questioning'
        else:
            return 'neutral'
    
    def determine_tone(self, sentiment: str) -> str:
        """
        Determine the appropriate tone based on comment sentiment.
        
        Args:
            sentiment: The detected sentiment from analyze_comment_sentiment
            
        Returns:
            str: The appropriate tone to use for the reply
        """
        tone_mapping = {
            'struggling': 'empathetic',
            'positive': 'humble',
            'questioning': 'biblical',
            'neutral': 'inviting'
        }
        return tone_mapping.get(sentiment, 'inviting')
    
    def generate_reply(self, comment: str, custom_tone: Optional[str] = None, 
                      model: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate an AI reply to a user comment.
        
        Args:
            comment: The user's comment to reply to
            custom_tone: Optional custom tone override
            model: Optional model override (uses .env OPENAI_MODEL if not specified)
            
        Returns:
            Dict containing the reply, tone used, and sentiment detected
        """
        try:
            # Use model from .env if not specified
            model = model or self.model
            
            # Analyze sentiment and determine tone
            sentiment = self.analyze_comment_sentiment(comment)
            tone = custom_tone or self.determine_tone(sentiment)
            
            # Generate appropriate prompt
            prompt = self.prompt_generator.create_prompt(comment, tone)
            
            # Call OpenAI API with configuration from .env
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a compassionate spiritual guide who responds to comments with empathy, wisdom, and grace. Your responses should be authentic, humble, and grounded in spiritual truth."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
            
            ai_reply = response.choices[0].message.content.strip()
            
            return {
                'reply': ai_reply,
                'tone_used': tone,
                'sentiment_detected': sentiment,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            return {
                'reply': None,
                'tone_used': tone if 'tone' in locals() else None,
                'sentiment_detected': sentiment if 'sentiment' in locals() else None,
                'success': False,
                'error': str(e)
            }
    
    def batch_generate_replies(self, comments: list, custom_tones: Optional[Dict[int, str]] = None) -> list:
        """
        Generate replies for multiple comments at once.
        
        Args:
            comments: List of comment strings
            custom_tones: Optional dictionary mapping comment index to custom tone
            
        Returns:
            List of reply dictionaries
        """
        results = []
        custom_tones = custom_tones or {}
        
        for i, comment in enumerate(comments):
            custom_tone = custom_tones.get(i)
            result = self.generate_reply(comment, custom_tone)
            results.append(result)
            
        return results

# Convenience function for backend integration
def generate_comment_reply(comment: str, api_key: Optional[str] = None, 
                          tone: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to generate a single reply.
    
    Args:
        comment: The user's comment
        api_key: OpenAI API key
        tone: Optional custom tone
        
    Returns:
        Dictionary with reply and metadata
    """
    ai_system = CommentReplyAI(api_key)
    return ai_system.generate_reply(comment, tone)