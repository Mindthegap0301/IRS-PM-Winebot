from flask_seeder import Seeder

from app.models.question import Question
from app.models.weight import Weight
from app.utils.common import is_same_db_data


class WeightSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    # run() will be called by Flask-Seeder
    def run(self):
        new_weights = {
            # Work Style
            "cons_fre": {
                # "style_self_control": {
                #     "weight_value": 0.77
                # },
                "cons_fre": {
                    "weight_value": 1.0
                }
            },
            "role_wine": {
                "role_wine": {
                    "weight_value": 1.0
                },
                # "style_persistence": {
                #     "weight_value": 0.84
                # },
                # "style_initiative": {
                #     "weight_value": 0.79
                # }
            },
            "life_style": {
                # "style_concern_for_others": {
                #     "weight_value": 0.83
                # },
                "life_style": {
                    "weight_value": 1.0
                }
            },
            "wine_taste": {
                "wine_taste": {
                    "weight_value": 1.0
                }
            },
            "reputation": {
                "reputation": {
                    "weight_value": 1.0
                }
            },

            # Work Context
            "per_week": {
                "per_week": {
                    "weight_value": 1.0
                }
            },
            "new_wine": {
                "new_wine": {
                    "weight_value": 1.0
                },
                # "context_outdoors_under_cover": {
                #     "weight_value": 0.85
                # },
                # "context_in_an_enclosed_vehicle_or_equipment": {
                #     "weight_value": 0.83
                # },
                # "context_very_hot_or_cold_temperatures": {
                #     "weight_value": 0.82
                # }
            },
            # "own_wine": {
            #     # "context_spend_time_sitting": {
            #     #     "weight_value": 0.84
            #     # },
            #     # "context_spend_time_standing": {
            #     #     "weight_value": 0.85
            #     # },
            #     "own_wine": {
            #         "weight_value": 1.0
            #     },
            #     # "context_spend_time_bending_or_twisting_the_body": {
            #     #     "weight_value": 0.79
            #     # }
            # },
            "friend_gather": {
                "friend_gather": {
                    "weight_value": 1.0
                }
            },
            "visit_winery": {
                # "context_exposed_to_contaminants": {
                #     "weight_value": 0.8
                # },
                "visit_winery": {
                    "weight_value": 1.0
                },
                # "context_wear_common_protective_or_safety_equipment_such_as_safety_shoes_glasses_gloves_hearing_protection_hard_hats_or_life_jackets": {
                #     "weight_value": 0.79
                # }
            }
        }

        for question in Question.query.filter(Question.code.in_(new_weights.keys())).all():
            current_new_weights = new_weights[question.code]

            for weight in self.db.session.query(Weight).filter(Weight.question_id == question.id, Weight.variable.in_(current_new_weights.keys())).all():
                # Only merge options which already exist in the database
                update_weight = current_new_weights.pop(weight.variable)
                update_weight['id'] = weight.id

                if not is_same_db_data(weight, update_weight):
                    self.db.session.merge(Weight(**update_weight))

            # Only add those options which did not exist in the database
            def map_items(key):
                item = current_new_weights[key]
                item["variable"] = key
                item["question_id"] = question.id
                return Weight(**item)

            current_new_weights_keys = current_new_weights.keys()
            if current_new_weights_keys:
                insert_weights = list(
                    map(map_items, current_new_weights_keys))
                self.db.session.add_all(insert_weights)
                print("Add %s weights" % str(len(insert_weights)))
            self.db.session.commit()
