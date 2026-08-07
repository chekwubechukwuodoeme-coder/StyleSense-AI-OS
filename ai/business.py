from ai.model import ask_gemini


def business_agent(idea):

    prompt = f"""
You are a world-class Fashion Business Consultant.

Your ONLY responsibility is business strategy.

Fashion Business Idea:

{idea}

Return Markdown.

# Executive Summary
# Business Model
# Brand Positioning
# Mission
# Vision
# Target Audience
# Customer Persona
# Unique Selling Proposition (USP)
# Competitor Analysis
# Revenue Streams
# Pricing Strategy
# Sales Channels
# Growth Strategy
# Potential Risks
# Business Recommendations

Do NOT generate clothing designs.
Do NOT generate marketing campaigns.
Do NOT recommend fabrics.

Focus ONLY on business.
"""

    return ask_gemini(prompt)


def fashion_cofounder(idea):

    prompt = f"""
You are the world's greatest Fashion Business Consultant.

A user wants to launch this fashion business:

{idea}

Create a complete business blueprint.

Return Markdown.

Include:

# Brand Name
Generate 10 premium names.

# Brand Story

# Mission

# Vision

# Target Audience

# Customer Persona

# Competitor Analysis

# Unique Selling Proposition

# First Collection
Create 10 clothing ideas.

# Recommended Fabrics

# Manufacturing Plan

# Estimated Startup Cost

# Pricing Strategy

# Marketing Strategy

# Social Media Strategy

# Website Plan

# AI Growth Strategy

# 12 Month Roadmap

# Risks

# Success Tips
"""

    return ask_gemini(prompt)