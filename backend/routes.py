from app import app, db
from flask import request, jsonify
from models import Story


# Get all stories
@app.route("/api/stories", methods=["GET"])
def get_stories():
    stories = Story.query.all()
    result = [story.to_json() for story in stories]
    return jsonify(result), 200


# Add a story
@app.route("/api/stories", methods=["POST"])
def add_story():
    try:
        data = request.json

        required_fields = ["name", "story"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"missing field {field}"}), 400

        name = data.get("name")
        story = data.get("story")

        img_url = f"https://avatar.iran.liara.run/public?username={name}"

        new_story = Story(name=name, story=story, img_url=img_url)

        db.session.add(new_story)
        db.session.commit()

        return jsonify({"msg": "story added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Remove a story
@app.route("/api/stories/<int:id>", methods=["DELETE"])
def remove_story(id):
    try:
        story = Story.query.get(id)
        if story is None:
            return jsonify({"error": "story not found"}), 404

        db.session.delete(story)
        db.session.commit()

        return jsonify({"msg": "story deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Update a story
@app.route("/api/stories/<int:id>", methods=["PATCH"])
def update_story(id):
    try:
        story = Story.query.get(id)

        if story is None:
            return jsonify({"error": "story not found"}), 404

        data = request.json

        story.name = data.get("name", story.name)
        story.story = data.get("story", story.story)

        db.session.commit()

        return jsonify(story.to_json()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
