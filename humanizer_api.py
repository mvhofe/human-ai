from flask import Blueprint, request, jsonify
from src.humanizer_logic.humanizer import TextHumanizer

humanizer_bp = Blueprint("humanizer_bp", __name__)

@humanizer_bp.route("/api/humanize", methods=["POST"])
def handle_humanize_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    input_text = data["text"]
    # Default to 'academic' style as per user's primary requirement for ESMT thesis
    style = data.get("style", "academic").lower()
    # Validate style parameter
    if style not in ["default", "academic"]:
        return jsonify({"error": "Invalid 'style' parameter. Must be 'default' or 'academic'."}), 400
        
    lexical_sub_rate = float(data.get("lexical_sub_rate", 0.1 if style == "academic" else 0.15))
    # Contractions are managed by the style parameter within the transformer now
    # apply_contractions = bool(data.get("apply_contractions", style != "academic")) 

    if not input_text.strip():
        return jsonify({"humanized_text": "", "analysis": {}, "message": "Input text was empty."}), 200

    try:
        tool = TextHumanizer()
        humanized_text, analysis_results = tool.humanize_text(
            raw_text=input_text,
            lexical_sub_rate=lexical_sub_rate,
            style=style # Pass the style to the humanizer
        )
        return jsonify({
            "humanized_text": humanized_text,
            "original_analysis": analysis_results,
            "style_applied": style
        }), 200
    except Exception as e:
        print(f"Error during humanization: {str(e)}") 
        return jsonify({"error": "An error occurred during text humanization.", "details": str(e)}), 500

