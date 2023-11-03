from flask_seeder import Seeder, generator
from sqlalchemy import delete
from app.models.question import Question
from app.utils.common import is_same_db_data


class QuestionSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    # run() will be called by Flask-Seeder
    def run(self):
        new_questions = {
            "cons_fre": {
                "order": 10,
                "group": "style",
                "code": "cons_fre",
                "text": "How would you describe your <b>alcohol consumption frequency</b>?",
            },
            "role_wine": {
                "order": 20,
                "group": "style",
                "code": "role_wine",
                "text": "How significant is the <b>role of alcohol consumption<b> in your cultural or social traditions and rituals?",
            },
            "life_style": {
                "order": 30,
                "group": "style",
                "code": "life_style",
                "text": "To what degree does your passion for alcohol beverage influence your <b>lifestyle and daily choices<b>?",
            },
            "wine_taste": {
                "order": 40,
                "group": "style",
                "code": "wine_taste",
                "text": "How crucial is the element of <b>wine tasting and exploration<b> for you?",
            },
            "reputation": {
                "order": 50,
                "group": "style",
                "code": "reputation",
                "text": "How much does the <b>reputation of the brand, winery or vineyard<b> influence your choices?",
            },
            "per_week": {
                "order": 60,
                "group": "context",
                "code": "per_week",
                "text": "How often do you drink alcohol beverage on average <b>per week<b>?",
            },
            "new_wine": {
                "order": 70,
                "group": "context",
                "code": "new_wine",
                "text": "How often are you willing to try a <b>new type of wine/alcohol beverage<b>?",
            },
            "friend_gather": {
                "order": 90,
                "group": "context",
                "code": "friend_gather",
                "text": "What is your typical frequency of drinking at <b>friend gatherings<b>?",
            },
            "visit_winery": {
                "order": 100,
                "group": "context",
                "code": "visit_winery",
                "text": "How often do you <b>visit a winery<b>?",
            },
            # "own_wine": {
            #     "order": 80,
            #     "group": "context",
            #     "code": "own_wine",
            #     "text": 'How often do you typically drink red wine on your own?'
            # },
            "highest_price": {
                "order": 110,
                "group": "salary",
                "code": "highest_price",
                "text": "What is the <b>highest price<b> for wine/alcohol beverage that you are willing to accept?",
                "min_response_length": 1,
            },
            "price_ideal": {
                "order": 120,
                "group": "salary",
                "code": "price_ideal",
                "text": "What is the <b>ideal price<b> for wine/alcohol beverage that you find acceptable?",
                "min_response_length": 1,
            },
            "fav_grape": {
                "order": 200,
                "group": "education",
                "code": "education_level",
                "text": "Do you have any favorite <b> varieties<b>?",
            },
            "fav_meth": {
                "order": 210,
                "group": "education",
                "code": "fav_meth",
                "text": "What‘s your favorite wine production method?",
                "min_response_length": 1,
            },
            # Open-ended
            "general": {
                "order": 1,
                "group": "description",
                "code": "general",
                "text": "Please give us a general description about the wine/alcohol beverage you‘d like to have.",
                "min_response_length": 10,
            },
            "flavour": {
                "order": 2,
                "group": "experience",
                "code": "flavour",
                "text": "Please describe the flavors you enjoy in wine/alcohol beverage, such as fruity.",
                "min_response_length": 10,
            },
            "brand": {
                "order": 3,
                "group": "variety",
                "code": "brand",
                "text": "Do you have a preferred brand, winery or region?",
                "min_response_length": 10,
            },
            "pairing": {
                "order": 4,
                "group": "pairing",
                "code": "pairing",
                "text": "What kind of food do you usually pair with wine/alcohol beverage?",
                "min_response_length": 10,
            },
            # Priority
            "priority": {
                "order": 400,
                "group": "priority",
                "code": "priority",
                "text": "Do you prefer us to recommend wines/alcohol beverage that align with which of the following priorities?",
            },
        }

        original_new_questions = new_questions.copy()

        for each in Question.query.filter(
            Question.code.in_(new_questions.keys())
        ).all():
            # Only merge those posts which already exist in the database
            update_question = new_questions.pop(each.code)
            update_question["id"] = each.id

            if not is_same_db_data(each, update_question):
                self.db.session.merge(Question(**update_question))
                print(f"Update question: {update_question['code']}")

        # Only add those posts which did not exist in the database
        new_questions_values = new_questions.values()

        if new_questions_values:
            insert_questions = list(
                map(lambda item: Question(**item), new_questions_values)
            )
            self.db.session.add_all(insert_questions)
            print("Add %s questions" % str(len(new_questions_values)))

        # Now we commit our modifications (merges) and inserts (adds) to the database!
        self.db.session.commit()

        # Purge non-existent items
        data_codes = original_new_questions.keys()
        delete_statement = delete(Question).where(Question.code.not_in(data_codes))
        self.db.session.execute(delete_statement)

        self.db.session.commit()
