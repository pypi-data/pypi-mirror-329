class GitHubEvent:

    def __init__(self, name, action, payload):
        self._name: str = name
        self._action: str = action
        self._payload: str = payload

    @property
    def name(self):
        """str: The name of the event"""
        return self._name

    @property
    def action(self):
        """str: The action of the event"""
        return self._action

    @property
    def payload(self):
        """str: The payload of the event"""
        return self._payload


class StarCreated(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('star', 'created', payload)


class StarDeleted(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('star', 'deleted', payload)


class IssuesAssigned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'assigned', payload)


class IssuesClosed(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'closed', payload)


class IssuesDeleted(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'deleted', payload)


class IssuesDemilestoned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'demilestoned', payload)


class IssuesEdited(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'edited', payload)


class IssuesLabeled(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'labeled', payload)


class IssuesLocked(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'locked', payload)


class IssuesMilestoned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'milestoned', payload)


class IssuesOpened(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'opened', payload)


class IssuesPinned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'pinned', payload)


class IssuesReopened(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'reopened', payload)


class IssuesTransferred(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'transferred', payload)


class IssuesUnassigned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'unassigned', payload)


class IssuesUnlabeled(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'unlabeled', payload)


class IssuesUnlocked(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'unlocked', payload)


class IssuesUnpinned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issues', 'unpinned', payload)


class IssueCommentCreated(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issue_comment', 'created', payload)


class IssueCommentDeleted(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issue_comment', 'deleted', payload)


class IssueCommentEdited(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('issue_comment', 'edited', payload)


class PullRequestAssigned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'assigned', payload)


class PullRequestAutoMergeDisabled(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'auto_merge_disabled', payload)


class PullRequestAutoMergeEnabled(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'auto_merge_enabled', payload)


class PullRequestClosed(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'closed', payload)


class PullRequestConvertedToDraft(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'converted_to_draft', payload)


class PullRequestDemilestoned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'demilestoned', payload)


class PullRequestDequeued(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'dequeued', payload)


class PullRequestEdited(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'edited', payload)


class PullRequestEnqueued(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'enqueued', payload)


class PullRequestLabeled(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'labeled', payload)


class PullRequestLocked(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'locked', payload)


class PullRequestMilestoned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'milestoned', payload)


class PullRequestOpened(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'opened', payload)


class PullRequestReadyForReview(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'ready_for_review', payload)


class PullRequestReopened(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'reopened', payload)


class PullRequestReviewRequestRemoved(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'review_request_removed', payload)


class PullRequestReviewRequested(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'review_requested', payload)


class PullRequestSynchronize(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'synchronize', payload)


class PullRequestUnassigned(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'unassigned', payload)


class PullRequestUnlabeled(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'unlabeled', payload)


class PullRequestUnlocked(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request', 'unlocked', payload)


class PullRequestReviewCommentCreated(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request_review_comment', 'created', payload)


class PullRequestReviewCommentDeleted(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request_review_comment', 'deleted', payload)


class PullRequestReviewCommentEdited(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('pull_request_review_comment', 'edited', payload)


class WikiPageCreated(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('gollum', 'created', payload)


class WikiPageEdited(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('gollum', 'edited', payload)


class LabelCreated(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('label', 'created', payload)


class LabelDeleted(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('label', 'deleted', payload)


class LabelEdited(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('label', 'edited', payload)


class Push(GitHubEvent):
    def __init__(self, payload=None):
        super().__init__('push', '', payload)
