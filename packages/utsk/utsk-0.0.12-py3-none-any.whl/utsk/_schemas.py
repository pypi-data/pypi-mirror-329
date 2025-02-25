from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from typing_extensions import TypedDict


class WhereField(TypedDict):
    field: str
    operator: Literal[
        "==",
        "!=",
        ">",
        "<",
        "in",
        "notIn",
        "contains",
        "notContains",
        "like",
    ]
    value: str | int | list[str]


class BaseMessage(TypedDict, total=False):
    ts: str
    threadTs: Optional[str]
    userId: str
    userTeamId: str
    botId: Optional[str]
    botName: Optional[str]
    teamId: str
    text: str
    subtype: Optional[str]
    conversationId: str
    timestamp: str
    user: Optional[User]
    metadata: Optional[dict]

    # All these fields depend on the message type
    channelId: Optional[str]
    parentId: Optional[str]
    botUsername: Optional[str]
    botImage: Optional[str]
    deletedAt: Optional[str]
    updatedAt: Optional[str]
    sourceType: Optional[
        Union[
            Literal[
                "slack",
                "email",
            ],
            str,
        ]
    ]
    files: Optional[List[dict]]
    emailId: Optional[str]
    widgetMessageId: Optional[str]
    microsoftTeamsMessageId: Optional[str]
    blocks: Optional[List[dict]]
    reactions: Optional[List[dict]]
    isPrivateNote: Optional[bool]
    id: Optional[str]
    slackChannel: Optional[dict]
    sentByUser: Optional[User]
    submittedByUser: Optional[User]
    resolvedContent: Optional[List]
    triageThread: Optional[dict]


class Message(BaseMessage):
    conversation: Optional[Conversation]


class Tag(TypedDict, total=False):
    id: str
    name: str


class User(TypedDict, total=False):
    id: str
    name: str
    email: str
    slackId: str
    photo: str
    phoneNumber: str
    createdAt: str
    status: str
    deleted: bool
    backupUserId: str
    awayUntil: str
    slackTeamId: str
    updatedAt: str
    title: str
    pronoun: str
    department: str
    slackTeam: dict


class UserTeam(TypedDict, total=False):
    id: str
    name: str
    slackId: str


class SlackChannel(TypedDict, total=False):
    id: str
    name: str
    isShared: bool
    isPrivate: bool


class AutoresponderOptions(TypedDict, total=False):
    enabled: bool
    condition: Literal["always", "outside-working-hours"] | str
    message: str


class SupportStep(TypedDict, total=False):
    type: Literal["assignment", "escalation", "reminder", "triage"]
    assigneeId: Optional[str]
    assigneeType: Optional[Literal["user", "team"]]
    minutes: int
    shouldCycleThroughTeamMembers: Optional[bool]
    maxCycles: Optional[int]
    cycleMinutes: Optional[int]


class Customer(TypedDict, total=False):
    name: str
    primarySupportAssigneeId: Optional[str]
    primarySupportAssigneeType: Optional[Literal["user", "team"]]
    secondarySupportAssigneeId: Optional[str]
    secondarySupportAssigneeType: Optional[Literal["user", "team"]]
    replyTimeoutMinutes: Optional[int]
    defaultTriageChannelId: Optional[str]
    disableAutomatedTicketing: Optional[bool]
    botHandling: Optional[Literal["off", "all"]]
    autoresponder: Optional[AutoresponderOptions]
    supportSteps: Optional[List[SupportStep]]
    slackTeamId: Optional[str]
    assignToTaggedUserEnabled: Optional[bool]
    slackChannelId: Optional[str]
    createdAt: str
    updatedAt: str
    tags: List[Tag]
    slackChannel: Optional[SlackChannel]


IssueStatus = Literal["open", "in_progress", "on_hold", "closed"]


class Conversation(TypedDict, total=False):
    id: str
    status: IssueStatus
    customerId: Optional[str]
    channelId: str
    wasManuallyCreated: bool
    friendlyId: int
    createdAt: str
    updatedAt: str
    closedAt: Optional[str]
    statusUpdatedAt: Optional[str]
    responseTime: Optional[int]
    responseTimeWorking: Optional[int]
    resolutionTime: Optional[int]
    resolutionTimeWorking: Optional[int]
    title: Optional[str]
    priority: Optional[str]
    initialMessage: BaseMessage
    latestMessage: Optional[BaseMessage]
    triageMessages: List[BaseMessage] | None
    assignedToUserId: Optional[User]
    tags: List[Tag]
    customer: Optional[Customer]
    wakeUpAt: Optional[str]
    summary: Optional[str]
    url: Optional[str]


class TicketTypeField(TypedDict, total=False):
    label: str
    description: str | None
    type: Literal[
        "short-answer",
        "long-answer",
        "checkbox",
        "single-select",
        "multi-select",
        "user-select",
    ]
    required: bool
    public: bool
    options: list[str] | None
    conditionals: dict[str, list[str]] | None
    id: str | None


class TicketType(TypedDict, total=False):
    label: str
    description: Optional[str]
    createdAt: str
    updatedAt: str
    fields: list[TicketTypeField]
    defaultSlackChannelId: str | None
    defaultCustomerId: str | None
    id: str


class FromEmail(TypedDict):
    name: str
    email: str


class ReplyToEmail(TypedDict, total=False):
    name: str
    email: str


class Reputation(TypedDict, total=False):
    spf: str
    dkim: str
    senderIp: str
    spamScore: float
    spamReport: str


class Header(TypedDict, total=False):
    key: str
    line: str


class FromUser(TypedDict):
    id: str
    name: str
    email: str


class Ticket(TypedDict):
    id: str
    friendlyId: int


class SlackMessage(TypedDict):
    id: str
    ticketId: str
    ticket: Ticket


class Inbound(TypedDict):
    id: str
    timestamp: str
    slackMessage: SlackMessage


class InboundEmail(TypedDict):
    id: str
    tenantId: str
    checksum: str
    messageId: str
    inReplyTo: Optional[str]
    referenceMessageIds: List[str]
    ccs: List[Any]
    tos: List[Dict[str, str]]
    fromUserId: str
    subject: str
    htmlContent: str
    textContent: str
    attachments: List[Any]
    reputation: Reputation
    processedAt: str
    inboundEmailRuleId: str
    fromEmail: FromEmail
    replyToEmail: ReplyToEmail
    isAutoreply: bool
    headers: List[Header]
    createdAt: str
    fromUser: FromUser
    inbound: Inbound


class Recipient(TypedDict):
    type: Literal["customer"]
    id: str


class SendAs(TypedDict):
    type: Literal["user", "support-rep"]
    id: str


class Outbound(TypedDict, total=False):
    id: str
    status: Literal["scheduled", "draft", "sent", "failed"]
    deliveryMethod: Literal["slack"]
    subject: str
    blocks: List[dict]
    recipients: List[Recipient]
    sendAs: SendAs
    runAt: str


class ApprovalRequest(TypedDict, total=False):
    status: Literal["approved", "rejected", "pending"]
    id: str
    tenantId: str
    assignedToGroupId: Optional[str]
    assignedToUserId: Optional[str]
    statusChangedAt: Optional[datetime]
    conversationId: str
    title: Optional[str]
    notes: Optional[str]
    createdAt: datetime
    approverUser: Optional[User]
    approverGroup: Optional[UserTeam]


__all__ = [
    "WhereField",
    "BaseMessage",
    "Message",
    "Tag",
    "User",
    "UserTeam",
    "SlackChannel",
    "AutoresponderOptions",
    "SupportStep",
    "Customer",
    "IssueStatus",
    "Conversation",
    "TicketTypeField",
    "TicketType",
    "FromEmail",
    "ReplyToEmail",
    "Reputation",
    "Header",
    "FromUser",
    "Ticket",
    "SlackMessage",
    "Inbound",
    "InboundEmail",
    "Recipient",
    "SendAs",
    "Outbound",
    "ApprovalRequest",
]
