from flask_seeder import Seeder
from app.models.question import Question
from app.models.option import Option
from app.utils.common import is_same_db_data

level_options = {
    "1": {
        "order": 10,
        "value": "1",
        "data_type": "number",
        "label": "None"
    },
    "2": {
        "order": 20,
        "value": "2",
        "data_type": "number",
        "label": "Low"
    },
    "3": {
        "order": 30,
        "value": "3",
        "data_type": "number",
        "label": "Average"
    },
    "4": {
        "order": 40,
        "value": "4",
        "data_type": "number",
        "label": "High"
    },
    "5": {
        "order": 50,
        "value": "5",
        "data_type": "number",
        "label": "Extremely high"
    }
}

importance_options = {
    "1": {
        "order": 10,
        "value": "1",
        "data_type": "number",
        "label": "Not at all"
    },
    "2": {
        "order": 20,
        "value": "2",
        "data_type": "number",
        "label": "Somewhat important"
    },
    "3": {
        "order": 30,
        "value": "3",
        "data_type": "number",
        "label": "Important"
    },
    "4": {
        "order": 40,
        "value": "4",
        "data_type": "number",
        "label": "Very important"
    },
    "5": {
        "order": 50,
        "value": "5",
        "data_type": "number",
        "label": "Extremely important"
    }
}

frequency_options = {
    "1": {
        "order": 10,
        "value": "1",
        "data_type": "number",
        "label": "Never"
    },
    "2": {
        "order": 20,
        "value": "2",
        "data_type": "number",
        "label": "A few times every <b>year</b>"
    },
    "3": {
        "order": 30,
        "value": "3",
        "data_type": "number",
        "label": "A few times every <b>month</b>"
    },
    "4": {
        "order": 40,
        "value": "4",
        "data_type": "number",
        "label": "A few times every <b>week</b>"
    },
    "5": {
        "order": 50,
        "value": "5",
        "data_type": "number",
        "label": "Every time"
    }
}


class OptionSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    # run() will be called by Flask-Seeder
    def run(self):
        new_options = {
            # Work Style
            "cons_fre": level_options, "role_wine": importance_options, "life_style": importance_options, "wine_taste": importance_options, "reputation": importance_options,

            # Work Context
            "per_week": {
                "1": {
                    "order": 10,
                    "value": "1",
                    "data_type": "number",
                    "label": "Less than 3 times"
                },
                "2": {
                    "order": 20,
                    "value": "2",
                    "data_type": "number",
                    "label": "4 to 6 times"
                },
                "3": {
                    "order": 30,
                    "value": "3",
                    "data_type": "number",
                    "label": "More than 7 times"
                }
            }, "new_wine": frequency_options, "friend_gather": frequency_options, "visit_winery": frequency_options,
            # "own_wine": frequency_options,
            # Education
            "fav_grape": {
                "2": {
                    "order": 10,
                    "value": "2",
                    "data_type": "number",
                    "label": "Cabernet Sauvignon"
                },
                "6": {
                    "order": 20,
                    "value": "6",
                    "data_type": "number",
                    "label": "Merlot"
                },
                "8": {
                    "order": 30,
                    "value": "8",
                    "data_type": "number",
                    "label": "Pinot Noir"
                },
                "11": {
                    "order": 40,
                    "value": "11",
                    "data_type": "number",
                    "label": "None in particular or not listed above"
                }
            },

            # Priority
            "priority": {
                "wine_flav": {
                    "order": 10,
                    "value": "wine_flav",
                    "data_type": "string",
                    "label": "drinking habits"
                },
                "pre_region": {
                    "order": 20,
                    "value": "pre_region",
                    "data_type": "string",
                    "label": "taste"
                }
            }
        }

        for question in Question.query.filter(Question.code.in_(new_options.keys())).all():
            current_new_options = new_options[question.code] if question.code in new_options else None

            if current_new_options:
                for option in self.db.session.query(Option).filter(Option.question_id == question.id, Option.value.in_(current_new_options.keys())).all():
                    # Only merge options which already exist in the database
                    update_option = current_new_options.pop(option.value)
                    update_option['id'] = option.id

                    if not is_same_db_data(option, update_option):
                        self.db.session.merge(Option(**update_option))

                # Only add those options which did not exist in the database
                def map_items(key):
                    item = current_new_options[key]
                    item["question_id"] = question.id
                    return Option(**item)

                current_new_options_keys = current_new_options.keys()
                if current_new_options_keys:
                    insert_options = list(
                        map(map_items, current_new_options_keys))
                    self.db.session.add_all(insert_options)
                    print("Add %s options" % str(len(insert_options)))
            self.db.session.commit()
