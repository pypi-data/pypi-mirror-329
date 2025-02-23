import json
from pathlib import Path
from typing import List

from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.matchers.matcher import Matcher
from helix_personmatching.models.rules.RuleWeight import RuleWeight
from helix_personmatching.models.scoring_option import ScoringOption


def test_match_unknown_gender() -> None:
    print("")
    data_dir: Path = Path(__file__).parent.joinpath("./person_data")

    with open(data_dir.joinpath("client_person.json")) as file:
        client_person_json = file.read()

    with open(data_dir.joinpath("person.json")) as file:
        person_json = file.read()

    matcher = Matcher()

    scores: List[MatchScore] = matcher.match(
        source_json=client_person_json,
        target_json=person_json,
        verbose=True,
        # only_matches=True,
        options=[
            # a fixed high boost to simulate the current existing customization
            #  done in the PROA pipeline
            ScoringOption(
                rule_name="Rule-050",
                weight=RuleWeight(
                    exact_match=0.0,
                    partial_match=0.0,
                    missing=0.0,
                    boost=0.051,
                ),
            ),
        ],
    )

    assert len(scores) == 1
    score = scores[0]
    scores_json = score.to_json(include_rule_scores=True)
    print(f"scores_json: {scores_json}")

    print(f"score.matched: {score.matched}")
    assert score.matched is True

    with open(data_dir.joinpath("expected_scores.json")) as file:
        expected_scores = json.loads(file.read())

    assert json.loads(scores_json) == expected_scores
