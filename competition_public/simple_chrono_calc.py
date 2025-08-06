"""
Simplified Chronotype Calculator 
This is an educational implementation showing basic chronotype analysis concepts.
For competition transparency while protecting proprietary algorithms.
"""

from datetime import datetime
from typing import Dict, Any

def simple_chronotype_calculation(birth_date: str) -> Dict[str, Any]:
    """
    Basic chronotype calculation for competition demonstration.
    This is a simplified educational version - not the commercial algorithm.
    """
    try:
        # Parse birth date
        if "/" in birth_date:
            dt = datetime.strptime(birth_date, "%d/%m/%Y")
        else:
            dt = datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format"}
    
    # Simple algorithm based on birth month and day (educational purposes)
    month = dt.month
    day = dt.day
    
    # Basic personality mapping (simplified for transparency)
    cognitive_styles = ["Analytical", "Creative", "Practical", "Intuitive"]
    stress_responses = ["High", "Moderate", "Low"]
    energy_patterns = ["Steady", "Variable", "Intense", "Cyclical"]
    
    # Simple modular arithmetic for demonstration
    cognitive_index = (month + day) % len(cognitive_styles)
    stress_index = (day % 3)
    energy_index = ((month * day) % len(energy_patterns))
    
    # Basic element mapping for demonstration (Western astrology)
    elements = ["Air", "Fire", "Earth", "Water"]
    element_index = (month + day) % len(elements)
    
    # Calculate risk periods (simplified)
    current_month = datetime.now().month
    high_risk_months = [(current_month + i) % 12 + 1 for i in [2, 6]]
    recovery_months = [(current_month + i) % 12 + 1 for i in [4, 8]]
    
    return {
        "chrono_signature": f"Simple-{cognitive_styles[cognitive_index][:4]}-{month:02d}",
        "personality_profile": {
            "cognitive_style": cognitive_styles[cognitive_index],
            "stress_response": stress_responses[stress_index],
            "energy_pattern": energy_patterns[energy_index],
            "primary_element": elements[element_index]
        },
        "burnout_timing": {
            "current_risk": stress_responses[stress_index],
            "high_risk_months": high_risk_months,
            "recovery_months": recovery_months
        },
        "note": "This is a simplified educational implementation for competition transparency"
    }

def generate_basic_recommendations(profile: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate basic wellness recommendations based on simple profile.
    Educational version for competition submission.
    """
    cognitive_style = profile.get("cognitive_style", "Practical")
    stress_response = profile.get("stress_response", "Moderate")
    
    # Simple recommendation mapping
    recommendations = {
        "stress_management": f"For {stress_response} stress response: Practice regular breathing exercises and maintain consistent sleep schedule.",
        "energy_optimization": f"As a {cognitive_style} type: Focus on structured planning and regular breaks.",
        "recovery_timing": "Use your recovery months for rest and self-care activities."
    }
    
    return recommendations

# Competition demonstration function
def demo_chronotype_analysis(birth_date: str = "1990-01-15") -> None:
    """
    Demonstration function showing basic chronotype analysis workflow.
    This shows the concept without revealing proprietary algorithms.
    """
    print("=== Simple Chronotype Analysis Demo ===")
    print(f"Analyzing birth date: {birth_date}")
    
    # Basic analysis
    result = simple_chronotype_calculation(birth_date)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"\nChrono-Signature: {result['chrono_signature']}")
    print("\nPersonality Profile:")
    for key, value in result['personality_profile'].items():
        print(f"  {key}: {value}")
    
    print("\nBurnout Timing:")
    print(f"  Current Risk: {result['burnout_timing']['current_risk']}")
    print(f"  High Risk Months: {result['burnout_timing']['high_risk_months']}")
    print(f"  Recovery Months: {result['burnout_timing']['recovery_months']}")
    
    # Generate recommendations
    recommendations = generate_basic_recommendations(result['personality_profile'])
    print("\nBasic Recommendations:")
    for category, advice in recommendations.items():
        print(f"  {category}: {advice}")
    
    print(f"\nNote: {result['note']}")

if __name__ == "__main__":
    # Run demonstration
    demo_chronotype_analysis()
    
    # Test with different date
    print("\n" + "="*50)
    demo_chronotype_analysis("1985-07-22")
