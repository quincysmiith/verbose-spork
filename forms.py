# Forms
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DecimalField,
    SelectField,
    BooleanField,
    DateField,
)
from wtforms.validators import DataRequired

### Forms ###


class WeightEntryForm(FlaskForm):
    date = StringField("Date", validators=[DataRequired()])
    user = SelectField("User", choices=["Marquin", "Caroline"], validate_choice=False)
    weight = DecimalField("Weight (kgs)", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FoodEntryForm(FlaskForm):
    meal_type = SelectField(
        "Meal",
        choices=["Breakfast", "Brunch", "Lunch", "Snack", "Dinner", "Dessert"],
        validate_choice=False,
    )
    consume_date = StringField("Date", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Log Food")
