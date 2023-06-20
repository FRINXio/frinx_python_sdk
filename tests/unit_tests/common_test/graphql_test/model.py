from __future__ import annotations

import typing

from pydantic import Field

from frinx.common.graphql.graphql_types import ENUM
from frinx.common.graphql.graphql_types import Input
from frinx.common.graphql.graphql_types import Interface
from frinx.common.graphql.graphql_types import Mutation
from frinx.common.graphql.graphql_types import Payload
from frinx.common.graphql.graphql_types import Query
from frinx.common.graphql.graphql_types import Subscription

String: typing.TypeAlias = str
Int: typing.TypeAlias = int
Boolean: typing.TypeAlias = bool
ID: typing.TypeAlias = str
Float: typing.TypeAlias = float


class DeviceServiceState(ENUM):
    IN_SERVICE = 'IN_SERVICE'
    OUT_OF_SERVICE = 'OUT_OF_SERVICE'
    PLANNING = 'PLANNING'


class DeviceSize(ENUM):
    LARGE = 'LARGE'
    MEDIUM = 'MEDIUM'
    SMALL = 'SMALL'


class GraphEdgeStatus(ENUM):
    ok = 'ok'
    unknown = 'unknown'


class BaseGraphNode(Interface):
    coordinates: typing.Optional[GraphNodeCoordinates]
    device_type: typing.Optional[Boolean] = Field(alias='deviceType')
    id: typing.Optional[Boolean]
    interfaces: typing.Optional[GraphNodeInterface]
    software_version: typing.Optional[Boolean] = Field(alias='softwareVersion')


class Node(Interface):
    id: typing.Optional[Boolean]


class AddBlueprintInput(Input):
    name: String
    template: String


class AddDeviceInput(Input):
    address: typing.Optional[String]
    blueprint_id: typing.Optional[String] = Field(alias='blueprintId')
    device_size: typing.Optional[DeviceSize] = Field(alias='deviceSize')
    device_type: typing.Optional[String] = Field(alias='deviceType')
    label_ids: typing.Optional[list[String]] = Field(alias='labelIds')
    model: typing.Optional[String]
    mount_parameters: typing.Optional[String] = Field(alias='mountParameters')
    name: String
    password: typing.Optional[String]
    port: typing.Optional[Int]
    service_state: typing.Optional[DeviceServiceState] = Field(alias='serviceState')
    username: typing.Optional[String]
    vendor: typing.Optional[String]
    version: typing.Optional[String]
    zone_id: String = Field(alias='zoneId')


class GraphNodeCoordinatesInput(Input):
    device_name: String = Field(alias='deviceName')
    x: Float
    y: Float


class UpdateBlueprintInput(Input):
    name: typing.Optional[String]
    template: typing.Optional[String]


class AddBlueprintPayload(Payload):
    blueprint: typing.Optional[Blueprint] = Field(response='Blueprint')


class Blueprint(Payload):
    created_at: typing.Optional[Boolean] = Field(response='String', alias='createdAt', default=True)
    id: typing.Optional[Boolean] = Field(response='ID', default=True)
    name: typing.Optional[Boolean] = Field(response='String', default=True)
    template: typing.Optional[Boolean] = Field(response='String', default=True)
    updated_at: typing.Optional[Boolean] = Field(response='String', alias='updatedAt', default=True)


class BlueprintConnection(Payload):
    edges: typing.Optional[BlueprintEdge] = Field(response='BlueprintEdge')
    page_info: typing.Optional[PageInfo] = Field(response='PageInfo', alias='pageInfo')
    total_count: typing.Optional[Boolean] = Field(response='Int', alias='totalCount', default=True)


class BlueprintEdge(Payload):
    cursor: typing.Optional[Boolean] = Field(response='String', default=True)
    node: typing.Optional[Blueprint] = Field(response='Blueprint')


class DeleteBlueprintPayload(Payload):
    blueprint: typing.Optional[Blueprint] = Field(response='Blueprint')


class GraphNodeCoordinates(Payload):
    x: typing.Optional[Boolean] = Field(response='Float', default=True)
    y: typing.Optional[Boolean] = Field(response='Float', default=True)


class AddBlueprintMutation(Mutation):
    _name: str = Field('addBlueprint', const=True)
    input: AddBlueprintInput
    payload: AddBlueprintPayload


class DeleteBlueprintMutation(Mutation):
    _name: str = Field('deleteBlueprint', const=True)
    id: String
    payload: DeleteBlueprintPayload


class UpdateBlueprintMutation(Mutation):
    _name: str = Field('updateBlueprint', const=True)
    id: String
    input: UpdateBlueprintInput
    payload: UpdateBlueprintPayload


class GraphNodeInterface(Payload):
    id: typing.Optional[Boolean] = Field(response='String', default=True)
    name: typing.Optional[Boolean] = Field(response='String', default=True)
    status: typing.Optional[Boolean] = Field(response='GraphEdgeStatus', default=True)


class PageInfo(Payload):
    end_cursor: typing.Optional[Boolean] = Field(response='String', alias='endCursor', default=True)
    has_next_page: typing.Optional[Boolean] = Field(response='Boolean', alias='hasNextPage', default=True)
    has_previous_page: typing.Optional[Boolean] = Field(response='Boolean', alias='hasPreviousPage', default=True)
    start_cursor: typing.Optional[Boolean] = Field(response='String', alias='startCursor', default=True)


class BlueprintsQuery(Query):
    _name: str = Field('blueprints', const=True)
    after: typing.Optional[String]
    before: typing.Optional[String]
    first: typing.Optional[Int]
    last: typing.Optional[Int]
    payload: BlueprintConnection


class UniconfigShellSubscription(Subscription):
    _name: str = Field('uniconfigShell', const=True)
    input: typing.Optional[String]
    session_id: String = Field(alias='sessionId')
    trigger: typing.Optional[Int]
    payload: Boolean


class UpdateBlueprintPayload(Payload):
    blueprint: typing.Optional[Blueprint] = Field(response='Blueprint')


BaseGraphNode.update_forward_refs()
Node.update_forward_refs()
AddBlueprintInput.update_forward_refs()
AddDeviceInput.update_forward_refs()
GraphNodeCoordinatesInput.update_forward_refs()
UpdateBlueprintInput.update_forward_refs()
AddBlueprintPayload.update_forward_refs()
Blueprint.update_forward_refs()
BlueprintConnection.update_forward_refs()
BlueprintEdge.update_forward_refs()
DeleteBlueprintPayload.update_forward_refs()
GraphNodeCoordinates.update_forward_refs()
AddBlueprintMutation.update_forward_refs()
DeleteBlueprintMutation.update_forward_refs()
UpdateBlueprintMutation.update_forward_refs()
GraphNodeInterface.update_forward_refs()
PageInfo.update_forward_refs()
BlueprintsQuery.update_forward_refs()
UniconfigShellSubscription.update_forward_refs()
UpdateBlueprintPayload.update_forward_refs()
