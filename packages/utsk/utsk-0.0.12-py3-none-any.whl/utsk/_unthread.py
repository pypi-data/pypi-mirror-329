from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from types import TracebackType
from typing import Any, AsyncGenerator, Literal, Optional, Sequence, cast

import httpx

from utsk._schemas import (
    Conversation,
    Customer,
    InboundEmail,
    IssueStatus,
    Message,
    Tag,
    TicketType,
    TicketTypeField,
    User,
    WhereField,
)
from utsk._utils import async_timed_cache

logger = logging.getLogger(__name__)


def _as_uuid(id_or_url: str) -> uuid.UUID:
    return uuid.UUID(id_or_url.split("?")[0].split("/")[-1])


def _exclude_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


class Client:
    def __init__(self, api_key: str | None = None, bearer_token: str | None = None):
        self.api_key = api_key or os.environ["UNTHREAD_API_KEY"]
        if bearer_token:
            self._headers = {"Authorization": f"Bearer {bearer_token}"}
        else:
            self._headers = {"x-api-key": self.api_key}
        self._client = httpx.AsyncClient(
            base_url="https://api.unthread.io/api/",
            timeout=httpx.Timeout(5.0, read=30.0, write=30.0),
        )
        self._channel_id = os.environ.get("SLACK_CHANNEL_ID")

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        __exc_type: Optional[type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        await self._client.aclose()
        return None

    async def get_conversation(self, conversation_id: str) -> Conversation:
        response = await self._client.get(
            f"/conversations/{_as_uuid(conversation_id)}",
            headers=self._headers,
        )
        response.raise_for_status()
        convo = response.json()
        convo["url"] = f'https://langchain.slack.com/archives/{convo["id"]}'
        return convo

    async def get_inbound_email(self, email_id: str) -> InboundEmail:
        response = await self._client.get(
            f"/inbound-emails/{_as_uuid(email_id)}",
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()

    async def get_conversation_id_from_inbound_email(self, email_id: str) -> str | None:
        email = await self.get_inbound_email(email_id)
        try:
            return email["inbound"]["slackMessage"]["ticket"]["id"]
        except (KeyError, TypeError):
            logger.warning(f"Email {email_id} does not have a conversation ID")
            return None

    async def get_user(self, user_id: str) -> User:
        response = await self._client.get(
            f"/users/{user_id}",
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()

    async def list_conversations(
        self,
        where: list[WhereField] | None = None,
    ) -> AsyncGenerator[Conversation, None]:
        cursor = None
        while True:
            response = await self._client.post(
                "/conversations/list",
                headers=self._headers,
                json=_exclude_none({"cursor": cursor, "where": where}),
            )
            response.raise_for_status()
            data = response.json()
            for convo in data["data"]:
                yield convo
            if not data["cursors"]["hasNext"]:
                break
            cursor = data["cursors"]["next"]

    async def list_conversations_by_status(
        self,
        include_status: IssueStatus | Sequence[IssueStatus] | None = None,
        exclude_status: IssueStatus | Sequence[IssueStatus] | None = None,
        where: list[WhereField] | None = None,
    ) -> AsyncGenerator[Conversation, None]:
        """List conversations by status.

        Args:
            include_status (str | Sequence[str] | None): Status or statuses to include.
            exclude_status (str | Sequence[str] | None): Status or statuses to exclude.
            where (list[WhereField] | None): Additional where conditions.
        """
        conditions: list = []
        if include_status:
            include_status = (
                [include_status] if isinstance(include_status, str) else include_status
            )
            conditions.append(
                {"field": "status", "operator": "in", "value": include_status}
            )
        if exclude_status:
            exclude_status = (
                [exclude_status] if isinstance(exclude_status, str) else exclude_status
            )
            conditions.append(
                {"field": "status", "operator": "notIn", "value": exclude_status}
            )
        if where:
            conditions.extend(where)
        async for convo in self.list_conversations(where=conditions):
            yield convo

    async def update_conversation(
        self,
        conversation_id: str,
        *,
        status: str | None = None,
        priority: str | None = None,
        notes: str | None = None,
        wake_up_at: str | None = None,
        assigned_to_user_id: str | None = None,
        ticket_type_id: str | None = None,
        ticket_type_fields: dict[str, Any] | None = None,
        exclude_none: bool = True,
        customer_id: str | None = None,
    ) -> Conversation:
        payload = {
            "status": status,
            "priority": priority,
            "notes": notes,
            "wakeUpAt": wake_up_at,
            "assignedToUserId": assigned_to_user_id,
            "ticketTypeId": (str(_as_uuid(ticket_type_id)) if ticket_type_id else None),
            "ticketTypeFields": ticket_type_fields,
            "customerId": customer_id,
        }
        if exclude_none:
            payload = _exclude_none(payload)
        response = await self._client.patch(
            f"/conversations/{_as_uuid(conversation_id)}",
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()
    
    async def add_collaborator_to_conversation(
        self, 
        conversation_id: str,
        collaborator_type_id: str,
        entity_id: str,
        entity_type: Literal["user", "group", "team"],
    ) -> Conversation:
        payload = {
            "entityId": entity_id,
            "entityType": entity_type,
        }
        response = await self._client.put(
            f"/conversations/{_as_uuid(conversation_id)}/collaborators/{collaborator_type_id}",
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    @async_timed_cache(60 * 60 * 24)
    async def _get_tag_id(self, tag: str) -> str:
        tag_id = None
        try:
            tag_id = str(uuid.UUID(tag))
        except ValueError:
            async for tag_ in self.list_tags(
                where=[{"field": "name", "operator": "==", "value": tag}]
            ):
                tag_id = tag_["id"]
                break
        if not tag_id:
            raise ValueError(f"Tag {tag} not found")
        return tag_id

    async def tag_conversation(
        self,
        conversation_ids: list[str] | str,
        *,
        tag: str,
    ) -> Conversation:
        tag_id = await self._get_tag_id(tag)
        conversations = (
            conversation_ids
            if isinstance(conversation_ids, list)
            else [conversation_ids]
        )
        conversations = [str(_as_uuid(convo)) for convo in conversations]

        response = await self._client.post(
            f"/tags/{tag_id}/conversations/create-links",
            headers=self._headers,
            json=conversations,
        )
        response.raise_for_status()
        return response.json()

    async def create_triage_thread(
        self, conversation_id: str, *, channel_id: str | None = None
    ) -> Message | None:
        channel_id = channel_id or self._channel_id

        response = await self._client.post(
            f"/conversations/{_as_uuid(conversation_id)}/triage",
            headers=self._headers,
            json={"channelId": channel_id},
        )
        response.raise_for_status()
        result = response.json()
        if "message" in result:
            return result["message"]
        return None

    async def assign_ticket_type(
        self,
        conversation_id: str,
        *,
        type_id: str | None = None,
        type_name: str | None = None,
        langsmith_thread_id: str | None = None,
        langsmith_thread_url: str | None = None,
        ai_help_quality: str | None = None,
        ai_help_score: int | None = None,
    ) -> Conversation:
        ticket_type_fields: dict | None = None
        ticket_type = None

        if not type_id:
            if not type_name:
                raise ValueError("Either type_id or type_name is required")
            ticket_type = await self.get_ticket_type(name=type_name)
            type_id = ticket_type["id"]
        if (
            langsmith_thread_id
            or langsmith_thread_url
            or ai_help_quality
            or ai_help_score
        ):
            if not ticket_type:
                ticket_type = await self.get_ticket_type(ticket_type_id=type_id)
            # Assign type_id: value in a dict
            url_field_id = next(
                (
                    field["id"]
                    for field in ticket_type["fields"]
                    if field["label"] == "langsmith_thread_url"
                ),
                None,
            )
            id_field_id = next(
                (
                    field["id"]
                    for field in ticket_type["fields"]
                    if field["label"] == "langsmith_thread_id"
                ),
                None,
            )
            ai_help_quality_field_id = next(
                (
                    field["id"]
                    for field in ticket_type["fields"]
                    if field["label"] == "AI Help Quality"
                ),
                None,
            )
            ai_help_score_field_id = next(
                (
                    field["id"]
                    for field in ticket_type["fields"]
                    if field["label"] == "AI Help Score"
                ),
                None,
            )
            ticket_type_fields = {}
            if langsmith_thread_url and url_field_id:
                ticket_type_fields[url_field_id] = langsmith_thread_url
            if langsmith_thread_id and id_field_id:
                ticket_type_fields[id_field_id] = langsmith_thread_id
            if ai_help_quality and ai_help_quality_field_id:
                ticket_type_fields[ai_help_quality_field_id] = ai_help_quality
            if ai_help_score and ai_help_score_field_id:
                ticket_type_fields[ai_help_score_field_id] = ai_help_score  # type: ignore
        return await self.update_conversation(
            conversation_id,
            ticket_type_id=type_id,
            ticket_type_fields=ticket_type_fields,
        )

    async def untag_conversation(
        self,
        conversation_ids: list[str] | str,
        *,
        tag: str,
    ) -> Conversation:
        tag_id = await self._get_tag_id(tag)
        conversations = (
            conversation_ids
            if isinstance(conversation_ids, list)
            else [conversation_ids]
        )
        conversations = [str(_as_uuid(convo)) for convo in conversations]
        response = await self._client.post(
            f"/tags/{tag_id}/conversations/delete-links",
            headers=self._headers,
            json=conversations,
        )
        response.raise_for_status()
        return response.json()

    async def list_users(
        self,
        where: list[WhereField] | None = None,
    ) -> AsyncGenerator[User, None]:
        cursor = None
        while True:
            response = await self._client.post(
                "/users/list",
                headers=self._headers,
                json=_exclude_none({"cursor": cursor, "where": where}),
            )
            response.raise_for_status()
            data = response.json()
            for user in data["data"]:
                yield user
            if not data["cursors"]["hasNext"]:
                break
            cursor = data["cursors"]["next"]

    async def get_user_by_email(self, email: str) -> User:
        where_fields = [WhereField(field="email", operator="==", value=email)]
        if os.environ.get("ASSIGNEE_SLACK_TEAM_ID"):
            where_fields.append(
                WhereField(
                    field="slackTeamId",
                    operator="==",
                    value=os.environ["ASSIGNEE_SLACK_TEAM_ID"],
                )
            )
        async for user in self.list_users(where=where_fields):
            return user
        raise ValueError(f"User with email {email} not found")

    async def assign_to_user_email(
        self,
        conversation_id: str,
        email: str,
    ) -> Conversation:
        user = await self.get_user_by_email(email)
        return await self.update_conversation(
            conversation_id,
            assigned_to_user_id=user["id"],
        )

    async def list_messages(
        self, conversation_id: str, where: list[WhereField] | None = None
    ) -> AsyncGenerator[Message, None]:
        cursor = None
        while True:
            response = await self._client.post(
                f"/conversations/{_as_uuid(conversation_id)}/messages/list",
                headers=self._headers,
                json=_exclude_none({"cursor": cursor, "where": where}),
            )
            response.raise_for_status()
            messages = response.json()
            for message in messages["data"]:
                yield message
            if not messages["cursors"]["hasNext"]:
                break
            cursor = messages["cursors"]["next"]

    async def list_triage_messages(
        self, conversation_id: str
    ) -> AsyncGenerator[Message, None]:
        # /api/conversations/:conversationId/triage-messages/list
        cursor = None
        while True:
            response = await self._client.post(
                f"/conversations/{_as_uuid(conversation_id)}/triage-messages/list",
                headers=self._headers,
                json=_exclude_none({"cursor": cursor}),
            )
            response.raise_for_status()
            messages = response.json()
            for message in messages["data"]:
                message["isPrivateNote"] = True
                yield message
            if not messages["cursors"]["hasNext"]:
                break
            cursor = messages["cursors"]["next"]

    async def list_all_messages(
        self,
        conversation_id: str,
        *,
        exclude_unthread_bot: bool = True,
    ) -> AsyncGenerator[Message, None]:
        messages = []
        async for message in self.list_messages(conversation_id):
            messages.append(message)
        async for message in self.list_triage_messages(conversation_id):
            messages.append(message)
        messages.sort(key=lambda x: float(x["ts"]))
        for message in messages:
            if not exclude_unthread_bot:
                yield message
                continue
            if message.get("sentByUser"):
                yield message
                continue
            if is_triage_thread_initial_message(message):
                continue
            if message.get("botName") not in ["Unthread", "Unthread Bot"]:
                yield message
                continue

    async def add_follower_to_conversation(
        self, conversation_id: str, *, email: str
    ) -> None:
        convo_id = _as_uuid(conversation_id)
        user = await self.get_user_by_email(email)
        response = await self._client.post(
            f"/conversations/{convo_id}/add-follower",
            headers=self._headers,
            json=_exclude_none(
                {
                    "entityId": user["id"],
                    "entityType": "user",
                }
            ),
        )
        response.raise_for_status()
        response.json()
        return None

    async def list_tags(
        self,
        where: list[WhereField] | None = None,
    ) -> AsyncGenerator[Tag, None]:
        cursor = None
        while True:
            response = await self._client.post(
                "/tags/list",
                headers=self._headers,
                json=_exclude_none({"cursor": cursor, "where": where}),
            )
            response.raise_for_status()
            data = response.json()
            for tag in data["data"]:
                yield tag
            if not data["cursors"]["hasNext"]:
                break
            cursor = data["cursors"]["next"]

    async def get_customer(self, customer_id: str) -> Customer:
        response = await self._client.get(
            f"/customers/{_as_uuid(customer_id)}",
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()

    async def _post_message(
        self,
        *,
        conversation_id: str,
        triage_thread_ts: float | str | None = None,
        markdown: str | None = None,
        blocks: list[dict] | None = None,
        is_private_note: bool,
        is_autoresponse: bool = False,
    ) -> Message:
        if not markdown and not blocks:
            raise ValueError("Either markdown or blocks is required")
        if markdown and blocks:
            raise ValueError("Only one of markdown or blocks is allowed")
        payload = _exclude_none(
            {
                "triageThreadTs": (str(triage_thread_ts) if triage_thread_ts else None),
                "markdown": markdown,
                "blocks": blocks,
                "isPrivateNote": is_private_note,
                "isAutoresponse": is_autoresponse,
            }
        )
        response = await self._client.post(
            f"/conversations/{_as_uuid(conversation_id)}/messages",
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def get_triage_thread_ts(
        self, conversation_id: str, on_missing: Literal["create", "ignore"] = "ignore"
    ) -> tuple[str, str] | None:
        conv = await self.get_conversation(conversation_id)
        triage_dets = get_convo_triage_message_ts(conv)
        if not triage_dets:
            if on_missing == "ignore":
                return None
            if on_missing == "create":
                await self.create_triage_thread(conversation_id)
                conv = await self.get_conversation(conversation_id)
            triage_dets = get_convo_triage_message_ts(conv)
            if not triage_dets:
                return None
        return triage_dets

    async def post_internal_message(
        self,
        *,
        conversation_id: str,
        triage_thread_ts: float | str | None = None,
        markdown: str | None = None,
        blocks: list[dict] | None = None,
        create_triage_thread: bool = False,
        ensure_channel_id: str | None = None,
    ) -> Message:
        if not triage_thread_ts:
            triage_thread_ts, triage_thread_cid = await self.get_triage_thread_ts(
                conversation_id,
                on_missing="create" if create_triage_thread else "ignore",
            )
            if not triage_thread_ts:
                raise ValueError("Failed to get triage thread")
            if ensure_channel_id and triage_thread_cid != ensure_channel_id:
                raise ValueError(
                    "Triage thread channel ID does not match ensure_channel_id"
                )
        if "/unthread send" in str(markdown) + str(blocks):
            raise ValueError(
                'Cannot send internal messages containing "/unthread send" command'
            )
        return await self._post_message(
            conversation_id=conversation_id,
            triage_thread_ts=triage_thread_ts,
            markdown=markdown,
            blocks=blocks,
            is_private_note=True,
        )

    async def post_external_message(
        self,
        *,
        conversation_id: str,
        markdown: str | None = None,
        primary_medium: Literal["email", "slack"] = "email",
        is_autoresponse: bool = False,
    ) -> Message:
        # Strip unthread send command then add back in the response
        markdown = (markdown or "").replace("/unthread send", "").strip()
        if primary_medium == "email":
            markdown = f"{markdown}\n\n/unthread send"
        return await self._post_message(
            conversation_id=conversation_id,
            markdown=markdown,
            is_private_note=False,
            is_autoresponse=is_autoresponse,
        )

    async def get_reporting_time_series(
        self,
        start_date: datetime,
        end_date: datetime,
        metric: Literal[
            "totalCount",
            "responseTimeMean",
            "responseTimeWorkingMean",
            "responseTimeMedian",
            "resolutionTimeMean",
            "resolutionTimeWorkingMean",
            "resolutionTimeMedian",
            "conversationsResolved",
        ],
        date_dimension: Literal["day", "week", "month"] = "day",
        timezone: str = "UTC",
        dimensions: Optional[
            list[Literal["assigneeId", "customerId", "tagId", "sourceType"]]
        ] = None,
        filters: Optional[
            dict[
                Literal["assigneeId", "customerId", "tagId", "sourceType"],
                str | list[str],
            ]
        ] = None,
    ) -> dict:
        payload = _exclude_none(
            {
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d"),
                "metric": metric,
                "dateDimension": date_dimension,
                "timezone": timezone,
                "dimensions": dimensions,
                "filters": filters,
            }
        )
        response = await self._client.post(
            "/reporting/time-series",
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def get_ticket_type(
        self, *, ticket_type_id: str | None = None, name: str | None = None
    ) -> TicketType:
        if ticket_type_id:
            response = await self._client.get(
                f"/ticket-types/{_as_uuid(ticket_type_id)}",
                headers=self._headers,
            )
            response.raise_for_status()
            return response.json()
        if not name:
            raise ValueError("Either ticket_type_id or name is required")
        async for ticket_type in self.list_ticket_types(name=name):
            return ticket_type
        raise ValueError(f"Ticket type {name} not found")

    @async_timed_cache(60 * 60 * 24)
    async def get_ticket_type_id(self, name: str) -> str | None:
        ticket_type = await self.get_ticket_type(name=name)
        return ticket_type["id"] if ticket_type else None

    async def create_ticket_type(
        self, name: str, *, if_exists: Literal["insert", "skip"] = "skip"
    ) -> dict:
        if if_exists == "skip":
            try:
                ticket_type_id = await self.get_ticket_type_id(name)
                if ticket_type_id:
                    return {"id": ticket_type_id, "name": name}
            except ValueError:
                pass
        response = await self._client.post(
            "/ticket-types",
            headers=self._headers,
            json=_exclude_none({"name": name}),
        )
        response.raise_for_status()
        return response.json()

    async def update_ticket_type(
        self,
        ticket_type_id: str,
        *,
        description: str | None = None,
        fields: list[TicketTypeField] | None = None,
    ) -> dict:
        response = await self._client.patch(
            f"/ticket-types/{ticket_type_id}",
            headers=self._headers,
            json=_exclude_none(
                {
                    "description": description,
                    "fields": fields,
                }
            ),
        )
        response.raise_for_status()
        return response.json()

    async def list_ticket_types(
        self, *, name: str | None = None
    ) -> AsyncGenerator[TicketType, None]:
        where_fields = []
        if name:
            where_fields.append({"field": "name", "operator": "==", "value": name})
        cursor = None
        while True:
            response = await self._client.post(
                "/ticket-types/list",
                headers=self._headers,
                json=_exclude_none({"cursor": cursor, "where": where_fields}),
            )
            response.raise_for_status()
            data = response.json()
            for ticket_type in data["data"]:
                yield ticket_type
            if not data["cursors"]["hasNext"]:
                break
            cursor = data["cursors"]["next"]

    async def delete_ticket_type(self, ticket_type_id: str):
        response = await self._client.delete(
            f"/ticket-types/{ticket_type_id}",
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()

    async def update_customer(
        self,
        customer_id: str,
        *,
        name: str | None = None,
        slack_channel_id: str | None = None,
        autoresponder: dict | None = None,
        support_steps: list[dict] | None = None,
        default_triage_channel_id: str | None = None,
        disable_automated_ticketing: bool | None = None,
        primary_support_assignee_id: str | None = None,
        primary_support_assignee_type: str | None = None,
        secondary_support_assignee_id: str | None = None,
        secondary_support_assignee_type: str | None = None,
        reply_timeout_hours: int | None = None,
        bot_handling: dict | None = None,
        email_domains: list[str] | None = None,
        custom_fields: list[dict] | None = None,
    ) -> Customer:
        payload = _exclude_none(
            {
                "name": name,
                "slackChannelId": slack_channel_id,
                "autoresponder": autoresponder,
                "supportSteps": support_steps,
                "defaultTriageChannelId": default_triage_channel_id,
                "disableAutomatedTicketing": disable_automated_ticketing,
                "primarySupportAssigneeId": primary_support_assignee_id,
                "primarySupportAssigneeType": primary_support_assignee_type,
                "secondarySupportAssigneeId": secondary_support_assignee_id,
                "secondarySupportAssigneeType": secondary_support_assignee_type,
                "replyTimeoutHours": reply_timeout_hours,
                "botHandling": bot_handling,
                "emailDomains": email_domains,
                "customFields": custom_fields,
            }
        )
        response = await self._client.patch(
            f"/customers/{_as_uuid(customer_id)}",
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def create_customer(
        self,
        *,
        name: str,
        slack_channel_id: str | None = None,
        email_domains: list[str] | None = None,
    ) -> Customer:
        payload = _exclude_none(
            {
                "name": name,
                "slackChannelId": slack_channel_id,
                "emailDomains": email_domains,
            }
        )
        response = await self._client.post(
            "/customers",
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def delete_customer(self, customer_id: str) -> None:
        response = await self._client.delete(
            f"/customers/{_as_uuid(customer_id)}",
            headers=self._headers,
        )
        response.raise_for_status()

    async def list_customers(
        self,
        where: list[WhereField] | None = None,
    ) -> AsyncGenerator[Customer, None]:
        cursor = None
        while True:
            response = await self._client.post(
                "/customers/list",
                headers=self._headers,
                json=_exclude_none({"cursor": cursor, "where": where}),
            )
            response.raise_for_status()
            data = response.json()
            for customer in data["data"]:
                yield customer
            if not data["cursors"]["hasNext"]:
                break
            cursor = data["cursors"]["next"]


def is_triage_thread_initial_message(m: Message) -> bool:
    if not m.get("triageThread") or not (
        (m.get("triageThread") or {}).get("initialMessage") or {}
    ).get("ts"):
        return False
    return m["ts"] == m["triageThread"]["initialMessage"]["ts"]  # type: ignore


def get_convo_triage_message_ts(conversation: Conversation) -> tuple[str, str] | None:
    if conversation.get("triageMessages"):
        msgs = cast(list[Message], conversation["triageMessages"])
        initial_triage = msgs[0]
        return (initial_triage["ts"], initial_triage["channelId"])
    return None
