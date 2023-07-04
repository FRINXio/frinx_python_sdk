import json

from model import AddBlueprintInput
from model import AddBlueprintMutation
from model import AddBlueprintPayload
from model import Blueprint
from model import BlueprintConnection
from model import BlueprintEdge
from model import BlueprintsQuery

from frinx.common.graphql.schema_converter import GraphqlJsonParser


class TestTaskGenerator:
    def test_render_json(self) -> None:
        reference_file = 'tests/unit_tests/common_test/graphql_test/model.py'
        json_schema = 'tests/unit_tests/common_test/graphql_test/schema.json'
        reference = open(reference_file).read()
        schema = json.loads(open(json_schema).read())
        converted = GraphqlJsonParser(input_json=schema).render()
        assert reference == converted

    def test_render_query(self) -> None:
        reference = '{ blueprints { edges { cursor node { createdAt name template updatedAt } } totalCount } }'
        query = BlueprintsQuery(
            payload=BlueprintConnection(
                edges=BlueprintEdge(
                    node=Blueprint(
                        name=True,
                        id=False
                    )
                )
            )
        ).render()
        assert reference == query

    def test_render_mutation(self) -> None:
        bp_inputs = 'name: "IOS", template: "{ "cli": { "cli-topology:host": "sample-topology" } }"'
        bp_payload = 'blueprint { createdAt name template updatedAt }'
        reference = f'mutation {{ addBlueprint ( input: {{ {bp_inputs} }}) {{ { bp_payload } }} }}'
        mutation = AddBlueprintMutation(
            input=AddBlueprintInput(
                name='IOS',
                template='{ "cli": { "cli-topology:host": "sample-topology" } }'
            ),
            payload=AddBlueprintPayload(
                blueprint=Blueprint(
                    createdAt=True,
                    id=False,
                    name=True,
                    template=True,
                    updatedAt=True
                )
            )
        ).render()
        assert reference == mutation
