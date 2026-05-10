from flask import abort, render_template

from sixdegrees.app.blueprints.person import bp
from sixdegrees.app.blueprints.person.queries import get_person


@bp.get("/<person_id>")
def detail(person_id: str):
    person = get_person(person_id)
    if person is None:
        abort(404)
    return render_template("person/detail.html", person=person)
