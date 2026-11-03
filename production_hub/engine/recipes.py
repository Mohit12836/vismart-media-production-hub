"""Production recipes describe real render paths, not promises of virality."""
RECIPES = {
    "kinetic": {"name": "Kinetic captions", "kind": "native", "layout": "kinetic", "formats": ["reel", "story"], "cost": "local", "needs": "Script, one scene per line"},
    "listicle": {"name": "Tips / listicle", "kind": "native", "layout": "listicle", "formats": ["reel", "story", "long"], "cost": "local", "needs": "Original tips, one scene per line"},
    "quiz": {"name": "Question + reveal", "kind": "native", "layout": "quiz", "formats": ["reel", "story"], "cost": "local", "needs": "Question, clues, answer on final line"},
    "storytelling": {"name": "Narrated storytelling", "kind": "native", "layout": "story", "formats": ["reel", "story", "long"], "cost": "local + chosen voice", "needs": "Story beats; optional voice"},
    "photo_story": {"name": "Photo motion story", "kind": "assets", "layout": "photo", "formats": ["reel", "story", "long"], "cost": "local + supplied images", "needs": "Local image assets and story beats"},
    "canva_template": {"name": "Canva template video", "kind": "external", "formats": ["reel", "story", "long"], "cost": "depends on Canva plan/assets", "needs": "Exported MP4; Canva connection alone is not VPS authorization"},
    "flow_cinematic": {"name": "Flow cinematic", "kind": "external", "formats": ["reel", "story", "long"], "cost": "provider credits", "needs": "Edited MP4 from Flow workflow"},
    "screen_demo": {"name": "Screen / app demo", "kind": "external", "formats": ["reel", "story", "long"], "cost": "local + supplied recording", "needs": "Edited MP4 screen recording"},
    "directed_motion": {"name": "Directed motion ad", "kind": "native", "layout": "directed", "formats": ["reel", "story"], "cost": "local + chosen voice", "needs": "Creative plan JSON: visual hook, scene direction, payoff; exact voice timing"},
    "chat_story": {"name": "Directed chat story", "kind": "native", "layout": "directed", "formats": ["reel", "story"], "cost": "local + chosen voice", "needs": "Creative plan JSON with conversation beats and a truthful/fiction-labelled payoff"},
    "choice_quiz": {"name": "A/B choice + reveal", "kind": "native", "layout": "directed", "formats": ["reel", "story"], "cost": "local + chosen voice", "needs": "Creative plan JSON with two options, correct answer and explanation"},
}
