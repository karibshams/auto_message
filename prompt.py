class PromptGenerator:
    """
    Generates customized prompts for AI responses based on comment tone and content.
    Ensures replies are empathetic, spiritual, and tone-matched.
    """
    
    def __init__(self):
        self.tone_guidelines = {
            'empathetic': {
                'description': 'Compassionate and acknowledges the emotion behind the comment',
                'style': 'gentle, understanding, validating feelings',
                'focus': 'emotional support and spiritual comfort'
            },
            'biblical': {
                'description': 'Rooted in spiritual truth without being overly formal',
                'style': 'wise, grounded in faith, thoughtful',
                'focus': 'spiritual guidance and biblical wisdom'
            },
            'inviting': {
                'description': 'Leaves space for dialogue and reflection',
                'style': 'open-ended, encouraging conversation',
                'focus': 'fostering connection and continued dialogue'
            },
            'humble': {
                'description': 'Points back to God and comes from a place of grace',
                'style': 'modest, grateful, God-centered',
                'focus': 'deflecting praise to God and expressing gratitude'
            },
            'witty': {
                'description': 'Light, faith-filled humor when appropriate',
                'style': 'gentle humor, joy-filled, lighthearted',
                'focus': 'bringing joy while maintaining spiritual depth'
            }
        }
        
        self.base_instructions = """
        Your response should be:
        - Authentic and personal, not generic or robotic
        - Spiritually grounded but not preachy
        - Compassionate and understanding
        - Humble and gracious
        - 2-3 sentences maximum
        - Written in a conversational, warm tone
        
        Avoid:
        - Sales language or promotional content
        - Being overly formal or religious jargon
        - Dismissing or minimizing feelings
        - Giving unsolicited advice unless clearly requested
        - Generic phrases like "Thank you for sharing"
        """
    
    def create_prompt(self, comment: str, tone: str) -> str:
        """
        Create a customized prompt based on the comment and desired tone.
        
        Args:
            comment: The user's original comment
            tone: The tone to use for the reply ('empathetic', 'biblical', 'inviting', 'humble', 'witty')
            
        Returns:
            str: A complete prompt for the AI to generate an appropriate reply
        """
        if tone not in self.tone_guidelines:
            tone = 'inviting'  # Default fallback
            
        tone_info = self.tone_guidelines[tone]
        
        # Build the specific prompt based on tone
        if tone == 'empathetic':
            tone_specific = f"""
            The user seems to be experiencing difficulty or struggle. Your reply should:
            - Acknowledge their feelings without trying to fix everything
            - Offer gentle spiritual encouragement
            - Show that you understand their situation
            - Be {tone_info['style']}
            """
            
        elif tone == 'biblical':
            tone_specific = f"""
            The user appears to be seeking understanding or has questions. Your reply should:
            - Offer spiritual wisdom or insight
            - Reference spiritual principles naturally (without forcing Bible verses)
            - Be thoughtful and grounded in faith
            - Be {tone_info['style']}
            """
            
        elif tone == 'inviting':
            tone_specific = f"""
            Your reply should encourage continued conversation and reflection. It should:
            - Ask a gentle follow-up question or invite further sharing
            - Be welcoming and open
            - Create space for dialogue
            - Be {tone_info['style']}
            """
            
        elif tone == 'humble':
            tone_specific = f"""
            The user seems positive or grateful. Your reply should:
            - Deflect praise appropriately to God or the community
            - Express gratitude
            - Be modest about any role you might have played
            - Be {tone_info['style']}
            """
            
        elif tone == 'witty':
            tone_specific = f"""
            Your reply should bring some lightness while maintaining spiritual depth. It should:
            - Include gentle, faith-filled humor if appropriate
            - Be joyful and uplifting
            - Maintain respect and sensitivity
            - Be {tone_info['style']}
            """
        
        # Construct the full prompt
        full_prompt = f"""
        A user has left this comment: "{comment}"
        
        {tone_specific}
        
        {self.base_instructions}
        
        Generate a reply that is {tone_info['description']} and focuses on {tone_info['focus']}.
        
        Reply:
        """
        
        return full_prompt.strip()
    
    def get_tone_examples(self, tone: str) -> dict:
        """
        Get example comments and replies for a specific tone.
        
        Args:
            tone: The tone to get examples for
            
        Returns:
            dict: Examples with sample comments and appropriate replies
        """
        examples = {
            'empathetic': {
                'comment': "I'm struggling to believe this applies to me.",
                'reply': "I hear the struggle in your words, and that's so understandable. Sometimes the most profound truths feel the hardest to accept for ourselves. You're not alone in feeling this way. ❤️"
            },
            'biblical': {
                'comment': "I don't understand why this keeps happening to me.",
                'reply': "Those 'why' questions can feel so heavy, can't they? Sometimes our greatest growth comes through seasons we never would have chosen. His plans often unfold in ways we can't see in the moment."
            },
            'inviting': {
                'comment': "This really made me think.",
                'reply': "I love when something sparks that kind of reflection! What part resonated most with you? I'd be curious to hear what thoughts it stirred up."
            },
            'humble': {
                'comment': "Thank you so much for sharing this wisdom!",
                'reply': "You're so kind! Any wisdom here isn't mine - I'm just grateful when something resonates and encourages someone's heart. That's all God's grace at work. 🙏"
            },
            'witty': {
                'comment': "I needed to hear this today!",
                'reply': "Isn't it amazing how the right words show up exactly when we need them? Someone upstairs has pretty good timing! 😊 Hope it brings some light to your day."
            }
        }
        
        return examples.get(tone, {})
    
    def validate_tone(self, tone: str) -> bool:
        """
        Validate if a tone is supported.
        
        Args:
            tone: The tone to validate
            
        Returns:
            bool: True if tone is valid, False otherwise
        """
        return tone in self.tone_guidelines
    
    def get_available_tones(self) -> list:
        """
        Get list of all available tones.
        
        Returns:
            list: List of available tone names
        """
        return list(self.tone_guidelines.keys())
    
    def get_tone_description(self, tone: str) -> str:
        """
        Get description of a specific tone.
        
        Args:
            tone: The tone to describe
            
        Returns:
            str: Description of the tone
        """
        if tone in self.tone_guidelines:
            return self.tone_guidelines[tone]['description']
        return "Tone not found"

# Convenience function for quick prompt generation
def generate_prompt(comment: str, tone: str = 'inviting') -> str:
    """
    Quick function to generate a prompt.
    
    Args:
        comment: User's comment
        tone: Desired tone for reply
        
    Returns:
        str: Generated prompt
    """
    generator = PromptGenerator()
    return generator.create_prompt(comment, tone)

if __name__ == "__main__":
    # Quick test of prompt generation
    generator = PromptGenerator()
    
    test_comment = "I'm having a hard time with forgiveness."
    test_tone = "empathetic"
    
    prompt = generator.create_prompt(test_comment, test_tone)
    print("Generated Prompt:")
    print("=" * 50)
    print(prompt)
    print("=" * 50)
    
    print(f"\nExample for {test_tone} tone:")
    example = generator.get_tone_examples(test_tone)
    if example:
        print(f"Comment: {example['comment']}")
        print(f"Reply: {example['reply']}")